library(datasets)

#Load Data
data("mtcars")

#View first 4 rows
head(mtcars, 5)

#information
?mtcars

#Load ggplot package
library(ggplot2)

#create a scatterplot of displacement (disp) and miles per gallon (mpg)
ggplot(aes(x=disp,y=mpg,),data=mtcars)+geom_point()

#add a title
ggplot(aes(x=disp,y=mpg,),data=mtcars)+geom_point()+ggtitle("displacement vs miles per gallon")

#change axis name
ggplot(aes(x=disp,y=mpg,),data=mtcars)+geom_point()+ggtitle("displacement vs miles per gallon") + labs(x = "Displacement", y = "Miles per Gallon")

#make a factor
mtcars$vs <- as.factor(mtcars$vs)

#create a boxplot of the distribution for v-shaped and Straight Engine
ggplot(aes(x=vs, y=mpg), data = mtcars)+ geom_boxplot()

#add colours to boxplot
ggplot(aes(x=vs, y=mpg, fill = vs), data = mtcars)+
  geom_boxplot(alpha=0.3) +
  theme(legend.position = "none")

#Create Histogram of the Weight
ggplot(aes(x=wt), data=mtcars) + geom_histogram(binwidth =0.5)
