import json
from datakey import DataKey

class GenerateService:
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
            "const { AppStatus } = require('../enum/app.enum');\n",
            "const AppSeleted = require('../enum/app_selected.enum');\n",
            "const { getSelectData,formatPaginatonPayload,unGetSelectData,} = require('../utils');\n",
            "const { convertToObjectIdMongoDb } = require('../utils');\n"
            "const ErrorMessage = require('../enum/error.message');;\n"
            "const { BadRequestError } = require('../core/error.response');\n\n"

            "const {findAllDocumentSelect} = require('../models/repositories/general.repo');\n"
            f"const {self.modelName}Model = require('../models/{self.fileName}.model');\n\n"

            f"class {self.className}Service  \n",
            "{"
        ]
        
        # check exist
        for obj in self.data:
            if (not DataKey.is_nan(obj.get(DataKey.check_exist.value))) and (not obj.get(DataKey.type.value) == DataKey.nameObjectType.value ):
                method_name = DataKey.to_first_upper_case(obj[DataKey.key.value]);
                obj_key = obj[DataKey.key.value];
                func_name = f"static find{self.className}By{method_name} = async function ({obj_key}) "
                lines.append(f"    {func_name} ")
                lines.append("{\n")
                func_body = f"const found{self.className} = await {self.modelName}Model.findOne({{{obj_key}: {obj_key}}}).lean();\nreturn found{self.className};"
                lines.append(f"{func_body}\n")
                lines.append("}\n\n")


        methods = {
            "find": {
                "suffix": f"{self.className}ByIdLean",
                "args": f"{self.modelName}Id",
                "body": f"const found{self.className} = await {self.modelName}Model.findById({self.modelName}Id).lean();\nreturn found{self.className};"
            },
            "checkExists": {
                "args": f"{self.modelName}Id",
                "body": f"const found{self.className} = await {self.className}Service.find{self.className}ByIdLean({self.modelName}Id);\nif (!found{self.className}) {{\n" + "throw new BadRequestError(`${ErrorMessage."   + f"{self.fileName.upper()}_NOT_FOUND" + "}:${" + f"{self.modelName}Id}}`);\n}}\nreturn found{self.className};"
            },
            "create": {
                "args": "data",
                "body": f"const {self.modelName} = await {self.modelName}Model.create(data);\nreturn {self.modelName};"
            },
            "findDetail": {
                "suffix": "ById",
                "args": f"{self.modelName}Id, unSelected = ['__v']",
                "body": f"const {self.modelName} = await {self.modelName}Model.findById({self.modelName}Id)"
            },
            "update": {
                "args": f"{{{self.modelName}Id, data}}",
                "body": f"const {self.modelName} = await {self.modelName}Model.findOneAndUpdate(\n    {{ _id: convertToObjectIdMongoDb({self.modelName}Id) }},\n    {{ $set: data }},\n    {{ new: true }}\n).lean();\nreturn {self.modelName};"
            },
            "countDocuments": {
                "args": "filter",
                "body": f"return await {self.modelName}Model.countDocuments(filter);"
            },
            "findAll": {
                "args": "{options, sort, filter = {}, select = []}",
                "body": f"const sortBy = {{{self.fileName}_name: 1}};\nreturn await findAllDocumentSelect({{\n    filter,\n    options,\n    sortBy,\n    select,\n    model: {self.modelName}Model,\n}});"
            }
        }
        
        # Generate methods
        for method_name, method_info in methods.items():
            if method_info.get("suffix"):
                func_name = f"{method_name}{method_info['suffix']}"
            else:
                func_name = f"{method_name}{self.modelName.capitalize()}"
            args = method_info.get("args", "")
            lines.append(f"    static {func_name} = async function ({args}) ")
            lines.append("{\n")
           
            if method_name == "findDetail":
                lines.append(f"    {method_info['body']}\n")
                for obj in self.data:
                    if (not DataKey.is_nan(obj.get(DataKey.join_detail.value))) and obj.get(DataKey.type.value) == DataKey.nameObjectType.value:
                        #.populate({{ path: 'creatorBy', select: AppSeleted.user }})
                        obj_key = obj[DataKey.key.value];
                        obj_ref = obj[DataKey.ref.value].lower();
                        lines.append(f".populate({{ path: '{obj_key}', select: AppSeleted.{obj_ref} }})\n")
                lines.append(".select(unGetSelectData(unSelected))\n.lean();\n")
                lines.append(f"\nreturn {self.modelName};\n")
            elif method_name == "findAll" :
                populateList = [];
                for obj in self.data:
                    if (not DataKey.is_nan(obj.get(DataKey.join_get.value))) and obj.get(DataKey.type.value) == DataKey.nameObjectType.value:
                        #.populate({{ path: 'creatorBy', select: AppSeleted.user }})
                        obj_key = obj[DataKey.key.value];
                        print(obj_key)
                        obj_ref = obj[DataKey.ref.value].lower();
                        populateList.append(f"{{ path: '{obj_key}', select: AppSeleted.{obj_ref} }}\n")
                
                if(populateList.__len__ == 0):
                    lines.append(f"    {method_info['body']}\n")
                else:
                   command = f"const sortBy = {{{self.fileName}_name: 1}};\nreturn await findAllDocumentSelect({{\n    filter,\n    options,\n    sortBy,\n    select,\n    model: {self.modelName}Model,\n    populateList: [{",".join(populateList)}]\n}});"
                   lines.append(f"    {command}\n")
            else :
                lines.append(f"    {method_info['body']}\n")
            lines.append("}\n\n")

        lines.append("}\n\n")

        lines.append(f"module.exports = {self.className}Service;")

        # Write the lines to the file
        with open(f"backend/services/{self.fileName}.service.js", "w") as f:
            f.writelines(lines)
