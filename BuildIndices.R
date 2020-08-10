# # Libraries
library(dplyr)
library(lubridate)
library(reshape2)
library(ggplot2)

# # Directory
path <- ''
setwd(path)

# # Import Data
today_reforma <- read.csv(paste(path, "data/today_reforma.csv", sep = "/"),
                          stringsAsFactors = F)
today_mural <- read.csv(paste(path, "data/today_mural.csv", sep = "/"),
                        stringsAsFactors = F)
today_elnorte <- read.csv(paste(path, "data/today_elnorte.csv", sep = "/"),
                          stringsAsFactors = F)

RawCount <- read.csv(paste(path, "data/RawCount.csv", sep = "/"),
                     stringsAsFactors = F)

# # Date Format
today_reforma$date <- dmy(today_reforma$date)
today_mural$date <- dmy(today_mural$date)
today_elnorte$date <- dmy(today_elnorte$date)

colnames(today_reforma)[1] <- 'fecha'
colnames(today_mural)[1] <- 'fecha'
colnames(today_elnorte)[1] <- 'fecha'

# # Fix Dates of RawCount
df <- dplyr::select(RawCount, -c(X, titulo)) %>%
  mutate(conteo = 1)

meses.l <- c('Ene', "Feb", "Mar", "Abr", "May", "Jun",
          "Jul", "Ago", "Sep", "Oct", "Nov", "Dic")
meses.n <- c('01', '02', '03', '04', '05', '06',
          '07', '08', '09', '10', '11', '12')
for(i in 1:12){
  df$fecha <- gsub(meses.l[i], meses.n[i], df$fecha)
}
rm(meses.l, meses.n)
df$fecha <- dmy(df$fecha)


# An indicator is built for each period and then they are added
df_reforma <- filter(df, periodico == 'reforma') %>%
  select(-periodico) %>%
  group_by(fecha=floor_date(fecha, "month"), topico) %>%
  summarize(conteo=sum(conteo)) %>%
  dcast(fecha ~ topico)
df_reforma[is.na(df_reforma)] <- 0

df_mural <- filter(df, periodico == 'mural') %>%
  select(-periodico) %>%
  group_by(fecha=floor_date(fecha, "month"), topico) %>%
  summarize(conteo=sum(conteo)) %>%
  dcast(fecha ~ topico)
df_mural[is.na(df_mural)] <- 0

df_elnorte <- filter(df, periodico == 'elnorte') %>%
  select(-periodico) %>%
  group_by(fecha=floor_date(fecha, "month"), topico) %>%
  summarize(conteo=sum(conteo)) %>%
  dcast(fecha ~ topico)
df_elnorte[is.na(df_elnorte)] <- 0

df_reforma <- left_join(df_reforma, today_reforma, by = 'fecha')
df_mural <- left_join(df_mural, today_mural, by = 'fecha')
df_elnorte <- left_join(df_elnorte, today_elnorte, by = 'fecha')

colnames(df_reforma) <- c("fecha", "t0", "t1", "t2", "t3", "t4", "t5", "t6", "t7",
                          "t8", "t9", "today")
colnames(df_mural) <- c("fecha", "t0", "t1", "t2", "t3", "t4", "t5", "t6", "t7",
                          "t8", "t9", "today")
colnames(df_elnorte) <- c("fecha", "t0", "t1", "t2", "t3", "t4", "t5", "t6", "t7",
                          "t8", "t9", "today")


### Sum by Topics
## Classification
# Monetary Policy: topics 2, 6 y 8
# Fiscal Policy: topics 1, 3, y 7
# Trade Policy: topics 4 y 0
# Regulatory Policy: topics 5 y 6


df_reforma <- df_reforma %>%
  mutate(p_mon = (t2 + t6 + t8)/today * 100) %>%
  mutate(p_fis = (t1 + t3 + t7)/today * 100) %>%
  mutate(p_com = (t4 + t0)/today * 100) %>%
  mutate(p_reg = (t5 + t6)/today * 100) %>%
  select(fecha, p_mon, p_fis, p_com, p_reg)

