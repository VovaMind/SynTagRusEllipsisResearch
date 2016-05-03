library(e1071)
library(adabag)
library(kernlab)
library(rpart)
library(class)

buildOverall <- function(tbl)
{
        print(tbl)
        total <- sum(tbl)
        
        # usual quality
        q1 <- (tbl[1,1] / (tbl[1,1] + tbl[2,1]))
        # null quality
        q2 <- (tbl[2,2] / (tbl[1,2] + tbl[2,2]))
        # total quality
        q3 <- (tbl[1,1] + tbl[2,2]) / total
        
        print(c(q1,q2,q3))
        0
}

setwd("C:\\R_projects\\!aspa")
input_data <- read.table("!features_links_double_slots_filt.csv") #read.csv
n = nrow(input_data)

input_data$label <- as.factor(input_data$label)

for (i in 1:(ncol(input_data)-1))
{  
        input_data[,i] <- as.numeric(input_data[,i])
        input_data[,i] <- input_data[,i] * 1.0
}

colnames(input_data) <- gsub("_","",colnames(input_data))

random_seed <- sample(0:10, n, replace=T)

test <- input_data[random_seed < 3,]
train <- input_data[random_seed >= 3,]

boost_model <- boosting(label~., data=train, mfinal=6)
boost_result <- predict(boost_model, test)
print("boost")
buildOverall(table(boost_result$class, test$label))

bagging_model <- bagging(label ~ ., data=train, mfinal=10)
bagging_result <- predict(bagging_model, test)
print("bagging")
buildOverall(table(bagging_result$class, test$label))

knn_model <- knn(train[,1:ncol(test)-1], test[,1:ncol(test)-1], train$label, k = 1)
print("1_NN")
buildOverall(table(knn_model, test$label))

knn_model <- knn(train[,1:ncol(test)-1], test[,1:ncol(test)-1], train$label, k = 1)
print("3_NN")
buildOverall(table(knn_model, test$label))

knn_model <- knn(train[,1:ncol(test)-1], test[,1:ncol(test)-1], train$label, k = 1)
print("5_NN")
buildOverall(table(knn_model, test$label))

knn_model <- knn(train[,1:ncol(test)-1], test[,1:ncol(test)-1], train$label, k = 7)
print("7_NN")
buildOverall(table(knn_model, test$label))

knn_model <- knn(train[,1:ncol(test)-1], test[,1:ncol(test)-1], train$label, k = 9)
print("9_NN")
buildOverall(table(knn_model, test$label))

knn_model <- knn(train[,1:ncol(test)-1], test[,1:ncol(test)-1], train$label, k = 11)
print("11_NN")
buildOverall(table(knn_model, test$label))
n
knn_model <- knn(train[,1:ncol(test)-1], test[,1:ncol(test)-1], train$label, k = 13)
print("13_NN")
buildOverall(table(knn_model, test$label))

knn_model <- knn(train[,1:ncol(test)-1], test[,1:ncol(test)-1], train$label, k = 15)
print("15_NN")
buildOverall(table(knn_model, test$label))

rpart_model <- rpart(train$label ~ ., data=train)
rpart_result <- predict(rpart_model, test)
rpart_result2 <- apply(rpart_result, 1, which.max)
print("rpart")
buildOverall(table(rpart_result2, test$label))

svm_model <- svm(train$label~., data = train)
svm_result <- predict(svm_model, test)
print("SVM")
buildOverall(table(svm_result, test$label))

#nullInputData <- input_data[input_data$label == 1,]
#nullResult <- predict(svm_model, nullInputData)
#print(table(nullResult, nullInputData$label))
