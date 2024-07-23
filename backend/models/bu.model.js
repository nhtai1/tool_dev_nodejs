'use strict';
const mongoose = require('mongoose');
const { Schema } = mongoose;

const DOCUMENT_NAME = 'BU';
const COLLECTION_NAME = 'bu';

const buSchema = new Schema({
    bu_image: { type: Object },
    bu_name: { type: String, required: true, unique: true, trim: true },
    bu_description: { type: String },
    bu_code: { type: String, required: true, unique: true, trim: true },
    isActive: { type: Boolean, default: True },
    time: { type: Number, default: Date.now },
    creatorBy: { type: Schema.Types.ObjectId, ref: 'User', required: true },
    updatedBy: { type: Schema.Types.ObjectId, ref: 'User' },
}, {collection: COLLECTION_NAME, timestamps: true,});

module.exports = mongoose.model(DOCUMENT_NAME, buSchema);
