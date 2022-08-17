from django.shortcuts import render , redirect
from django.db.models import Q
from django.http import HttpResponse
from django.contrib import messages # For using error messages.
from django.contrib.auth.decorators import login_required
from .models import Room , Topic , Message, User
# from django.contrib.auth.forms import UserCreationForm #For creating form to create user.
from django.contrib.auth import authenticate , login , logout # This module is for login and logout function.
from .form import RoomForm , Userform , MyUserCreationForm

# Create your views here.
# rooms = [
#     {"id": 1 , "name" : "Let's code!" },
#     {"id": 2 , "name" : "Fun day with Python" },
#     {"id": 3 , "name" : "Working with JavaScript" },
# ]

def loginpage(request):
    page = 'login'
    if request.method == "POST":
        username = request.POST.get('username') # request.POST.get- Gets the username and pass from the form of login.html.
        password = request.POST['password']

        user = authenticate(request , username = username, password = password) # This cjecks the credentials

        if user is not None: # If not authenticate user = none but if authenticate;
            login(request, user)
            return redirect('home')

        elif user is None:
            messages.error(request , 'Email or Password is incorrect')


    content = {'page' : page}
    return render(request , 'base/login_register.html' , content)


def logoutpage(request):
    logout(request)
    return redirect('home')

# def signup(request):
#     if request.method == "POST":
#         first_name= request.POST['first_name']
#         last_name= request.POST['last_name']
#         email= request.POST['email']
#         password= request.POST['password']
#         user = User.objects.create_user(first_name,email,password)
#         user.save()
#     return render(request, 'base/register.html')

def registerpage(request):
    form = MyUserCreationForm()
    if request.method == "POST":
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit = False)

            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration')
    return render(request, 'base/login_register.html' , {'form' : form})


def home(request):
    if request.method == "GET":
        q = request.GET.get('q','') # This gets the date from the request which has name 'q'.
        rooms = Room.objects.filter(topic__name__icontains = q) # This filter room to be rendered using.filter(topic__name__icontains=q)
        room_message = Message.objects.filter(room__topic__name__icontains = q) # This filter room to be rendered using.filter(topic__name__icontains=q)
    if request.method == "POST":
        q = request.POST.get('q')
        rooms = Room.objects.filter(name__icontains = q)
    topics = Topic.objects.all()[0:4]
    room_count = Room.objects.all().count

    content = {"rooms" : rooms , "topics" : topics, "room_count" : room_count , 'room_message':room_message,}
    return render(request , "base/home.html" , content)

def room(request , pk):
    rooms = Room.objects.get(id=pk)
    room_messages = rooms.message_set.all().order_by('-created') # Reverse the database relation.
    participants = rooms.participants.all()

    if request.method == 'POST':
        message = Message.objects.create(user=request.user, room=rooms , body=request.POST['body'])
        rooms.participants.add(request.user) # Many to many relation add.
        return redirect('room' , pk=rooms.id)
    return render(request , "base/room.html" , {"room" : rooms,
    'room_message' : room_messages, 'participants' : participants} )

def profile_page(request,pk):
    user = User.objects.get(id=pk)
    rooms = Room.objects.filter(host = user)
    topics = Topic.objects.all()
    user_messages = Message.objects.filter(user =user)
    content = {'users' : user, 'rooms' : rooms, 'topics' : topics , 'room_message' : user_messages,}
    return render(request, 'base/profile.html' , content)

@login_required(login_url='login')
def createroom(request):
    form  = RoomForm
    topics = Topic.objects.all()
    if request.method == "POST":
        topic_name  = request.POST.get('topic')
        topic , created = Topic.objects.get_or_create(name=topic_name)

        Room.objects.create(
            host = request.user,
            topic = topic ,
            name = request.POST.get('name'),
            description = request.POST.get('description'),
        )
        return redirect("home")

    content = {"form" : form , 'topics' : topics,}
    return render(request , "base/room_form.html" , content)

def editroom(request , pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room) # This prefills the RoomForm class with room data 

    if request.user != room.host:
        return HttpResponse(f"This room can be only edited by {room.host}." )

    if request.method == "POST":
        topic_name  = request.POST.get('topic')
        topic , created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.description = request.POST.get('description')
        room.topic = topic
        room.save()
        return redirect("home")

    content = {"form" : form , 'room' : room,}
    return render(request , "base/room_form.html" , content)

@login_required(login_url='login')
def deleteroom(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
      return HttpResponse(f"This room can be only deleted by {room.host}." )

    if request.method == "POST":
        room.delete()
        return redirect("home")

    content = {"obj" : room}
    return render(request , "base/delete.html" , content)


@login_required(login_url='login')
def deleteMessage(request, pk):
    room_message = Message.objects.get(id=pk)

    if request.user != room_message.user:
      return HttpResponse(f"This message can be only deleted by {room_message.user}." )

    if request.method == "POST":
        room_message.delete()
        return redirect("home")

    content = {"obj" : room_message}
    return render(request , "base/delete.html" , content)

@login_required(login_url='login')
def editUser(request):
    user = request.user
    form = Userform(instance=user)
    if request.method == "POST":
        form = Userform(request.POST, request.FILES ,instance=user )
        if form.is_valid():
            form.save()
            return redirect('profilepage' , pk=user.id)
    content = {'form' : form}
    return render(request, 'base/edit-user.html', content )


def topicspage(request):
    q = request.GET.get('q','')
    topics = Topic.objects.filter(name__icontains=q)
    content = {'topics':topics}
    return render(request, 'base/topics.html' , content)

def activitypage(request):
    room_messages = Message.objects.all()
    content = {'room_messages':room_messages}
    return render(request, 'base/activity.html' , content)