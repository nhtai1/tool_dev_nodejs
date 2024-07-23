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
const buModel = require("../models/bu.model");

class BuService {
  static findBuByCode = async function (bu_code) {
    const foundBu = await buModel.findOne({ bu_code: bu_code }).lean();
    return foundBu;
  };

  static findBuByIdLean = async function (buId) {
    const foundBu = await buModel.findById(buId).lean();
    return foundBu;
  };

  static checkExistsBu = async function (buId) {
    const foundBu = await BuService.findBuByIdLean(buId);
    if (!foundBu) {
      throw new BadRequestError(`${ErrorMessage.BU_NOT_FOUND}:${buId}`);
    }
    return foundBu;
  };

  static createBu = async function (data) {
    const bu = await buModel.create(data);
    return bu;
  };

  static findDetailById = async function (buId, unSelected = ["__v"]) {
    const bu = await buModel
      .findById(buId)
      .populate({ path: "creatorBy", select: AppSeleted.user })
      .populate({ path: "updatedBy", select: AppSeleted.user })
      .select(unGetSelectData(unSelected))
      .lean();

    return bu;
  };

  static updateBu = async function ({ buId, data }) {
    const bu = await buModel
      .findOneAndUpdate(
        { _id: convertToObjectIdMongoDb(buId) },
        { $set: data },
        { new: true }
      )
      .lean();
    return bu;
  };

  static countDocumentsBu = async function (filter) {
    return await buModel.countDocuments(filter);
  };

  static findAllBu = async function ({
    options,
    sort,
    filter = {},
    select = [],
  }) {
    const sortBy = { bu_name: 1 };
    return await findAllDocumentSelect({
      filter,
      options,
      sortBy,
      select,
      model: buModel,
      populateList: [],
    });
  };
}

module.exports = BuService;
