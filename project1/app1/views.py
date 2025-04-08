from django.shortcuts import render, redirect
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import ToDo
from .serializer import ToDoSerializer


# Create your views here.
# @api_view(['GET','POST','PUT','DELETE'])
# def index(request):
#     if request.method == 'GET':
#         people_detail = {
#             'name': 'Ajay',
#             'age' : 27,
#             'job' : 'Developer'
#         }
#         return Response(people_detail)
#     elif request.method == 'POST':
#         return Response("This is a POST Method")
#     elif request.method == 'PUT':
#         return Response("This is a PUT Method")
#     else:
#         return Response("This is a DELETE Method")

def index(request):
    return render(request, 'index.html')


@api_view(['GET', 'POST'])
def todo_list_create(request):
    if request.method == 'GET':
        todos = ToDo.objects.all()
        serializer = ToDoSerializer(todos, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ToDoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def todo_detail(request, pk):
    try:
        todo = ToDo.objects.get(pk=pk)
    except ToDo.DoesNotExist:
        return Response({'error': 'To-Do item not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ToDoSerializer(todo)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ToDoSerializer(todo, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'PATCH': 
        serializer = ToDoSerializer(todo, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        todo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

def todo_detail_view(request, pk):
    try:
        todo = ToDo.objects.get(pk=pk)
    except ToDo.DoesNotExist:
        return HttpResponse('To-Do not found', status=404)

    if request.method == 'POST' and 'update_status' in request.POST:
        todo.completed = not todo.completed
        todo.save()
        return redirect('todo_detail_view', pk=pk)

    return render(request, 'todo_detail.html', {'todo': todo})

