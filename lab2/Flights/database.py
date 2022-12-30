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
            sql_request = '''CREATE TABLE airport
                             (
                                 id      SERIAL PRIMARY KEY,
                                 name    VARCHAR(255),
                                 city    VARCHAR(255),
                                 country VARCHAR(255)
                             );'''

            cursor.execute(sql_request)
            cursor.execute("insert into airport (name, city, country) values (%s, %s, %s)",
                               ("Шереметьево", "Москва", "Россия"))
            cursor.execute("insert into airport (name, city, country) values (%s, %s, %s)",
                               ("Пулково", "Санкт-Петербург", "Россия"))

            sql_request = '''CREATE TABLE flight
                             (
                                 id              SERIAL PRIMARY KEY,
                                 flight_number   VARCHAR(20)              NOT NULL,
                                 datetime        TIMESTAMP WITH TIME ZONE NOT NULL,
                                 from_airport_id INT REFERENCES airport (id),
                                 to_airport_id   INT REFERENCES airport (id),
                                 price           INT                      NOT NULL
                             );'''
            cursor.execute(sql_request)
            cursor.execute("insert into flight (flight_number, datetime, from_airport_id, to_airport_id, price) values (%s, %s, %s, %s, %s)",
                               ("AFL031", "2021-10-08 20:00", 2, 1, 1500))
            cursor.execute("insert into flight (flight_number, datetime, from_airport_id, to_airport_id, price) values (%s, %s, %s, %s, %s)",
                               ("AFL0312", "2021-10-08 20:00", 1, 2, 2000))
            self.connection.commit()
        except:
            self.connection.rollback()
        cursor.close()
        self.connection.close()
        self.connection = False

    def get_flights(self, page, size):
        offset = (page - 1)*size
        if not(self.connection):
            self.connect()
        cursor = self.connection.cursor()
        response = False
        try:
            sql_request = '''select flight_number, (select city from airport where from_airport_id = id) as from_city,
                             (select name from airport where from_airport_id = id) as from_name,
                             (select city from airport where to_airport_id = id) as to_city,
                             (select name from airport where to_airport_id = id) as to_name,
                             datetime, price from flight limit %s offset %s'''
            params = (size, offset)
            cursor.execute(sql_request, params)
            flights = cursor.fetchall()


            response = {"page": page, "pageSize": size, "totalElements": len(flights), "items": []}
            for flight in flights:
                items = dict()
                items['flightNumber'] = flight[0]
                items['fromAirport'] = flight[1] + ' ' + flight[2]
                items['toAirport'] = flight[3] + ' ' + flight[4]
                items['date'] = flight[5]
                items['price'] = flight[6]
                response['items'].append(items)            
        except:
            self.connection.rollback()
        cursor.close()
        self.connection.close()
        self.connection = False
        return response









