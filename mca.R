library("FactoMineR")
library("factoextra")

df <- read.csv("november_2018.csv")
head(df)
row.names(df) <- df$gigyaid
df$gigyaid <- NULL

res.mca <- MCA(df, graph = FALSE)
eigenvalues <- get_eigenvalue(res.mca)
plot(fviz_screeplot(res.mca, addlabels = TRUE, ylim = c(0, 45)))
plot(fviz_mca_var(res.mca, choice = "mca.cor", 
             ggtheme = theme_minimal()))
plot(fviz_mca_var(res.mca, ggtheme = theme_minimal()))

library("corrplot")
corrplot(var$cos2, is.corr=FALSE)

plot(fviz_mca_var(res.mca,
             ggtheme = theme_minimal()))

plot(fviz_cos2(res.mca, choice = "var", axes = 1))
plot(fviz_contrib(res.mca, choice = "var", axes = 1, top = 30))
plot(fviz_contrib(res.mca, choice = "var", axes = 2, top = 30))