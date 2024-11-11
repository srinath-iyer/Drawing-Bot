import uasyncio as asyncio
import bot
from bot import Bot
import script

robot = Bot()

# Define the handle_request function that will process incoming requests
def web_page(): 
  html = open("interface.html","r").read()
  return html

async def handle_request(reader, writer):
    new_messages = "" # If something notable happens, we add the 
    try:
        # Read the request (up to 1024 bytes)
        request = await reader.read(1024)
        request = request.decode('utf-8')
        if '/status' in request:
            status = str(robot.get_status).replace("'",'"')
            print(status)
            std_messages = status
            std_messages[""]
        elif '/enable' in request:
            print("ENABLE")
            robot.enable()
            response = "Robot is enabled" if robot.enabled else "Error in enabling"
            
        elif '/e-stop' in request:
            robot.disable()
            response = "Robot has been disabled. If you were mid-script, you will need to start over."

        elif '/auto-home' in request:
            robot.auto_zero()
            reponse = "Robot is zeroed" if robot.is_robot_zero else "That didn't work. Try again."

        elif '/start-script' in request: # This one is complicated; we have to call the main() in script.py
            if(robot.is_robot_zero() and robot.enabled):
                if hasattr(script, 'main'):
                    script.main()
                else:
                    response = "script.py does not have a main method."

        elif '/teleop-button' in request: # string parsing; do this later.
            request.find('/teleop-button')

        elif '/' in request:  # Default route to serve the main HTML page
            # Read the HTML content from the file
            response = web_page()
        
        # Prepare the HTTP response
        header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n'
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
