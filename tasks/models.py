from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True) #cuando lo creamos se llena automaticamente
    datecompleted = models.DateTimeField(null=True, blank=True) # este espacio el usuario debera llenarlo y sera un campo vacio inicialmente
    important = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE) #relaciona la tabla task con la tabla user, la tabla user es una especial de django con la que se maneja el login y demas
    #CASCADE es si se elimina un usuario de la tabla USER se elimina tambien este elemento de la tabla Task
    def __str__(self):
        return self.title +'- by ' + self.user.username