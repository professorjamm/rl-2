import socket
import json
import time

HOST = 'localhost'
PORT = 2234

# Create a socket object
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

# Receive data from the server
received_data = sock.recv(1024)
decoded_data = received_data.decode("utf-8")
response = json.loads(decoded_data)
print(response)

# Start the timer
game_time = response["game_time"]

print("\nTimer:")
 
while game_time:
        mins, secs = divmod(game_time, 60)
        timeformat = '{:02d}:{:02d}'.format(mins, secs)
        print(timeformat, end='\r')
        
        # Update the game time in the response JSON
        response["game_time"] = game_time
        
        # Send the updated response to the server
        sock.sendall(json.dumps(response).encode("utf-8"))
        
        #print(game_time)
        time.sleep(1)
        game_time -= 1

print("\n\n")

# Close the socket
sock.close()
