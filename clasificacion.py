"""
desde las noticias en bruto hasta la generaci�n de conteos raw
"""

# Modulos
import pandas as pd
import sqlite3
import spacy
nlp = spacy.load('es_core_news_sm')


"""
import os
path = ""
os.chdir(path)
"""


# Construcción del Data Frame inicial -----------------------------------------
# Importar tablas
con = sqlite3.connect('data/Corpus.db')
reforma = pd.read_sql_query("SELECT * from Reforma", con)
mural = pd.read_sql_query("SELECT * from Mural", con)
elnorte = pd.read_sql_query("SELECT * from Elnorte", con)
con.close()

# variable de periodico
reforma['periodico'] = "reforma"
mural['periodico'] = "mural"
elnorte['periodico'] = "elnorte"

# dataframe completo
data = pd.concat([reforma, mural, elnorte])



#Limpieza del Corpus-----------------------------------------------------------
## quitar articulos vacios
data = data.drop(data[data['articulo']==""].index)

## Primera limipieza (quita restos de html)
limp = ['[', ']', '<div class="texto" id="divTexto">', '</div>', '<p>', '</p>',
        '<span class="highlighter">', '</span>', '\r', '\n', '<br/>',
        '<tbody>', '</tbody>', '<td>', '</td>', '<tr>', '</tr>',
        'table', 'align', "center", 'border', 'id=', 'TABLA', '<', '>']

for i in range(len(limp)):
    data['articulo'] = data['articulo'].str.replace(limp[i], '')

# Sacamos los textos para facilitar el código
docs = []

for doc in data['articulo']:   # Esto es para usar spacy (tarda), tokeniza
    docs.append(nlp(doc))

## lemmatiza, quita puntuacion, numeros y stopwords
docs = [[w.lemma_
          for w in doc
              if not w.is_stop
              and not w.is_punct
              and not w.like_num] for doc in docs]

# Quita palabras muy cortas
docs = [[token for token in doc if len(token) > 2] for doc in docs]

# Pasa a minúsculas
docs = [[token.lower() for token in doc] for doc in docs]

# Busca bigramas
import gensim
bigram = gensim.models.Phrases(docs)
docs = [bigram[doc] for doc in docs]


# Vectorización (bag-of-words) -----------------------------------------------
from gensim.corpora import Dictionary
dictionary = Dictionary(docs)

# filtra palabras que aparecen en menos de 20 docs o en más del 50%
dictionary.filter_extremes(no_below=20, no_above=0.5)

# bow: Bag of Words
corpus = [dictionary.doc2bow(doc) for doc in docs]

print('Number of unique tokens: %d' % len(dictionary))
print('Number of documents: %d' % len(corpus))


# Clasificación --------------------------------------------------------------
# Entrenamiento del modelo LDA (con GENSIM)
from gensim.models import LdaModel
# Parametros de entrenamiento
num_topics = 10
chunksize = 2000
passes = 20
iterations = 400
eval_every = None  # Perplejidad del modelo. (tarda mucho si se activa)
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


# Post Modelación ------------------------------------------------------------
doc_topics=[]   # listas de tópicos con sus respectivas probas por documento
for i in range(len(corpus)):
    doc_topics.append(model.get_document_topics(corpus[i]))

import operator   # para ordenar las tuplas por probabilidad
for tup in doc_topics:   # Solamente se toma el tópico con más probabilidad
    tup.sort(key = operator.itemgetter(1), reverse = True)

lis_topics = []   # Vector de tópicos por documento (para pegar en el DF)
for t in range(len(doc_topics)):
    lis_topics.append(doc_topics[t][0][0])

# Palabras clave de cada tópico
topicos = model.show_topics()
print(topicos)

# pegado a la base original
df = data
df['topico'] = lis_topics
del df['articulo']

df.to_csv("data/RawCount.csv")
