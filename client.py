import socket, cv2, pickle
import numpy as np


class Client:
    def __init__(self, host: str, port: int, username=None):
        self.host = host
        self.port = port
        self.username = input("Username :>>> ") if not username else username
        self.cap = cv2.VideoCapture(0)

    def start(self) -> None:
        print("[+] Creating socket...")
        self.sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[+] Connecting to the server...")
        self.sckt.connect((self.host, self.port))
        print("[?] Server said: \"%s\"" % self.sckt.recv(1024).decode())
        try:
            while True:
                frame = self.cap.read()[1]
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                self.sckt.send(pickle.dumps(gray))
                self.sckt.recv(1024)
        except Exception as e:
            print(e)
            self.sckt.send(b"STOP")
        self.sckt.close()
        print("[-] Closing connection...")
        


def main():
    client = Client("127.0.0.1", 5000)
    client.start()


if __name__ == '__main__':
    main()
