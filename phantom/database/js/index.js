const fs = require("fs")
const net = require("net")
const path = require('path')

const connectToDatabase = require("./src/connectToDatabase")

var normalizedPath = path.join(__dirname, "src/schemas");

var schemas = {}
fs.readdirSync(normalizedPath).forEach(function(file) {
    schemas[file.substring(0, file.length-3)] = require("./src/schemas/" + file);
});

console.log(process.argv[2])
connectToDatabase(process.argv[2]).catch((err)=>{
    console.log(err.name)
    process.exit(4)
})

socket_addr = path.join(__dirname, "src/tmp/db.sock")

var handler = (socket) => {
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

var server = net.createServer(handler)

fs.unlink( 
    socket_addr, 
    () => {

        var timer;
        var timeout = 15000;
        try {
            server.listen(socket_addr)

            server.on('connection', (socket) => {
                clearTimeout(timer);
                console.log('Client connected.');
                socket.write('__boop');
            })

            server.on('error', (err) => {
                clearTimeout(timer);
                if (err.code === 'EADDRINUSE') {
                    console.log('Address in use, retrying...');
                    setTimeout(() => {
                        server.close();
                        server.listen(socket_addr);
                    }, 1000);
                }
            }) 

            server.on('close', () => {
                console.log("Closing connection")
                process.exit(20)
            })

            timer = setTimeout(() => {
                console.log("[ERROR] Attempt at connection exceeded timeout value");
                server.close();
            }, timeout);

        } catch (err){
            console.log("Error starting server") 
        }
    }
);