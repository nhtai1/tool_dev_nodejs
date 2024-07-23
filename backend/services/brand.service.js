"use strict";

const { AppStatus } = require("../enum/app.enum");
const AppSeleted = require("../enum/app_selected.enum");
const {
  getSelectData,
  formatPaginatonPayload,
  unGetSelectData,
} = require("../utils");
const { convertToObjectIdMongoDb } = require("../utils");
const ErrorMessage = require("../enum/error.message");
const { BadRequestError } = require("../core/error.response");

const {
  findAllDocumentSelect,
} = require("../models/repositories/general.repo");
const brandModel = require("../models/brand.model");

class BrandService {
  static findBrandByCode = async function (brand_code) {
    const foundBrand = await brandModel
      .findOne({ brand_code: brand_code })
      .lean();
    return foundBrand;
  };

  static findBrandByIdLean = async function (brandId) {
    const foundBrand = await brandModel.findById(brandId).lean();
    return foundBrand;
  };

  static checkExistsBrand = async function (brandId) {
    const foundBrand = await BrandService.findBrandByIdLean(brandId);
    if (!foundBrand) {
      throw new BadRequestError(`${ErrorMessage.BRAND_NOT_FOUND}:${brandId}`);
    }
    return foundBrand;
  };

  static createBrand = async function (data) {
    const brand = await brandModel.create(data);
    return brand;
  };

  static findDetailById = async function (brandId, unSelected = ["__v"]) {
    const brand = await brandModel
      .findById(brandId)
      .populate({ path: "brand_bu", select: AppSeleted.bu })
      .populate({ path: "creatorBy", select: AppSeleted.user })
      .populate({ path: "updatedBy", select: AppSeleted.user })
      .select(unGetSelectData(unSelected))
      .lean();

    return brand;
  };

  static updateBrand = async function ({ brandId, data }) {
    const brand = await brandModel
      .findOneAndUpdate(
        { _id: convertToObjectIdMongoDb(brandId) },
        { $set: data },
        { new: true }
      )
      .lean();
    return brand;
  };

  static countDocumentsBrand = async function (filter) {
    return await brandModel.countDocuments(filter);
  };

  static findAllBrand = async function ({
    options,
    sort,
    filter = {},
    select = [],
  }) {
    const sortBy = { brand_name: 1 };
    return await findAllDocumentSelect({
      filter,
      options,
      sortBy,
      select,
      model: brandModel,
      populateList: [{ path: "brand_bu", select: AppSeleted.bu }],
    });
  };
}

module.exports = BrandService;
