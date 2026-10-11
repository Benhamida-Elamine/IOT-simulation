import psycopg2

def insert_measurement(conn, measurement):
    cursor = conn.cursor()
    insert_query = psycopg2.SQL(
        "INSERT INTO metadata (machine_id, temperature, vibration, rpm, status, measured_at) VALUES (%s, %s, %s, %s, %s, %s)"
    )
    cursor.execute(insert_query, (
        measurement["machine_id"],
        measurement["temperature_c"],
        measurement["vib_m_s"],
        measurement["rpm"],
        measurement["status"],
        measurement["timestamp"]
    ))
    
    