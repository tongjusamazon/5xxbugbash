from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response
import os
import time

def stream_response(request):
    def generate():
        name = os.environ.get('NAME', 'world')
        for i in range(5):  # Send 5 chunks
            chunk = f"Chunk {i+1}: Hello, {name}!\n"
            yield chunk.encode('utf-8')
            time.sleep(1)  # Simulate delay between chunks

    return Response(app_iter=generate(),
                    content_type='text/plain',
                    charset='utf-8')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    with Configurator() as config:
        config.add_route('hello', '/')
        config.add_view(stream_response, route_name='hello')
        app = config.make_wsgi_app()
    server = make_server('0.0.0.0', port, app)
    server.serve_forever()
