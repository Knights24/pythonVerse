from django.shortcuts import redirect, render
from .models import Task
from .foms import TaskForm

# Create your views here.

def index(request):
    tasks = Task.objects.all()
    form = TaskForm()

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('/')
    
    context = {'task': tasks, 'form' : form}
    return render(request, 'index.html',context)

def delete_task(request, id):
    task = Task.objects.get(id=id)
    task.delete()
    return redirect('/')