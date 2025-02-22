import socket
import sys
import os
import time
import signal
import subprocess

class Wrapper:
    TERMINATION_REQ = "Terminate with CTRL-C"

    def _create_connection(self, port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('localhost', port))
        s.listen(1)
        print(f"Listening for termination request on port {port}...")  # Debugging
        conn, addr = s.accept()
        return conn

    def _wait_on_ctrl_c_request(self, conn):
        while True:
            data = conn.recv(1024).decode()
            if data == self.TERMINATION_REQ:
                return True
        return False

    def _cleanup_and_fire_ctrl_c(self, conn):
        conn.close()
        print("CTRL+C received, stopping recording...")
        os.kill(os.getpid(), signal.SIGINT)  # Send SIGINT to the current process

    def _signal_handler(self, signal, frame):
        time.sleep(1)
        sys.exit(0)

    def __init__(self, cmd, port):
        print(f"Starting Wrapper for command: {cmd} on port {port}")  # Debugging
        signal.signal(signal.SIGINT, self._signal_handler)

        # Start FFmpeg process
        self.process = subprocess.Popen(cmd, shell=True)

        conn = self._create_connection(port)
        if self._wait_on_ctrl_c_request(conn):
            self._cleanup_and_fire_ctrl_c(conn)
        else:
            sys.exit(0)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python winctrlc.py <command> <port>")
        sys.exit(1)

    command_string = sys.argv[1]
    port_no = int(sys.argv[2])

    Wrapper(command_string, port_no)
