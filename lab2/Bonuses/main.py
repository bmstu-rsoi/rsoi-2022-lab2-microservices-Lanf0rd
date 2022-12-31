from flask import request
import flask
from database import Data_Base



class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.app = flask.Flask(__name__)

        self.app.add_url_rule("/manage/health", view_func = self.get_say_ok)
        self.app.add_url_rule("/api/v1/privilege", view_func = self.get_privilege)

        
    def run_server(self):
        return self.app.run(host = self.host, port = self.port)
    def get_say_ok(self):
        return "OK"
        
    def get_privilege(self):
        client = request.headers.get("X-User-Name")
        new_db = Data_Base()
        privilege = new_db.get_privilege(client)
        return privilege











if __name__ == "__main__":

    server_host = "0.0.0.0"
    server_port = 8050

    server = Server(server_host, server_port)
    server.run_server()
