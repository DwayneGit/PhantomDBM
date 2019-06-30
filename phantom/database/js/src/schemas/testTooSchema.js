const mongoose = require("mongoose")
testTooSchema = new mongoose.Schema({
    Name: String,
    Age: { 
        type: Number,
        required: true
    }
}, {collection: "testToo"})

module.exports = mongoose.model("testTooHello",testTooSchema)