#!/usr/bin/python

import json, sys, getopt, re

# Usage: ./get_code.py -i <inputfile>

def main(argv): 
  inputfile = argv[0]
  
  with open(inputfile) as json_data: 
    d=json.load(json_data)
    json_data.close()
  code_array = d["hits"]["hits"]
  
  output_json = []
  
  for element in code_array:
    gistid = element["_id"]
    e = element["_source"]
    code = e["code"].encode('ascii', 'ignore')
    author = e["userId"]
    
    code = get_js_only(code)
    if(code != None): 
      filename = 'data/' + author + '_' + gistid + '.html'
      outfile = open(filename, 'w')
      outfile.write(code)
      simple_e = {}
      simple_e["uid"] = author + '_' + gistid
      simple_e["created_at"] = e["created_at"]
      simple_e["updated_at"] = e["updated_at"]
      simple_e["api"] = e["api"]
      simple_e["readme"] = e["readme"]
      simple_e["description"] = e["description"]
      simple_e["code"] = code # e["code"]
      output_json.append(simple_e)
    
    
  print len(output_json)
  with open('nodes.json', 'w') as datafile:
    json.dump(output_json, datafile)   
    
def get_js_only(code):
  re.DOTALL
  re.MULTILINE
  match = re.search('<script>.*</script>', code, re.DOTALL)
  if(match != None):
    return match.group(0)
  else:
    # print "\n\n-------------------------------------------------------------"
    # print code
    return None
  
if __name__ == "__main__":
   main(sys.argv[1:])