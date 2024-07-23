"use strict";

const express = require("express");
const { authentication, isPermission } = require("../../auth/authUtils");
const { isCaching } = require("../../middelware/is_limit");
const buController = require("../../controllers/bu.controller");
const asyncHandler = require("../../helpers/asyncHandler");
const { uploadImage } = require("../../utils/upload/multer.upload");
const { UserRole } = require("../../enum/app.enum");

const router = express.Router();

router.get("/detail", isCaching, asyncHandler(buController.getBuDetail));
router.get("/all", isCaching, asyncHandler(buController.getAllBu));

/// authentication ////
router.use(authentication);

router.use(isPermission([UserRole.Admin]));

router.post(
  "/create",
  uploadImage.single("image"),
  asyncHandler(buController.createBu)
);

router.patch(
  "/update",
  uploadImage.single("image"),
  asyncHandler(buController.updateBu)
);

module.exports = router;
