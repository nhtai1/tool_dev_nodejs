"use strict";

const express = require("express");
const { authentication, isPermission } = require("../../auth/authUtils");
const { isCaching } = require("../../middelware/is_limit");
const brandController = require("../../controllers/brand.controller");
const asyncHandler = require("../../helpers/asyncHandler");
const { uploadImage } = require("../../utils/upload/multer.upload");
const { UserRole } = require("../../enum/app.enum");

const router = express.Router();

router.get("/detail", isCaching, asyncHandler(brandController.getBrandDetail));
router.get("/all", isCaching, asyncHandler(brandController.getAllBrand));

/// authentication ////
router.use(authentication);

router.use(isPermission([UserRole.Admin]));

router.post(
  "/create",
  uploadImage.single("image"),
  asyncHandler(brandController.createBrand)
);

router.patch(
  "/update",
  uploadImage.single("image"),
  asyncHandler(brandController.updateBrand)
);

module.exports = router;
