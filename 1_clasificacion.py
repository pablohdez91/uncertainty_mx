"""
desde las noticias en bruto hasta la generaci�n de conteos raw
"""

# Modulos
import pandas as pd
import sqlite3
import spacy
nlp = spacy.load('es_core_news_sm')


# inputs
prog = "C:/Users/Pablo/Documents/MAESTRIA/TESIS/programas"
noticias = prog + '/inputs/noticias.db'
noticias_act = prog + "/inputs/noticias_ene20-abr20.db"
t_reforma = prog + '/inputs/today_reforma.csv'
t_mural = prog + '/inputs/today_mural.csv'
t_elnorte = prog + '/inputs/today_elnorte.csv'

# outputs
raw_count = prog + '/inputs/raw_count.csv'


"""
t_inicial = time.time()
t_avance = time.time()
print('tardó '+str(t_avance-t_inicial)+' segundos')
"""


# Construcción del Data Frame inicial -----------------------------------------
# Importar tablas
con = sqlite3.connect(noticias)
reforma = pd.read_sql_query("SELECT * from Reforma", con)
mural = pd.read_sql_query("SELECT * from Mural", con)
elnorte = pd.read_sql_query("SELECT * from Elnorte", con)
con.close()

# Pegar actualizaciones
con = sqlite3.connect(noticias_act)
reforma_act = pd.read_sql_query("SELECT * from Reforma", con)
mural_act = pd.read_sql_query("SELECT * from Mural", con)
elnorte_act = pd.read_sql_query("SELECT * from Elnorte", con)
con.close()


# variable de periodico
reforma['periodico'] = "reforma"
mural['periodico'] = "mural"
elnorte['periodico'] = "elnorte"
reforma_act['periodico'] = "reforma"
mural_act['periodico'] = "mural"
elnorte_act['periodico'] = "elnorte"

data = pd.concat([reforma, reforma_act, mural, mural_act, elnorte, elnorte_act])



#Limpieza del Corpus-----------------------------------------------------------
## quitar articulos vacios
data = data.drop(data[data['articulo']==""].index)
#data_toy = data.sample(frac = 0.1).reset_index()

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

"""
# En caso de necesitar agregar stopwords adicionales a las precargadas
my_stop_words = [""]
for stopword in my_stop_words:
    lexeme = nlp.vocab[stopword]
    lexeme.is_stop = True
"""

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

# pegado a la base original
df = data
df['topico'] = lis_topics
del df['articulo']

df.to_csv("temp_raw_count.csv")


## Ajusta el formato de las Fechas
meses_l =['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 
          'Nov', 'Dic']

for i in range(len(meses_l)):
    df['fecha'] = df['fecha'].str.replace(meses_l[i], str(i+1))
    
df['fecha'] = pd.to_datetime(df['fecha'], format = '%d-%m-%Y')

# Contador de artículos
df['index'] = 1

# Crea el Data Frame con los Raw Counts
from pandas import Grouper
df = df.groupby(['topico', Grouper(key = 'fecha', freq = '1m')]).sum()
df = df.reset_index(drop=False)
df = df.pivot(index='fecha', columns='topico', values=['index'])
df = df.reset_index(drop=False)
df = df.rename(columns={'fecha':'date'})


# Crea el vector de total de articulos para ajustar los raw counts
# Carga los individuales
today_reforma = pd.read_csv(t_reforma)
today_mural = pd.read_csv(t_mural)
today_elnorte = pd.read_csv(t_elnorte)

# Pegado 
today = pd.merge(today_reforma, today_mural, how='outer', on='date')
today = pd.merge(today, today_elnorte, how='outer', on='date')
today = today.rename(columns={'today_x':'reforma', 'today_y':'mural', 'today':'elnorte'})
today['today']=today['reforma']+today['mural']+today['elnorte']
today=today.drop(columns=['reforma','mural','elnorte'])
today['date'] = pd.to_datetime(today['date'], format = '%d/%m/%Y')

# Cambia la fecha a end of period para poder hacer el merge con df
today.index = today['date']
today.index = today.index.to_period('M').to_timestamp('M')
today=today.drop(columns='date')
today=today.reset_index(drop=False)

final = pd.merge(df, today, how='outer', on='date')

# Guadra el raw count
final.to_csv("raw_count.csv")

# No te olvides de guardar las palabras clave de los tópicos para hacer la 
# clasificacion
print(topicos)



# Ya de aqui se pasa a R para hacer la creación de indices y los análisis
del(elnorte, elnorte_act, eval_every, final, i, id2word, iterations, limp, lis_topics, meses_l, model, mural, mural_act, noticias, noticias_act, num_topics, passes, prog, raw_count, reforma, reforma_act, t, t_elnorte, t_mural, t_reforma, temp, today, today_elnorte, today_mural, today_reforma, tup)