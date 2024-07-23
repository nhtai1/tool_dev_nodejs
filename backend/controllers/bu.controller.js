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
const BuFilter = require("../helpers/filter/bu.filter");
const buValidator = require("../helpers/validate/bu.validate");
//service
const BuService = require("../services/bu.service");

const FILED_RETURN = ["_id", "bu_image", "bu_name", "bu_code", "isActive"];

const FILED_RETURN_CREATE = [
  "_id",
  "bu_image",
  "bu_name",
  "bu_code",
  "isActive",
];
const FILED_UNSELECTED = ["__v", "time"];
const KEY_IMAGE = "bu_image";

class BuController extends BaseController {
  checkExistsBuByCode = async function (bu_code, id) {
    if (!bu_code) {
      return;
    }
    const foundBu = await BuService.findBuByCode(bu_code);
    if (foundBu && foundBu._id.toString() !== id?.toString()) {
      throw new BadRequestError(ErrorMessage.BU_CODE_IS_EXISTING);
    }
    return;
  };
  getAllBu = async (req, res, next) => {
    const options = super.getPageAndItem(req.query);

    const filter = new BuFilter(req.query).getFilter();

    const { data, pagination } = await BuService.findAllBu({
      filter,
      options,
      select: FILED_RETURN,
    });

    await new GETLISTOK({ message: "", data, pagination }).send(req, res, {
      saveCaching: true,
    });
  };

  getBuDetail = async (req, res, next) => {
    const buId = req.query.buId;

    super.checkDataNotNull(buId, ErrorMessage.BU_ID_IS_REQUIRED);

    const result = await BuService.findDetailById(buId, FILED_UNSELECTED);

    super.checkDataNotNull(result, ErrorMessage.BU_NOT_FOUND);

    await new SuccessResponse({ message: "", data: result }).send(req, res, {
      saveCaching: true,
    });
  };

  createBu = async (req, res, next) => {
    super.validate(req.body, buValidator.create);
    const { bu_code } = req.body;
    await this.checkExistsBuByCode(bu_code, null);

    const data = await super.getImageFile(
      req,
      { ...req.body, creatorBy: req.user.userId },
      KEY_IMAGE
    );

    const result = await BuService.createBu(data);

    await new CREATED({
      message: ErrorMessage.BU_CREATED,
      data: getInfoData({ object: result, fileds: FILED_RETURN_CREATE }),
    }).send(req, res, {
      deleteCaching: true,
      deleteOptions: [AppRouterName.bu],
    });
  };

  updateBu = async (req, res, next) => {
    super.validate(req.body, buValidator.update);
    const buId = req.query.buId;
    super.checkDataNotNull(buId, ErrorMessage.BU_ID_IS_REQUIRED);
    const { bu_code } = req.body;
    await this.checkExistsBuByCode(bu_code, buId);

    const data = super.updateNestedObjectParse({
      ...req.body,
      updatedBy: req.user.userId,
    });
    const imageData = await super.getImageFile(req, data, KEY_IMAGE);

    const result = await BuService.updateBu({ buId, data: imageData });
    super.checkDataNotNull(result, ErrorMessage.BU_NOT_FOUND);

    await new SuccessResponse({
      message: ErrorMessage.BU_UPDATED,
      data: getInfoData({ object: result, fileds: FILED_RETURN_CREATE }),
    }).send(req, res, {
      deleteCaching: true,
      deleteOptions: [AppRouterName.bu],
    });
  };
}

module.exports = new BuController();
