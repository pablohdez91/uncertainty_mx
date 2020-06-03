

path <- 'C:/Users/Pablo/Documents/MAESTRIA/TESIS/programas'
inp <- paste(path, 'inputs', sep = '/')
out <- paste(path, 'outputs', sep = '/')
setwd(path)

# Librerias
library(dplyr)
library(lubridate)
library(reshape2)
library(ggplot2)


## Clasificacion: ()
# Politica Monetaria: 1, 5, 6, 7
# Politica Fiscal: 0, 2, 6, 7
# Politica Comercial: 2, 9
# Riesgo Politico / Regulacion: 4, 8

#### Indices por periodico
today_reforma <- read.csv(paste(inp, "today_reforma.csv", sep = "/"), 
                          stringsAsFactors = F)
today_mural <- read.csv(paste(inp, "today_mural.csv", sep = "/"), 
                        stringsAsFactors = F)
today_elnorte <- read.csv(paste(inp, "today_elnorte.csv", sep = "/"), 
                          stringsAsFactors = F)

today_reforma$date <- dmy(today_reforma$date)
today_mural$date <- dmy(today_mural$date)
today_elnorte$date <- dmy(today_elnorte$date)

colnames(today_reforma)[1] <- 'fecha'
colnames(today_mural)[1] <- 'fecha'
colnames(today_elnorte)[1] <- 'fecha'

temp_raw_count <- read.csv(paste(inp, "temp_raw_count2.csv", sep = "/"),
                           stringsAsFactors = F)

df <- dplyr::select(temp_raw_count, -c(X, titulo)) %>%
  mutate(conteo = 1)

# Arregla fechas
meses.l <- c('Ene', "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct",
           "Nov", "Dic")
meses.n <- c('01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', 
             '12')
for(i in 1:12){
  df$fecha <- gsub(meses.l[i], meses.n[i], df$fecha)
}
rm(meses.l, meses.n)
df$fecha <- dmy(df$fecha)


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


# suma de tópicos
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

df <- df %>% 
  mutate(mon = p_mon.x + p_mon.y + p_mon) %>%
  mutate(fis = p_fis.x + p_fis.y + p_fis) %>%
  mutate(com = p_com.x + p_com.y + p_com) %>%
  mutate(reg = p_reg.x + p_reg.y + p_reg) %>%
  mutate(epu = mon + fis + com + reg) %>%
  select(fecha, epu, mon, fis, com, reg)

write.csv(df, paste(inp, 'indices2.csv', sep = '/'))

# solo desde 1993
df <- df[-c(1:36),]
#indices <- indices[-c(1:36),]

# incertidumbre general
graph1 <- ggplot(df, aes(x = fecha, y = epu)) + 
      geom_line() + 
      labs(title="", y="", x="") + 
      scale_x_date(breaks = "1 year", date_labels = "%Y") +  
      theme_bw() +
      theme(axis.text.x = element_text(angle = 45, vjust=0.5),
            panel.grid.minor = element_blank()) 
graph1
ggsave(paste(out,'graph1.jpg',sep="/"), graph1)

# Politica Monetaria
graph2 <- ggplot(df, aes(x = fecha, y = mon)) + 
  geom_line() +
  labs(title="", y="", x="") + 
  scale_x_date(breaks = "1 year", date_labels = "%Y") +  
  theme_bw() +
  theme(axis.text.x = element_text(angle = 45, vjust=0.5),
        panel.grid.minor = element_blank()) 
graph2
ggsave(paste(out,'graph2.jpg',sep="/"), graph2)

# Politica Fiscal
graph3 <- ggplot(df, aes(x = fecha, y = fis)) + 
  geom_line() +
  labs(title="", y="", x="") + 
  scale_x_date(breaks = "1 year", date_labels = "%Y") +  
  theme_bw() +
  theme(axis.text.x = element_text(angle = 45, vjust=0.5),
        panel.grid.minor = element_blank()) 
graph3
ggsave(paste(out,'graph3.jpg',sep="/"), graph3)

# Politica Comercial
graph4 <- ggplot(df, aes(x = fecha, y = com)) + 
  geom_line() +
  labs(title="", y="", x="") + 
  scale_x_date(breaks = "1 year", date_labels = "%Y") +  
  theme_bw() +
  theme(axis.text.x = element_text(angle = 45, vjust=0.5),
        panel.grid.minor = element_blank()) 
graph4
ggsave(paste(out,'graph4.jpg',sep="/"), graph4)

# Riesgo Politico / Regulación
graph5 <- ggplot(df, aes(x = fecha, y = reg)) + 
  geom_line() +
  labs(title="", y="", x="") + 
  scale_x_date(breaks = "1 year", date_labels = "%Y") +  
  theme_bw() +
  theme(axis.text.x = element_text(angle = 45, vjust=0.5),
        panel.grid.minor = element_blank()) 
graph5
ggsave(paste(out,'graph5.jpg',sep="/"), graph5)








# Visualizacion por tópicos
rc <- read.csv(paste(inp, 'raw_count2.csv', sep = '/'))

r_c <- rc %>%
  select(-X, -X..date......, -today)
colnames(r_c) <- c('fecha', "t0", "t1", "t2", "t3", "t4", "t5", "t6", "t7",
                   "t8", "t9")
r_c$fecha <- ymd(r_c$fecha)

r_c <- group_by(r_c, fecha=floor_date(fecha, "month"))
r_c[is.na(r_c)] <- 0


ggplot(r_c, aes(x = fecha, y = t8)) + geom_line()






### Distribuciones
indices <- read.csv(paste(inp, 'indices.csv', sep = '/'), stringsAsFactors = F)

ggplot(indices, aes(epu)) + geom_histogram(bins = 50) + theme_bw()



library(ggpubr)
ggarrange(p_remesas, p_prod, p_epu, p_epumx + rremove("x.text"),
          ncol = 2, nrow = 2)

