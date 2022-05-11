#!/usr/local/bin/python3

import jinja2
import cgi
import mysql.connector
import numpy as np
from violinplot import plot_probe

def main():

	templateLoader = jinja2.FileSystemLoader( searchpath='templates')
	env = jinja2.Environment(loader=templateLoader)
	template = env.get_template('gene_page.html')
	print('Content-type: text/html\n')
	f = cgi.FieldStorage()
	params = {}
	for key in f.keys():#get gene symbol and name from url
	  params[key] = f[key].value

	conn = mysql.connector.connect(user='rhamil32', password='@101@9+1z',
	host='localhost', database='rhamil32')
	curs = conn.cursor()
	if 'symbol' not in params.keys() or 'name' not in params.keys():
		params['symbol']="NOTFOUND"
		params['name']="NOTFOUND"

	qry = """select Probe.probe_id, Probe.p_value, Probe.fold_change from Gene join Probe on Gene.gene_symbol=Probe.gene_symbol	 where Gene.gene_symbol=%s and Gene.gene_name like %s;"""
	name=params["name"].replace("_"," ")#the spaces in the url were replaced with underscores to keep url validity
	curs.execute(qry, (params['symbol'],'%'+name+'%'))
	probe_results=dict()
	for probe_id,p_value,fold_change in curs:
		probe_results[probe_id]=[p_value,fold_change,[],[]]

	qry = """select Expression.sample_id, Expression.probe_id, Expression.value from Gene join Probe on Gene.gene_symbol=Probe.gene_symbol join Expression on Probe.probe_id=Expression.probe_id where Gene.gene_symbol=%s and Gene.gene_name like %s;
		"""
	curs.execute(qry, (params['symbol'],'%'+name+'%'))

	for sample_id,probe_id,value in curs:#get data for violin plot
		if "normal" in sample_id:
			probe_results[probe_id][2].append(value)
		else:
			probe_results[probe_id][3].append(value)
	for probe in probe_results.keys():#get means for probe table
		probe_results[probe].append(np.mean(probe_results[probe][2]))
		probe_results[probe].append(np.mean(probe_results[probe][3]))
	
	message=f"{len(probe_results)} probe(s) found matching the specified gene name and symbol."
	temp=[]
	for probe in probe_results.keys():#data for probe table
		temp.append([probe,probe_results[probe][4],probe_results[probe][5],probe_results[probe][1],probe_results[probe][0],'"http://bfx3.aap.jhu.edu/rhamil32/final_project/plots/'+probe+'.png"'])
		plot_probe(probe_results,probe)
	qry="""select Gene_ontology.go_term from Gene join Gene_ontology on Gene.gene_symbol=Gene_ontology.gene_symbol where Gene.gene_symbol=%s and Gene.gene_name like %s;"""
	curs.execute(qry, (params['symbol'],'%'+params['name'].replace("_"," ")+'%'))#get GO terms for button links
	
	terms=[go_term[0] for go_term in curs]
	
	print(template.render(cursor=temp,message=message,symbol=params["symbol"],name=name,go_terms=zip([term.replace(" ","_") for term in terms],terms)))
	curs.close()
	conn.close()


if __name__ == '__main__':
	main()
