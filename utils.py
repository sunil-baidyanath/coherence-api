'''
Created on Dec 9, 2021

@author: sunilthakur
'''
'''
Created on Dec 9, 2021

@author: sunilthakur
'''

import json
import boto3
from botocore.exceptions import ClientError

class DynamoDBClient(object):
    
    def __init__(self, config=None):
        
        self.config = config
        self.dynamodb = boto3.client('dynamodb')
        
    
    def exists_table(self, tablename):
        try:
            response = self.dynamodb.describe_table(TableName=tablename)
            print(response)
            return True
        
        except ClientError as ex:
            print(ex)
            return False
    
    def create_table(self, tablename, options):
        # options = {'partition_by': 'name_index', 'sort_by': 'id'}
        
        try:
            response = self.dynamodb.create_table(
                AttributeDefinitions=[
                    {
                        'AttributeName': options['partition_by'],
                        'AttributeType': 'S',
                    },
                    {
                        'AttributeName': options['sort_by'],
                        'AttributeType': 'S',
                    }
                ],
                KeySchema=[
                    {
                        'AttributeName': options['partition_by'],
                        'KeyType': 'HASH',
                    },
                    {
                        'AttributeName': options['sort_by'],
                        'KeyType': 'RANGE',
                    },
                ],
                ProvisionedThroughput={
                    'ReadCapacityUnits': 5,
                    'WriteCapacityUnits': 5,
                },
                TableName = tablename,
            )
            
            print(response)
            return response
            
        except ClientError as ex:
            print(ex)
            return None
            # do something here as you require
            # /pass
        
    def put_items(self, tablename, items):
        for item in items:
            data = {'name_first': {}, 'id': {}, 'data': {}}
            data['name_first']['S'] = item['name_first']
            data['id']['S'] = item['id']
            data['data']['S'] = json.dumps(item)
            
            self.dynamodb.put_item(
                TableName = tablename,
                Item = data)
            
    def get_item_by_id(self, tablename, item_id, name_index = None):
        params = {}
        
        if name_index:
            params['name_index'] = {}
            params['name_index']['S'] = name_index
        
        params['name'] = {}    
        params['name']['S'] = item_id
        
        response = self.dynamodb.get_item(
            Key=params, 
            TableName=tablename
        )
        
        return response['Item']
    
        
    def get_items_by_index(self, tablename, name_index):
        
        output_items = []
        
        scan_kwargs = {
            'FilterExpression': 'name_index = :name_index',
            'ProjectionExpression': "id, #name, #d",
            'ExpressionAttributeNames': {'#d': 'data', '#name': 'name'},
            'ExpressionAttributeValues': {":name_index":{"S":name_index}},
            'TableName': tablename
        }
        
        done = False
        start_key = None
        while not done:
            if start_key:
                scan_kwargs['ExclusiveStartKey'] = start_key
            response = self.dynamodb.scan(**scan_kwargs)
            
            scanned_items = response.get('Items', [])
            for item in scanned_items:
                output_items.append(item)
                
            start_key = response.get('LastEvaluatedKey', None)
            done = start_key is None

        return output_items  
     
    
    def query_items(self, tablename, params):
        item_name = params['name']
        index = params['name_index']
        # table = self.dynamodb.Table(tablename)
        output_items = []
        
        scan_kwargs = {
            'FilterExpression': 'name_index = :name_index',
            'ProjectionExpression': "id, #d",
            'ExpressionAttributeNames': {'#d': 'data'},
            'ExpressionAttributeValues': {":name_index":{"S":index}},
            'TableName': tablename
        }
        
        done = False
        start_key = None
        while not done:
            if start_key:
                scan_kwargs['ExclusiveStartKey'] = start_key
            response = self.dynamodb.scan(**scan_kwargs)
            
            scanned_items = response.get('Items', [])
            for item in scanned_items:
                data = json.loads(item['data']['S'])
                if data['preferred_name'].startswith(item_name):
                    output_items.append(item)
                
            start_key = response.get('LastEvaluatedKey', None)
            done = start_key is None

        return output_items
        
    