#!/usr/local/bin/python3

import jinja2
import mysql.connector

def main():
	#try:
	sample=dict()
	probe=[]
	expression=dict()
	for i,line in enumerate(open("data/Renal_GSE53757.csv")):
		temp=line.split(",")
		if len(temp)>0:
			if i==0:
				probe=temp[2:]
			else:
				expression[int(temp[0])]=[float(val) for val in temp[2:]]
				sample[int(temp[0])]=temp[1]
	print(sample,probe)
	conn = mysql.connector.connect(user='rhamil32', password='@101@9+1z',
	host='localhost', database='rhamil32')
	
	curs = conn.cursor()
	#search featureprop.value for matching gene symbols or gene products, ignoring case:
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
	
	curs.close()
	conn.close()

if __name__ == '__main__':
	main()









