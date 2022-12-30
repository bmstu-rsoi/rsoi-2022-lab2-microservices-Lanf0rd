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
            sql_request = '''CREATE TABLE privilege
                             (
                                 id       SERIAL PRIMARY KEY,
                                 username VARCHAR(80) NOT NULL UNIQUE,
                                 status   VARCHAR(80) NOT NULL DEFAULT 'BRONZE'
                                     CHECK (status IN ('BRONZE', 'SILVER', 'GOLD')),
                                 balance  INT
                             );'''

            cursor.execute(sql_request)
            cursor.execute("insert into privilege (username, status, balance) values (%s, %s, %s)",
                               ("UserName", "GOLD", 1500))
            
            sql_request = '''CREATE TABLE privilege_history
                             (
                                 id             SERIAL PRIMARY KEY,
                                 privilege_id   INT REFERENCES privilege (id),
                                 ticket_uid     uuid        NOT NULL,
                                 datetime       TIMESTAMP   NOT NULL,
                                 balance_diff   INT         NOT NULL,
                                 operation_type VARCHAR(20) NOT NULL
                                     CHECK (operation_type IN ('FILL_IN_BALANCE', 'DEBIT_THE_ACCOUNT'))
                             );'''
            cursor.execute(sql_request)
            cursor.execute("insert into privilege_history (privilege_id, ticket_uid, datetime, balance_diff, operation_type) values (%s, %s, %s, %s, %s)",
                               (1, "049161bb-badd-4fa8-9d90-87c9a82b0668", "2021-10-08T19:59:19Z", 1500, "FILL_IN_BALANCE"))
            self.connection.commit()
        except:
            self.connection.rollback()
        cursor.close()
        self.connection.close()
        self.connection = False



    def get_privilege(self, client):
        if not(self.connection):
            self.connect()
        cursor = self.connection.cursor()
        response = False
        try:
            cursor.execute("select balance, status, id from privilege where username = %s;", (client,))
            client_data = cursor.fetchall()

            response = {"balance": client_data[0], "status": client_data[1], "history": []}
            cursor.execute("select datetime, ticket_uid, balance_diff, operation_type from privilege_history where privilege_id = %s;", (client_data[2],))
            client_bonuses = cursor.fetchall()

            for client_bonus in client_bonuses:
                items = dict()
                items["date"] = client_bonus[0]
                items["ticketUid"] = client_bonus[1]
                items["balanceDiff"] = client_bonus[2]
                items["operationType"] = client_bonus[3]
                response["history"].append(items)            
        except:
            self.connection.rollback()
        cursor.close()
        self.connection.close()
        self.connection = False
        
        return response





