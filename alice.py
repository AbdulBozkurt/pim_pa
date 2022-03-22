import socket
from public_constants import *
import random
import hashlib


class DiffieHellmanServerSocket:

    def __init__(self, ip_address: str, port: int, verbose: bool = False, conn_socket: socket.socket = None) -> None:
        self._verbose: bool = verbose
        self.ip_address: str = ip_address
        self.port: int = port
        if conn_socket is None:
            self.socket: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.is_connection_socket: bool = False
        else:
            self.socket: socket.socket = conn_socket
            self.is_connection_socket: bool = True
        self._verbose_print("Init done")

    def bind(self) -> None:
        self._verbose_print("Trying to bind...")
        self.socket.bind((self.ip_address, self.port))
        self._verbose_print("Bind successful")

    def listen(self, backlog: int):
        self._verbose_print(f"Listening with backlog {backlog}")
        self.socket.listen(backlog)

    def close(self) -> None:
        self.socket.close()
        self._verbose_print("Closing socket")

    def _verbose_print(self, message: str) -> None:
        if self._verbose:
            print(f"{('  ' if self.is_connection_socket else '')}DHServerSocket({self.ip_address}, {self.port}): "
                  f"{message}")

    def send(self, message: str) -> None:
        self._verbose_print(f"Trying to send message: \"{message}\"")
        self.socket.send(message.encode())
        self._verbose_print("Sending done")

    def receive(self, size: int = 1024) -> str:
        raw_response: bytes = self.socket.recv(size)
        self._verbose_print(f"Received {len(raw_response)} bytes")
        decoded: str = raw_response.decode()
        self._verbose_print(f"Received decoded message: \"{decoded}\"")
        return decoded

    def accept(self):
        conn, address = self.socket.accept()
        self._verbose_print(f"Accepted connection with address: {address}")
        connection_socket = DiffieHellmanServerSocket(address[0], address[1], self._verbose, conn)
        return connection_socket, address


def main():
    sock = DiffieHellmanServerSocket(ip, port, verbose)
    sock.bind()
    sock.listen(1)
    try:
        while 1:
            d = random.randint(1, sub_group_size - 1)
            print(f"Secret d: {d}\nAwaiting connection...")
            conn, address = sock.accept()
            data = conn.receive()
            q_bob = PointElement.deserialize(data, curve1)
            print(f"Received q_bob: {q_bob}")
            q = p1 * d
            print(f"Sending q_alice: {q}")
            conn.send(q.serialize())
            conn.close()
            result = d * q_bob
            print(f"Resulting point: {result}")
            hash_ = hashlib.sha512(str(result).encode()).hexdigest()
            print(f"Resulting hash: {hash_}\n")
    finally:
        sock.close()


if __name__ == '__main__':
    main()
