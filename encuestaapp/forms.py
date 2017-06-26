from django import forms
from django.core.exceptions import ValidationError
from encuestaapp.models import Encuesta, Pregunta
import re

class EncuestaForm(forms.ModelForm):
    nombreEncuesta=forms.CharField(max_length=100,required=True,label="Nombre")
    descripcion = forms.CharField(max_length=255,required=True,label="Descripcion")
    	
    
    class Meta:
        model = Encuesta
        fields = ['nombreEncuesta', 'descripcion']
	
    

    def clean_nombreEncuesta(self):
        nombreEncuesta = self.cleaned_data.get('nombreEncuesta') 
        if(re.match("[a-zA-Z]",nombreEncuesta) == None):
            raise forms.ValidationError("Debe iniciar con un caracter")
        else:
            if (re.match("[a-z0-9-A-Z]*",nombreEncuesta) == None):
                raise forms.ValidationError("Deben de ser caracters alfanumericos")
        return nombreEncuesta

        def clean_descripcion(self):
            descripcion = self.cleaned_data.get('descripcion') 
            num_words = len(descripcion.split())
            if num_words < 4:
                raise forms.ValidationError("Deben de ser minimo 4 palabras!")
            else:
                if (re.match("\[a-z0-9-A-Z]*",descripcion) ==None):
                    raise forms.ValidationError("Deben de ser caracters alfanumericos") 
            return descripcion

class PreguntaForm(forms.ModelForm):
    encuesta= Encuesta
    titulo=forms.CharField(max_length=100,required=True,label="Titulo")
    
        
    
    class Meta:
        model = Pregunta
        fields = ['encuesta','titulo']
    
    

    def clean_titulo(self):
        titulo = self.cleaned_data.get('titulo') 
        if(re.match("[a-zA-Z]",titulo) == None):
            raise forms.ValidationError("Debe iniciar con un caracter")
        else:
            if (re.match("[a-z0-9-A-Z]*", titulo) == None):
                raise forms.ValidationError("Deben de ser caracters alfanumericos")
        return titulo

        
