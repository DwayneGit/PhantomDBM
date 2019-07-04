const fs = require("fs")
const path = require('path')

class mongooseDOA {

    constructor(db_uri, collection){
        var host = /(?<=\/)([\w]+)(?<!:)/g.exec(db_uri)[0]
        var port = /(?<=:)([\w]+)(?<!\/)/g.exec(db_uri)[0]
        var database = /\/([\w]+)$/g.exec(db_uri)[1]

        var schemas = {}
        const normalizedPath = path.join(__dirname, "../schemas/" + database + "_" + collection + "/");
        fs.readdirSync(normalizedPath).forEach(function(file) {
            schemas[file.substring(0, file.length-3)] = require( normalizedPath + file);
        });
    }

    insert_data_handler(schema_addr){
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