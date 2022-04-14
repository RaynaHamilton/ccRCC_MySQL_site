renal<-read.table("../data/Renal_GSE53757.csv",sep=",",header=T,row.names=1)
library("AnnotationDbi")

library("hgu133plus2.db")
#we will write seprate files for probe ids to gene names, probe ids to GO terms 
#and GO terms to GO descriptions to avoid storing lots of wasteful redundant data
#this is similar to how our database will be structured!
probes<-as.character(colnames(renal))
genes <- select(hgu133plus2.db,keys=substr(probes,2,50), columns=c("SYMBOL", "GENENAME","ENTREZID"),keytype="PROBEID")
write.table(genes,file="../data/probes_to_genes.tsv",quote=F,row.names=F)

library("GO.db")
go_terms<-select(hgu133plus2.db,keys=unique(genes$SYMBOL), columns=c("GO"),keytype="SYMBOL")

write.table(go_terms[,c("SYMBOL","GO")],"../data/genes_to_GO.tsv",quote=F,row.names=F)

go_names<-Term(unique(go_terms$GO))
go_names<-cbind(c(names(go_names)),go_names)
write.table(go_names,"../data/GO_to_names.tsv",quote=F,row.names=F)


