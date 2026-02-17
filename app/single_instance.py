from PyQt5.QtNetwork import QLocalServer, QLocalSocket


class SingleInstance:
    def __init__(self, key: str):
        self.key = key
        self.server = QLocalServer()

        # Remove stale lock (in case of crash)
        QLocalServer.removeServer(self.key)

        if not self.server.listen(self.key):
            raise RuntimeError("Another instance is already running")

    @staticmethod
    def is_running(key: str) -> bool:
        socket = QLocalSocket()
        socket.connectToServer(key)
        return socket.waitForConnected(100)
