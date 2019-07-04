const fs = require("fs")
const path = require('path')
const normalizedPath = path.join(__dirname, "../schemas/");

var schemas = {}
fs.readdirSync(normalizedPath).forEach(function(file) {
    schemas[file.substring(0, file.length-3)] = require(normalizedPath + file);
});

module.exports = (schema_addr) => {
    return (socket) => {
        console.log("Connection established...")
        socket.on('data', (data) => {
            try {
                console.debug(data.toString('utf8'))
                if(data.toString('utf8') === "end"){
                    process.exit(1)
                }
                
                var d = JSON.parse(data.toString())
                var test = new schemas[schema_addr](d)
                
                test.save().then((err) => {
                    socket.write("Document saved")
                })
            }
            catch (err) {
                console.error(err)
                socket.write("err")
                // socket.end()
            }
        })

        socket.on('error', (err) => {
            if (err.code === 'ECONNRESET') {
                console.error('Collection');
                setTimeout(() => {
                    socket.end();
                }, 1000);
            }
            else{
                console.error(err)
            }
        })
    }
}