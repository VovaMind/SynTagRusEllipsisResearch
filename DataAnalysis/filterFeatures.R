setwd("C:\\R_projects\\!aspa")
input_data <- read.csv("!features_f_links.csv")

col_sum <- colSums(input_data)
input_data2 <- input_data[,col_sum>0]
numCol <- ncol(input_data2) - 1

corr <- rep(0, numCol)
for(i in 1:numCol)
{
        corr[i] <- cor(input_data2[,i], input_data2$label)
}

write.table(input_data2, "!!features_f_links_filt.csv")
