schema_addr = "./js/src/schemas/"

def generateMongooseSchema(schema):
    fp = open(schema_addr+schema["name"]+".js", "w+")

    fp.write('const mongoose = require("mongoose")\n')
    fp.write(schema["name"] + " = new mongoose.Schema(")
    fp.write(schema["data"] + ", " + schema['options'] + ")\n\n")
    fp.write("module.exports = mongoose.model(\""+ schema['model'] +"\"," +  schema['name'] +")")

    fp.close()

schema_data = {
    "name": "testTooSchema",
    "data": """{
    Name: String,
    Age: { 
        type: Number,
        required: true
    }
}""",
    "options": '{collection: "testToo"}',
    "model": "testTooHello"
}

generateMongooseSchema(schema_data)
