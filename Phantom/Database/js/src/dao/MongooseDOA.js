const fs = require("fs")
const path = require('path')

class MongooseDOA {

    constructor(db_uri, collection){
        var host = /(?<=\/)([\w]+)(?<!:)/g.exec(db_uri)[0]
        var port = /(?<=:)([\w]+)(?<!\/)/g.exec(db_uri)[0]
        var database = /\/([\w]+)$/g.exec(db_uri)[1]

        var s = {}
        const normalizedPath = path.join(__dirname, "../schemas/" + database + "_" + collection + "/");
        fs.readdirSync(normalizedPath).forEach(function(file) {
            s[file.substring(0, file.length-3)] = require( normalizedPath + file);
        });

        this.schemas = s
        this.model = null
        this.setModelFlag = false
    }

    insert_data_handler(){
        return (socket) => {
            console.log("Connection established...")
            socket.on('data', (data) => {
                try {
                    // console.debug(data.toString('utf8'))
                    if(data.toString('utf8') === "end"){
                        process.exit(1)
                    }
                    if(this.setModelFlag){
                        this.model=data.toString('utf8')
                        this.setModelFlag=false
                        socket.write(data.toString('utf8'))
                        return
                    }
                    else if(data.toString('utf8') === "set_model"){
                        this.setModelFlag=true
                        socket.write("send_model")
                        return
                    }

                    var d = JSON.parse(data.toString())
                    var test = new this.schemas[this.model](d)
                    
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

module.exports = MongooseDOA