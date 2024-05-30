import threading
import time
from datetime import datetime
import zmq

# Temperature and Humidity parameters
TEMP_RANGE = (11.0, 29.4)
HUMIDITY_RANGE = (70.0, 100.0)
SENSOR_LIMIT = 10  # Number of sensor readings to average

def initialize_sockets():
    context = zmq.Context()
    sockets = {
        "sensor": context.socket(zmq.PULL),
        "quality": context.socket(zmq.REQ),
        "cloud": context.socket(zmq.REQ),
        "health": context.socket(zmq.PUSH),
        "actuator": context.socket(zmq.PULL),
    }
    
    try:
        print("Initializing sockets...")
        sockets["sensor"].bind("tcp://*:5555")
        sockets["quality"].connect("tcp://10.51.51.183:5580")
        sockets["cloud"].connect("tcp://54.92.238.228:5581")
        sockets["health"].connect("tcp://10.138.208.85:5558")
        sockets["actuator"].bind("tcp://*:5556")
    except zmq.ZMQError as e:
        print(f"Socket initialization error: {e}")
        raise

    return context, sockets

def process_data(sensor_type, measurement):
    if sensor_type == "temperatura":
        process_temperature(measurement)
    elif sensor_type == "humedad":
        process_humidity(measurement)
    elif sensor_type == "humo":
        process_smoke(measurement)

def process_temperature(measurements):
    if len(measurements) >= SENSOR_LIMIT:
        average_temp = sum(measurements) / SENSOR_LIMIT
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"Average Temperature: {average_temp} at {timestamp}")
        if not (TEMP_RANGE[0] <= average_temp <= TEMP_RANGE[1]):
            send_alert("temperatura", average_temp, "incorrecto")
            
def process_humidity(measurements):
    if len(measurements) >= SENSOR_LIMIT:
        average_humidity = sum(measurements) / SENSOR_LIMIT
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"Average Humidity: {average_humidity} at {timestamp}")
        if not (HUMIDITY_RANGE[0] <= average_humidity <= HUMIDITY_RANGE[1]):
            send_alert("humedad", average_humidity, "incorrecto")

def process_smoke(measurement):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if measurement:
        print(f"Smoke detected at {timestamp}")
        send_alert("humo", measurement, "detected")

def send_alert(sensor_type, measurement, status):
    alert_message = {
        "message_type": "alert",
        "sensor_type": sensor_type,
        "measurement": measurement,
        "status": status,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    sockets["quality"].send_json(alert_message)
    response_quality = sockets["quality"].recv_json()
    print(f"Quality System Response: {response_quality}")

    sockets["cloud"].send_json(alert_message)
    response_cloud = sockets["cloud"].recv_json()
    print(f"Cloud Response: {response_cloud}")

def handle_sensor_data(sockets):
    measurements = {"temperatura": [], "humedad": []}
    while True:
        message = sockets["sensor"].recv_string()
        parts = message.split()
        sensor_type = parts[0]
        measurement = float(parts[1]) if sensor_type != "humo" else parts[1] == "True"
        timestamp = " ".join(parts[2:])
        print(f"Received {sensor_type} measurement: {measurement} at {timestamp}")
        
        if sensor_type in measurements:
            measurements[sensor_type].append(measurement)
            if len(measurements[sensor_type]) >= SENSOR_LIMIT:
                process_data(sensor_type, measurements[sensor_type][:SENSOR_LIMIT])
                measurements[sensor_type] = measurements[sensor_type][SENSOR_LIMIT:]
        else:
            process_data(sensor_type, measurement)

def handle_actuator_data(sockets):
    while True:
        message = sockets["actuator"].recv_string()
        if message == "Activate":
            print("Activating actuator due to smoke detection.")

def send_heartbeat(sockets):
    while True:
        try:
            sockets["health"].send_json({"heartbeat": "ping"})
        except zmq.ZMQError as e:
            print(f"Heartbeat error: {e}")
        time.sleep(1)

if __name__ == "__main__":
    context, sockets = initialize_sockets()

    sensor_thread = threading.Thread(target=handle_sensor_data, args=(sockets,))
    sensor_thread.start()

    actuator_thread = threading.Thread(target=handle_actuator_data, args=(sockets,))
    actuator_thread.start()

    heartbeat_thread = threading.Thread(target=send_heartbeat, args=(sockets,))
    heartbeat_thread.start()

    try:
        sensor_thread.join()
        actuator_thread.join()
        heartbeat_thread.join()
    except KeyboardInterrupt:
        print("Shutdown initiated.")
    finally:
        print("Closing sockets and terminating context.")
        for socket in sockets.values():
            socket.close()
        context.term()
