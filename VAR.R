
path <- 'C:/Users/Pablo/Documents/MAESTRIA/TESIS/programas'
inp <- paste(path, 'inputs', sep = '/')
out <- paste(path, 'outputs', sep = '/')
setwd(path)

# Librerias
library(dplyr)
library(lubridate)
library(reshape2)
library(ggplot2)
library(siebanxicor)



# API Banxico
token <- 'a3c791b30d94f4987fa391cd497451d9b4bd96c8d24a41e7dfc05faa81eff2ac'
setToken(token)

# Funciones
getDataFrame <- function(id, names){
  json <- getSeriesData(id)
  
  # Extrae objetos de la lista
  for(i in 1:length(id)){
    assign(names[i], getSerieDataFrame(json, id[i]))
  }
  # Pega los objetos en un Data Frame
  df <- Reduce(function(x,y) full_join(x=x, y=y, by = 'date'), mget(names))
  colnames(df) <- c('date', names)
  return(df)
}
pega_clave <- function(id, info, names){
  temp <- data.frame(id, names)
  colnames(temp)[1] <- 'idSerie'
  info <- full_join(info, temp, by = 'idSerie')
  colnames(info)[8] <- 'Clave'
  return(info)
}

## importa series
id <- c('SR16735', 'SF4782', 'SR16525', 'SF282')
nombres <- c('igae', 'ipc', 'ifb', 'cetes')
info <- getSeriesMetadata(id, locale = 'es')
info <- pega_clave(id, info, nombres)
data <- getDataFrame(id, nombres)
colnames(data)[1] <- 'fecha'
data <- data[1:326,]

incert <- read.csv(paste(inp, 'indices.csv', sep = '/'), stringsAsFactors = F)
incert$fecha <- dmy(incert$fecha)

df <- left_join(data, incert, by = 'fecha')
df <- xts(df, order.by = seq(as.Date("1993-01-01"),
                               length=length(df$fecha),
                               by="months"))[,-1]


# por variables
epu <- diff(log(df$epu)) #[-1]

d.igae <- diff(log(data$igae))
d.ipc <- diff(log(data$ipc))
d.inv <- diff(log(data$ifb))
int <- data$cetes[-1]

data.var <- xts(cbind(epu, d.igae, d.ipc, d.inv, int),
                order.by = seq(as.Date("1993-02-01"),
                               length=length(epu),
                               by="months"))


### Modelación -----------------------
## Selección de Orden
VARselect(data.var, lag.max = 15, type = 'const')  # Gana p=1

## Estimación del Modelo Ganador
est.var <- VAR(data.var, p=3, type='const')

### 5. Análisis ----------
## Impulso Respuesta
irf.marg <- irf(est.var, impulse = 'epu', 
                n.ahead = 12, cumulative = F)
plot(irf.marg)

irf.cum <-irf(est.var, impulse = 'epu', response = 'remesas', 
              n.ahead = 12, cumulative = )
plot(irf.cum)

## Variance Decomposition
fevd(var1, n.ahead = 12)




