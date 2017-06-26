
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, render_to_response, get_list_or_404
from encuestaapp.models import Encuesta, Pregunta, Respuesta, EncuestaRespondida
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from encuestaapp.forms import EncuestaForm, PreguntaForm
from django.template import RequestContext
from ipware.ip import get_ip


def inicio(request):
	return render(request,'home.html')

#Aqui se realiza el login

def ingresar(request):
    if request.method == 'POST':
        formulario = AuthenticationForm(request.POST)
        if formulario.is_valid:
            usuario = request.POST['username']
            clave = request.POST['password']
            acceso = authenticate(username=usuario, password=clave)
            if acceso is not None:
                if acceso.is_active:
                    login(request, acceso)
                    return HttpResponseRedirect('/Administracion')
                else:
                    return HttpResponseRedirect('/ingresar')
            else:
                return HttpResponseRedirect('/ingresar')
    else:
        formulario = AuthenticationForm()
    context = {'formulario': formulario}
    return render(request, 'login.html', context)

@login_required(login_url='/ingresar')
def cerrar(request):
    logout(request)
    return HttpResponseRedirect('/')



#-----------------------Tratamiento de Encuestas--------------------------------

#Aqui se listan las encuestas
class ListEncuestaView(ListView): 
	
    template_name = 'encuesta_list.html'
    model = Encuesta


#Aqui se crea una nueva encuesta
class CreateEncuestaView(CreateView): 
    model = Encuesta
    template_name = 'edit_encuesta.html' 
    form_class = EncuestaForm

    def get_context_data(self, **kwargs): 
       context=super(CreateEncuestaView,self).get_context_data(**kwargs) 
       context['action']=reverse('encuesta-new')
       return context

    def get_success_url(self):
        return reverse('encuesta-list') 

#Aqui se muestra el detalle de cada encuesta
class DetailEncuesta(DetailView):
    model = Encuesta
    template_name = 'detalle_encuesta.html' 
    
    def get_context_data(self, **kwargs):
        context=super(DetailEncuesta, self).get_context_data(**kwargs)
        context['lista_preguntas'] = Pregunta.objects.all()

        return context

#Aqui se elimina una encuesta
class DeleteEncuesta(DeleteView):
    model = Encuesta 
    template_name = 'delete_encuesta.html'
    def get_success_url(self):
        return reverse('encuesta-list') 

#Aqui se actualiza la encuesta
class UpdateEncuestaView(UpdateView):
    model = Encuesta 
    template_name = 'edit_encuesta.html'
    form_class = EncuestaForm 

    def get_context_data(self, **kwargs):
        context=super(UpdateEncuestaView,self).get_context_data(**kwargs)
        context['action']=reverse('encuesta-edit',kwargs={'pk':self.get_object().id})
        return context

    def get_success_url(self): 
        return  reverse('encuesta-list')


#-----------------------Tratamiento de Contestar una encuesta--------------------------------

#En estas 4 funciones se muestran y guardan los votos de cada encuesta
def ResponderEncuesta(request, encuestaid):
    encuesta= get_object_or_404(Encuesta, id= encuestaid)
    preguntas= get_list_or_404(Pregunta, encuesta_id = encuestaid)
    return render(request, 'responder.html',{'encuesta':encuesta , 'preguntas':preguntas} )

def Votar(request, encuestaid):
    encuesta=get_object_or_404(Encuesta, id= encuestaid)
    ip_user= get_ip(request)
    
    if encuesta.visitas == 0:
        valido=True
        preguntas=get_list_or_404(Pregunta, encuesta=encuesta)
        if valido == True:
            encuRespo=EncuestaRespondida(encuesta=encuesta, ip=ip_user)
            encuRespo.save()
            if request.method == 'POST':
                for pregunta in preguntas:
                    if pregunta.id == 1:
                        listado = []
                        listado.append(int(request.POST.get('pp'+str(pregunta.id))))
                    else:
                        listado= request.POST.getlist('pp'+str(pregunta.id))
                    for elemento in listado:
                        respuesta= Respuesta.objects.get(id= elemento)
                        respuesta.votosRespuesta +=1
                        respuesta.save()

            encuesta.visitas +=1
            encuesta.save()
            return HttpResponseRedirect(reverse('gracias', args=(encuesta.id,)))
    else:
        valido=True
        enRe= get_list_or_404(EncuestaRespondida, encuesta_id = encuesta.id)
        for comp in enRe:
            if ip_user == comp.ip:
                valido=False

        if valido == True:
            encuRespo=EncuestaRespondida(encuesta=encuesta, ip=ip_user)
            encuRespo.save()
            if request.method == 'POST':
                for pregunta in preguntas:
                    if pregunta.id == 1:
                        listado = []
                        listado.append(int(request.POST.get('pp'+str(pregunta.id))))
                    else:
                        listado= request.POST.getlist('pp'+str(pregunta.id))
                    for elemento in listado:
                        respuesta= Respuesta.objects.get(id= elemento)
                        respuesta.votosRespuesta +=1
                        respuesta.save()

            encuesta.visitas +=1
            encuesta.save()
            return HttpResponseRedirect(reverse('gracias', args=(encuesta.id,)))

        else:
            return HttpResponseRedirect(reverse('error', args=(encuesta.id,)))





           

