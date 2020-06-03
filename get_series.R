################################################################################
## Datos de Banxico SIE
## Este código descarga y ordena series de datos del SIE de Banxico
################################################################################

library(dplyr)

# API Banxico
library(siebanxicor)
token <- 'a3c791b30d94f4987fa391cd497451d9b4bd96c8d24a41e7dfc05faa81eff2ac'
setToken(token)

library(httr)
library(jsonlite)
library(rjson)
token_inegi_bie <- '146bc7ae-ca4f-7eb0-e7cf-741357298a84'
token_inegi_denue <- '28893272-a746-4c7d-9c82-d2e36ad4694f'


### Funciones
# Los argumentos de la función son dos vectores de cadena del mismo tamaño
# uno con los id de las series, y el otro con los nombres que se le van a poner
# a las series.
# La función descarga los datos de la API de Banco de México (los cuales vienen
# en formato lista), extrae los dataframes y los pega en uno solo.
# Regresa un data frame con las n series descargadas.

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

# Toma los nombres clave de las variables y los pega en el Data Frame de 
# informacion
pega_clave <- function(id, info, names){
  temp <- data.frame(id, names)
  colnames(temp)[1] <- 'idSerie'
  info <- full_join(info, temp, by = 'idSerie')
  colnames(info)[8] <- 'Clave'
  return(info)
}




### Producción -----------------------------------------------------------------
# IGAE (Desestacionalizadas)
id.igae <- c('SR16735', 'SR16738', 'SR16741', 'SR16744')
info.igae <- getSeriesMetadata(id.igae, locale = 'es')
names.igae <- c('igae', 'igae_1', 'igae_2', 'igae_3')
info.igae <- pega_clave(id.igae, info.igae, names.igae)
igae <- getDataFrame(id.igae, names.igae)


# Producción Industrial
id.prind <- c('SR16695', 'SR16696','SR16697','SR16698', 'SR16699')
info.prind <- getSeriesMetadata(id.prind, locale = 'es')
names.prind <- c("prind", "prind_min", "prind_elec", "prind_cons", 
                 "prind_manu")
info.prind <- pega_clave(id.prind, info.prind, names.prind)
prind <- getDataFrame(id.prind, names.prind)


# PIB
id.pib <- c('SR16620', 'SR16621', 'SR16622', 'SR16627')
info.pib <- getSeriesMetadata(id.pib, locale = 'es')
names.pib <- c('pib', 'pib_1', 'pib_2', 'pib_3')
info.pib <- pega_clave(id.pib, info.pib, names.pib)
pib <- getDataFrame(id.pib, names.pib)



### Consumo -----------------------------------------------------------------
# indice de volumen de consumo privado en el mercado interno
id.icons <- c('SR16563',	'SR16564',	'SR16565',	'SR16566',	'SR16567')
info.icons <- getSeriesMetadata(id.icons, locale = 'es')
names.icons <- c('icons',	'icons_bs',	'icons_b',	'icons_s',	'icons_imp')
info.icons <- pega_clave(id.icons, info.icons, names.icons)
icons <- getDataFrame(id.icons, names.icons)


# Venta de Automoviles
id.autos <- c('SR1043',	'SR1049',	'SR1052',	'SR1055')
info.autos <- getSeriesMetadata(id.autos, locale = 'es')
names.autos <- c('autos', 'autos_nac',	'autos_imp',	'autos_exp')
info.autos <- pega_clave(id.autos, info.autos, names.autos)
autos <- getDataFrame(id.autos, names.autos)



### Ahorro --------------------------------------------------------------------

### Remuneraciones y Productividad -------------------------------------------------------------
id.ryp <- c('SL11345',	'SL11346',	'SL11349',	'SL11350',	'SL11353', 'SL11354')
info.ryp <- getSeriesMetadata(id.ryp, locale = 'es')
names.ryp <- c('rem_man',	'rem_com',	'prod_man',	'prod_com',	'cumo_man',
              'cumo_com')
info.ryp <- pega_clave(id.ryp, info.ryp, names.ryp)
ryp <- getDataFrame(id.ryp, names.ryp)


### Empleo --------------------------------------------------------------------
# Tasa de Desempleo Abierto
id.tda <- c('SL1',	'SL5',	'SL6')
info.tda <- getSeriesMetadata(id.tda, locale = 'es')
names.tda <- c('tda', 'tda_h', 'tda_m')
info.tda <- pega_clave(id.tda, info.tda, names.tda)
tda <- getDataFrame(id.tda, names.tda)

### Salarios ------------------------------------------------------------------
id.sal <- c('SL138',	'SL136',	'SL137',	'SL11136',	'SL11137',	'SL11138',
         'SL11139',	'SL2829',	'SL2830',	'SL5113',	'SL5114',	'SL2827',	'SL2828')
