import hashlib
import socket
import random

from public_constants import *


class DiffieHellmanClientSocket:

    def __init__(self, ip_address: str, port: int, verbose: bool = False) -> None:
        self._verbose: bool = verbose
        self.ip_address: str = ip_address
        self.port: int = port
        self.socket: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._verbose_print("Init done")

    def connect(self) -> None:
        self._verbose_print("Trying to connect...")
        self.socket.connect((self.ip_address, self.port))
        self._verbose_print("Connected successfully")

    def close(self) -> None:
        self.socket.close()
        self._verbose_print("Closing socket")

    def _verbose_print(self, message: str) -> None:
        if self._verbose:
            print(f"DHClientSocket({self.ip_address}, {self.port}): {message}")

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


def main():
    d = random.randint(1, sub_group_size - 1)
    print(f"Secret d: {d}")
    q = p1 * d
    s = DiffieHellmanClientSocket(ip, port, verbose)
    s.connect()
    try:
        print(f"Sending q_bob: {q}")
        s.send(q.serialize())
        q_alice_str = s.receive()
        q_alice = PointElement.deserialize(q_alice_str, curve1)
        print(f"Received q_alice: {q_alice}")
        result = d * q_alice
        data = s.receive()
        z = PointElement.deserialize_z(data, curve1)
        s.send(result.serialize_z())
    finally:
        s.close()
    result = result.projection(z)
    print(f"Resulting point: {result}")
    hash_ = hashlib.sha512(str(result).encode()).hexdigest()
    print(f"Resulting hash: {hash_}")


if __name__ == "__main__":
    main()
