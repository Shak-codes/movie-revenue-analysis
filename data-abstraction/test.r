setwd("~/GitHub/movie-revenue-analysis/data")

library(car)

## Load movie data
df <- read.csv("movie_data.csv")


## Remove movies that have undesirable data
rows_to_remove <- c()
for(idx in 1:nrow(df)) {
  if(df$Revenue[idx] == 0) {
    rows_to_remove <<- c(rows_to_remove, idx)
  }
  else if(df$Budget[idx] == 0) {
    rows_to_remove <<- c(rows_to_remove, idx)
  }
  else if(df$Runtime[idx] == 0) {
    rows_to_remove <<- c(rows_to_remove, idx)
  }
  else if(df$Average.Production.Company.Earnings[idx] == 0) {
    rows_to_remove <<- c(rows_to_remove, idx)
  }
  else if(df$Average.Director.Earnings[idx] == 0) {
    rows_to_remove <<- c(rows_to_remove, idx)
  }
  else if(df$Average.Producer.Earnings[idx] == 0) {
    rows_to_remove <<- c(rows_to_remove, idx)
  }
  else if(df$Average.Actor.Earnings[idx] == 0) {
    rows_to_remove <<- c(rows_to_remove, idx)
  }
}
filtered.df <- df[-rows_to_remove,]


## Get response and explanatory variables
response <- filtered.df$Revenue
covariates <- filtered.df[,-c(1, 2, 29)]
covariates <- covariates[,-c(16, 26, 27)]

count <- 0

for(i in 1:4849) {
  if(explanatory_variables$Original_Language[i] == "en") {
    count <<- count + 1
  }
}



M <- lm(response ~ ., data=covariates)
summary(M)
car::vif(M)

## Function for removing high collinearity
removeHighCollinearity <- function(v, model, covariates) {
  
  ## Get all VIF values for the initial model
  vif.values <- vif(model)
  
  ## Loop until no VIF value is greater than v (the input)
  while (max(vif.values) > v){
    
    ## Find the index at which the max VIF value is
    ind <- which.max(vif.values)
    
    ## Remove the covariate with the highest VIF
    covariates <- covariates[-c(ind)]
    
    ## Update the model and the VIF values for the new covariates 
    model <- lm(response ~ ., data=covariates)
    vif.values <- vif(model)
  }
  
  return (covariates)
}

cov.reduced <- removeHighCollinearity(10, M, explanatory_variables)
