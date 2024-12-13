import websockets
import asyncio
import os

from tools import ChunkTools
 
# Creating WebSocket server
async def ws_server(websocket):
    print("WebSocket: Server Started.")
 
    try:
        while True:
            # Receiving values from client
            id = await websocket.recv()
            chsize = await websocket.recv()
 
            # Prompt message when any of the field is missing
            if id == "":
                print("Error Receiving Value from Client.")
                break
 

            # Printing details received by client
            print(f"Clients Requests An Files {id}")
            if os.listdir(os.getcwdb() + "/files/").count(id.lower()):
                with ChunkTools().getCompParts("files/"+id) as fs:
                    for x in fs:
                        await websocket.send(x)
 
    except websockets.ConnectionClosedError:
        print("Internal Server Error.")
 
 
async def main():
    async with websockets.serve(ws_server, "localhost", 7890):
        await asyncio.Future()  # run forever
 
if __name__ == "__main__":
    asyncio.run(main())