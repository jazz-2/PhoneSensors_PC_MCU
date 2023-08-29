# https://github.com/jazz-2
import socket, traceback
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from functools import partial
import threading
import time

simulationTime=0
sensor=0
receivedData = "0"
clearFigure = False
expectedData = "11"

def readPhoneData():
    ####=================================================================
    hostNameOrIP = socket.gethostname() #'?.?.?.?' #computer IP
    print("'readPhoneData' hostNameOrIP:", hostNameOrIP)
    port = 5555
    ####=================================================================
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    s.bind((hostNameOrIP, port))

    initialTime=0.0
    previousTime=0
    reset=True
    while 1:
        try:           

            global simulationTime
            global sensor
            global receivedData
            global clearFigure
            print();


            message, address = s.recvfrom(8192)
            print (message)
            sensorsData_str = message.decode('UTF-8') #conversion to string 

            #receivedData = expectedData #to skip the message from a microcontroller
            if receivedData != expectedData:
                sensor=0.0
                reset = True
                sensorsData_str="Reset, string NULL"
            else:              
                if reset==True:
                    reset=False
                    clearFigure = True

                    sensor=0.0
                    initialTime=0.0
                    previousTime=0.0


                AccelerStrToFind = " 3, " # " 3,  " #string to find
                Acceler_pos_int = sensorsData_str.find(AccelerStrToFind)+1 #14 #location of searched data
                Time_pos_int = Acceler_pos_int-2
                GyroStrToFind = " 4, "
                Gyro_pos_int = sensorsData_str.find(GyroStrToFind)+1

                if initialTime==0:
                    initialTime = float(sensorsData_str[ 0 : Time_pos_int ])
                    print("initialTime: ", initialTime)

                simulationTime = float(sensorsData_str[ 0 : Time_pos_int ])
                simulationTime = round(simulationTime - initialTime, 4)
               
                Accelerometer_x = float(sensorsData_str[ Acceler_pos_int+2 : Acceler_pos_int+2+8 ])
                Gyroscope_x = float(sensorsData_str[ Gyro_pos_int+2 : Gyro_pos_int+2+8 ])

                dt = round( simulationTime-previousTime, 4) #sampling time

                ####=================================================================
                IfSensorDataWasSend = AccelerStrToFind
                sensor = Accelerometer_x
                ####=================================================================

                if sensorsData_str.find( IfSensorDataWasSend ) == -1: #We use UDP so data may be lost.
                    sensor=0.0
                    print ( "data not sent!" )
                #if abs(sensor) < 0.095 or abs(sensor) > 50: #remove small values
                #    sensor=0.0
                    
                previousTime = simulationTime

                print ( "sensor: ", sensor)  

            
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            traceback.print_exc()

def my_backround_fun():

    download_thread = threading.Thread(target=readPhoneData) 
    download_thread.start()

my_backround_fun()

def server_for_MCU():
    ####=================================================================
    hostNameOrIP = socket.gethostname() #'?.?.?.?' #computer IP
    print("'server_for_MCU' hostNameOrIP:", hostNameOrIP )
    port = 5004
    ####=================================================================

    server_socket = socket.socket() 
    server_socket.bind((hostNameOrIP, port))

    while True:

        server_socket.listen(2)
        conn, address = server_socket.accept() 
        print("Client address: ", str(address))
        while True:

            data = conn.recv(100).decode()
            if not data:
                break       

            global receivedData
            receivedData =  str(data)
            print("received data from client: ", receivedData)

            if receivedData == expectedData:
                global sensor
                sensorTreshold = 7.5

                while True:
                    time.sleep(0)
                    if sensor > sensorTreshold or sensor < -sensorTreshold: #send data to a microcontroler if the condition is met
                        receivedData="0"
                        data ="22"
                        sensor=0.0
                        break
            else:
                data ="00"
                print("received wrong data")

            conn.send(data.encode())
            print("send to client: ", str(data))

        conn.close() 

def my_backround_fun_server():

    download_thread = threading.Thread(target=server_for_MCU) 
    download_thread.start()

my_backround_fun_server()

fig, ax = plt.subplots()
line1, = ax.plot([], [], 'b.')

x_axis=10
y_axis=10
def init():
    global x_axis
    ax.set_xlim(-0, x_axis)
    ax.set_ylim(-y_axis, y_axis)
    return line1,
def update(frame, ln, x, y):

    global clearFigure
    global x_axis
    
    if clearFigure==True:
        clearFigure=False
        del x[:]
        del y[:]

    y.append( sensor )
    x.append( simulationTime ) 
    ln.set_data(x, y)


    if simulationTime >= x_axis-1:
        x_axis=x_axis+5
        ax.set_xlim(0, x_axis)


    return ln,

ani = animation.FuncAnimation( fig, partial(update, ln=line1, x=[], y=[]),
    frames=np.linspace(0, 2*np.pi, 128),
    init_func=init, interval=0, blit=True)

plt.xlabel('Time [s]')
plt.ylabel('Sensor data')
plt.grid(visible=None, which='both', axis='both')
plt.show()
