# uncertainty_mx
El objetivo de este repositorio es construir indicadores de incertidumbre de política económica para México. Estos indicadores se contruyen utilizando una metodología desarrollada en [Baker, Bloom y Davis (2016)](https://academic.oup.com/qje/article/131/4/1593/2468873) y [Azqueta-Galvadon, et. al. (2020)](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3516756), la cual se basa en la medición de la cobertura relativa de los artículos periodísticos. Se crean cuatro indicadores temáticos (Política Monetaria, Política Fiscal, Política Comercial y Política Regulatoria) y uno de incertidumbre por Política Económica en general, para el periodo enero 1993 - mayo 2020. Esta metodología se fundamenta en un algoritmo de clasificación no supervisado conocido como Latent Dirichlet Allocation (LDA).

El procedimiento consta de tres pasos. En el primero se hace Web Scraping de las páginas de los periódicos de Grupo Reforma (Reforma, Mural y El Norte). El segundo paso consta del pre-proceso del texto extraído de estas páginas de internet y la aplicación del algorítmo LDA para la extracción de tópicos de los artículos. Finalmente se construyen los indicadores de incertidumbre como conteos normalizados de artículos periodísticos correspondientes a ciertos tópicos relacionados con las temáticas de cada indicador. 

Adicionalmente se crea un indicador diario, más sencillo, de incertidumbre económica por COVID-19.

## Web Scraping
*WebScraping.py* realiza el Web Scraping de los artículos periodísticos de Grupo Reforma desde sus páginas de internet y genera el archivo *Corpus.db* (el cual no se puede incluír en este repositorio por su tamaño). Para poder ejecutar correctamente es necesario tener una membresía para dichos periodicos. 

*WebScraping_today.py* Crea vectores mensuales que cuentan el total de artículos publicados que contienen la palabra "hoy", por periodico. Estos vectores se utilizan como *proxies* del total de artículos publicados por un periodico. Se utilizan para normalizar los conteos de arítulos por tópicos en el archivo *BuildIndices.R*

## Extracción de Tópicos
*TopicExtraction.py* toma el texto en bruto de *Corpus.db*, lo procesa y modela para generar los conteos del archivo *RawCount.csv*.

## Construcción de los Índices
*BuildIndices.R* toma *RawCount.csv* y los vectores hechos en *WebScrapping_today.py* para construir las series de tiempo del archivo *uncertainty_mx.csv* para las cuales también se presentan gráficas.

## Incertidumbre Diaria por COVID-19
Este indicador es únicamente un conteo de artículos en los que aparecen las palabras clave: "economía", "incertidumbre" y "coronavirus", normalizado por el total de articulos en los que aparece la palabra "hoy". El Web Scraping se hacen en el archivo *WebScraping_covid.py*, los indicadores y la grafica se construyen en el archivo *covid_daily/covid.R*.


$$ \int_{-\inf}^{\inf} f_{X}(x) dx = 1 $$
