import redis
import psycopg2
import time
r = redis.Redis(host="redis", port=6379, db=0)
conn = psycopg2.connect(dbname="votes", user="postgres", password="postgres", host="postgres", port=5432)
cur = conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS votes (id SERIAL PRIMARY KEY, vote TEXT)")
conn.commit()
while True:
    vote = r.blpop("votes", timeout=5)
    if vote:
        vote = vote[1].decode("utf-8")
        cur.execute("INSERT INTO votes (vote) VALUES (%s)", (vote,))
        conn.commit()
    time.sleep(1)
