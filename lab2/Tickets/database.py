import psycopg2


class Data_Base:
    def __init__(self):
        self.connection = False
        self.create_tables()

    def connect(self):
        self.connection = psycopg2.connect(dbname = "postgres",
                                           user = "program",
                                           password = "test",
                                           host = "postgres")

    def create_tables(self):
        if not(self.connection):
            self.connect()
        cursor = self.connection.cursor()
        try:
            sql_request = '''CREATE TABLE ticket
                             (
                                 id            SERIAL PRIMARY KEY,
                                 ticket_uid    uuid UNIQUE NOT NULL,
                                 username      VARCHAR(80) NOT NULL,
                                 flight_number VARCHAR(20) NOT NULL,
                                 price         INT         NOT NULL,
                                 status        VARCHAR(20) NOT NULL
                                     CHECK (status IN ('PAID', 'CANCELED'))
                             );'''

            cursor.execute(sql_request)
            self.connection.commit()
        except:
            self.connection.rollback()
        cursor.close()
        self.connection.close()
        self.connection = False

    def get_tickets(self, client):
        if not(self.connection):
            self.connect()
        cursor = self.connection.cursor()
        response = []
        try:
            cursor.execute("select ticket_uid, flight_number, status from ticket where username = %s;", (client,))
            tickets = cursor.fetchall()

            for ticket in tickets:
                items = dict()
                items["ticketUid"] = ticket[0]
                items["flightNumber"] = ticket[1]
                items["status"] = ticket[2]
                response.append(items)            
        except:
            self.connection.rollback()
        cursor.close()
        self.connection.close()
        self.connection = False
        return response

    def get_ticket(self, client, ticketUid):
        if not(self.connection):
            self.connect()
        cursor = self.connection.cursor()
        response = False
        try:
            cursor.execute("select ticket_uid, flight_number, status from ticket where username = %s and ticket_uid = %s;", (client, ticketUid))
            ticket = cursor.fetchall()
            if ticket[0]:
                response = dict()
                response["ticketUid"] = ticket[0]
                response["flightNumber"] = ticket[1]
                response["status"] = ticket[2]    
        except:
            self.connection.rollback()
        cursor.close()
        self.connection.close()
        self.connection = False
        return response









