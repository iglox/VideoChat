import socket

class Server:
    def __init__(self, address="localhost", port=5000, servername="VideoChat", pool_lower_port=5001, pool_upper_port=65535, queue_length=5):
        self.address = address
        self.port = port
        self.servername = servername
        self.queue_length = queue_length
        self.pool = list(range(pool_lower_port, pool_upper_port))

        if self.address in self.pool:
            self.pool.remove(self.address)


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
                conn.send(("Hello from %s" % self.servername).encode())
                conn.close()

        except (OSError, KeyboardInterrupt) as e:
            if e == OSError:
                print("Error on creation..\n\t%s" % str(e))
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
