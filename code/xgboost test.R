library(readr)
library(caret)
library(xgboost)
library(plyr)
library(dplyr)
library(doParallel)

setwd('C:/Users/crock/Documents/GitHub/Nenana/')

df <- read.csv('data/parsed_whole_dataset.csv')

# create feature list
features <- as.vector(names(df))
remove <- c('Year', 'iceout')
features <- setdiff(features, remove)

# create the test and training splits
a <- createDataPartition(df$iceout, p = 0.81, list=FALSE)
training <- df[a,]
test <- df[-a,]

# create standard reference names for the test/train splits
trainX <- training[features]
trainy <- training$iceout
testX <- test[features]
testy <- test$iceout

# build control
ctrl <- trainControl(method = "repeatedcv",
                     number = 3,              # 3 fold cross validation
                     repeats = 9,							# do 5 repititions of cv
                     summaryFunction=defaultSummary,	
                     classProbs=FALSE,
                     allowParallel = TRUE)

# build search grid
xgb.grid <- expand.grid(nrounds = 650, #the maximum number of iterations
                        eta = c(0.1, 0.2, 0.25), # shrinkage
                        max_depth = c(6, 10),
                        gamma = c(0.2, 0.6, 0.85),
                        colsample_bytree = c(0.1, 0.2),
                        min_child_weight = c(0.5, 1),
                        subsample = c(0.6, 0.85, 1)
                        )

# train and tune the model
xgb.tune <-train(x=trainX,
                 y=trainy,
                 method="xgbTree",
                 metric="rmse",
                 #feval=maeSummary,
                 trControl=ctrl,
                 tuneGrid=xgb.grid)
)

# notes from the tuning
xgb.tune$bestTune
plot(xgb.tune)  		# Plot the performance of the training models
res <- xgb.tune$results
res


# make preditions
xgb.pred <- predict(xgb.tune,testX)

xgb.pred
testy
