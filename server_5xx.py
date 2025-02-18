from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response
import os
import random

def hello_world(request):
    if random.random() < 0.5:  # 50% chance of generating an error
        return Response(status_code=500, body="Internal Server Error")
    
    # Normal response
    name = os.environ.get('NAME', 'world')
    message = f"GM all, {name}!\n"
    return Response(message)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    with Configurator() as config:
        config.add_route('hello', '/')
        config.add_view(hello_world, route_name='hello')
        app = config.make_wsgi_app()
    server = make_server('0.0.0.0', port, app)
    server.serve_forever()
