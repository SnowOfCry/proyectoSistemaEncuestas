from django.db import models
from django.utils import timezone
from django import forms
from django.core.urlresolvers import reverse 


# Create your models here.
 
class Encuesta(models.Model):
    nombreEncuesta=models.CharField(max_length=100,null=False)
    descripcion = models.CharField(max_length=255)
    visitas = models.IntegerField(default=0)
    fechaCreacion=models.DateField(auto_now_add=timezone.now().date())

    def get_absolute_url(self):
        return reverse('encuesta-view', kwargs={'pk':self.id} )


    def __unicode__(self):
        return self.nombreEncuesta
    

class Pregunta(models.Model):
    encuesta=models.ForeignKey(Encuesta,null=False, on_delete=models.CASCADE )
    titulo= models.CharField(max_length=255)

    def get_absolute_url(self):
        return reverse('encuestaview',kwargs={'pk':self.encuesta})

    def __unicode__(self):
        return self.titulo

class Respuesta(models.Model):
    pregunta=models.ForeignKey(Pregunta,null=False, on_delete=models.CASCADE )
    titulo= models.CharField(max_length=255)
    votosRespuesta= models.IntegerField(default=0)

    def get_absolute_url(self):
        return reverse('preguntaview',kwargs={'pk':self.id})
    
    def __unicode__(self):
        return self.titulo

class EncuestaRespondida(models.Model):
    encuesta=models.ForeignKey(Encuesta,null=False, on_delete=models.CASCADE )
    ip= models.CharField(max_length=50, null=False)



 