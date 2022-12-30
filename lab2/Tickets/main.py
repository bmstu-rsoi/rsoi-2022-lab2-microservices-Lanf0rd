from flask import request
import flask
from database import Data_Base



class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.app = flask.Flask(__name__)

        self.app.add_url_rule("/api/v1/tickets", view_func = self.get_tickets)

    def run_server(self):
        return self.app.run(host = self.host, port = self.port)
        
    def get_tickets(self):
        client = request.headers.get("X-User-Name")
        new_db = Data_Base()
        tickets = new_db.get_tickets(client)
        return tickets













if __name__ == "__main__":

    server_host = "0.0.0.0"
    server_port = 8070

    server = Server(server_host, server_port)
    server.run_server()
