#!/usr/local/bin/python3

import jinja2
import mysql.connector

def main():
	#try:
	sample=dict()
	probe=[]
	expression=dict()
	for i,line in enumerate(open("data/Renal_GSE53757.csv")):
		temp=line.strip().split(",")
		if len(temp)>0:
			if i==0:
				probe=temp[2:]
			else:
				expression[int(temp[0])]=[float(val) for val in temp[2:]]
				sample[int(temp[0])]=temp[1]
	#print(sample,probe)
	
	probes_to_genes=dict()
	genes_to_names=dict()
	for line in open("data/probes_to_genes.tsv"):
		temp=line.strip().split("\t")
		if len(temp)==4:
			if temp[0] not in probes_to_genes.keys():#ideally each probe would map to a single gene, but unfortunately this is not true for ~2000 of them
				probes_to_genes[temp[0]]=[temp[1]]
			else:
				probes_to_genes[temp[0]].append(temp[1])
			genes_to_names[temp[1]]=temp[2] #1-to-1 relationship between gene symbols and names
			
			
	genes_to_go=dict()
	for line in open("data/genes_to_GO.tsv"):
		temp=line.strip().split("\t")
		if len(temp)==2:
			if temp[0] not in genes_to_go.keys():
				if temp[1]!="NA":
					genes_to_go[temp[0]]=[temp[1]] #use a list as we expect a many-to-many relationship between genes and go ids
			else:
				genes_to_go[temp[0]].append(temp[1])
	
	go_to_names=dict()
	for line in open("data/GO_to_names.tsv"):
		temp=line.strip().split("\t")
		if len(temp)==2:
			go_to_names[temp[0]]=temp[1]
			
	#print(sample,probe,expression,probes_to_genes,genes_to_names,genes_to_go)
	#print(probes_to_genes,genes_to_names,genes_to_go)
	conn = mysql.connector.connect(user='rhamil32', password='@101@9+1z',
	host='localhost', database='rhamil32')
	
	curs = conn.cursor()
	
	qry = 'show tables;'
	curs.execute(qry)#curs.execute(qry, ("%"+product.lower()+"%",))
	temp=[table[0] for table in curs]
	print(temp)
	for table in temp:
		curs.execute("drop table "+table+";")
	tables={"Sample":"sample_id int not null, class varchar(6) not null","Gene":"gene_symbol varchar(10) not null, gene_name varchar(50) not null","Expression":"sample_id int not null, probe_id varchar(15) not null, value float not null","Probe":"probe_id varchar(15) not null, gene_symbol varchar(10) not null, p_value float not null, fold_change float not null","Gene_ontology":"gene_symbol varchar(10) not null, go_id char(10) not null","Ontology_term":"go_id char(10) not null, term varchar(200) not null"}
	for table,cols in tables.items():
		qry="create table "+table+"("+cols+");"
		print(qry)
		curs.execute(qry)
		
	for sample_id,class_id in sample.items():
		curs.execute("insert into Sample values (%s,%s);",(sample_id,class_id))
		#curs.execute('select * from Sample;')
		#print([value for value in curs])
	for sample_id,value_list in expression.items():
		for i,value in enumerate(value_list):
			curs.execute("insert into Expression values (%s,%s,%s);",(sample_id,probe[i],value))
	for symbol,name in genes_to_names.items():
		curs.execute("insert into Gene values (%s,%s);",(symbol,name))
	for gene,go_id_list in genes_to_go.items():
		for go_id in go_id_list:
			curs.execute("insert into Gene_ontology values (%s,%s);",(gene,go_id))
	for go_id,go_term in go_to_names.items():
		curs.execute("insert into Ontology_term values (%s,%s);",(go_id,go_term))
	conn.commit()
	curs.close()
	conn.close()

if __name__ == '__main__':
	main()









