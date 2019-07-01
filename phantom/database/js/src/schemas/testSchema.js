const mongoose = require("mongoose")
var testSchema = new mongoose.Schema({
    "Name": String,
	"Age": Number,
	"Relationship_Status": String
}, {"collection": "test"})

module.exports = mongoose.model("testModel",testSchema)