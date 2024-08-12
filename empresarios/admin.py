from django.contrib import admin

from empresarios.models import Empresas, Documento, Metricas

admin.site.register(Empresas)
admin.site.register(Documento)
admin.site.register(Metricas)
