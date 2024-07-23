import json
from datakey import DataKey

class GenerateController:
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
            "const {SuccessResponse,CREATED,GETLISTOK,} = require('../core/success.response');\n",
            "const BaseController = require('./base/base.controller');\n",
            "const ErrorMessage = require('../enum/error.message');\n"
            "const { BadRequestError, NotFoundError } = require('../core/error.response');\n"
            "const { getInfoData } = require('../utils');\n"
            "const AppRouterName = require('../routers/router.name');\n\n"

            "//helper\n"
            f"const {self.className}Filter = require('../helpers/filter/{self.fileName}.filter');\n"
            f"const {self.modelName}Validator = require('../helpers/validate/{self.fileName}.validate');\n",

            "//service\n"
            f"const {self.className}Service = require('../services/{self.fileName}.service');\n"
        ]
        
        FILED_RETURN = [];
        FILED_RETURN_CREATE = [];
        FILED_UNSELECTED = ["'__v'"];
        KEY_IMAGE = "";

        funcCheckExist = [];
        createdConditionCheckExist = [];

        updateConditionCheckExist = [];

        for obj in self.data:
            obj_key = obj[DataKey.key.value];
            if (not DataKey.is_nan(obj.get(DataKey.check_exist.value))) and (obj.get(DataKey.type.value) == DataKey.nameObjectType.value ):
                obj_ref = obj[DataKey.ref.value];
                lines.append(f"const {obj_ref}Service = require('../services/{obj_ref.lower()}.service');\n")

                #funtion check
                funcCheckExist.append(f"check{obj_ref}Exist = async function ({obj_ref.lower()}Id)" + "{\n")
                funcCheckExist.append(f"if (!{obj_ref.lower()}Id)" + "{ return; }\n")
                funcCheckExist.append(f"return await {obj_ref}Service.checkExists({obj_ref.lower()}Id);" + "}\n")

                #condition check
                createdConditionCheckExist.append(f"const {{{obj_key}}} = req.body;")
                createdConditionCheckExist.append(f"await this.check{obj_ref}Exist({obj_key}); ")

            if (not DataKey.is_nan(obj.get(DataKey.check_exist.value))) and not (obj.get(DataKey.type.value) == DataKey.nameObjectType.value ):
                method_name = DataKey.to_first_upper_case(obj[DataKey.key.value]);
                obj_key = obj[DataKey.key.value];

                func_name = f"checkExists{self.className}By{method_name}"

                funcCheckExist.append(f"{func_name} = async function ({obj_key}, id) " + "{\n")
                funcCheckExist.append(f"if (!{obj_key})" + "{ return; }\n")
                funcCheckExist.append(f"const found{self.className} = await {self.className}Service.find{self.className}By{method_name}({obj_key});\n")
                funcCheckExist.append(f"if (found{self.className} && (found{self.className}._id.toString() !== id?.toString()))" + "{\n")
                funcCheckExist.append(f"throw new BadRequestError(ErrorMessage.{obj_key.upper()}_IS_EXISTING);" + "}return;};")

                createdConditionCheckExist.append(f"const {{{obj_key}}} = req.body;")
                createdConditionCheckExist.append(f"await this.{func_name}({obj_key}, null);")

                updateConditionCheckExist.append(f"const {{{obj_key}}} = req.body;")
                updateConditionCheckExist.append(f"await this.{func_name}({obj_key}, {self.modelName}Id);")


            if DataKey.contains_image(obj_key):
                KEY_IMAGE = obj_key

            if not DataKey.is_nan(obj.get(DataKey.select.value)):
                FILED_RETURN.append(f"'{obj_key}'")
                if not (obj.get(DataKey.type.value) == DataKey.nameObjectType.value ):
                    FILED_RETURN_CREATE.append(f"'{obj_key}'")

            if not DataKey.is_nan(obj.get(DataKey.unselect.value)):
                FILED_UNSELECTED.append(f"'{obj_key}'")
        
        lines.append(f"\nconst FILED_RETURN = ['_id', {", ".join(FILED_RETURN)}];\n")
        lines.append(f"\nconst FILED_RETURN_CREATE = ['_id', {", ".join(FILED_RETURN_CREATE)}];\n")
        lines.append(f"const FILED_UNSELECTED = [{", ".join(FILED_UNSELECTED)}];\n")
        lines.append(f"const KEY_IMAGE = '{KEY_IMAGE}';\n\n")
        
        lines.append(f"class {self.className}Controller extends BaseController \n")
        lines.append("{\n")
   
        lines.extend(funcCheckExist);

        lines.append(f"""
        getAll{self.className} = async (req, res, next) => {{
            const options = super.getPageAndItem(req.query);

            const filter = new {self.className}Filter(req.query).getFilter();

            const {{ data, pagination }} = await {self.className}Service.findAll{self.className}({{ filter, options, select: FILED_RETURN }});

            await new GETLISTOK({{ message: '', data, pagination }}).send(req, res, {{ saveCaching: true }});
        }};

        get{self.className}Detail = async (req, res, next) => {{
            const {self.modelName}Id = req.query.{self.modelName}Id;

            super.checkDataNotNull({self.modelName}Id, ErrorMessage.{self.modelName.upper()}_ID_IS_REQUIRED);

            const result = await {self.className}Service.findDetailById({self.modelName}Id, FILED_UNSELECTED);

            super.checkDataNotNull(result, ErrorMessage.{self.modelName.upper()}_NOT_FOUND);

            await new SuccessResponse({{ message: '', data: result }}).send(req, res, {{ saveCaching: true }});
        }};

        create{self.className} = async (req, res, next) => {{
            super.validate(req.body, {self.modelName}Validator.create);
            {"\n".join(createdConditionCheckExist)}

            const data = await super.getImageFile(req, {{ ...req.body, creatorBy: req.user.userId }}, KEY_IMAGE);

            const result = await {self.className}Service.create{self.className}(data);

            await new CREATED({{ message: ErrorMessage.{self.modelName.upper()}_CREATED, data: getInfoData({{ object: result, fileds: FILED_RETURN_CREATE }}) }}).send(req, res, {{ deleteCaching: true, deleteOptions: [AppRouterName.{self.fileName}] }});
        }};

        update{self.className} = async (req, res, next) => {{
            super.validate(req.body, {self.modelName}Validator.update);
            const {self.modelName}Id = req.query.{self.modelName}Id;
            super.checkDataNotNull({self.modelName}Id, ErrorMessage.{self.modelName.upper()}_ID_IS_REQUIRED);
            {"\n".join(updateConditionCheckExist)}

            const data = super.updateNestedObjectParse({{ ...req.body, updatedBy: req.user.userId }});
            const imageData = await super.getImageFile(req, data, KEY_IMAGE);

            const result = await {self.className}Service.update{self.className}({{ {self.modelName}Id, data: imageData }});
            super.checkDataNotNull(result, ErrorMessage.{self.modelName.upper()}_NOT_FOUND);

            await new SuccessResponse({{ message: ErrorMessage.{self.modelName.upper()}_UPDATED, data: getInfoData({{ object: result, fileds: FILED_RETURN_CREATE }}) }}).send(req, res, {{ deleteCaching: true, deleteOptions: [AppRouterName.{self.fileName}] }});
        }};
        """)
        

        lines.append("}\n\n")
        lines.append(f"module.exports =new {self.className}Controller();")
        # Write the lines to the file
        with open(f"backend/controllers/{self.fileName}.controller.js", "w") as f:
            f.writelines(lines)
