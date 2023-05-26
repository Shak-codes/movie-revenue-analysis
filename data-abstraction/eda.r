setwd("~/GitHub/movie-revenue-analysis/data")

library(car)
library(ggplot2)
library(readr)
library(corrplot)
library(lmtest)
library(sandwich)
library(dplyr)
library(robustbase)
library(ggResidpanel)


###################################
###################################
#####                         #####
########## DATA  CURATION #########
#####                         #####
###################################
###################################

## Load movie data
df <- data.frame(read.csv("movie_data.csv"))
df <- df[1:29]

##### ##### ##### ##### ##### ##### ##### ##### #####
##### Remove data not suitable for our analysis #####
##### ##### ##### ##### ##### ##### ##### ##### #####

## Vector to store movies to be removed from our analysis
rows_to_remove <- c() 

## Finding movies with unsuitable data
for(idx in 1:nrow(df)) {
  if(df$Revenue[idx] < 1000000) {
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
  } else if (df$Days.Since.Release[idx] > 8427) {
    rows_to_remove <<- c(rows_to_remove, idx)
  }
}

## Defining response and covariate dataframes made up from only 
## suitable data
df <- df[-rows_to_remove,]
response <- df$Revenue
covariates <- df[,-c(1, 2, 27)]
genre.covariates <- covariates[,-c(20, 21, 22, 23, 24, 25, 26)]


### Assessing movie genre frequency ###
### ### ### ### ### ### ### ### ### ###

## Function to plot genre frequency data
plotBar <- function(data) {
  ## Set vectors
  genre_values <- c()
  frequency_values <- c()
  category_values <- c()
  ypos_values <- c()
  
  ## Get genre frequency data
  for(i in 1:ncol(data)) {
    len <- length(data[,i])
    total_true <- 0
    total_false <- 0
    for(j in 1:len) {
      if(data[,i][j] == FALSE) {
        total_false <- total_false + 1
      } else { total_true <- total_true + 1 }
    }
    ## Update vectors with genre information
    genre_values <- c(genre_values, colnames(data[i]), colnames(data[i]))
    frequency_values <- c(frequency_values, total_true, total_false)
    category_values <- c(category_values, "True", "False")
    ypos_values <- c(ypos_values, 0.5 * total_true,
                     total_true + total_false - 0.5 * total_false)
  }
  ## Create data frame for genre frequency
  genre_freq <- data.frame(
    Genres = genre_values,
    Frequency = frequency_values,
    Category = category_values
  )
  ## Plot the genre frequency data
  ggplot(genre_freq, aes(x = Genres, y = Frequency)) +
    ggtitle("Frequency of Genres within movies") + 
    geom_col(aes(fill = Category), width = 0.9) +
    guides(fill=guide_legend(title="Present in movie?")) +
    geom_text(aes(label = Frequency), y = ypos_values,color = "white") +
    theme(text = element_text(size = 16, family = "Luminari"),
          axis.text.y = element_text(size = 14, family = "Luminari"),
          axis.text.x = element_text(size = 14, family = "Luminari"),
          plot.title = element_text(hjust = 0.5))
  
}

plotBar(genre.covariates)

## Remove genres that do not have sufficient data to be included
## within our model
covariates <- covariates[-c(6, 10, 12, 16, 18, 19)]

## Regress Revenue on the adequate covariates
M <- lm(response ~ ., data=covariates)






























###################################
###################################
#####                         #####
##########    OUTLIERS    #########
#####                         #####
###################################
###################################

###      Assessing X outliers       ###
### ### ### ### ### ### ### ### ### ###

## Computing leverage
M <- lm(response ~ ., data=covariates)
Xmat <- model.matrix(M) ## design matrix
H <- Xmat%*%solve(t(Xmat)%*%Xmat, tol = 1e-20)%*%t(Xmat) ## Hat matrix
diag(H)
lev <- hatvalues(M) ## leverage (h_i)
hbar <- mean(lev) ## \bar{h}
c(sum(lev),ncol(model.matrix(M)))## check trace is same as rank of 

## Plotting leverage
plot(lev,ylab="Leverage")
abline(h=2*hbar,lty=2, col = 'red') ## add line at 2hbar
ids <- which(lev>2*hbar) ## x values for labelling points >2hbar
points(lev[ids]~ids,col="red",pch=19) ## add red points >2hbar
text(x=ids,y=lev[ids], labels=ids, cex= 0.6, pos=2) ## label points >2hbar

## Investigating high leverage points
df[ids,]
hist(response,xlab="Outcome")
abline(v=response[2894],lwd=2,col="blue") ## add highest leverage point

###      Assessing Y outliers       ###
### ### ### ### ### ### ### ### ### ###

## studentized residuals
res <- resid(M) # raw residuals
stud <- res/(sigma(M)*sqrt(1-lev)) # studentized residuals


## refit the model n times 
n <- nrow(df) ## number of observations
e_i <- rep(NA,n) ## jackknife/LOO residuals (raw)
r_i <- rep(NA,n) ## jackknife/LOO residuals (studentized)
sigma_i <- rep(NA,n)
for(ii in 1:n){
  resp <- response[-ii] ## exclude obs i
  dat <- covariates[-ii,]
  g_i <- lm(resp~.,data=dat) ## fit model
  ## get jackknife residual (not studentized)
  e_i[ii] <- response[ii]-predict(g_i,newdata=cbind(covariates, response)[ii,]) 
  ## get jackknife residual (studentized)
  xi <- model.matrix(M)[ii,] ## x for new obs i
  X_i <- model.matrix(g_i) ## design matrix excluding obs i
  r_i[ii] <- e_i[ii]/(sigma(g_i)*sqrt(1+t(xi)%*%solve(t(X_i)%*%X_i, tol = 1e-20)%*%xi))
  ## sqrt(MSE) excluding i
  sigma_i[ii] <- sigma(g_i) ## get jackknife sigma(-i)
}

