################################################################################

library(readxl)
library(dplyr)
library(lubridate)


path <- 'C:/Users/Pablo/Documents/MAESTRIA/TESIS/programas'
setwd(path)
inp <- paste(path, 'inputs', sep = '/')
out <- paste(path, 'outputs', sep = '/')

indices <- read.csv(paste(inp, "indices2.csv", sep = '/'), 
                    stringsAsFactors = F) %>%
  select(-X)
indices$fecha <- ymd(indices$fecha)
#indices <- indices[37:length(indices$fecha),]

### Test for Jumps--------------------------------------------------------------


### Filtros
library(mFilter)

## La función encuentra Spikes
spikes <- function(fechas, serie, factor){
  hp.serie <- hpfilter(ts(serie))
  lim <- mean(hp.serie$trend) + sd(hp.serie$trend) * factor
  
  df.serie <- data.frame(fechas, serie) %>%
    mutate(spike = as.numeric(serie > lim)) %>%
    filter(spike == 1) %>%
    select(-spike)
  
  return(df.serie)
}

spikes.epu <- spikes(indices$fecha, indices$epu, 2) %>%
  mutate(indice = 'epu')
spikes.p_mon <- spikes(indices$fecha, indices$mon, 2) %>%
  mutate(indice = 'p_mon')
spikes.p_fis <- spikes(indices$fecha, indices$fis, 2) %>%
  mutate(indice = 'p_fis')
spikes.com <- spikes(indices$fecha, indices$com, 2) %>%
  mutate(indice = 'com')
spikes.reg <- spikes(indices$fecha, indices$reg, 2) %>%
  mutate(indice = 'reg')


# Output
spikes <- Reduce(rbind, 
       list(spikes.epu, spikes.p_mon, spikes.p_fis, spikes.com, spikes.reg))
# spikes <- spikes[order(spikes$fechas),]

write.csv(spikes, file = paste(out, 'spikes2.csv', sep = '/'))


# Un Shock es un periodo de tiempo en el que se registra por lo menos un pico de incertidumbre. Definimos pico de incertidumbre como aquel mes en el que la realización del indice de incertidumbre en cuestión sobrepasa la media de referencia por 1.65 desviaciones estándar. La media y la desviación estandar de referencia son la media y la desviación estandar muestrales del índice, suavizado mediante un filtro de Hodrick-Prescott.



