import socket 
import selectors 
import logging 

import message_handler import MessageHandler 
from key_value_store import KeyValueStore

class Server:
    def __init__(self, host='127.0.0.1', port=6789):
        self.selector = selectors.DefaultSelector()
        self.host = host
        self.port = port
        self.listen_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.db = KeyValueStore()

    def start(self):
        self.listen_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.listen_sock.bind((self.host, self.port))
        self.listen_sock.listen(100)
        self.listen_sock.setblocking(False)
        self.selector.register(self.listen_sock, selectors.EVENT_READ, data=None)

        logging.info(f"Listening on {(self.host, self.port)}")

        try:
            while True:
                events = self.selector.select()
                for key, mask in events:
                    if key.data is None:
                        self._accept_connection(key.fileobj)
                    else:
                        handler = key.data 
                        try:
                            handler.process_events(mask)
                        except Exception:
                            logging.error(
                                f"Main: Error: Exception for {handler.addr}:\n"
                                f"{traceback.format_exc()}"
                            )
                            handler.close()
        except KeyboardInterrupt:
            logging.error("Caught keyboard interrupt, exiting")
        finally:
            self.shut_down()

    def shut_down(self):
        self.selector.close()

    def _accept_connection(self, sock):
        conn, addr = sock.accept()
        logging.info(f"Accepted connection from {addr}")
        conn.setblocking(False)
        handler = MessageHandler(self.selector, conn, addr, self.db)
        self.selector.register(conn, selectors.EVENT_READ, data=handler)
