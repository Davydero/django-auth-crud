from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task # de nuestro archivo models tomamos la clase Task para que haga un formulario en base a esos parametros
        fields = ['title', 'description', 'important']
        widgets = { #es un diccionario que sirve para enviar otros atributos
            'title': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Write a title'}),
            'description': forms.Textarea(attrs={'class':'form-control', 'placeholder':'Write a description'}),
            'important': forms.CheckboxInput(attrs={'class':'form-check-input m-auto'})
        }