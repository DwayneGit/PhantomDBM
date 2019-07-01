const fs = require("fs")
const net = require("net")
const path = require('path')

const mongoose_dao = require("./src/dao/mongoose_dao")
const connectToDatabase = require("./src/utility/connectToDatabase")

// console.log(process.argv)
connectToDatabase(process.argv[3]).catch((err)=>{
    console.error(err.name)
    process.exit(4)
})

const socket_addr = path.join(__dirname, "src/tmp/db.sock")

if (!fs.existsSync(socket_addr)) {
    fs.mkdirSync(path.join(__dirname, "src/tmp"))
}

var server = null
var dao = new mongoose_dao()

try{
    if(process.argv[2] == "insert"){
        server = net.createServer(dao.insertDataSocket(process.argv[4]))
    }
    else if(process.argv[2] == "find"){
        server = net.createServer(dao.findDataSocket())
    }
    else{
        throw new Error("Error: Invalid database operation")
    }
}
catch(err){
    console.error(err.message)
    process.exit(7)
}

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
                    console.error('Address in use, retrying...');
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
                console.error("[ERROR] Attempt at connection exceeded timeout value");
                server.close();
            }, timeout);

        } catch (err){
            console.error("Error starting server") 
        }
    }
);  
