import serial

ser = serial.Serial('COM4', 9600)  # replace 'COM4' with your port
ser.write(b'Your data')  # send data
ser.close()
