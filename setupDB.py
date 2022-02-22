import psycopg2

conn = psycopg2.connect(database="postgres", user='admin', password='password', host='127.0.0.1', port= '5432')
conn.autocommit = True
print(conn)

#Add database later