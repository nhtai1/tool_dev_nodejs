"use strict";

const { convertToObjectIdMongoDb } = require("../../utils");

class BuFilter {
  constructor(query) {
    this.query = query;
  }

  getFilter = function () {
    const filter = {};

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

module.exports = BuFilter;
