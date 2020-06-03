
require(dplyr)
require(lubridate)
require(ggplot2)
require(reshape2)
library(readxl)
library(stargazer)



### Directorios
setwd('H:/Tesis/programas')
inputs <- 'H:/Tesis/inputs'
outputs <- 'H:/Tesis/outputs'


### Funciones
# reemplaza missings por ceros
haz.cero.na=function(x){
  ifelse(is.na(x),0,x)
}



# -----------------------------------------------------------------------------
# Del análisis de palabras clave  de los topicos se construyen los indices
# de la siguiente manera:
#   politica monetaria (p_mon): 1+6+9
#   politica fiscal (p_fis): 4+5+7
#   comercio (com): 3+9
#   regulacion (reg): 2+8
# ----------------------------------------------------------------------------

raw_count <- read.csv(paste(inputs,'1_raw_count.csv',sep="/"))
fecha <- raw_count['date']

bbd <- read_excel(paste(inputs,'Mexico_Policy_Uncertainty_Data.xlsx',sep='/'))




indices <- select(raw_count, -date, -X, -X..date......)
colnames(indices) <- c('topico0', 'topico1', 'topico2', 'topico3', 
                       'topico4', 'topico5', 'topico6', 'topico7', 'topico8', 
                       'topico9','today')
indices <- data.frame(sapply(indices,haz.cero.na))
indices <- data.frame(fecha, indices)

indices = mutate(indices, p_mon = (topico1+topico6+topico9)/today *100) %>%
  mutate(p_fis = (topico4+topico5+topico7)/today *100) %>%
  mutate(com = (topico3+topico9)/today *100) %>%
  mutate(reg = (topico2+topico8)/today *100) %>%
  mutate(epu = (p_mon+p_fis+com+reg)/4) %>%   # promedio para que sea comparable
  select(date, p_mon, p_fis, com, reg, epu) %>%
  slice(1:(length(indices$date)-2))   # quita ene y feb de 2020 (no hay datos)

indices$date <- ymd(indices$date)

write.csv(indices, file="indices.csv")


indices <- slice(indices, 37:length(indices$date))



## graficas individuales
# Politica Monetaria
pl_pmon <-ggplot(indices, aes(x=date)) + 
  geom_line(aes(y=p_mon)) + 
  labs(title="", 
       y="", x="") + 
  scale_x_date(breaks = "1 year", date_labels = "%Y") +  
  theme_bw() +
  theme(axis.text.x = element_text(angle = 45, vjust=0.5),
        panel.grid.minor = element_blank()) 
pl_pmon
ggsave(paste(outputs,'1_pmon.jpg',sep="/"), pl_pmon)

# Politica Fiscal
pl_pfis <- ggplot(indices, aes(x=date)) + 
  geom_line(aes(y=p_fis)) + 
  labs(title="", 
       y="", x="") + 
  scale_x_date(breaks = "1 year", date_labels = "%Y") +  
  theme_bw() +
  theme(axis.text.x = element_text(angle = 45, vjust=0.5),
        panel.grid.minor = element_blank()) 
pl_pfis
ggsave(paste(outputs,'1_pfis.jpg',sep="/"), pl_pfis)

# Comercio
pl_com <- ggplot(indices, aes(x=date)) + 
  geom_line(aes(y=com)) + 
  labs(title="", 
       y="", x="") + 
  scale_x_date(breaks = "1 year", date_labels = "%Y") +  
  theme_bw() +
  theme(axis.text.x = element_text(angle = 45, vjust=0.5),
        panel.grid.minor = element_blank()) 
pl_com
ggsave(paste(outputs,'1_com.jpg',sep="/"), pl_com)


# Regulacion
pl_reg <- ggplot(indices, aes(x=date)) + 
  geom_line(aes(y=reg)) + 
  labs(title="", 
       y="", x="") + 
  scale_x_date(breaks = "1 year", date_labels = "%Y") +  
  theme_bw() +
  theme(axis.text.x = element_text(angle = 45, vjust=0.5),
        panel.grid.minor = element_blank()) 
pl_reg
ggsave(paste(outputs,'1_reg.jpg',sep="/"), pl_reg)


# Incertidumbre General
pl_unc <- ggplot(indices, aes(x=date)) + 
  geom_line(aes(y=epu)) + 
  labs(title="", 
       y="", x="") + 
  scale_x_date(breaks = "1 year", date_labels = "%Y") +  
  theme_bw() +
  theme(axis.text.x = element_text(angle = 45, vjust=0.5),
        panel.grid.minor = element_blank()) 
pl_unc
ggsave(paste(outputs,'1_unc.jpg',sep="/"), pl_unc)


# tabla descriptivos
stargazer(select(indices, -date))
# extras


cor(select(indices, -date))

library("Hmisc")
rcorr(as.matrix(select(indices, -date)))


# Grafica conjunta
ggplot(melt(indices,id="date"),
       aes(x=date,y=value, colour=variable, group=variable)) + geom_line()
