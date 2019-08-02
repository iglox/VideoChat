import socket, logging, os, cv2, pickle, struct
import numpy as np

"""
    import warnings
    warnings.filterwarnings("ignore")
"""

class Server:
    def __init__(self, address="localhost", port=5000, servername="VideoChat", pool_lower_port=5001, pool_upper_port=65535, queue_length=5):
        self.address = address
        self.port = port
        self.servername = servername
        self.queue_length = queue_length
        self.pool = list(range(pool_lower_port, pool_upper_port))
        
        if self.address in self.pool:
            self.pool.remove(self.address)
        """
        if os.path.exists('./log/server.log'):
            os.rename("./log/server.log", "./log/server.log.bak")

        open("./log/server.log","w").close()
        logging.basicConfig(filename='server.log', level=logging.DEBUG)
        logging.debug('This message should go to the log file')
        logging.info('So should this')
        logging.warning('And this, too')
        """

    def __recv_data(self, sckt):
        data = b''
        while len(data) < struct.calcsize("L"):
            data += sckt.recv(4096)
        packed_msg_size = data[:struct.calcsize("L")]

        data = data[struct.calcsize("L"):]
        msg_size = struct.unpack("L", packed_msg_size)[0]

        while len(data) < msg_size:
            data += sckt.recv(4096)
        frame_data = data[:msg_size]
        data = data[msg_size:]

        frame = pickle.loads(frame_data)
        return frame

    def start(self) -> None:
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print("[*] Created socket")
            self.server_socket.bind((self.address, self.port))
            print("[*] Set up socket")
            self.server_socket.listen(self.queue_length)
            print("[*] Start listening with %d queue length" % self.queue_length)

            while True:
                conn, addr = self.server_socket.accept()
                print("[+] New connection from %s:%s\n[!] Greeting the new client" % (addr[0], addr[1]))
                conn.send(("Hello from %s" % self.servername).encode())
                username = conn.recv(2056).decode()
                print("[!] %s:%s's username is: %s" % (addr[0], addr[1], username))
                conn.send(b"OK")

                frame = self.__recv_data(conn)
                conn.send(b"ACK")
                while frame != "STOP":
                    try:
                        cv2.imshow('frame', frame)
                        if cv2.waitKey(1) == 27:
                            break
                    except Exception as e:
                        print("[e] error", e)

                    frame = self.__recv_data(conn)
                    conn.send(b"ACK")

                cv2.destroyAllWindows()
                print("[!] Closing the socket with %s:%s" % (addr[0], addr[1]))
                conn.sendall(b"STOP")
                conn.close()
                print("[-] Successfully closed the socket with %s:%s" % (addr[0], addr[1]))

        except (OSError, KeyboardInterrupt) as e:
            if e == OSError:
                print("[e] Error on creation..\n\t%s" % str(e))
            else:  # if e == KeyboardInterrupt:
                print(e)
                print("\n[x]Shutting down the server...")
            self.server_socket.close()
        except (AttributeError) as e:
            print("[x]", e)
            self.server_socket.close()


def main():
    server = Server(servername="Server_xyz")
    server.start()


if __name__ == '__main__':
    main()
