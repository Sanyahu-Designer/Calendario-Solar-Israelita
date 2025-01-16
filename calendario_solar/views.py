from django.views.generic import View
from django.http import HttpResponse
import requests

class ViteAppView(View):
    def get(self, request, *args, **kwargs):
        try:
            # Proxy the request to Vite dev server
            response = requests.get('http://localhost:5173' + request.path)
            return HttpResponse(
                content=response.content,
                status=response.status_code,
                content_type=response.headers.get('content-type', 'text/html')
            )
        except requests.RequestException:
            # Se o Vite não estiver rodando, retorna uma mensagem amigável
            return HttpResponse(
                'Frontend server is not running. Please start it with "npm run dev" in the frontend directory.',
                status=503
            )
