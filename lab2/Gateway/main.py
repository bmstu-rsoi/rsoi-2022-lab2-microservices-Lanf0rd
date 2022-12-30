import flask
from flask import request, Response
import requests


class Server:
    def __init__(self, host, port, tickets_port, flights_port, bonuses_port):
        self.host = host
        self.port = port
        self.Tickets = tickets_port
        self.Flights = flights_port
        self.Bonuses = bonuses_port
        self.app = flask.Flask(__name__)

        self.app.add_url_rule("/api/v1/flights", view_func = self.get_flights)
        self.app.add_url_rule("/api/v1/tickets", view_func = self.get_tickets)
        self.app.add_url_rule("/api/v1/tickets", view_func = self.post_tickets, methods = ["POST"])
        self.app.add_url_rule("/api/v1/tickets/<ticketUid>", view_func = self.get_tickets_by_id)
        self.app.add_url_rule("/api/v1/tickets/<ticketUid>", view_func = self.delete_tickets_by_id, methods = ["DELETE"])
        self.app.add_url_rule("/api/v1/me", view_func = self.get_me)
        self.app.add_url_rule("/api/v1/privilege", view_func = self.get_privelege)

    def run_server(self):
        return self.app.run(host = self.host, port = self.port)
    
    def get_flights(self):
        param_page = request.args.get("page", default = 0, type = int)
        param_size = request.args.get("size", default = 0, type = int)
        url = "http://flight:" + str(self.Flights) + "/api/v1/flights"
        response = requests.get(url, params = {"page": param_page, "size": param_size})
        if response.status_code == 200:
            return response.json()
        return Response(status = 404)

    def get_tickets(self):
        return "get tickets"

    def post_tickets(self):
        return "post tickets"

    def get_tickets_by_id(self, ticketUid):
        return "get tickets by uid " + ticketUid

    def delete_tickets_by_id(self, ticketUid):
        return "delete tickets by uid " + ticketUid

    def get_me(self):
        return "Its my data"

    def get_privelege(self):
        return "Its my prevelege"



if __name__ == "__main__":

    server_host = '0.0.0.0'
    server_port = 8080
    tickets_port = 8070
    flights_port = 8060
    bonuses_port = 8050

    server = Server(server_host, server_port, tickets_port, flights_port, bonuses_port)
    server.run_server()

































