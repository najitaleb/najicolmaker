# -*- coding: utf-8 -*-

import pandas as pd
import argparse
import os
import yaml
import json
import requests
import bioblend
import pexpect
from bioblend import galaxy

def convertPath(path):
    sep= os.sep
    if sep != '/':
          path = path.replace(sep, '/')
    return path



parser = argparse.ArgumentParser(description='File takes tab-separated input file \
                                 and outputs .yml file. galaxy then creates collection \
                                 from yaml file with api ')

parser.add_argument('--collection_type', type=str, default='list:list:list',
                    help='list:list:list or list:list:paired')

#parser.add_argument('path_to_dir', type=str,
#                    help='Input path to directory where manifest is located')

parser.add_argument('--output_file_name', type=str, default='newcol.yml',
                    help='Name you want to give to output yaml file')

parser.add_argument('--manifest_name', type=str, default='man1.csv',
                    help='input the manifest file you want to read')  

parser.add_argument('--collection_name', type=str, default='FCS Collection',
                    help='input what name to give the collection in Galaxy')

parser.add_argument("--url", type=str, dest="url", required=True \
                    , help="Galaxy URL", default="http://10.15.33.17:9280")
    
parser.add_argument("--api", type=str, dest="api_key" \
                    , required=True, help="API Key", default = "31cf2d7a932b12806369facfe0c0f0c8")

#parser.add_argument('--target', type=str,
                        #help='file describing data library to fetch')

parser.add_argument("--fcsdirname", type=str, required=True \
                    , help="Input the name of the directory with FCS files and manifest"\
                    , default = "exampledir")



args = parser.parse_args()


gi = galaxy.GalaxyInstance(url= args.url, key=args.api_key)

fcsdirpath = os.path.abspath(str(args.fcsdirname))


df = pd.read_csv(str(args.manifest_name), sep ="\t" )  # dataframe of all columns
dfjr = df.filter(like='path', axis=1) #dataframe of only file[x] columns


if args.collection_type == "list:list:list":

    
    f = open(str(args.output_file_name),"w+")
    f.write("destination:\n  ")   
    f.write("type: hdca\n  ")  
    f.write("name: Test Set\n  ") #change hardcoded name
    f.write("description: a\n") 
    f.write("collection_type: " + str(args.collection_type) + '\n') 
    # add option for paired files
    f.write("name: " + str(args.collection_name) + "\n")
    f.write("elements:\n")


    
    i=1
    for line in df:
        f.write("  - name: " + "Data Samples" + "\n    ")
        f.write("elements:\n    ")
        
        f.write("- name: " + str(df.iloc[i-1][0]) + "\n      ")
        f.write("elements:\n        ")
        
        f.write("- src: path\n          ")
        f.write("link_data_only: true\n          ")
        badpath = str(dfjr.iloc[i-1][0])
        goodpath = convertPath(badpath)
        f.write("path: " + goodpath + "\n          ")
        j = dfjr.iloc[0][0]
        k = j.split('.',1)[1]
        f.write("ext: " + k + "\n\n")
                   
        if i == df.shape[0]:
            break
        else:
            i+=1
    
    
    my_str = str(args.output_file_name)
    substr = "."
    inserttxt = "man"
    idx = my_str.index(substr)
    mancol = my_str[:idx] + inserttxt + my_str[idx:]
    
    
    
    g = open(mancol,"w+")
    g.write("destination:\n  ")   
    g.write("type: hdca\n  ")  
    g.write("name: Manifest\n  ") #change hardcoded name
    g.write("description: a\n") 
    g.write("collection_type: " + str(args.collection_type) + '\n') 
    # add option for paired files
    g.write("name: Manifest" + "\n")
    g.write("elements:\n")
    g.write("  - name: " + "Data Samples" + "\n    ")
    g.write("elements:\n    ")
        
    g.write("- name: man test " + "\n      ")
    g.write("elements:\n        ")
    
    g.write("- src: path\n          ")
    g.write("link_data_only: true\n          ")

    g.write("path: " + str(os.path.abspath(args.manifest_name)) + "\n          ")
    pol = str(args.manifest_name)
    manext = pol.split('.',1)[1]
    g.write("ext: " + manext + "\n\n")



            
            
 ################################################################################### conditional for paired

           
elif args.collection_type == "list:list:paired":
    
    f = open(str(args.output_file_name),"w+")
    f.write("destination:\n  ")   
    f.write("type: hdca\n  ")  
    f.write("name: Test Pair\n  ") #change hardcoded name
    f.write("description: a\n") 
    f.write("collection_type: " + str(args.collection_type) + '\n')
    f.write("name: " + str(args.collection_name) + "\n")
    f.write("elements:\n")


    i=1
    for line in df:
        f.write("  - name: " + str(df.iloc[i-1][0]) + '\n    ')
        f.write("elements:\n    ")
        f.write("- name: aaa\n      ")
        f.write("elements:\n      ")
        f.write("- src: path\n        ")
        f.write("name: forward \n        ")
        f.write("link_data_only: true\n        ")
        
        badpath = str()
        goodpath = convertPath(badpath)
        
        f.write("path: " + goodpath + "\n        ")      
        j = df.iloc[0][1]
        k = j.split('.',1)[1]

        f.write("ext: " + k + "\n      ")
        f.write("- src: path\n        ")
        f.write("name: reverse \n        ")
        f.write("link_data_only: true\n        ")
        badpath2 = str(dfjr.iloc[i-1][1])
        goodpath2 = convertPath(badpath2)
        
        f.write("path: " + goodpath2 + "\n        ")
               
        f.write("ext: " + k + "\n\n") 
        if i == df.shape[0]:
            break
        else:
            i+=1
            
    my_str = str(args.output_file_name)
    substr = "."
    inserttxt = "man"
    idx = my_str.index(substr)
    mancol = my_str[:idx] + inserttxt + my_str[idx:]        
            
            
    g = open(mancol,"w+")
    g.write("destination:\n  ")   
    g.write("type: hdca\n  ")  
    g.write("description: a\n") 
    g.write("collection_type: list:list:list" + '\n') 
    # add option for paired files
    g.write("name: Manifest" + "\n")
    g.write("elements:\n")
    g.write("  - name: " + "Data Samples" + "\n    ")
    g.write("elements:\n    ")
        
    g.write("- name: man test " + "\n      ")
    g.write("elements:\n        ")
    
    g.write("- src: path\n          ")
    g.write("link_data_only: true\n          ")

    g.write("path: " + str(os.path.abspath(args.manifest_name)) + "\n          ")
    pol = str(args.manifest_name)
    manext = pol.split('.',1)[1]
    g.write("ext: " + manext + "\n\n")

        

#############################################################################################
#start of fetch            
    
    
    
with open(args.output_file_name, "r") as f:
    target = yaml.load(f)

histories_url = args.url + "/api/histories"
new_history_response = requests.post(histories_url, data={'key': args.api_key})
	
print(new_history_response.json())
fetch_url = args.url + '/api/tools/fetch'
payload = {
 'key': args.api_key,
    'targets': json.dumps([target]),
    'history_id': new_history_response.json()["id"]
        
}
print(payload)
hist1 = str(gi.histories.get_most_recently_used_history()["id"])
response = requests.post(fetch_url, data=payload,)

print(response.content)
print("\n")



with open(mancol, "r") as g:
    target = yaml.load(g)



payload = {
 'key': args.api_key,
    'targets': json.dumps([target]),
    'history_id': hist1 
        
}
 
response = requests.post(fetch_url, data=payload,)
print(response.content)
