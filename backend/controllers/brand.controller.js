"use strict";

const {
  SuccessResponse,
  CREATED,
  GETLISTOK,
} = require("../core/success.response");
const BaseController = require("./base/base.controller");
const ErrorMessage = require("../enum/error.message");
const { BadRequestError, NotFoundError } = require("../core/error.response");
const { getInfoData } = require("../utils");
const AppRouterName = require("../routers/router.name");

//helper
const BrandFilter = require("../helpers/filter/brand.filter");
const brandValidator = require("../helpers/validate/brand.validate");
//service
const BrandService = require("../services/brand.service");
const BUService = require("../services/bu.service");

const FILED_RETURN = [
  "_id",
  "brand_bu",
  "brand_image",
  "brand_name",
  "brand_code",
  "isActive",
];

const FILED_RETURN_CREATE = [
  "_id",
  "brand_image",
  "brand_name",
  "brand_code",
  "isActive",
];
const FILED_UNSELECTED = ["__v", "time"];
const KEY_IMAGE = "brand_image";

class BrandController extends BaseController {
  checkBUExist = async function (buId) {
    if (!buId) {
      return;
    }
    return await BUService.checkExists(buId);
  };
  checkExistsBrandByCode = async function (brand_code, id) {
    if (!brand_code) {
      return;
    }
    const foundBrand = await BrandService.findBrandByCode(brand_code);
    if (foundBrand && foundBrand._id.toString() !== id?.toString()) {
      throw new BadRequestError(ErrorMessage.BRAND_CODE_IS_EXISTING);
    }
    return;
  };
  getAllBrand = async (req, res, next) => {
    const options = super.getPageAndItem(req.query);

    const filter = new BrandFilter(req.query).getFilter();

    const { data, pagination } = await BrandService.findAllBrand({
      filter,
      options,
      select: FILED_RETURN,
    });

    await new GETLISTOK({ message: "", data, pagination }).send(req, res, {
      saveCaching: true,
    });
  };

  getBrandDetail = async (req, res, next) => {
    const brandId = req.query.brandId;

    super.checkDataNotNull(brandId, ErrorMessage.BRAND_ID_IS_REQUIRED);

    const result = await BrandService.findDetailById(brandId, FILED_UNSELECTED);

    super.checkDataNotNull(result, ErrorMessage.BRAND_NOT_FOUND);

    await new SuccessResponse({ message: "", data: result }).send(req, res, {
      saveCaching: true,
    });
  };

  createBrand = async (req, res, next) => {
    super.validate(req.body, brandValidator.create);
    const { brand_bu } = req.body;
    await this.checkBUExist(brand_bu);
    const { brand_code } = req.body;
    await this.checkExistsBrandByCode(brand_code, null);

    const data = await super.getImageFile(
      req,
      { ...req.body, creatorBy: req.user.userId },
      KEY_IMAGE
    );

    const result = await BrandService.createBrand(data);

    await new CREATED({
      message: ErrorMessage.BRAND_CREATED,
      data: getInfoData({ object: result, fileds: FILED_RETURN_CREATE }),
    }).send(req, res, {
      deleteCaching: true,
      deleteOptions: [AppRouterName.brand],
    });
  };

  updateBrand = async (req, res, next) => {
    super.validate(req.body, brandValidator.update);
    const brandId = req.query.brandId;
    super.checkDataNotNull(brandId, ErrorMessage.BRAND_ID_IS_REQUIRED);
    const { brand_code } = req.body;
    await this.checkExistsBrandByCode(brand_code, brandId);

    const data = super.updateNestedObjectParse({
      ...req.body,
      updatedBy: req.user.userId,
    });
    const imageData = await super.getImageFile(req, data, KEY_IMAGE);

    const result = await BrandService.updateBrand({ brandId, data: imageData });
    super.checkDataNotNull(result, ErrorMessage.BRAND_NOT_FOUND);

    await new SuccessResponse({
      message: ErrorMessage.BRAND_UPDATED,
      data: getInfoData({ object: result, fileds: FILED_RETURN_CREATE }),
    }).send(req, res, {
      deleteCaching: true,
      deleteOptions: [AppRouterName.brand],
    });
  };
}

module.exports = new BrandController();
