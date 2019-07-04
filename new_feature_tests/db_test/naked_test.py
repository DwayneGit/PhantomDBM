import sys, os, signal, socket
import time
from Naked.toolshed.shell import execute_js, muterun_js

newpid = os.fork()
s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

script = [
    '{"Name":"Shame Wow", "Age":8}',
    '{"Name":"Dedotated Wam", "Age":7}',
    '{"Name":"Something Clever", "Age":9}'
]

try:
    if newpid == 0:
        execute_js('./js/index.js',
                   arguments='mongodb://localhost:27017/test ' + 'testTooSchema')

        # if response.exitcode == 0:
        #     print(response.stdout)
        # else:
        #     sys.stderr.write(response.stderr)

    else:
        server_addr = "./js/src/tmp/db.sock"

        print('Connecting to %s' % server_addr)

        time.sleep(3)

        try:
            s.connect(server_addr)

        except socket.error as err:
            print(str(err))
            sys.exit(1)

        try:
            for doc in script:
                s.sendall(bytes(doc, encoding='utf-8'))
                data = s.recv(1024)
                print('Received "%s"' % data.decode("utf-8"))

                time.sleep(1)

        finally:
            print('Closing socket')
            s.sendall(bytes("end", encoding='utf-8'))

            s.shutdown(1)
            s.close()
            os.waitpid(newpid, 0)
            sys.exit(1)

except KeyboardInterrupt:
    os.kill(newpid, signal.SIGTERM)
    s.close()
    sys.exit('exited')
