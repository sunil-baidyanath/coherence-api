'''
Created on Dec 9, 2021

@author: sunilthakur
'''

from utils import DynamoDBClient

import json

class Disease(object):
    
    def __init__(self):
        self.tablename = 'diseases'
        self.db = DynamoDBClient()
        
    def get_disease_by_id(self, disease_id, index=None):
        result = self.db.get_item_by_id(self.tablename, disease_id, index)
        
        if result:
            return json.loads(result['data']['S'])
        else:
            return None
        
    
    def get_diseases_by_index(self, index):
        result = self.db.get_items_by_index(self.tablename, index)
        items = []
        if result:
            for item in result:
                items.append(json.loads(item['data']['S'])['preferred_name'].title())
        
        return items
    
    def get_diseases_by_name(self, name):
        index = name[0:1]
        items = []
        params = {'name': name, 'name_index': index}
        
        result = self.db.query_items(self.tablename, params)
        if result:
            for item in result:
                items.append(json.loads(item['data']['S'])['preferred_name'].title())

        return items
        