renal<-read.table("../data/Renal_GSE53757.csv",sep=",",header=T,row.names=1)
library("AnnotationDbi")

library("hgu133plus2.db")
#we will write seprate files for probe ids to gene names, probe ids to GO terms 
#and GO terms to GO descriptions to avoid storing lots of wasteful redundant data
#this is similar to how our database will be structured!
probes<-as.character(colnames(renal))
genes <- select(hgu133plus2.db,keys=substr(probes,2,50), columns=c("SYMBOL", "GENENAME","ENTREZID"),keytype="PROBEID")
write.table(genes,file="../data/probes_to_genes.tsv",quote=F,row.names=F,sep="\t")

library("GO.db")
go_terms<-select(hgu133plus2.db,keys=unique(genes$SYMBOL), columns=c("GO"),keytype="SYMBOL")

write.table(go_terms[,c("SYMBOL","GO")],"../data/genes_to_GO.tsv",quote=F,row.names=F,sep="\t")

go_names<-Term(unique(go_terms$GO))
go_names<-cbind(c(names(go_names)),go_names)
write.table(go_names,"../data/GO_to_names.tsv",quote=F,row.names=F,sep="\t")


print(paste(length(unique(genes$PROBEID)),length(unique(genes$SYMBOL)),length(unique(genes$GENENAME))))#"54675 21970 21958" - many-to-one relationship between probe ids and gene symbols, almost all gene symbols have a unique gene name
go_names<-data.frame(go_names)
print(paste(length(unique(go_names$V1)),length(unique(go_names$go_names)))) #"18264 18264" - one-to-one relationship between GO ids and names

temp<-genes[genes$PROBEID %in% names(table(genes$PROBEID)[table(genes$PROBEID)>1]),]
length(unique(temp$PROBEID))#2228 probe ids map to multiple gene symbols (too many to ignore)
