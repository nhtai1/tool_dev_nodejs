import json
from datakey import DataKey

class GenerateValidate:
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
            "const Joi = require('joi');\n\n",
        ]
        

        createdVaildate = [];

        updateVaildate = [];

        for obj in self.data:
            obj_key = obj[DataKey.key.value];
            obj_type = obj[DataKey.type.value];
            if(obj_type == DataKey.nameObjectType.value):
                obj_type = "string";
            type = f"Joi.{obj_type.lower()}()"
            if (not DataKey.is_nan(obj.get(DataKey.create.value))):
                obj_required = ".required()" if not DataKey.is_nan(obj.get(DataKey.required.value)) else ""
                obj_enum = f".valid(...{obj[DataKey.enum.value]})" if not DataKey.is_nan(obj.get(DataKey.enum.value)) else ""
                createdVaildate.append(f"{obj_key}: {type}{obj_enum}{obj_required}")
            
            if (not DataKey.is_nan(obj.get(DataKey.update.value))):
                updateVaildate.append(f"{obj_key}: {type}")


        
        lines.append(f"class {self.className}Validator\n")
        lines.append("{\n")

        lines.append(f"""
        create(body) {{
            const scheme = Joi.object({{
                {",\n".join(createdVaildate)}
            }});
                     
            return scheme.validate(body);
        }};

         update(body) {{
            const scheme = Joi.object({{
                {",\n".join(updateVaildate)}
            }});
                     
            return scheme.validate(body);
        }};

        """)
        

        lines.append("}\n\n")
        lines.append(f"module.exports =new {self.className}Validator();")
        # Write the lines to the file
        with open(f"backend/validate/{self.fileName}.validate.js", "w") as f:
            f.writelines(lines)
