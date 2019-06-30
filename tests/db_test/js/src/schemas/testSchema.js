const mongoose = require("mongoose")

testSchema = new mongoose.Schema({
    Name: String,
    Age: { 
        type: Number,
        required: true
    }
}, {collection: "test"})

module.exports = mongoose.model("test", testSchema)