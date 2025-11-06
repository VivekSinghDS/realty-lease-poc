import os 
from typing import List
from adapters.database.base import Database 
import json 

class _Local(Database):
    def __init__(self):
        pass 
    
    def create(self, query: dict):
        company_name: str = query.get('name', 'None')
        uid = company_name.lower().replace('-', '_').replace(' ', "_")
        if not os.path.exists(f"./companies/{company_name}"):
            os.makedirs(f"./companies/{uid}")
            os.makedirs(f"./companies/{uid}/lease")
            os.makedirs(f"./companies/{uid}/amendments")
            
        return {
            "message": "Company successfully created",
            "uid": uid, 
            "name": company_name
        }
    
    def get(self):
        company_folder = f"./companies"

        companies = []
        for file_name in os.listdir(company_folder):
            companies.append(file_name)

        return {"companies": companies}
    
    def get_single(self, query: dict):
        uid = query.get("uid", "None")
        base_path = os.path.join("./companies", uid)

        def load_json_files(folder, multiple=True):
            path = os.path.join(base_path, folder)
            if not os.path.isdir(path):
                return [] if multiple else {}
            files = [f for f in os.listdir(path) if f.endswith(".json")]
            if not files:
                return [] if multiple else {}
            if multiple:
                return [json.load(open(os.path.join(path, f))) for f in files]
            return json.load(open(os.path.join(path, files[0])))

        return {
            "lease": load_json_files("lease", multiple=False),
            "amendments": load_json_files("amendments")
        }
        
    def update(self, query: dict):
        return {
            
        }
        
    def delete(self, query: dict):
        return {
            
        }