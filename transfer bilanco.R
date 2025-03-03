library(readr)
library(tidyverse)
library(dplyr)

df <- data.frame()
season <- c("2020_2021", "2021_2022", "2022_2023", "2023_2024", "2024_2025")
for (i in 1:length(season)) {
  d <- read_csv(paste0("data/transfer/bundesliga_", season[i], ".csv"))
  df <- rbind(df, d)
}
dd <- read_csv("data/transfer/bundesliga_2021_2022.csv")

df
