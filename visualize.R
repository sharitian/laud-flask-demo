#!/usr/bin/Rscript
args = commandArgs(trailingOnly = TRUE)


library(tidyverse)
library(rlang)
library(tcltk)

setwd(getwd())
diamonds <- read.csv("report.csv")

scatter_plot <- function(xvar, yvar){
  ggplot(data = diamonds, mapping = aes_string(x = {{xvar}}, y = {{yvar}})) +
    geom_point(alpha = 0.5) + 
    geom_smooth(method = "lm", se = FALSE, color = "blue") +
    theme_bw() 
  
}

windows()
scatter_plot(args[1], args[2])
prompt <- "hit spacebar to close plots"
extra <- "some extra comment"
capture <- tk_messageBox(message = prompt, detail = extra)


