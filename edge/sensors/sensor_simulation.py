import random
import zmq
import time
from datetime import datetime

class Sensor:
    def __init__(self, tiempo, config_file, tipo_sensor):
        self.tipo_sensor = tipo_sensor
        self.tiempo = tiempo
        self.config = self.cargar_configuracion(config_file)

    def generar_medicion(self):
        value_status = random.choices(["correct", "out_of_bounds", "error"], weights = self.config, k = 1)[0]
        match value_status:
            case "correct":
                return self.generar_valor_correcto()
            case "out_of_bounds":
                return self.generar_valor_fuera_de_rango()
            case "error":
                return self.generar_valor_erroneo()

    def cargar_configuracion(self, config_file):
        with open(config_file, "r") as f:
            return [float(line) for line in f.read().splitlines()]

    def publicar_medicion(self):

        self.context = zmq.Context()

        #Proxy
        self.socket = self.context.socket(zmq.PUSH)
        self.socket.connect("tcp://10.43.100.158:5555")

        # Actuator
        self.actuator_socket = self.context.socket(zmq.PUSH)
        self.actuator_socket.connect("tcp://10.43.100.158:5556")
        
        # Quality system
        self.quality_socket = self.context.socket(zmq.PUSH)
        self.quality_socket.connect("tcp://10.43.100.158:5557")


        while True:
            medicion = self.generar_medicion()
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"\n{'='*40}\nMeasurement Report\n{'='*40}")
            print(f"Sensor Type   : {self.tipo_sensor}")
            print(f"Measurement   : {medicion}")
            print(f"Timestamp     : {timestamp}")
            print(f"{'='*40}\n")

            self.socket.send_string(f"{self.tipo_sensor} {medicion} at {timestamp}")
            if self.tipo_sensor == "Humo" and medicion == "True":
                self.actuator_socket.send_string("Activate")
                self.socket.send_string(f"Alert: {self.tipo_sensor} detected at {timestamp}")
                self.quality_socket.send_string(f"Quality System Alert: {self.tipo_sensor} detected at {timestamp}")
            
            time.sleep(self.tiempo)

        

    def generar_valor_correcto(self):
        pass

    def generar_valor_fuera_de_rango(self):
        pass

    def generar_valor_erroneo(self):
        pass
