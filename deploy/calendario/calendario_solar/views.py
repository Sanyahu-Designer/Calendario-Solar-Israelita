from django.views.generic import View
from django.http import HttpResponse, Http404
from django.shortcuts import render
import requests

class ViteAppView(View):
    FRONTEND_PATHS = {'/solar/'}
    
    def get(self, request, *args, **kwargs):
        # Verifica se o path está na lista de paths do frontend
        if not any(request.path.startswith(path) for path in self.FRONTEND_PATHS):
            raise Http404()

        # Em produção, sempre retorna o index.html do frontend
        return render(request, 'index.html')
