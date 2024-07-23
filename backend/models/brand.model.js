'use strict';
const mongoose = require('mongoose');
const { Schema } = mongoose;

const DOCUMENT_NAME = 'Brand';
const COLLECTION_NAME = 'brands';

const brandSchema = new Schema({
    brand_bu: { type: Schema.Types.ObjectId, ref: 'BU', required: true },
    brand_image: { type: Object },
    brand_name: { type: String, required: true, trim: true },
    brand_description: { type: String },
    brand_code: { type: String, required: true, unique: true, trim: true },
    isActive: { type: Boolean, default: True },
    time: { type: Number, default: Date.now },
    creatorBy: { type: Schema.Types.ObjectId, ref: 'User', required: true },
    updatedBy: { type: Schema.Types.ObjectId, ref: 'User' },
}, {collection: COLLECTION_NAME, timestamps: true,});

module.exports = mongoose.model(DOCUMENT_NAME, brandSchema);
