renal<-read.table("../data/Renal_GSE53757.csv",sep=",",header=T,row.names=1)
library("AnnotationDbi")

library("hgu133plus2.db")
#we will write seprate files for probe ids to gene names, probe ids to GO terms 
#and GO terms to GO descriptions to avoid storing lots of wasteful redundant data
#this is similar to how our database will be structured!
probes<-as.character(colnames(renal)[2:length(colnames(renal))])
temp<-probes
for (i in seq(length(probes))){
  if ( substr(probes[i],1,1)=="X" ){
    probes[i]=substr(probes[i],2,50)
  }
}
genes <- select(hgu133plus2.db,keys=probes, columns=c("SYMBOL", "GENENAME","ENTREZID"),keytype="PROBEID")
write.table(genes,file="../data/probes_to_genes.tsv",row.names=F,quote=F,sep="\t",col.names=F)
library("GO.db")
go_terms<-select(hgu133plus2.db,keys=unique(genes$SYMBOL), columns=c("GO"),keytype="SYMBOL")
go_terms<-go_terms[2:length(rownames(go_terms)),] #remove an NNA
write.table(go_terms[,c("SYMBOL","GO")],"../data/genes_to_GO.tsv",quote=F,row.names=F,sep="\t",col.names=F)

go_names<-Term(unique(go_terms$GO))
go_names<-cbind(c(names(go_names)),go_names)
write.table(go_names,"../data/GO_to_names.tsv",quote=F,row.names=F,sep="\t",col.names=F)


print(paste(length(unique(genes$PROBEID)),length(unique(genes$SYMBOL)),length(unique(genes$GENENAME))))#"54675 21970 21958" - many-to-one relationship between probe ids and gene symbols, almost all gene symbols have a unique gene name
go_names<-data.frame(go_names)
print(paste(length(unique(go_names$V1)),length(unique(go_names$go_names)))) #"18264 18264" - one-to-one relationship between GO ids and names as expected

temp<-genes[genes$PROBEID %in% names(table(genes$PROBEID)[table(genes$PROBEID)>1]),]
length(unique(temp$PROBEID))#2228 probe ids map to multiple gene symbols (too many to ignore), unfortunately this is also many-to-many



#now calculate p values and fold changes
t_test<-function(x,s1,s2){ #s1 and s2 are sample indices
  x1<-as.numeric(x[s1])
  x2<-as.numeric(x[s2])
  t_out<-t.test(x1,x2,alternative="two.sided",var.equal=T)
  out<-as.numeric(t_out$p.value)
  return(out)
}

renal<-data.frame(renal)
rownames(renal)<-paste(rownames(renal),renal$type)
renal<-renal[,colnames(renal)!="type"]
temp<-renal
colnames(renal)<-probes

t_results<-c()
for (col in colnames(renal)){#using an apply statement is more efficient here but the memory usage kept crashing R for me
  if (col!="type"){
    t_results<-c(t_results,t_test(renal[,col],grepl("normal",rownames(renal)),grepl("cc",rownames(renal))))
  }
}

t_results<-apply(cbind(rep(1,length(t_results)),t_results*length(t_results)),1,min)#bonferroni correction
#names(t_results)<-colnames(renal)[2:length(colnames(renal))]


control_means<-apply(renal[grepl("normal",rownames(renal)),],2,mean,na.rm=T)
cc_means<-apply(renal[grepl("cc",rownames(renal)),],2,mean,na.rm=T)
fc<-cc_means-control_means#data is log2 scale so fold change is a subtraction

change_results<-cbind(fc,t_results)
change_results<-data.frame(change_results)
colnames(change_results)<-c("fold_change","p_value")
rownames(change_results)<-probes
#just for fun, a volcano plot
plot(change_results)
points(change_results[abs(change_results$fold_change)>=2 & change_results$p_value<=0.05,],col="purple")
points(change_results[rownames(change_results)=="213479_at",],col="red",pch=19)#sanity check - this is the probe id of NPTX2,
#which the paper focused on.  It has a fold change of 4.3x and a p value of 9.67e-14 (with Bonferroni!) in my 
#analysis - overall very significant and the second-largest positive fold change


write.table(change_results,file="../data/probes_to_stats.tsv",quote=F,sep="\t",col.names=F)

