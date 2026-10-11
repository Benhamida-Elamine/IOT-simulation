from simulator import generate_measurement
import time 
from industrial_iot.measurements import measurements_init
from database import  insert_measurement 
from concurrent.futures import ThreadPoolExecutor

# ThreadPoolExecutor() utiliser pour executer la fonction generate_measurement en parallele pour chaque machine, ce qui permet de generer les mesures plus rapidement et d'ameliorer les performances de l'application.
if __name__ == "__main__": 
    while True:
        try : 
            with ThreadPoolExecutor() as executor:
                    resultats = executor.map(generate_measurement, measurements_init)
                    for resultat in resultats: 
                        insert_measurement(resultat) 
                        print(f"Inserted measurement for {resultat['machine_id']} at {resultat['timestamp']}") 
        except Exception as e:
            print(f"Error occurred: {e}") 
         
        time.sleep(10)  # Wait for 10 seconds before generating the next set of measurements        




# while True:
#    try: 
#        for machine in machines: 
#            measurement = generate_measurement(machine) 
#            insert_measurement(conn,measurement) 
#            print(f"Inserted measurement for {measurement['machine_id']} at {measurement['timestamp']}") 
#    except Exception as e:
#        print(f"Error occurred: {e}")
#    conn.commit()  
#    time.sleep(10)  # Wait for 10 seconds before generating the next set of measurements        
