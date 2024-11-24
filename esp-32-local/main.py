import uasyncio as asyncio
import bot
from bot import Bot
import script
import json

robot = Bot()
web_page = open("interface.html","r").read()

header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n'

async def start_script():
    if robot.enabled:
        robot.auto_zero()
        if hasattr(script, 'main'):
            print("Script being run")
            script.main(robot)
            await asyncio.sleep(0)
        else:
            print("Error: Script does not have a main method.")
    else:
        print("Error: Robot is not enabled.")
        await asyncio.sleep(0)
        
async def teleop_button(request):
    if robot.enabled:
        start_index = request.find('/teleop-button')
        request_str = request[start_index:]
        button_val = request_str[request_str.find('id')+3]
        step_val = request_str[request_str.find('step')+6:request_str.find("HTTP")-1]
        await robot.teleop(int(button_val), int(step_val))
    else:
        print("Error: Robot is not enabled.")
        await asyncio.sleep(0)
        
async def auto_zero():
    await robot.auto_zero()
    

async def handle_request(reader, writer):
    try:
        # Read the request (up to 1024 bytes)
        gc.collect()
        request = await reader.read(1024)
        request = request.decode('utf-8')

        if '/status' in request:
            response = robot.get_status()

        elif '/enable' in request:
            robot.enable()
            response = "Robot is enabled" if robot.enabled else "Error in enabling"
            
        elif '/e-stop' in request:
            robot.disable()
            response = "Robot has been disabled. If you were mid-script, you will need to start over."

        elif '/auto-home' in request:
            asyncio.create_task(auto_zero())
            response = "Robot zero task has been called"

        elif '/pen-up' in request:
            robot.pen_up()
            response = "Pen Up"
        
        elif '/pen-down' in request:
            robot.pen_down()
            response = "Pen Down"

        elif '/start-script' in request:
            asyncio.create_task(start_script())
            response = "script.main() has been called. See the terminal for more information."

        elif '/teleop-button' in request: # string parsing; do this later.
            asyncio.create_task(teleop_button(request))
            response = "Teleop Mode request has been called. See the terminal for more information."
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

