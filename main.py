import pandas as pd
import json

from model_generate import GenerateModel
from service_generate import GenerateService
from controller_generate import GenerateController
from vaildate_generate import GenerateValidate
from filter_generate import GenerateFilter
from router_generate import GenerateRouter

file_path = 'Models.xlsx'

sheets_info = [
    {'SHEET_NAME': 'BU', 'FILE_NAME': 'bu', 'DOCUMENT_NAME': 'BU', 'COLLECTION_NAME': 'bu', 'SCHEMA_NAME': 'bu', 'CLASS_NAME': 'Bu'},
    {'SHEET_NAME': 'Brand', 'FILE_NAME': 'brand', 'DOCUMENT_NAME': 'Brand', 'COLLECTION_NAME': 'brands', 'SCHEMA_NAME': 'brand', 'CLASS_NAME': 'Brand'},
]

for sheet_info in sheets_info:
    sheet_name = sheet_info['SHEET_NAME'];
    print(sheet_name)
    df = pd.read_excel(file_path, sheet_name=sheet_name)
    data_dict = df.to_dict(orient='records')
    json_data = json.dumps(data_dict, indent=4)
    
    model_generator = GenerateModel(sheet_info['FILE_NAME'], sheet_info['SCHEMA_NAME'], sheet_info['DOCUMENT_NAME'], sheet_info['COLLECTION_NAME'], json_data)
    model_generator.create()
    
    service_generator = GenerateService(sheet_info['FILE_NAME'], sheet_info['CLASS_NAME'], sheet_info['SCHEMA_NAME'], json_data)
    service_generator.create()
    
    controller_generator = GenerateController(sheet_info['FILE_NAME'], sheet_info['CLASS_NAME'], sheet_info['SCHEMA_NAME'], json_data)
    controller_generator.create()
    
    validate_generator = GenerateValidate(sheet_info['FILE_NAME'], sheet_info['CLASS_NAME'], sheet_info['SCHEMA_NAME'], json_data)
    validate_generator.create()
    
    filter_generator = GenerateFilter(sheet_info['FILE_NAME'], sheet_info['CLASS_NAME'], sheet_info['SCHEMA_NAME'], json_data)
    filter_generator.create()
    
    router_generator = GenerateRouter(sheet_info['FILE_NAME'], sheet_info['CLASS_NAME'], sheet_info['SCHEMA_NAME'], json_data)
    router_generator.create()
