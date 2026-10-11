import psycopg2 
from psycopg2 import sql , pool
from concurrent.futures import ThreadPoolExecutor

conn_pool =pool.ThreadedConnectionPool(
    minconn=1, maxconn=10,
    host="localhost",
    port=5432,
    database="postgres",
    user="postgres",
    password="postgres")  

#conn = psycopg2.connect(
#    host="localhost",
#    port=5432,
#    database="postgres",
#    user="postgres",
#    password="postgres"
#)

print("Connexion réussie à PostgreSQL !")

def insert_measurement( measurement):
    conn=None 
    try: 
        conn = conn_pool.getconn()
        cursor = conn.cursor() 
        insert_query = """
            INSERT INTO metadata 
            (machine_id, temperature, vibration, rpm, status, measured_at)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
        cursor.execute(insert_query, (
            measurement["machine_id"],
            measurement["temperature"],
            measurement["vibration"],
            measurement["rpm"],
            measurement["status"],
            measurement["timestamp"]
        )) 

        conn.commit()
    except Exception as e:
        print(f"Error occurred while inserting measurement: {e}")
    finally:
        if conn:
            conn_pool.putconn(conn) 
#                
#    conn = conn_pool.getconn()
#    cursor = conn.cursor() 
#    insert_query = """
#        INSERT INTO metadata 
#        (machine_id, temperature, vibration, rpm, status, measured_at)
#        VALUES (%s, %s, %s, %s, %s, %s)
#        """
#    cursor.execute(insert_query, (
#        measurement["machine_id"],
#        measurement["temperature"],
#        measurement["vibration"],
#        measurement["rpm"],
#        measurement["status"],
#        measurement["timestamp"]
#    )) 
#
#    conn.commit() 
#    conn_pool.putconn(conn) 
#


#while True:
#
#    for machine in machines: 
#        measurement = generate_measurement(machine) 
#        insert_query = sql.SQL(
#            "INSERT INTO metadata (machine_id, temperature, vibration, rpm, status, measured_at) VALUES (%s, %s, %s, %s, %s, %s)"
#        ) 
#        cursor.execute(insert_query, (
#            measurement["machine_id"],
#            measurement["temperature_c"],
#            measurement["vib_m_s"],
#            measurement["rpm"],
#            measurement["status"],
#            measurement["timestamp"]
#        )) 
#        conn.commit() 
#        print(f"Inserted measurement for {measurement['machine_id']} at {measurement['timestamp']}") 
#    time.sleep(10)  # Wait for 10 seconds before generating the next set of measurements   
#conn.close()