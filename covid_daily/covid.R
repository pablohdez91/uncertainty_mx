library(readr)
library(dplyr)
library(ggplot2)
library(lubridate)


path = ""
setwd(path)


### diarios
covid_reforma <- read_csv("covid/covid_reforma.csv")
colnames(covid_reforma) <- c('fecha', 'count', 'today', 'reforma')

covid_mural <- read_csv("covid/covid_mural.csv")
colnames(covid_mural) <- c('fecha', 'count', 'today', 'mural')

covid_elnorte <- read_csv("covid/covid_elnorte.csv")
colnames(covid_elnorte) <- c('fecha', 'count', 'today', 'elnorte')


covid.d <- full_join(covid_reforma, covid_mural, by = "fecha") %>%
  full_join(covid_elnorte, by = "fecha") %>%
  select(fecha, reforma, mural, elnorte) %>%
  mutate(unc_covid = reforma + mural + elnorte)

covid.d$fecha <- dmy(covid.d$fecha)

graph <- ggplot(covid.d, aes(x = fecha, y = unc_covid)) +
  geom_line() +
  labs(title="", y="", x="2020") +
  theme_bw() +
  theme(panel.grid.minor = element_blank())

ggsave('covid/unc_covid.png', graph)
