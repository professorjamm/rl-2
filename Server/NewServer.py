import asyncio
import websockets
import json
import time

HOST = 'localhost'
PORT = 1234

team1Score = 0
team2Score = 0
isReady = False

async def server(websocket, path):
    global team1Score, team2Score, isReady
    while True:
        received_data = await websocket.recv()
        response = json.loads(received_data)
        print(response)

        if not isReady:
            if response["type"] == "CHECK_READY":
                isReady = True
                response["type"] = "IS_READY"
                response["payload"] = True
                await websocket.send(json.dumps(response))
                continue

        game_time = response["payload"]["timer"]
        print("\nTimer:")

        score_update = {
            "type": "SCORE_UPDATE",
            "payload": {"score1": team1Score, "score2": team2Score}
        }

        while game_time >= 0:
            if game_time == 0:
                final_score_update = {
                    "type": "GAME_END",
                    "payload": {"score1": team1Score, "score2": team2Score, "timer": game_time}
                }
                await websocket.send(json.dumps(final_score_update))
                break
            if response["type"] == "KEY_INPUT":
                print("Key Pressed")

            mins, secs = divmod(game_time, 60)
            timeformat = '{:02d}:{:02d}'.format(mins, secs)
            print(timeformat, end='\r')

            if game_time%7==0:
                team1Score += 1
            elif game_time%5==0:
                team2Score += 1

            response["type"] = "TIMER_UPDATE"
            response["payload"] = game_time

            score_update["payload"]["score1"] = team1Score
            score_update["payload"]["score2"] = team2Score

            combined_json = {"time_update": response, "score_update": score_update}

            await websocket.send(json.dumps(score_update))
            await websocket.send(json.dumps(response))

            time.sleep(1)
            game_time -= 1

        print("\n\n")
        print("FINAL SCORE: Team 1: ", team1Score, " Team 2: ", team2Score)

start_server = websockets.serve(server, HOST, PORT)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
