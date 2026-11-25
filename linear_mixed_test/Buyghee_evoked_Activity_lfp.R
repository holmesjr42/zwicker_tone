library(Matrix)
library(lme4)
library(lmerTest)
library(MASS)
library(car)
library(mvtnorm)
library(survival)
library(TH.data)
library(multcomp)
library(emmeans)
library(ggplot2)
library(ggpubr)


############ read the file to analyse
InputOutput = read.csv(file.choose( ))

#summary(InputOutput)
#which(is.na(InputOutput)==T)

#boxplot(MUA ~ When*Layer,
#        col=c("white","lightgray"),InputOutput)


############################################################ create our models

Full.model = lmer(log(-amplitude, base = exp(1)) ~ condition + layer + dB + (1|sample), data=InputOutput,REML=FALSE)# log(amplitude, base = exp(1))
summary(Full.model)

Partial_1.model = lmer(log(-amplitude, base = exp(1)) ~ condition + layer + (1|sample), data=InputOutput,REML=FALSE)
summary(Partial_1.model)

Partial_2.model = lmer(log(-amplitude, base = exp(1)) ~ condition + dB + (1|sample), data=InputOutput,REML=FALSE)
summary(Partial_2.model)

Condition.model = lmer(log(-amplitude, base = exp(1)) ~ condition + (1|sample), data=InputOutput,REML=FALSE)
summary(Condition.model)


################check which model fits best
anova(Full.model,Partial_1.model)
anova(Full.model,Partial_2.model)
anova(Full.model,Condition.model)


################
Anova(Full.model,ddf="Kenward-Roger",refit=FALSE)
Anova(Partial_1.model,ddf="Kenward-Roger",refit=FALSE)
Anova(Partial_2.model,ddf="Kenward-Roger",refit=FALSE)
Anova(Condition.model,ddf="Kenward-Roger",refit=FALSE)


############################################################interactions 
Full.model = lmer(log(-amplitude, base = exp(1)) ~ condition_nr * layer_order * dB + (1|sample), data=InputOutput, REML=FALSE)
summary(Full.model)
Anova(Full.model)
Anova(Full.model, type="III")

############################################################ 
#emmeans(Full.model, list(pairwise ~ condition), adjust = "tukey")
emmeans(Full.model, specs=pairwise ~ condition_nr:layer_order, adjust = "tukey")
emmeans(Full.model, specs=pairwise ~ condition_nr:dB, adjust = "tukey")
hist(residuals(Full.model))
qqnorm(residuals(Full.model))
qqline(residuals(Full.model))
ggqqplot(residuals(Full.model))
plot(fitted(Full.model),residuals(Full.model))
shapiro.test(residuals(Full.model))
############################################################ all layer

