from django.contrib import admin
from encuestaapp.models import Encuesta,Pregunta,Respuesta

# Register your models here.

admin.site.register(Encuesta)
admin.site.register(Pregunta)
admin.site.register(Respuesta)
