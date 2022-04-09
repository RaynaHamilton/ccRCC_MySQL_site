#!/usr/local/bin/python3

import jinja2
import cgi
import mysql.connector

def main():
	templateLoader = jinja2.FileSystemLoader( searchpath='templates')
	env = jinja2.Environment(loader=templateLoader)
	template = env.get_template('unit06_results.html')
    
	form = cgi.FieldStorage()
	product = form.getfirst('product')
	print('Content-type: text/html\n')
	
	conn = mysql.connector.connect(user='rhamil32', password='@101@9+1z',
	host='localhost', database='rhamil32_chado')
	if product is None:
		product=""
	curs = conn.cursor()
	#search featureprop.value for matching gene symbols or gene products, ignoring case:
	qry = 'select feature.uniquename, featureprop.value from feature join featureprop on feature.feature_id=featureprop.feature_id join cvterm on featureprop.type_id=cvterm.cvterm_id where lower(featureprop.value) like %s and cvterm.name ="gene_product_name";'
	curs.execute(qry, ("%"+product.lower()+"%",))
	temp=[[uniquename.decode(),value.decode()] for (uniquename,value) in curs]
	if len(temp)==0:
		message=f"No results found matching the query string '{product}'.\nPlease try a more general search term."
	else:
		message=f"{len(temp)} results found matching the query string '{product}'."
	print(template.render(cursor=temp,message=message))
	curs.close()
	conn.close()

if __name__ == '__main__':
	main()









