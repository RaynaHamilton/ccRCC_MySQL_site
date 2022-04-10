renal<-read.table("data/Renal_GSE53757.csv",sep=",",header=T,row.names=1)
library("AnnotationDbi")

library("hgu133plus2.db")
#we will write seprate files for probe ids to gene names, probe ids to GO terms 
#and GO terms to GO descriptions to avoid storing lots of wasteful redundant data
#this is similar to how our database will be structured!
probes<-as.character(colnames(renal))
genes <- select(hgu133plus2.db,keys=substr(probes,2,50), columns=c("SYMBOL", "GENENAME","ENTREZID"),keytype="PROBEID")
write.table(genes,file="data/probes_to_names.tsv",quote=F,row.names=F)

library("GO.db")
go_terms<-select(hgu133plus2.db,keys=substr(probes,2,50), columns=c("GO"),keytype="PROBEID")
write.table(go_terms[c("PROBEID","GO")],"data/probes_to_GO.tsv",quote=F,row.names=F)

go_names<-Term(unique(go_terms$GO))
go_names<-cbind(c(names(go_names)),go_names)
write.table(go_names,"data/GO_to_names.tsv",quote=F,row.names=F)
go_names


kd<-log(kd,2)

t_test<-function(x,s1,s2){ #s1 and s2 are sample indices
  x1<-as.numeric(x[s1])
  x2<-as.numeric(x[s2])
  t_out<-t.test(x1,x2,alternative="two.sided",var.equal=T)
  out<-as.numeric(t_out$p.value)
  return(out)
}
t_result<-apply(kd,1,t_test,s1=1:6,s2=7:11)