## compute jackknife residuals in 4 ways
### using jackknife residuals e(-i)
jack0 <- r_i
### formula with raw residuals e
jack1 <- res/((sigma_i*sqrt(1-lev))) 
### with no need to refit
p <- 4 ## number of  covariates
jack2 <- stud*sqrt((n-p-2)/(n-p-1-stud^2)) 
### built in function
jack3 <- rstudent(M) 

## check that these are the same (aside from rounding error)
sum(round(jack1,10)!=round(jack0,10))
sum(round(jack1,10)!=round(jack2,10))
sum(round(jack1,10)!=round(jack3,10))
sum(abs(jack1-jack0))
sum(abs(jack1-jack2))
sum(abs(jack1-jack3))


### jackknife residuals
plot(jack1,ylab="Studentized Jackknife Residuals")
points(jack1[ids]~ids,col="red",pch=19) ## add high leverage points
text(ids,jack1[ids], labels=ids, cex= 0.6, pos=2) ## label points >2hbar

plot(abs(jack1),ylab="|Studentized Jackknife Residuals|")
points(abs(jack1)[ids]~ids,col="red",pch=19) ## add high leverage points
text(ids,abs(jack1)[ids], labels=ids, cex= 0.6, pos=2) ## label points >2hbar




























###################################
###################################
#####                         #####
#######  MODEL ASSUMPTIONS  #######
#####                         #####
###################################
###################################


###       Assessing Normality       ###
### ### ### ### ### ### ### ### ### ###
res1 <- resid(all.M) # raw residuals
stud1 <- res1/(sigma(all.M)*sqrt(1-hatvalues(all.M))) # studentized residuals

## plot distribution of studentized residuals
hist(stud1,breaks=12,
     probability=TRUE,xlim=c(-4,4),
     xlab="Studentized Residuals",
     main="Distribution of Residuals")
grid <- seq(-3.5,3.5,by=0.05)
lines(x=grid,y=dnorm(grid),col="blue") # add N(0,1) pdf

## qqplot of studentized residuals
qqnorm(stud1)
abline(0,1) # add 45 degree line


###        Assessing Linearity      ###
### ### ### ### ### ### ### ### ### ###
for(idx in 1:length(all.covariates)) {
  M.y <- lm(all.response ~ ., data=all.covariates[-c(idx)])
  M.x <- lm(all.covariates[[c(idx)]] ~ ., data=all.covariates[-c(idx)])
  res.y <- resid(M.y) # raw residuals
  res.x <- resid(M.x) # raw residuals
  ## plot of studentized residuals vs fitted values
  xtitle <- paste("Residuals of", names(all.covariates)[idx], "regressed on all other covariates", sep = " ")
  ytitle <- paste("Residuals of Revenue regressed on all covariates except", names(all.covariates)[idx], sep = " ")
  plot(res.y~res.x,
       xlab=xtitle,
       ylab=ytitle,
       main="e_y vs x_y")
  abline(lm(res.y ~ res.x), col = "blue") # add line
}

###  Assessing Heteroskedasticity   ###
### ### ### ### ### ### ### ### ### ###

# initial estimates (OLS)
Mcurrent <- lm(all.response ~ .,data=all.covariates)
resid <- abs(Mcurrent$residuals)
lresid <- log(resid^2)
Mg <- lm(lresid ~ ., data=all.covariates)
ghat <- fitted(Mg)
hhat <- exp(ghat)
Mnew <- lm(all.response ~ ., data= all.covariates, weights = 1/hhat)
bptest(Mnew)

wols1 <- lm(all.response ~ ., data = all.covariates, weights = 1/abs(fitted(all.M)))
wols2 <- lm(all.response ~ ., data = all.covariates, weights = 1/fitted(all.M)^2)
wols3 <- lm(all.response ~ ., data = all.covariates, weights = 1/resid(all.M)^2)
wols4 <- lm(all.response ~ ., data = all.covariates, weights = 1/abs(resid(all.M)))

resid_auxpanel(residuals = resid(Mnew), 
               predicted = fitted(Mnew), 
               plots = c("resid", "index"))

resid_auxpanel(residuals = sqrt(1/abs(fitted(all.M)))*resid(wols1), 
               predicted = fitted(wols1), 
               plots = c("resid", "index"))

resid_auxpanel(residuals = sqrt(1/fitted(all.M)^2)*resid(wols2), 
               predicted = fitted(wols2), 
               plots = c("resid", "index"))

resid_auxpanel(residuals = sqrt(1/resid(all.M)^2)*resid(wols3), 
               predicted = fitted(wols3), 
               plots = c("resid", "index"))

resid_auxpanel(residuals = sqrt(1/abs(resid(all.M)))*resid(wols4), 
               predicted = fitted(wols4), 
               plots = c("resid", "index"))

resid_auxpanel(residuals = sqrt(1/hhat)*resid(Mnew), 
               predicted = fitted(Mnew), 
               plots = c("resid", "index"))

summary(wols1)
summary(wols2)
summary(wols3)
summary(wols4)

bptest(wols1)
bptest(wols2)
bptest(wols3)
bptest(wols4)




