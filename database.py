import psycopg2

def connection():
    con = psycopg2.connect(
        host="localhost",
        database="ecommerce",
        user="postgres",
        password="1592005",
        port="5432"
    )
    if con:
        print("✅ Database Connected Successfully!")
    else:
        print("❌ Connection Failed!")
    return con

conn = connection()