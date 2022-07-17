import socket 
import selectors
import logging 

class MessageHandler:
    def __init__(self, selector, socket, addr, db):
        self.bufsize = 4096
        self.selector = selector 
        self.sock = socket 
        self.addr = addr 
        self.db = db
        self._recv_buffer = b""
        self._send_buffer = b""
        self.header = None 
        self.request = None
        self.response_created = False        

    def process_events(self, mask):
        if mask & selectors.EVENT_READ:
            self.read()
        if mask & selectors.EVENT_WRITE:
            self.write()

    def handle_request(self):
        pass

    def read(self):
        self._read_to_buffer()

        # extract header length 
        # extract header 
        # extract content if applicable   
        # handle request      

    def write(self):
        pass 

    def close(self):
        logging.info(f"Closing connection to {self.addr}")
        try:
            self.selector.unregister(self.sock)
        except Exception as e:
            logging.error(
                f"Error: selector.unregister() exception for "
                f"{self.addr}: {e!r}"
            )

        try:
            self.sock.close()
        except OSError as e:
            logging.error(f"Error: socket.close() excption for {self.addr}: {e!r}")
        finally:
            # Delete reference to socket object for garbage collection
            self.sock = None 


    def _read_to_buffer(self):
        try:
            data = self.sock.recv(self.bufsize)
        except BlockingIOError:
            # Resource temporarily unavaliable (errno EWOULDBLOCK)
            pass 
        else:
            if data:
                self._recv_buffer += data 
            else:
                raise RuntimeError("Peer closed") 
    
    def _send_buffer(self):
        pass
