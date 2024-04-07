# Modules
import pandas as pd
import sqlite3
import spacy
nlp = spacy.load('es_core_news_sm')

# Directory
"""
import os
path = ""
os.chdir(path)
"""


# Build Initial Data Frame -----------------------------------------------------
## Import Tables
con = sqlite3.connect('data/Corpus.db')
reforma = pd.read_sql_query("SELECT * from Reforma", con)
mural = pd.read_sql_query("SELECT * from Mural", con)
elnorte = pd.read_sql_query("SELECT * from Elnorte", con)
con.close()

## Create 'periodico' variable
reforma['periodico'] = "reforma"
mural['periodico'] = "mural"
elnorte['periodico'] = "elnorte"

## Append data frames
data = pd.concat([reforma, mural, elnorte])


# Pre-Processing ---------------------------------------------------------------
## Quit Empty articles
data = data.drop(data[data['articulo']==""].index)

## First clean (delete html code)
limp = ['[', ']', '<div class="texto" id="divTexto">', '</div>', '<p>', '</p>',
        '<span class="highlighter">', '</span>', '\r', '\n', '<br/>',
        '<tbody>', '</tbody>', '<td>', '</td>', '<tr>', '</tr>',
        'table', 'align', "center", 'border', 'id=', 'TABLA', '<', '>']

for i in range(len(limp)):
    data['articulo'] = data['articulo'].str.replace(limp[i], '')

## Pre-Processing
docs = []

for doc in data['articulo']:   # Tonenization (slow)
    docs.append(nlp(doc))

## lemmatization, delete punctuation, numbers and stopwords
docs = [[w.lemma_
          for w in doc
              if not w.is_stop
              and not w.is_punct
              and not w.like_num] for doc in docs]

## Delete short words
docs = [[token for token in doc if len(token) > 2] for doc in docs]

## to lowercase
docs = [[token.lower() for token in doc] for doc in docs]

## Search for bigrams
import gensim
bigram = gensim.models.Phrases(docs)
docs = [bigram[doc] for doc in docs]


# Vectorization (bag-of-words) -------------------------------------------------
from gensim.corpora import Dictionary
dictionary = Dictionary(docs)

## Filter words that appear in less than 20 docs or more than 50%
dictionary.filter_extremes(no_below=20, no_above=0.5)

## BOW: Bag of Words
corpus = [dictionary.doc2bow(doc) for doc in docs]

print('Number of unique tokens: %d' % len(dictionary))
print('Number of documents: %d' % len(corpus))


# Classification with LDA ------------------------------------------------------
## Training the model
from gensim.models import LdaModel
## Training parameters
num_topics = 10
chunksize = 2000
passes = 20
iterations = 400
eval_every = None  # Perplexity of the model. (takes a long time if activated)
# Make a index to word dictionary.
temp = dictionary[0]  # This is only to "load" the dictionary.
id2word = dictionary.id2token

model = LdaModel(
    corpus=corpus,
    id2word=id2word,
    chunksize=chunksize,
    alpha='auto',
    eta='auto',
    iterations=iterations,
    num_topics=num_topics,
    passes=passes,
    eval_every=eval_every
)


# Post Modelling ------------------------------------------------------------
doc_topics=[]
for i in range(len(corpus)):
    doc_topics.append(model.get_document_topics(corpus[i]))

## To order the tuples by probability
import operator
for tup in doc_topics:   # Solamente se toma el tópico con más probabilidad
    tup.sort(key = operator.itemgetter(1), reverse = True)

## Vector of topics for each document (to paste in the data frame)
lis_topics = []
for t in range(len(doc_topics)):
    lis_topics.append(doc_topics[t][0][0])

## Characteristic words for each topic
topicos = model.show_topics()
print(topicos)

## Paste to the initial data frame
df = data
df['topico'] = lis_topics
del df['articulo']

df.to_csv("data/RawCount.csv")
