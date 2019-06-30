const mongoose = require("mongoose")
var testSchema = new mongoose.Schema({
	Name: String,
	Age: {
		type: Number,
		required: true
	}
}, {"collection": "test"})

module.exports = mongoose.model("testModel",testSchema)