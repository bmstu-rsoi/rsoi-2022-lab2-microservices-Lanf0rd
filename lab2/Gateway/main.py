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

        self.app.add_url_rule("/manage/health", view_func = self.get_say_ok)
        self.app.add_url_rule("/api/v1/flights", view_func = self.get_flights)
        self.app.add_url_rule("/api/v1/tickets", view_func = self.get_tickets)
        self.app.add_url_rule("/api/v1/tickets", view_func = self.post_tickets, methods = ["POST"])
        self.app.add_url_rule("/api/v1/tickets/<ticketUid>", view_func = self.get_tickets_by_id)
        self.app.add_url_rule("/api/v1/tickets/<ticketUid>", view_func = self.delete_tickets_by_id, methods = ["DELETE"])
        self.app.add_url_rule("/api/v1/me", view_func = self.get_me)
        self.app.add_url_rule("/api/v1/privilege", view_func = self.get_privelege)

    def run_server(self):
        return self.app.run(host = self.host, port = self.port)
    def get_say_ok(self):
        return "OK"
    
    def get_flights(self):
        param_page = request.args.get("page", default = 0, type = int)
        param_size = request.args.get("size", default = 0, type = int)
        url = "http://flight:" + str(self.Flights) + "/api/v1/flights"
        response = requests.get(url, params = {"page": param_page, "size": param_size})
        if response.status_code == 200:
            return response.json()
        return Response(status = 404)

    def get_tickets(self):
        client = request.headers.get("X-User-Name")
        url1 = "http://ticket:" + str(self.Tickets) + "/api/v1/tickets"
        url2 = "http://flight:" + str(self.Flights) + "/api/v1/get_flight_by_number"
        response_tickets = requests.get(url1, headers={"X-User-Name": client})
        if response_tickets.status_code != 200:
            return Response(status = 404)
        
        for ticket in response_tickets:
            response_flight = requests.get(url2, params = {"flight_number": ticket["flightNumber"]})
            if response_flight.status_code != 200:
                return Response(status = 404)

            ticket["fromAirport"] = response_flight["fromAirport"]
            ticket["toAirport"] = response_flight["toAirport"]
            ticket["date"] = response_flight["date"]
            ticket["price"] = response_flight["price"]
        return response_tickets.json()

    def post_tickets(self):
        return "post tickets"

    def get_tickets_by_id(self, ticketUid):
        return "get tickets by uid " + ticketUid

    def delete_tickets_by_id(self, ticketUid):
        return "delete tickets by uid " + ticketUid

    def get_me(self):
        return "Its my data"

    def get_privelege(self):
        client = request.headers.get("X-User-Name")
        url = "http://bonus:" + str(self.Bonuses) + "/api/v1/privilege"
        response = requests.get(url, headers={"X-User-Name": client})
        if response.status_code == 200:
            return response.json()
        return Response(status = 404)



if __name__ == "__main__":

    server_host = "0.0.0.0"
    server_port = 8080
    tickets_port = 8070
    flights_port = 8060
    bonuses_port = 8050

    server = Server(server_host, server_port, tickets_port, flights_port, bonuses_port)
    server.run_server()

































