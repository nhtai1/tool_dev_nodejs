import json
from datakey import DataKey

class GenerateFilter:
    # modelName + Id
    # className + method
    def __init__(self, fileName, className, modelName, data):
        self.fileName = fileName
        self.className = className
        self.modelName = modelName
        self.data = json.loads(data)

    def create(self):
        # Define the model content
        lines = [
            "'use strict';\n\n",
            "const { convertToObjectIdMongoDb } = require('../../utils');\n\n",
        ]
        

        filterList = [];


        for obj in self.data:
            obj_key = obj[DataKey.key.value];
            obj_type = obj[DataKey.type.value];
            if(obj_type == DataKey.nameObjectType.value):
                filterList.append(f"const {obj_key} = this.query.{obj_key};")
                filterList.append(f"if ({obj_key})" + "{")
                filterList.append(f"filter.{obj_key} = convertToObjectIdMongoDb({obj_key});" +"}")
            
            if(obj_key == DataKey.nameKeyIsActive.value):
                filterList.append(f"const {obj_key} = this.query.{obj_key};")
                filterList.append(f"if ({obj_key})" + "{")
                filterList.append(f"filter.{obj_key} = {obj_key};" +"}")


        
        lines.append(f"class {self.className}Filter\n")
        lines.append("{\n")

        lines.append(f"""
            constructor(query) {{
                this.query = query;
            }}

            getFilter = function () {{
                const filter = {{}};

                {"\n".join(filterList)}
                return filter;
            }};
        """)
        

        lines.append("}\n\n")
        lines.append(f"module.exports = {self.className}Filter;")
        # Write the lines to the file
        with open(f"backend/filter/{self.fileName}.filter.js", "w") as f:
            f.writelines(lines)
