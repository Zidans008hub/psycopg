import psycopg2

conn = psycopg2.connect("dbname=kimdur user=postgres password=8002")
cur = conn.cursor()

# cur.execute("CREATE TABLE test (id serial PRIMARY KEY, num integer, data varchar(30));")

# Ma'lumot qo'shish (TO'G'RI)
cur.execute("INSERT INTO test(num, data) VALUES (20, 'va alaykum assalom');")

conn.commit()

cur.close()
conn.close()


def add_user():
    return None