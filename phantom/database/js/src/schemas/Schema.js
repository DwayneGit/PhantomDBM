const mongoose = require("mongoose")
var Schema = new mongoose.Schema({
}, {"collection": ""})

module.exports = mongoose.model("Model",Schema)