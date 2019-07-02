const mongoose = require("mongoose")
var testTooSchema = new mongoose.Schema({
			Name : String,
			Age : Number
		}, {
			collection: "testToo"
		})

module.exports = mongoose.model("testTooModel",testTooSchema)