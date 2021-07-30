#!/usr/bin/Rscript
args = commandArgs(trailingOnly = TRUE)

library(tidyverse)
library(rlang)
library(tcltk)
library(corrplot)
library(reshape2)

setwd(getwd())
data <- read.csv("laud/heat_df.csv")

com = data[,4:ncol(data)]

heat_map <- function(meth){
  cc = cor(com, method = meth)
  cc_df = as.data.frame(cc)
  cc_df$species = row.names(cc_df)
  ccm = melt(cc_df, id = "species")
  ccm$species <- factor(ccm$species, levels = unique(ccm$species))
  xx = ggplot(ccm, aes(x = variable, y = species)) + 
    geom_tile(aes(fill = value), colour = "grey45") + 
    coord_equal() + 
    scale_fill_gradient(low = "white", high = "red") + 
    theme(axis.text.y = element_text(face = "bold", colour = "grey25"), 
          legend.title = element_text(size = 10, face = "bold"),legend.position = "bottom", 
          axis.text.x = element_text(angle = 90, face = "bold",colour = "grey25", vjust = 0.5, hjust = 0), 
          panel.background = element_blank(), panel.border = element_rect(fill = NA, colour = NA), 
          axis.ticks = element_blank()) + 
    labs(x= "", y = "", fill = "Spearman's Correlation") + 
    scale_x_discrete(position = "top") +
    scale_y_discrete(limits = rev(levels(ccm$species)))
  
}

windows()
heat_map(args[1])
prompt <- "press okay to close plots."
extra <- "Go back to return to page."
capture <- tk_messageBox(message = prompt, detail = extra)
