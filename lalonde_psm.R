library('MatchIt')
library('tidyverse')
library(dplyr)
library(ggplot2)
library(cowplot)
data(lalonde)


#eda 
sum(is.na(lalonde))
summary(lalonde)
unique(lalonde$race)

lalonde$is_black<-ifelse(lalonde$race=='black',1,0)
lalonde$is_hispan<-ifelse(lalonde$race=='hispan',1,0)
lalonde$is_white<-ifelse(lalonde$race=='white',1,0)

#直接比较
num_cols<- c("age","educ","married","nodegree","re74","re75","re78","is_black","is_hispan","is_white")
lalonde %>%group_by(treat) %>%
  select(one_of(num_cols)) %>%
  summarise_all(funs(mean(.)))

lapply(num_cols, function(v) {t.test(lalonde[, v] ~ lalonde[, 'treat'])})


#lalonde%>%group_by(treat)%>%summarise(avg_age=mean(age),avg_educ=mean(educ),avg_re74=mean(re74),avg_re75=mean(re75),avg_re78=mean(re78))


#拟合
t<-lm(re78~age+educ+married+nodegree+re74+re75+is_black+is_hispan+is_white,data=lalonde)
summary(t)

t.test(lalonde$re74~lalonde$treat)

#psm
set.seed(613)
m <- matchit(treat ~ age+educ+married+nodegree+re74+re75+is_black+is_hispan+is_white,
                  data = lalonde, method = "nearest", replace = FALSE
            ,caliper=0.1
             )



summary(m)
plot(m, type = "jitter", interactive = FALSE)
lalonde$ps=m$distance
m_matched<-get_matches(m)

p1=ggplot(lalonde,aes(x=ps,fill=as.factor(treat)))+geom_density()+
  ggtitle('Propensity Score before matching')
p2=ggplot(m_matched,aes(x=distance,fill=as.factor(treat)))+geom_density()+
  ggtitle('Propensity Score after matching')
plot_grid(p1, p2)

plot(summary(m))


#m_matched<-match.data(m)

t.test(m_matched$re78~m_matched$treat,paired=TRUE)

m_matched['PSID300',]

#check sensitivity and robustness
## add random noise variable 
lalonde$noise=rnorm(614)
m_noise <- matchit(treat ~ age+educ+married+nodegree+re74+re75+is_black+is_hispan+is_white+random_effect,
             data = lalonde, method = "nearest", replace = FALSE
             ,caliper=0.1
)
summary(m_noise)
plot(summary(m_noise))
m_matched_noise<-get_matches(m_noise)
t.test(m_matched_noise$re78~m_matched_noise$treat,paired=TRUE)

## replace treatment variable with placebo 
lalonde$placebo=rbinom(n=614,size=1,prob=sum(lalonde$treat)/614)
m_placebo <- matchit(placebo ~ age+educ+married+nodegree+re74+re75+is_black+is_hispan+is_white+random_effect,
                   data = lalonde, method = "nearest", replace = FALSE
                   ,caliper=0.1)
m_matched_placebo<-get_matches(m_noise)
t.test(m_matched_placebo$re78~m_matched_placebo$placebo,paired=TRUE)