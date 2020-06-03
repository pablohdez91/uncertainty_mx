library(readxl)
library(dplyr)
library(forecast)
library(ggplot2)
library(lubridate)

pib <- read_excel("C:/Users/Pablo/Desktop/pib.xlsx", 
                    +     sheet = "Hoja2")

indices <- read.csv("~/MAESTRIA/TESIS/programas/inputs/indices2.csv", 
                    stringsAsFactors = F)
indices$fecha <- ymd(indices$fecha)

## pronostivo ARIMA
epu <- ts(indices$epu[c(49:363)], start = c(1994, 1), frequency = 12)
epu <- aggregate(epu, nfrequency = 4)

df <- data.frame(cbind(data.frame(pib$pib), epu))


auto.arima(pib$pib, include.mean = F)

mod1 <- arima(pib$pib, order = c(2,0,3), xreg = epu[-1])
plot(forecast(mod1, h = 1))
rm(list=ls())


## Pronóstico VAR

data.var <- cbind(pib$pib, epu.norm)
colnames(data.var) <- c('pib', 'epu')
VARselect(data.var)

mod <- VAR(data.var, type = 'const', p = 1)
pred <- predict(mod)
irf <- irf(mod, impulse = 'epu', response = 'pib')
plot(irf)

rm(list=ls())



# Análsis comparable

df <- indices %>%
  mutate(epu_norm = (epu - mean(epu)) / sd(epu)) %>%
  mutate(mon_norm = (mon - mean(mon)) / sd(mon)) %>%
  mutate(fis_norm = (fis - mean(fis)) / sd(fis)) %>%
  select(fecha, epu_norm, mon_norm, fis_norm)

covid <- tail(df, n = 17)

cor(covid[,-1])


covid.r <- reshape(data=covid, idvar="incert",
        varying = c("epu_norm","mon_norm", "fis_norm"),
        v.name=c("value"),
        times=c("Incertidumbre","P. Monetaria", "P. Fiscal"),
        direction="long")

gcovid <- ggplot(covid.r, aes(x = fecha, y = value)) + 
  geom_line(aes(linetype = time)) + 
  scale_linetype_manual(values = c("solid", "dashed", "dotted")) +
  theme_bw() +
  theme(legend.position = 'top', legend.title = element_blank()) +
  labs(title="", y="", x="") 
gcovid
ggsave(paste(out,'gcovid.png',sep="/"), gcovid)



# tabla maximos
max.epu <- df[order(-df$epu_norm),] %>%
  select(fecha, epu_norm) %>%
  head(n = 5)

max.mon <- df[order(-df$mon_norm),] %>%
  select(fecha, mon_norm) %>%
  head(n = 5)

max.fis <- df[order(-df$fis_norm),]%>%
  select(fecha, fis_norm) %>%
  head(n = 5)

max <- cbind(max.epu, max.mon, max.fis)
max



### diarios

library(readr)
covid_reforma <- read_csv("~/MAESTRIA/TESIS/programas/inputs/covid_reforma.csv")
colnames(covid_reforma) <- c('fecha', 'count', 'today', 'reforma')

covid_mural <- read_csv("~/MAESTRIA/TESIS/programas/inputs/covid_mural.csv")
colnames(covid_mural) <- c('fecha', 'count', 'today', 'mural')

covid_elnorte <- read_csv("~/MAESTRIA/TESIS/programas/inputs/covid_elnorte.csv")
colnames(covid_elnorte) <- c('fecha', 'count', 'today', 'elnorte')


covid.d <- full_join(covid_reforma, covid_mural, by = "fecha") %>%
  full_join(covid_elnorte, by = "fecha") %>%
  select(fecha, reforma, mural, elnorte) %>%
  mutate(unc_covid = reforma + mural + elnorte)

covid.d$fecha <- dmy(covid.d$fecha)

ggplot(covid.d, aes(x = fecha, y = unc_covid)) + 
  geom_line()

graph <- ggplot(covid.d, aes(x = fecha, y = unc_covid)) + 
  geom_line() + 
  labs(title="", y="", x="2020") + 
  theme_bw() +
  theme(panel.grid.minor = element_blank()) 
graph
ggsave(paste(out,'unc_covid.png',sep="/"), graph)

max.d <- covid.d %>%
  select(fecha, unc_covid) %>%
  arrange(desc(unc_covid)) %>%
  head(n = 10)





