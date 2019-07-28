import socket, cv2, pickle, sys, struct
import numpy as np


class Client:
    def __init__(self, host: str, port: int, username=None):
        self.host = host
        self.port = port
        self.username = input("Username :>>> ").strip() if not username else username

        while self.username == "" or not len(self.username) < 20:
            print("[I] len(Username) < 20 and Username.strip()!=\"\"")
            self.username = input("Username :>>> ").strip()

        self.cap = cv2.VideoCapture(0)

    def start(self) -> None:
        print("[+] Creating socket...")
        self.sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[+] Connecting to the server...")
        self.sckt.connect((self.host, self.port))
        print("[!] Server said: \"%s\"" % self.sckt.recv(1024).decode())
        print("[!] Sending username...")
        self.sckt.sendall(self.username.encode())
        print("[!] Server said: \"%s\"" % self.sckt.recv(1024).decode())
        try:
            while True:
                _, frame = self.cap.read()
                data = pickle.dumps(frame)
                self.sckt.sendall(struct.pack("L", len(data)) + data)
                if self.sckt.recv(1024).decode() == "STOP":
                    break
        except Exception as e:
            print(e)
            self.sckt.send(b"STOP")
        print("[!] Closing connection")
        self.sckt.close()
        print("[-] Connection closed")
        


def main():
    client = Client("127.0.0.1", 5000)
    client.start()


if __name__ == '__main__':
    main()
