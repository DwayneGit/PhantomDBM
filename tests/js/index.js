var connectToDatabase = require(process.argv[2])

const fs = require("fs")
const net = require("net")
const path = require('path')
const utf8 = require('utf8')
const testModel = require("./src/schemas/testSchema")

connectToDatabase('mongodb://localhost:27017/test')

const socket_path = "src/tmp/db.sock"

socket_addr = path.join(__dirname, socket_path)

var handler = (socket) => {

        socket.on('data', (data) => {
            try {
                console.log(data.toString('utf8'))
                if(data.toString() == "end"){
                    console.log("Connection ended")
                    socket.end()
                    return
                }
                
                var d = JSON.parse(data.toString())
                var test = new testModel(d)
                
                test.save().then((err) => {
                    socket.write("Document saved")
                })
            }
            catch (err) {
                // console.log(err)
                socket.write("Error: Error sending data")
                // socket.end()
            }
        })

        socket.on('end', () => { 
        })
}

fs.unlink( 
    socket_addr, 
    () => {
        var server = net.createServer(handler).listen(socket_addr)

        server.on('connection', (socket) => {
            console.log('Client connected.');
            console.log('Sending boop.');
            socket.write('__boop');
        })

        server.on('error', (err) => {
            if (err.code === 'EADDRINUSE') {
                console.log('Address in use, retrying...');
                setTimeout(() => {
                server.close();
                server.listen(socket_addr);
                }, 1000);
            }
        }) 

        server.on('close', () => {
            console.log("Mongo exited")
            return process.exit(22);
        })
    }
);