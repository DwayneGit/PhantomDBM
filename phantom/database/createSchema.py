import os
def generate_mongoose_schema(name, 
                             schema, 
                             options="{}", 
                             schema_addr="./phantom/database/js/src/schemas/"):
    # print(os.getcwd())
    fp = open(schema_addr+ name +"Schema.js", "w+")
    fp.write('const mongoose = require("mongoose")\n')
    fp.write("var " + name + "Schema = new mongoose.Schema(")
    fp.write(schema + ", " + options + ")\n\n")
    fp.write("module.exports = mongoose.model(\""+ name + 'Model' +"\"," + name + "Schema" +")")

    fp.close()
