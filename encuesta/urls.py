"""encuesta URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""


from encuestaapp.views import ListEncuestaView, DeleteEncuesta, CreateEncuestaView, CreatePregunta, Votar, inicio, ingresar, cerrar, DetailEncuesta, ResponderEncuesta, UpdateEncuestaView
from encuestaapp.views import DetailPregunta, Deletepregunta, UpdatePregunta, CreateRespuesta, UpdateRespuesta, Deleterespuesta,GraciasView,ErrorView,ResultadoView

from django.conf.urls import url, include
from django.contrib.auth.decorators import login_required
from django.contrib import admin

urlpatterns = [
    #Urls referentes a el login y logout
    url(r'^$', inicio),
    url(r'^inicio/',inicio),
    url(r'^admin/', admin.site.urls),
    url(r'^ingresar/$', ingresar),
    url(r'^cerrar/$', login_required(cerrar)),

    #Urls referentes a las encuestas
    url(r'^Administracion/$', login_required(ListEncuestaView.as_view()), name="encuesta-list"),
    url(r'^newEncuesta/$', login_required(CreateEncuestaView.as_view()), name="encuesta-new"),
    url(r'^detalle/(?P<pk>\d+)/$', login_required(DetailEncuesta.as_view()), name='encuesta-view'),
    url(r'^delete/(?P<pk>\w+)/$',DeleteEncuesta.as_view(),name='encuesta-delete',),
    url(r'^update/(?P<pk>\w+)/$',UpdateEncuestaView.as_view(),name='encuesta-edit',),

    #Urls referentes a la accion de llenar una encuesta
    url(r'^responder/(?P<encuestaid>\d+)/$', ResponderEncuesta, name='responder'),
    url(r'^votar/(?P<encuestaid>\d+)/$', Votar, name='votar'),
    url(r'^Gracias/(?P<encuestaid>\d+)/$', GraciasView, name='gracias'),
    url(r'^Error/(?P<encuestaid>\d+)/$', ErrorView, name='error'),
    url(r'^Resultados/(?P<encuestaid>\d+)/$', ResultadoView, name='resultado'),


    #Urls referentes a las preguntas
    url(r'^Encuesta/(?P<encuestaid>\d+)/NuevaPregunta/$',login_required(CreatePregunta), name="pregunta-new"),
    url(r'^Encuesta/(?P<encuestaid>\d+)/Pregunta/(?P<preguntaid>\d+)/$',login_required(DetailPregunta), name="detalle-pregunta"),
    url(r'^Encuesta/(?P<encuestaid>\d+)/EliminarPregunta/(?P<preguntaid>\d+)/$',login_required(Deletepregunta), name="pregunta-delete"),
    url(r'^Encuesta/(?P<encuestaid>\d+)/EditarPregunta/(?P<preguntaid>\d+)/$',login_required(UpdatePregunta), name="pregunta-edit"),

    #Urls referentes a las respuestas
    url(r'^Encuesta/(?P<encuestaid>\d+)/Pregunta/(?P<preguntaid>\d+)/NuevaRespuesta/$',login_required(CreateRespuesta), name="respuesta-new"),
    url(r'^Encuesta/(?P<encuestaid>\d+)/Pregunta/(?P<preguntaid>\d+)/EditRespuesta/(?P<respuestaid>\d+)/$',login_required(UpdateRespuesta), name="respuesta-update"),
    url(r'^Encuesta/(?P<encuestaid>\d+)/Pregunta/(?P<preguntaid>\d+)/DeleteRespuesta/(?P<respuestaid>\d+)/$',login_required(Deleterespuesta), name="respuesta-delete"),
    
    ]
