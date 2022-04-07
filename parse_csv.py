#!/usr/bin/env python3

def main():
    col_names=[]
    values=[]

    #parse DAVID results for gene symbols and names
    file=open("DAVID_results.tsv")
    probe_map=dict()
    try: 
        for i,line in enumerate(file):
            if i!=0:
                temp=line.split("\t")
                if len(temp)==3:
                    probe_map[temp[0]]=temp[1] #get O(1) access to gene names from probe name index
    except:
        print("An error occured, perhaps this is not a valid tsv file?")
           
    #parse csv expression data
    file = open("Renal_GSE53757.csv")
    try: 
        for i,line in enumerate(file):
            if i==0:
                col_names=line.split(",")
                indices_to_keep=[]
                for i,val in enumerate(col_names):
                    if val in list(probe_map.keys()):
                        indices_to_keep.append(i)
            else:
                to_add=line.split(",")
                
                if len(to_add)!=len(col_names):
                    
                    raise ValueError("All rows should have the same column count.")
                values.append([to_add[i] for i in indices_to_keep])
                for j,val in enumerate(values[-1]):
                
                    if j!=1:
                        values[-1][j]=float(val)
    except:
        print("An error occured, perhaps this is not a valid csv file?")

    col_names=[col_names[i] for i in indices_to_keep]
    print(f"{len(col_names)} probes found.")
    print(f"{len(values)} samples found.")

    
    #put info into database
    
    conn = mysql.connector.connect(user='hopkins', password='fakepass', host='localhost', database='biotest')
    cursor = conn.cursor()
    
    queries = ["""CREATE TABLE sample(INT sample_id,VARCHAR class);""", """CREATE TABLE expression(INT sample_id,VARCHAR probe_id,FLOAT value);""",
    """CREATE TABLE gene(VARCHAR probe_id,FLOAT p_value, FLOAT fold_change,VARCHAR symbol,VARCHAR name);"""]
    for qry in queries:
        cursor.execute(qry)


    conn.close()

    
if __name__ == '__main__':
    main()