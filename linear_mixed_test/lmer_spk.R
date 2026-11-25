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


#-data_loading-------------------------------------------------------
##-3_0_continuous----------------------------------------------------
dats=read.csv("/home/bhc/OneDrive/Work/PhD/projects/zwicker_tone_2018_2021/data/dataset/dataframe/3_0_spk.csv")
dats$condition <- factor(dats$condition, levels = c("control", "NN"))

##3_1_chunked--------------------------------------------------------
dats=read.csv("/home/bhc/OneDrive/Work/PhD/projects/zwicker_tone_2018_2021/data/dataset/dataframe/3_1_spk.csv")
dats$condition <- factor(dats$condition, levels = c("control", "nn_on", "nn_off", "wn_off"))

##3_1_chunked_low_edge--------------------------------------------------------
dats=read.csv(
  "/home/bhc/OneDrive/Work/PhD/projects/zwicker_tone_2018_2021/data/dataset/dataframe/edge/3_1_low_spk.csv"
  )
dats$condition <- factor(dats$condition, levels = c("control", "nn_on", "nn_off", "wn_off"))

##3_1_chunked_high_edge--------------------------------------------------------
dats=read.csv(
  "/home/bhc/OneDrive/Work/PhD/projects/zwicker_tone_2018_2021/data/dataset/dataframe/edge/3_1_high_spk.csv"
  )
dats$condition <- factor(dats$condition, levels = c("control", "nn_on", "nn_off", "wn_off"))

#-factor level adjust---------------------------------------------
dats <- dats[,-1] # just removing index column
dats$layer <- factor(dats$layer, levels = c("supra", "infra", "granular"))
dats$dB <- factor(dats$dB, levels = c(40, 50, 60, 70))
dats$spl <- factor(dats$spl, levels = c("a", "b", "c", "d"))

#-models----------------------------------------------------------------------------------------

mod.full = lmer(log(firing_rate) ~ condition + layer + dB + (1|sample), data=InputOutput,REML=FALSE)#
summary(Full.model)

mod.part1 = lmer(log(firing_rate) ~ condition + layer + (1|sample), data=InputOutput,REML=FALSE)
summary(Partial_1.model)

mod.part2 = lmer(log(firing_rate) ~ condition + dB + (1|sample), data=InputOutput,REML=FALSE)
summary(Partial_2.model)

mod.cond = lmer(log(firing_rate) ~ condition + (1|sample), data=InputOutput,REML=FALSE)
summary(Condition.model)


#-model comparison to find which factor is not important--------------------------------------
anova(mod.full, mod.part1)
anova(mod.full, mod.part2)
anova(mod.full, mod.cond)

#-anova test for each model-------------------------------------------------------------------
Anova(mod.full,ddf="Kenward-Roger",refit=FALSE)
Anova(mod.part1,ddf="Kenward-Roger",refit=FALSE)
Anova(mod.part2,ddf="Kenward-Roger",refit=FALSE)
Anova(mod.cond,ddf="Kenward-Roger",refit=FALSE)

#-interaction_check---------------------------------------------------------------------------
aggregate(log(firing_rate) ~ condition, data=dats, mean)
aggregate(log(firing_rate) ~ layer, data=dats, mean)
with(dats, tapply(log(firing_rate), list(condition, layer), mean))
interaction.plot(x.factor=dats$condition, trace.factor=dats$layer, response=log(dats$firing_rate))
interaction.plot(x.factor=dats$layer, trace.factor=dats$condition, response=log(dats$firing_rate))

#ggplot(dats, aes(x=layer, y=log(firing_rate), color=condition)) + geom_point()
#-interactions-------------------------------------------------------------------------------- 
mod.interact = lmer(log(firing_rate) ~ spl + condition * layer + (1|sample), data=dats, REML=FALSE)

mod.interact3 = lmer(log(firing_rate) ~ condition * layer * spl + (1|sample), data=dats, REML=FALSE)

mod.default = lmer(log(firing_rate) ~ condition + layer + spl + (1|sample), data=dats, REML=FALSE)

mod.interact4 = lmer(log(firing_rate) ~ condition_nr * layer_order * dB + (1|sample), data=inout, REML=FALSE)

# interaction check for models
emmip(mod.interact3, condition ~ layer, CIs=TRUE)
emmip(mod.default, layer ~ spl)

summary(mod.interact3,ddf="Kenward-Roger",refit=FALSE)
anova(mod.interact, type="I")
anova(mod.interact3, type="I")
anova(mod.interact4, type="I")


#-export summary and anova result in csv----------------------------------------------------------
csv1 = summary(mod.interact3)$coefficients
csv2 = anova(mod.interact3, type="I")

write.csv(
  csv1,"/home/bhc/OneDrive/Work/PhD/projects/zwicker_tone_2018_2021/data/dataset/dataframe/3_1_low_spk_summary.csv"
)

write.csv(
  csv2, "/home/bhc/OneDrive/Work/PhD/projects/zwicker_tone_2018_2021/data/dataset/dataframe/3_1_low_spk_anova.csv"
)

#-Post-hoc-----------------------------------------------------------------------------------------
emmeans(mod.interact3, specs=pairwise ~ condition, adjust = "tukey")
emmeans(mod.interact3, specs=pairwise ~ layer, adjust = "tukey")
emmeans(mod.interact3, specs=pairwise ~ spl, adjust = "tukey")
a = emmeans(mod.interact3, specs=pairwise ~ condition:layer, adjust = "tukey")

emmeans(mod.interact3, specs=pairwise ~ condition:spl, adjust = "tukey")
lsmeans(mod.interact3, list(pairwise ~ condition|layer, pairwise ~ layer|condition))

testcl = lsmeans(mod.interact3, list(pairwise ~ condition|layer), adjust = "tukey")
testlc = lsmeans(mod.interact3, list(pairwise ~ layer|condition), adjust = "tukey")
a = test(rbind(testlc, testcl), adjust = "tukey")
b = test(rbind(testcl, testlc), adjust = "tukey")

#-model checking-----------------------------------------------------
hist(residuals(Full.model))
qqnorm(residuals(mod.default))
qqline(residuals(mod.default))
ggqqplot(residuals(mod.interact3))
plot(fitted(mod.interact4),residuals(mod.interact4))
shapiro.test(residuals(mod.interact4))


