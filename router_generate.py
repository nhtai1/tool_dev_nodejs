import json
from datakey import DataKey

class GenerateRouter:
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
            "const express = require('express');\n",
             "const { authentication, isPermission } = require('../../auth/authUtils');\n",
            "const { isCaching } = require('../../middelware/is_limit');\n",
            f"const {self.modelName}Controller = require('../../controllers/{self.fileName}.controller');\n",
            "const asyncHandler = require('../../helpers/asyncHandler');\n",
            "const { uploadImage } = require('../../utils/upload/multer.upload');\n",
            "const { UserRole } = require('../../enum/app.enum');\n\n",
            "const router = express.Router();\n\n",
        ]
        


        uploadImage = "";

        for obj in self.data:
            obj_key = obj[DataKey.key.value];
            if DataKey.contains_image(obj_key):
                uploadImage = "uploadImage.single('image'),"

        lines.append(f"""
            router.get('/detail', isCaching, asyncHandler({self.modelName}Controller.get{self.className}Detail));
            router.get('/all', isCaching, asyncHandler({self.modelName}Controller.getAll{self.className}));

            /// authentication ////
            router.use(authentication);

            router.use(isPermission([UserRole.Admin]));

            router.post(
            '/create',
            {uploadImage}
            asyncHandler({self.modelName}Controller.create{self.className})
            );

            router.patch(
            '/update',
            {uploadImage}
            asyncHandler({self.modelName}Controller.update{self.className})
            );
        """)
        

        lines.append("\nmodule.exports = router")
        # Write the lines to the file
        with open(f"backend/router/{self.fileName}.router.js", "w") as f:
            f.writelines(lines)
