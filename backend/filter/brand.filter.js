"use strict";

const { convertToObjectIdMongoDb } = require("../../utils");

class BrandFilter {
  constructor(query) {
    this.query = query;
  }

  getFilter = function () {
    const filter = {};

    const brand_bu = this.query.brand_bu;
    if (brand_bu) {
      filter.brand_bu = convertToObjectIdMongoDb(brand_bu);
    }
    const isActive = this.query.isActive;
    if (isActive) {
      filter.isActive = isActive;
    }
    const creatorBy = this.query.creatorBy;
    if (creatorBy) {
      filter.creatorBy = convertToObjectIdMongoDb(creatorBy);
    }
    const updatedBy = this.query.updatedBy;
    if (updatedBy) {
      filter.updatedBy = convertToObjectIdMongoDb(updatedBy);
    }
    return filter;
  };
}

module.exports = BrandFilter;
