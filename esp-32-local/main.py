import uasyncio as asyncio
import bot
from bot import Bot
import script
import json

robot = Bot()
web_page = open("interface.html","r").read()

header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n'

async def handle_command(data):
    data = data.split(":")
    if data[1] == 'stop':
        robot.disable()
        return "robot stopped"
    elif data[1] == 'auto-home':
        await robot.auto_zero()
        return "robot zeroed"
    elif data[1] == 'enable':
        robot.enable()
        return "robot enabled"
    elif data[1] == 'start':
        if(robot.loc_x != 0 or robot.loc_y != 0):
            await robot.auto_zero()
        if hasattr(script, 'main'):
            print("Script being run")
            await script.main(robot)
            return "script run"
    elif data[1] == 'pen-up':
        robot.pen_up()
        return "pen up"
    elif data[1] == 'pen-down':
        robot.pen_down()
        return "pen down"
    elif data[1] == 'move':
        await robot.teleop(int(data[2]), int(data[3]))
        return "teleop done"

    

async def handle_request(reader, writer):
    try:
        # Read the request (up to 1024 bytes)
        gc.collect()
        request = await reader.read(1024)
        request = request.decode('utf-8')
        if '/status' in request:
            response = await robot.get_status()

        elif '/command' in request:
            print(request[request.find('/command'):request.find('HTTP')])
            response = await handle_command(request[request.find('/command'):request.find('HTTP')])
            
        elif '/' in request:  # Default route to serve the main HTML page
            # Read the HTML content from the file
            response = web_page
        
        # Prepare the HTTP response
        full_response = header + response
        
        # Send the response
        writer.write(full_response.encode('utf-8'))
        await writer.drain()
    except Exception as e:
        print("Error handling request:", e)
    finally:
        writer.close()
        await writer.wait_closed()

# Start the server
async def start_server():
    # Start the server at '0.0.0.0' (any IP) and port 80
    server = await asyncio.start_server(handle_request, '0.0.0.0', 80)
    
    print('Serving on port 80...')

    # Instead of using `server.sockets`, we don't need to get the address explicitly
    try:
        while True:
            await asyncio.sleep(3600)  # Keep the server running
    except asyncio.CancelledError:
        pass
    


# Run the server
try:
    asyncio.run(start_server())
except KeyboardInterrupt:
    print("Server stopped")


