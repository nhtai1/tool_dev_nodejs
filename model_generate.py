import json
from datakey import DataKey

class GenerateModel:
    def __init__(self, fileName, schemaName, documentName, collectionName, data):
        self.fileName = fileName
        self.schemaName = schemaName
        self.documentName = documentName
        self.collectionName = collectionName
        self.data = json.loads(data)

    def create(self):
        # Define the model content
        lines = [
            "'use strict';\n",
            "const mongoose = require('mongoose');\n",
            "const { Schema } = mongoose;\n\n",
            f"const DOCUMENT_NAME = '{self.documentName}';\n",
            f"const COLLECTION_NAME = '{self.collectionName}';\n\n",
            f"const {self.schemaName}Schema = new Schema({{\n"
        ]
        
        # Add fields from the data
        for obj in self.data:
            obj_name = obj[DataKey.key.value]
            obj_type = obj[DataKey.type.value]
            obj_ref = f", ref: '{obj[DataKey.ref.value]}'" if not DataKey.is_nan(obj.get(DataKey.ref.value)) else ""
            obj_required = ", required: true" if not DataKey.is_nan(obj.get(DataKey.required.value)) else ""
            obj_unique = ", unique: true" if not DataKey.is_nan(obj.get(DataKey.unique.value)) else ""
            obj_trim = ", trim: true" if not DataKey.is_nan(obj.get(DataKey.trim.value)) else ""
            obj_default = f", default: {obj[DataKey.default.value]}" if not DataKey.is_nan(obj.get(DataKey.default.value)) else ""
            obj_enum = f", enum: {obj[DataKey.enum.value]}" if not DataKey.is_nan(obj.get(DataKey.enum.value)) else ""

            command_str = f"type: {obj_type}{obj_ref}{obj_required}{obj_unique}{obj_trim}{obj_default}{obj_enum}"
            lines.append(f"    {obj_name}: {{ {command_str} }},\n")
            # print(command_str)
        
        lines.append("}, {collection: COLLECTION_NAME, timestamps: true,});\n\n")
        lines.append(f"module.exports = mongoose.model(DOCUMENT_NAME, {self.schemaName}Schema);\n")

        # Write the lines to the file
        with open(f"backend/models/{self.fileName}.model.js", "w") as f:
            f.writelines(lines)








