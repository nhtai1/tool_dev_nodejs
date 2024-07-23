"use strict";

const Joi = require("joi");

class BrandValidator {
  create(body) {
    const scheme = Joi.object({
      brand_bu: Joi.string().required(),
      brand_image: Joi.object(),
      brand_name: Joi.string().required(),
      brand_description: Joi.string(),
      brand_code: Joi.string().required(),
    });

    return scheme.validate(body);
  }

  update(body) {
    const scheme = Joi.object({
      brand_image: Joi.object(),
      brand_name: Joi.string(),
      brand_description: Joi.string(),
      brand_code: Joi.string(),
      isActive: Joi.boolean(),
    });

    return scheme.validate(body);
  }
}

module.exports = new BrandValidator();
