import psycopg2

# https://www.psycopg.org/docs/module.html
# https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNSTRING


conn = psycopg2.connect(host="db", port=5432, database="fastapi", user="postgres", password="postgres-admin")

cur = conn.cursor()

cur.execute("SELECT * FROM posts;")
print(cur.fetchone())