def GraciasView(request, encuestaid):
    e=get_object_or_404(Encuesta, id= encuestaid)
    return render(request, 'gracias.html',{'encuesta':e} )

def ErrorView(request, encuestaid):
    e=get_object_or_404(Encuesta, id= encuestaid)
    return render(request, 'error.html',{'encuesta':e, 'error_message':"Solo puedes votar una vez una encuesta"} )



#-----------------------Tratamiento de Preguntas--------------------------------

#Aqui se crea una pergunta
def CreatePregunta(request,encuestaid):
    encuesta= get_object_or_404(Encuesta, pk=encuestaid)

    if request.method == 'POST':
        pregunta=Pregunta()
        pregunta.encuesta= encuesta
        pregunta.titulo= request.POST['titulo']
        pregunta.save()

    return render_to_response('edit_pregunta.html',{'id':encuesta}, context_instance=RequestContext(request))


#Aqui se detallan los datos de cada pregunta con sus respuestas
def DetailPregunta(request, encuestaid, preguntaid ):
    encuesta= get_object_or_404(Encuesta, pk=encuestaid)
    pregunta=get_object_or_404(Pregunta, id =preguntaid)
    respuestas= pregunta.respuesta_set.all
    return render(request, 'detalle_pregunta.html',{'encuesta':encuesta , 'pregunta':pregunta, 'respuestas':respuestas} )

#Aqui se elimina una pregunta
def Deletepregunta(request, encuestaid, preguntaid ):
    encuesta= get_object_or_404(Encuesta, pk=encuestaid)
    pregunta=get_object_or_404(Pregunta, id =preguntaid)

    if request.method == 'POST':
        pregunta.delete()
        return HttpResponseRedirect(reverse('encuesta-view', args=(encuesta.id,)))

    return render_to_response('delete_pregunta.html',{'encuesta':encuesta, 'pregunta':pregunta}, context_instance=RequestContext(request))

#Aqui se actualiza una pregunta
def UpdatePregunta(request, encuestaid, preguntaid ):
    encuesta= get_object_or_404(Encuesta, pk=encuestaid)
    pregunta=get_object_or_404(Pregunta, id =preguntaid)

    if request.method == 'POST':
        pregunta.encuesta= encuesta
        pregunta.titulo= request.POST['titulo']
        pregunta.save()
        return HttpResponseRedirect(reverse('encuesta-view', args=(encuesta.id,)))

    return render_to_response('editar_pregunta.html',{'encuesta':encuesta, 'pregunta':pregunta}, context_instance=RequestContext(request))


#-----------------------Tratamiento de Respuestas--------------------------------


#Aqui se crea una respuesta
def CreateRespuesta(request, encuestaid, preguntaid):
    encuesta= get_object_or_404(Encuesta, pk=encuestaid)
    pregunta= get_object_or_404(Pregunta, id =preguntaid)

    if request.method == 'POST':
        respuesta=Respuesta()
        respuesta.pregunta= pregunta
        respuesta.titulo= request.POST['titulo']
        respuesta.save()

    return render_to_response('new_respuesta.html', {'pregunta':pregunta, 'encuesta':encuesta}, context_instance=RequestContext(request))

#Aqui se edita una respuesta
def UpdateRespuesta(request, encuestaid, preguntaid,respuestaid):
    encuesta= get_object_or_404(Encuesta, pk=encuestaid)
    pregunta= get_object_or_404(Pregunta, id =preguntaid)
    respuesta= get_object_or_404(Respuesta, id = respuestaid)

    if request.method == 'POST':
        respuesta.pregunta= pregunta
        respuesta.titulo= request.POST['titulo']
        respuesta.save()
        return HttpResponseRedirect(reverse('detalle-pregunta', args=(encuesta.id, pregunta.id)))

    return render_to_response('edit_respuesta.html', {'pregunta':pregunta, 'encuesta':encuesta, 'respuesta':respuesta}, context_instance=RequestContext(request))

#Aqui se elimina una respuesta
def Deleterespuesta(request, encuestaid, preguntaid, respuestaid ):
    encuesta= get_object_or_404(Encuesta, pk=encuestaid)
    pregunta= get_object_or_404(Pregunta, id =preguntaid)
    respuesta= get_object_or_404(Respuesta, id = respuestaid)

    if request.method == 'POST':
        respuesta.delete()
        return HttpResponseRedirect(reverse('detalle-pregunta', args=(encuesta.id, pregunta.id)))

    return render_to_response('delete_respuesta.html',{'encuesta':encuesta, 'pregunta':pregunta, 'respuesta':respuesta}, context_instance=RequestContext(request))








    

        