info.sal <- getSeriesMetadata(id.sal, locale = 'es')
names.sal <- c('revsal',	'empr',	'trab',	'revsal_man',	'revsal_otr',	'trab_man',
               'trab_otr',	'revsal_pub',	'revsal_priv',	'trab_pub',	'trab_priv',
               'salcon_ante',	'salcon_post')
info.sal <- pega_clave(id.sal, info.sal, names.sal)
sal <- getDataFrame(id.sal, names.sal)

### Inversión -----------------------------------------------------------------
# Indice de Volumen de Inversión Fija Bruta
id.ifb <- c('SR16536',	'SR16537',	'SR16538',	'SR16539',	'SR16541',
            'SR16542',	'SR16544',	'SR16545',	'SR16546')
info.ifb <- getSeriesMetadata(id.ifb, locale = 'es')
names.ifb <- c('ifb',	'ifb_maq',	'ifb_maqn',	'ifb_trann',	'ifb_maqi',
               'ifb_trani',	'ifb_const',	'ifb_conr',	'ifb_connr')
info.ifb <- pega_clave(id.ifb, info.ifb, names.ifb)
ifb <- getDataFrame(id.ifb, names.ifb)


### Deuda ---------------------------------------------------------------------
id.deuda <- c('SG18',	'SG19',	'SG20')
info.deuda <- getSeriesMetadata(id.deuda, locale = 'es')
names.deuda <- c('deuda',	'deuda_int',	'deuda_ext')
info.deuda <- pega_clave(id.deuda, info.deuda, names.deuda)
deuda <- getDataFrame(id.deuda, names.deuda)

### Tipo de Cambio -----------------------------------------------------------------
id.tdc <- c('SF17908', 'SF17906', 'SR28', 'SR1503')
info.tdc <- getSeriesMetadata(id.tdc, locale = 'es')
names.tdc <- c('fix_mean', 'fix_fin', 'tcr', 'tcr_int')
info.tdc <- pega_clave(id.tdc, info.tdc, names.tdc)
tdc <- getDataFrame(id.tdc, names.tdc)



### Bolsa  --------------------------------------------------------------------
# Valor, Indice y Operaciones
id.bolsa <- c('SF4774', 'SF4782', 'SF4801', 'SF4802', 'SF4817', 'SF4803')
info.bolsa <- getSeriesMetadata(id.bolsa, locale = 'es')
names.bolsa <- c('valor', 'ipc', 'op',	'op_seg',	'op_cb',	'op_ics')
info.bolsa <- pega_clave(id.bolsa, info.bolsa, names.bolsa)
bolsa <- getDataFrame(id.bolsa, names.bolsa)



### Precios -------------------------------------------------------------------
# Indice Nacional de Precios al Consumidor
id.inpc <- c('SP1', 'SP74625', 'SP74626', 'SP66540', 'SP74627', 'SP74628',
          'SP66542', 'SP56339', 'SP74630', 'SP56337', 'SP74631')
info.inpc <- getSeriesMetadata(id.inpc, locale = 'es')
names.inpc <- c('inpc',	'inpc_sub',	'inpc_merc',	'inpc_alim',	'inp_nalim',
                'inpc_serv',	'inpc_viv',	'inpc_educ',	'inpc_nsub',	
                'inpc_agro',	'inpc_ener')
info.inpc <- pega_clave(id.inpc, info.inpc, names.inpc)
inpc <- getDataFrame(id.inpc, names.inpc)



# Precios de Comercio Exterior
id.pcom <- c('SP12754',	'SP12755',	'SP12753')
info.pcom <- getSeriesMetadata(id.pcom, locale = 'es')
names.pcom <- c('ipexp',	'ipimp',	'tt')
info.pcom <- pega_clave(id.pcom, info.pcom, names.pcom)
pcom <- getDataFrame(id.pcom, names.pcom)


# Precios del Petrole (Mezcla Mexicana de Exportacion)
mme <- getSeriesData('SI744')
mme <- getSerieDataFrame(mme, 'SI744')



### Tasas de Interés ----------------------------------------------------------
# México
id.int <- c('SF282',	'SF3338',	'SF3270',	'SF3367',	'SF17806',	'SF17808',
         'SF46997',	'SF46998')
info.int <- getSeriesMetadata(id.int, locale = 'es')
names.int <- c('int_28d',	'int_91d',	'int_182d',	'int_364d',	'int_3a',
               'int_10a',	'int_20a',	'int_30a')
info.int <- pega_clave(id.int, info.int, names.int)
int <- getDataFrame(id.int, names.int)


# Estados Unidos





#### Pega info
output <- 'H:/Tesis/outputs'
setwd(output)
info <- Reduce(rbind, mget(ls(pattern = 'info')))
write.csv(info, 'info.csv')
