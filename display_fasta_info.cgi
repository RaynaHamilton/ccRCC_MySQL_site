#!/usr/local/bin/python3
import jinja2
# This line tells the template loader where to search for template files
templateLoader = jinja2.FileSystemLoader( searchpath="./templates" )
# This creates your environment and loads a specific template
env = jinja2.Environment(loader=templateLoader)
template = env.get_template('unit04.html')
# Load the genes from a GFF file
sequences=[]
file="e_coli_k12_dh10b.faa"
seqid,length,header=None,0,None
for line in open(file):
	if len(sequences)==20:
		break	
	if line.startswith(">"):
		if seqid is not None and header is not None:
			sequences.append((seqid,length,header))
			seqid,length,header=None,0,None
		if "|" in line:
			splitline=line.strip().split("|")
			seqid,header="|".join(splitline[:-1])[1:],splitline[-1]
	elif seqid is not None and header is not None:
		length+=len(line.strip())
	
if seqid is not None and header is not None and length>0:
			sequences.append((seqid,length,header))
		
print("Content-Type: text/html\n\n")
print(template.render(file=file,sequences=sequences))
