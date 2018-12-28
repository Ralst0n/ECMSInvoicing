from psycopg2 import sql
import psycopg2


class DBInterface():

    def __init__(self):
        self.conn = psycopg2.connect(
            host="ecmsinvoices.cjmikjb2h1ef.us-east-1.rds.amazonaws.com",
            port="5432",
            user="Ralst0n",
            password="ProgrammeR0ss",
            dbname="postgres"
        )

        self.cur = self.conn.cursor()

    def initialize_tables(self):
        self.cur.execute('''
            CREATE TABLE fhours (
            id SERIAL PRIMARY KEY,
            date date,
            classification varchar(6),
            rate numeric,
            straight_time numeric,
            overtime numeric,
            inspector varchar(64),
            project varchar(64)
            );'''
                         )
        print("fhours created")
        self.conn.commit()

        self.cur.execute('''
            CREATE TABLE fmileage (
                id SERIAL PRIMARY KEY,
                date date,
                type varchar(45),
                miles numeric,
                inspector varchar(64),
                project varchar(64)
                );'''
                         )
        print("fmileage created")
        self.conn.commit()

    def add_to_mileage(self, list, inspector, project):
        sql_string = "INSERT INTO fmileage (date, type, miles, inspector, project) VALUES (%s, %s, %s, %s, %s);"
        self.cur.execute(
            sql_string, (list[0], list[1], list[2], inspector, project))
        self.conn.commit()

    def add_to_hours(self, list, inspector, project):
        add_string = "INSERT INTO fhours (date, classification, rate, straight_time, overtime, inspector, project) VALUES (%s, %s, %s, %s, %s, %s, %s);"
        self.cur.execute(
            add_string, (list[0], list[1], list[2], list[3], list[4], inspector, project))
        self.conn.commit()

    def show_table(self, table):
        self.cur.execute(
            sql.SQL("SELECT * FROM {} ORDER BY date")
            .format(sql.Identifier(table))
        )
        rows = self.cur.fetchall()
        for row in rows:
            print(row)

    def query_result(self, query_string):
        self.cur.execute(query_string)

        result = self.cur.fetchall()
        return result

    def anyHoursLogged(self, inspector, start, end):
        query_string = f"SELECT SUM(straight_time) FROM fhours WHERE inspector='{inspector}' AND date BETWEEN {start} AND {end};'"
        self.cur.execute(query_string)

        # TODO FINISH METHOD


db = DBInterface()
db.initialize_tables()
#db.add_to_mileage(["20161227", "ojm", 322], "John Wick", "42069")
#db.add_to_hours(["20161227", "TCIS-2", 32.25, 40, 20], "John Wick", "42069")
# db.show_table('fmileage')
# db.show_table('fhours')

# qs = "SELECT SUM(straight_time) FROM fhours WHERE inspector='John M Vartabedian';"
# print(f"ST: {db.query_result(qs)}")
# qs = "SELECT SUM(overtime) FROM fhours WHERE inspector='John M Vartabedian';"
# print(f"OT: {db.query_result(qs)}")
# qs = "SELECT SUM(miles) FROM fmileage WHERE inspector='John M Vartabedian' and type<>'ojm';"
# print(f"OJM: {db.query_result(qs)}")
# qs = "SELECT SUM(miles) FROM fmileage WHERE inspector='John M Vartabedian' and type='ojm';"
# print(f"OJM: {db.query_result(qs)}")

# qh = "SELECT SUM(straight_time), SUM(overtime) FROM fhours WHERE inspector='John M Vartabedian' and date BETWEEN '2018-12-03' AND '2018-12-09';"
# print(f"WEEK OF 12-03: {db.query_result(qh)}")
# qc = "SELECT SUM(), SUM(overtime) FROM fmileage WHERE inspector='John M Vartabedian' and date BETWEEN '2018-12-03' AND '2018-12-09';"
# qo = "SELECT SUM(straight_time), SUM(overtime) FROM fhours WHERE inspector='John M Vartabedian' and date BETWEEN '2018-12-03' AND '2018-12-09';"
