

with open('/Users/vivek.singh/realty-poc/demofile.txt') as file:
    content = file.read()
    
import json 
content = json.loads(content)
data = ""
for i, tab in enumerate(content['tabs']):
    for fragment in tab['documentTab']['body']['content']:
        if "startIndex" not in fragment:
            continue 
        
        if "paragraph" in fragment:
            for value in fragment['paragraph']['elements']:
                
                # print(value)
                if "textRun" in value:
                    data += value['textRun']['content']
    break

with open("refined.txt", "a") as f:
  f.write(data)
    
    