const fs = require("fs")
const path = require('path')
const normalizedPath = path.join(__dirname, "../schemas");

var schemas = {}
fs.readdirSync(normalizedPath).forEach(function(file) {
    schemas[file.substring(0, file.length-3)] = require("./../schemas/" + file);
});

class mongooseDOA {

    constructor(){}

    findDataSocket( ){
        return (socket) => {
            console.log("Connection established...")
            socket.on('data', (data) => {
                try {
                    console.log(data.toString('utf8'))
                    if(data.toString('utf8') === "end"){
                        process.exit(1)
                    }
                    
                    var d = JSON.parse(data.toString())
                    var test = new schemas[process.argv[3]](d)
                    
                    test.save().then((err) => {
                        socket.write("Document saved")
                    })
                }
                catch (err) {
                    console.log(err)
                    socket.write("Error: Error sending data")
                    // socket.end()
                }
            })

            socket.on('error', (err) => {
                if (err.code === 'ECONNRESET') {
                    console.log('Collection');
                    setTimeout(() => {
                        socket.end();
                    }, 1000);
                }
                else{
                    console.log(err)
                }
            }) 
        }
    }
}

module.exports = mongooseDOA