df_mural <- df_mural %>%
  mutate(p_mon = (t2 + t6 + t8)/today * 100) %>%
  mutate(p_fis = (t1 + t3 + t7)/today * 100) %>%
  mutate(p_com = (t4 + t0)/today * 100) %>%
  mutate(p_reg = (t5 + t6)/today * 100) %>%
  select(fecha, p_mon, p_fis, p_com, p_reg)

df_elnorte <- df_elnorte %>%
  mutate(p_mon = (t2 + t6 + t8)/today * 100) %>%
  mutate(p_fis = (t1 + t3 + t7)/today * 100) %>%
  mutate(p_com = (t4 + t0)/today * 100) %>%
  mutate(p_reg = (t5 + t6)/today * 100) %>%
  select(fecha, p_mon, p_fis, p_com, p_reg)


df <- full_join(df_elnorte, df_mural, by = 'fecha') %>%
  full_join(df_reforma, by = 'fecha')
df[is.na(df)] <- 0


# Only since 1993
df <- df[-c(1:36),]

df <- df %>%
  mutate(mon = p_mon.x + p_mon.y + p_mon) %>%
  mutate(fis = p_fis.x + p_fis.y + p_fis) %>%
  mutate(com = p_com.x + p_com.y + p_com) %>%
  mutate(reg = p_reg.x + p_reg.y + p_reg) %>%
  mutate(epu = mon + fis + com + reg) %>%
  select(fecha, epu, mon, fis, com, reg)

# Save as csv
write.csv(df, paste(path, 'data/uncertainty_mx.csv', sep = '/'))


## Graphs
# Economic Policy Uncertainty
graph1 <- ggplot(df, aes(x = fecha, y = epu)) +
      geom_line() +
      labs(title="Economic Policy Uncertainty for Mexico", y="", x="") +
      scale_x_date(breaks = "1 year", date_labels = "%Y") +
      theme_bw() +
      theme(axis.text.x = element_text(angle = 45, vjust=0.5),
            panel.grid.minor = element_blank())
ggsave(paste(path,'data/epu.jpg',sep="/"), graph1)

# Monetary Policy
graph2 <- ggplot(df, aes(x = fecha, y = mon)) +
  geom_line() +
  labs(title="Economic Policy Uncertainty for Mexico (Monetary Policy)", y="", x="") +
  scale_x_date(breaks = "1 year", date_labels = "%Y") +
  theme_bw() +
  theme(axis.text.x = element_text(angle = 45, vjust=0.5),
        panel.grid.minor = element_blank())
ggsave(paste(path,'data/pmon.jpg',sep="/"), graph2)

# fiscal Policy
graph3 <- ggplot(df, aes(x = fecha, y = fis)) +
  geom_line() +
  labs(title="Economic Policy Uncertainty for Mexico (Fiscal Policy)", y="", x="") +
  scale_x_date(breaks = "1 year", date_labels = "%Y") +
  theme_bw() +
  theme(axis.text.x = element_text(angle = 45, vjust=0.5),
        panel.grid.minor = element_blank())
ggsave(paste(path,'data/pfis.jpg',sep="/"), graph3)

# Trade Policy
graph4 <- ggplot(df, aes(x = fecha, y = com)) +
  geom_line() +
  labs(title="Economic Policy Uncertainty for Mexico (Trade Policy)", y="", x="") +
  scale_x_date(breaks = "1 year", date_labels = "%Y") +
  theme_bw() +
  theme(axis.text.x = element_text(angle = 45, vjust=0.5),
        panel.grid.minor = element_blank())
ggsave(paste(path,'data/pcom.jpg',sep="/"), graph4)

# Regulatory Policy
graph5 <- ggplot(df, aes(x = fecha, y = reg)) +
  geom_line() +
  labs(title="Economic Policy Uncertainty for Mexico (Regulatory Policy)", y="", x="") +
  scale_x_date(breaks = "1 year", date_labels = "%Y") +
  theme_bw() +
  theme(axis.text.x = element_text(angle = 45, vjust=0.5),
        panel.grid.minor = element_blank())
ggsave(paste(path,'data/preg.jpg',sep="/"), graph5)
