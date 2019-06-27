library("FactoMineR")
library("factoextra")

df <- read.csv("data.csv")
head(df)
row.names(df) <- df$gigyaid
df$gigyaid <- NULL
colnames(df)

res.mca <- MCA(df, graph = FALSE)
eigenvalues <- get_eigenvalue(res.mca)
plot(fviz_screeplot(res.mca, addlabels = TRUE, ylim = c(0, 45)))
plot(fviz_mca_var(res.mca, choice = "mca.cor", 
             repel = TRUE, # Avoid text overlapping (slow)
             ggtheme = theme_minimal()))