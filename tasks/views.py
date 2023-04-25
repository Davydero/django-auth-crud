from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse
from django.db import IntegrityError
from .forms import TaskForm
from .models import Task
from django.utils import timezone
from django.contrib.auth.decorators import login_required
#django ya permite registerar usuarios
# Create your views here.
def home(request):
    return render(request, 'home.html')

def signup(request):
    if request.method == 'GET': #get es cuando se carga la pagina signup.html como siempre
        return render(request, 'signup.html',{
        'form': UserCreationForm  #se envia una variable formulario que se renderiza en el archivo html (formulario especial que tiene un nombre de usuario y dos contrasenas para corroborar)
    })
    else:
        if request.POST['password1']==request.POST['password2']:#verifica que las 2 contrasenas sean iguales para registrar el usuario
            try:
                #register user----- antes de registrar usuarios y demas se necesita iniciar la base de datos (primero hacer las migraciones )
                user = User.objects.create_user(username=request.POST['username'],password=request.POST['password1'])#se registra el nombre de usuario y la contrasena, que son recibidos en el POST
                user.save() #guarda el objeto user en la base de datos 
                login(request, user) #genera lo cookie de usuario, para identificarlo y ver a que cosas de la pagina puede acceder este usuario
                return redirect('tasks')
            except IntegrityError:#si se da algun error en la base de datos, como un nombre de usuario repetido
                return render(request, 'signup.html',{
                    'form':UserCreationForm,
                    'error':'Username already exists'
                })
        return render(request, 'signup.html',{
                    'form':UserCreationForm,
                    'error':'Password do not match' #pasamos el mensaje de error en la variable error
                })

@login_required
def tasks(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True)# los objetos en la base de datos con el usuario del request y que tengan el atributo datecompleted vacio
    return render(request,'tasks.html', { #es decir solo mostrara los tasaks que aun no fueron completados
        'tasks': tasks
    })

@login_required
def tasks_completed(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')# los objetos en la base de datos con el usuario del request 
    return render(request,'tasks.html', { #es decir solo mostrara los tasaks que aun no fueron completados
        'tasks': tasks
    })

@login_required
def create_task(request):

    if request.method =='GET': #si se recibe la peticion get se renderiza el formato del formulario
        return render(request, 'create_task.html', {
            'form': TaskForm
        })
    else: #en caso de post deberia recibir los datos del formulario y agregar a la base de datos
        try:
            form = TaskForm(request.POST) #se crea un objeto del tipo TaskForm con la informacion del request.post
            new_task = form.save(commit=False) # no queremos que se guarde, solo nos devuelva los datos que hay en ese formulario
            new_task.user = request.user #se le asigna el usuario
            new_task.save() #ahora si se guarda en la base de datos 
            return redirect('tasks') #llama a la funcion tasks que a su vez llama al html
        except ValueError:
            return render(request, 'create_task.html', {
                'form': TaskForm,
                'error': 'Please provide valid data'
            })

@login_required
def task_detail(request, task_id):
    #task = Task.objects.get(pk=task_id)
    if request.method == 'GET':
        task = get_object_or_404(Task, pk=task_id, user = request.user) #encuentra el objeto en la base de datos o nos devuelve el error 404
        form = TaskForm(instance=task)
        return render(request, 'task_detail.html',{
        'task': task,
        'form': form
        })
    else: #para hacer cambios en una tarea existente // basicamente esto es actualizar 
        try:
            task = get_object_or_404(Task, pk=task_id, user = request.user)
            form = TaskForm(request.POST, instance=task)
            form.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'task_detail.html', {
            'task': task,
            'form': form,
            'error': "Error updating task"
            })

@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.datecompleted = timezone.now()
        task.save()
        return redirect('tasks')

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')

@login_required
def signout(request):
    logout(request)
    return redirect('home')

def signin(request):
    if request.method=='GET':
        return render(request, 'signin.html',{
            'form':AuthenticationForm
        })
    else: #si es un metodo POST se ejecuta esta parte
        user = authenticate(request, username=request.POST['username'], 
                     password=request.POST['password'])
        # el authenticate nos devuelve vacio si no se ha podido autenticar (usuario no existe)
        if user is None: #no se pudo encontrar al usuario o no fue validp
            return render(request, 'signin.html',{
            'form':AuthenticationForm,
            'error': 'Username or password is incorrect'
        })
        else:
            login(request,user)
            return redirect('tasks')


        
        

       

