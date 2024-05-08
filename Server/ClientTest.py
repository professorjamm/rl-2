import socket
import json
import time

HOST = 'localhost'
PORT = 1234

# Create a socket object
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#sock.connect((HOST, PORT))
server_address = (HOST,PORT)
sock.bind(server_address)
sock.listen(5)
cs, addr = sock.accept()

def keyPressed():
        print("Key Pressed")

# Receive data from the server
received_data = sock.recv(1024)
decoded_data = received_data.decode("utf-8")
response = json.loads(decoded_data)
print(response)

team1Score = 0
team2Score = 0
isReady = False

while not isReady:
        # Check if type is "CHECK READY"
        if response["type"] == "CHECK_READY":
                #check with the user if they are ready
                isReady = True
                response["type"] = "IS_READY"
                response["payload"] = True
                sock.sendall(json.dumps(response).encode("utf-8"))
                break

# Receive data from the server
received_data = sock.recv(1024)
decoded_data = received_data.decode("utf-8")
response = json.loads(decoded_data)
print(response)
# Start the timer

# Set game_time to the number set on the timer
game_time = response["payload"]["timer"]

print("\nTimer:")

# Send the initial score update to the server
score_update = {
        "type": "SCORE_UPDATE",
        "payload": {"score1": team1Score, "score2": team2Score}
}

while game_time >= 0:
        if game_time == 0:
                # Send the final score update to the server
                final_score_update = {
                        "type": "GAME_END",
                        "payload": {"score1": team1Score, "score2": team2Score, "timer": game_time}
                }
                sock.sendall(json.dumps(final_score_update).encode("utf-8"))
                break
        if response["type"] == "KEY_INPUT":
                keyPressed(response["payload"])
        mins, secs = divmod(game_time, 60)
        timeformat = '{:02d}:{:02d}'.format(mins, secs)
        print(timeformat, end='\r')
        
        if game_time%7==0:
                team1Score += 1
        elif game_time%5==0:
                team2Score += 1
        
        # Update the game time in the response JSON
        response["type"] = "TIMER_UPDATE"
        response["payload"] = game_time
        
        # Update the score in the response JSON
        score_update["payload"]["score1"] = team1Score
        score_update["payload"]["score2"] = team2Score

        # Combine response and score_update into a single JSON
        combined_json = {"time_update": response, "score_update": score_update}
        
        # Send the combined JSON to the server
        sock.sendall(json.dumps(score_update).encode("utf-8"))
        sock.sendall(json.dumps(response).encode("utf-8"))
        
        time.sleep(1)
        game_time -= 1

print("\n")
print("FINAL SCORE: Team 1: ", team1Score, " Team 2: ", team2Score) 
# Close the socket
sock.close()
