#!/usr/local/bin/python3

import cgi, json
import os
import mysql.connector

def main():
	directory="./plots"
	for file in os.listdir(directory):
		os.remove(os.path.join(directory,file))#clean up violinplots made in previous searches
	print("Content-Type: application/json\n\n")
	form = cgi.FieldStorage()
	term = form.getvalue('search_term')
	search_type=form.getvalue('search_type')

	conn = mysql.connector.connect(user='rhamil32', password='@101@9+1z', host='localhost', database='rhamil32')
	cursor = conn.cursor()
	if search_type=="name":
		qry = """
			  SELECT gene_symbol, gene_name
				FROM Gene
			   WHERE gene_name LIKE %s
			   ORDER BY gene_symbol
		"""
	elif search_type=="symbol":
		qry = """
			  SELECT gene_symbol, gene_name
				FROM Gene
			   WHERE gene_symbol LIKE %s
			   ORDER BY gene_symbol
		"""
	elif search_type=="GO":
		qry = """
			  SELECT Gene.gene_symbol, Gene.gene_name, Gene_ontology.go_term
				FROM Gene_ontology inner join Gene
				ON Gene_ontology.gene_symbol=Gene.gene_symbol
			   WHERE go_term LIKE %s
			   ORDER BY Gene.gene_symbol,go_term;
		"""
	cursor.execute(qry, ('%' + term + '%', ))
	gene_symbol,gene_name=None,None
	if search_type in ['name','symbol']:
		results = { 'match_count': 0, 'matches': list() }
		for (gene_symbol,gene_name) in cursor:
			results['matches'].append({'locus_id': gene_symbol, 'product': gene_name,'term':'-'})
			results['match_count'] += 1
	else:
		results = { 'match_count': 0, 'matches': list() }
		for (gene_symbol,gene_name,other) in cursor:
			results['matches'].append({'locus_id': gene_symbol, 'product': gene_name,'other':other})
			results['match_count'] += 1
	conn.close()

	print(json.dumps(results))
	return results
if __name__ == '__main__':
	main()