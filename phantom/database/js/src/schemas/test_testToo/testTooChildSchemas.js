const mongoose = require("mongoose")
const testTooModel = require("./testTooSchema")
module.exports.Owner = new testTooModel.discriminator('Owner',
	new mongoose.Schema({
			    Job : String
            }, ))

module.exports.Janitor = new testTooModel.discriminator('Janitor',
	new mongoose.Schema({
			    Family_count : Number
            }, ))

