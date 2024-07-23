import json
import math
from enum import Enum

class DataKey(Enum):
    nameObjectType = "Schema.Types.ObjectId"
    nameKeyIsActive = "isActive"

    key = "key"
    type = "type"
    ref = "ref"
    required = "required"
    unique = "unique"
    trim = "trim"
    default = "default"
    enum = "enum"
    check_exist = "check_exist"
    join_get = "join_get"
    join_detail = "join_detail"
    select = "select"
    unselect = "unselect"
    create = "create"
    update = "update"

    @staticmethod
    def is_nan(value):
        try:
            return math.isnan(float(value))
        except (TypeError, ValueError):
            return value == "NaN"

    @staticmethod  
    def to_camel_case(snake_str):
        components = snake_str.split('_')
        if len(components) > 1:
            return components[0] + ''.join(x.title() for x in components[1:])
        return snake_str
    
    @staticmethod  
    def to_first_upper_case(snake_str):
        components = snake_str.split('_')
        if len(components) > 1:
            return ''.join(x.title() for x in components[1:])
        return snake_str
    
    @staticmethod  
    def contains_image(string):
        return "image" in string.lower()


