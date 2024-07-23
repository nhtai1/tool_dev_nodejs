"use strict";

const Joi = require("joi");

class BuValidator {
  create(body) {
    const scheme = Joi.object({
      bu_name: Joi.string().required(),
      bu_description: Joi.string(),
      bu_code: Joi.string().required(),
    });

    return scheme.validate(body);
  }

  update(body) {
    const scheme = Joi.object({
      bu_name: Joi.string(),
      bu_description: Joi.string(),
      bu_code: Joi.string(),
    });

    return scheme.validate(body);
  }
}

module.exports = new BuValidator();
