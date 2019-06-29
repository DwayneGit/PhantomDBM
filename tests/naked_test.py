import sys, os, signal, socket
import time
from Naked.toolshed.shell import execute_js, muterun_js

newpid = os.fork()
s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

script = [
    '{"Name":"Dedotated Wam", "Age":7}',
    '{"Name":"Shame Wow", "Age":8}',
    '{"Name":"Something Clever", "Age":9}'
]

try:
    if newpid == 0:
        response = execute_js('./js/index.js', arguments="./src/connectToDatabase")

        # if response.exitcode == 0:
        #     print(response.stdout)
        # else:
        #     sys.stderr.write(response.stderr)

    else:
        server_addr = ("./js/src/tmp/db.sock")

        print('Connecting to %s' % server_addr)

        time.sleep(3)

        try:
            s.connect(server_addr)
        except socket.error as err:
            print(str(err))
            os.kill(0, signal.SIGTERM)
            os.kill(newpid, signal.SIGTERM)
            sys.exit(1)

        # time.sleep(5)
        # message = 'おはようございます'

        # s.sendall(bytes(message, encoding='utf-8'))

        try:
            for doc in script:
                s.sendall(bytes(doc, encoding='utf-8'))
                data = s.recv(1024)
                print('Received "%s"' % data.decode("utf-8"))
                if data.decode("utf-8") == "done":
                    break
                time.sleep(1)

        finally:
            print('Closing socket')
            s.sendall(bytes("end", encoding='utf-8'))
            time.sleep(3)

            s.close()
            os.kill(0, signal.SIGTERM)
            sys.exit(1)

except KeyboardInterrupt:
    os.kill(newpid, signal.SIGTERM)
    s.close()
    sys.exit('exited')
