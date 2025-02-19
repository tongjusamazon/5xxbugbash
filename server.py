from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response
import os
import sys
from datetime import datetime

def log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{timestamp} - {message}", flush=True)

def hello_world(request):
    log("Received request")
    name = os.environ.get('NAME')
    if name == None or len(name) == 0:
        name = "world"
        log("WARNING: NAME environment variable not set, using default")
    message = "GM all, " + name + "!\n"
    log(f"Responding with message: {message}")
    return Response(message)

if __name__ == '__main__':
    log("Starting application")
    try:
        port = int(os.environ.get("PORT"))
        log(f"Using port: {port}")
    except (TypeError, ValueError):
        log("ERROR: PORT environment variable not set or not a valid integer")
        sys.exit(1)

    with Configurator() as config:
        log("Configuring Pyramid")
        config.add_route('hello', '/')
        config.add_view(hello_world, route_name='hello')
        app = config.make_wsgi_app()
    
    log("Starting server")
    server = make_server('0.0.0.0', port, app)
    try:
        log("Server is running. Press CTRL+C to stop.")
        server.serve_forever()
    except KeyboardInterrupt:
        log("Stopping server")
    except Exception as e:
        log(f"An error occurred: {str(e)}")
    finally:
        log("Server stopped")
