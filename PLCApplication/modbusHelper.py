"""
import os
import time
import sys
import json
import random
import paho.mqtt.client as mqtt
 
# Function to read sensor values
def read_from_sensor():
    temp = random.randint(25,45)
    hum = random.randint(50,60)
    air = random.randint(55,60)
    light = random.randint(100,180)
    return temp, hum, air,light
# Thingsboard platform credentials
THINGSBOARD_HOST = '192.168.66.98'
ACCESS_TOKEN = 'bqYfup8Bd4ejmATQjYia'
 
INTERVAL = 5
sensor_data = {'temperature' :0,'humidity':0,'air_quality':0,'light_intensity':0}
next_reading = time.time()
client = mqtt.Client()
client.username_pw_set(ACCESS_TOKEN)
client.connect(THINGSBOARD_HOST,1883,60)
 
client.loop_start()
 
try:
    while True:
        temp,hum,air,light = read_from_sensor()
        print("Temperature:",temp, chr(176) + "C")
        print("Humidity:", hum,"%rH")
        print("Air Quality:", air,"%")
        print("Light Intensity:",   light,"lux")
        sensor_data['temperature'] = temp
        sensor_data['humidity'] = hum
        sensor_data['air_quality'] = air
        sensor_data['light_intensity'] = light
 
        client.publish('v1/devices/me/telemetry',json.dumps(sensor_data),1)
        next_reading += INTERVAL
        sleep_time = next_reading-time.time()
        if sleep_time >0:
            time.sleep(sleep_time)
 
except KeyboardInterrupt:
    pass
 
client.loop_stop()
client.disconnect()

"""


from pymodbus.client.sync import ModbusTcpClient



def motorOn(client):
    """To switch on the PLC Conveyor"""
    
    client.write_coil(9,True)
    client.write_coil(9,False)
    print('Motor_On succeeded')
    
def motorOff(client):
    """To switch off the PLC Conveyor"""
    
    client.write_coil(8,True)
    client.write_coil(8,False)
    print('Motor_Off succeeded')
    
def connectModbus():
    """Connect to Modbus Device"""

    client = ModbusTcpClient("192.168.0.2")
    if(client):
        print("Connected")
    return client

def writeDefaultValuesToPLC(client,value):
    """Write Default Values To PLC once the program starts"""
    if(client.write_register(16,value)):
        print("value Written to the materialAbsentDelay is {}".format(value))
    
    
    
def readValuesFromPLC(client):
    """Read Values From PLC  - Returns PLC Data"""
    coils = []
    coils = client.read_coils(0, 8)
    print(coils.bits[0:8])
    materialAbsentDelay = client.read_holding_registers(12, 1)
    materialRejectedCount = client.read_holding_registers(8, 1)
    materialPassCount = client.read_holding_registers(4, 1)
    totalCount = client.read_holding_registers(0, 1)
    plcData = {
        "ProcessLineTripManual": coils.bits[0],
        "InspectionLineTripManual": coils.bits[1],
        "PackingLineTripManual": coils.bits[2],
        "MachineReady": coils.bits[3],
        "MachineRunning": coils.bits[4],
        "MaterialAbsent": coils.bits[5],
        "MaterialAbnormal": coils.bits[6],
        "MaterialDetectionSensor": coils.bits[7],
        "MaterialAbsentDelay": materialAbsentDelay.registers[0],
        "MaterialRejectedCount": materialRejectedCount.registers[0],
        "MaterialPassCount": materialPassCount.registers[0],
        "MaterialTotalCount": totalCount.registers[0]
    }
    return plcData


