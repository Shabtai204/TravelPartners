from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from .models import Trip, Type, Message, User
from .forms import TripForm, UserForm, myUserCreationForm


def login_page(request):
    page = 'login'
    # User cannot get in login page if he is already authenticated
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or Password does not exist')

    context = {'page': page}
    return render(request, 'core/login_register.html', context)


def logout_user(request):
    logout(request)
    return redirect('home')


def register_page(request):
    form = myUserCreationForm()

    if request.method == 'POST':
        form = myUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration!')
    return render(request, 'core/login_register.html', {'form': form})


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    trips = Trip.objects.filter(
        Q(type__name__icontains=q) |
        Q(title__icontains=q) |
        Q(description__icontains=q)
    )
    types = Type.objects.all()[0:5]
    trip_count = trips.count()
    trip_messages = Message.objects.filter(Q(trip__type__name__icontains=q))

    context = {'trips': trips, 'types': types,
               'trip_count': trip_count, 'trip_messages': trip_messages}
    return render(request, 'core/home.html', context)


def trip(request, trip_slug):
    trip = Trip.objects.get(slug=trip_slug)
    trip_messages = trip.message_set.all()
    participants = trip.participants.all()

    if request.method == 'POST':
        messages = Message.objects.create(
            user=request.user,
            trip=trip,
            body=request.POST.get('body')
        )
        trip.participants.add(request.user)
        return redirect('trip', trip_slug=trip_slug)

    context = {'trip': trip, 'trip_messages': trip_messages,
               'participants': participants}
    return render(request, 'core/trip.html', context)


def user_profile(request, profile_slug):
    user = User.objects.get(slug=profile_slug)
    trips = user.trip_set.all()
    trip_messages = user.message_set.all()
    types = Type.objects.all()
    context = {'user': user, 'trips': trips,
               'trip_messages': trip_messages, 'types': types}
    return render(request, 'core/profile.html', context)


@login_required(login_url="login")
def update_user(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', profile_slug=user.slug)

    return render(request, 'core/update_user.html', {'form': form})


@login_required(login_url="login")
def create_trip(request):
    form = TripForm()
    types = Type.objects.all()

    if request.method == 'POST':
        type_name = request.POST.get('type')
        type, created = Type.objects.get_or_create(name=type_name)

        Trip.objects.create(
            host=request.user,
            title=request.POST.get('title'),
            type=type,
            start_loc=request.POST.get('start_loc'),
            end_loc=request.POST.get('end_loc'),
            start_date=request.POST.get('start_date'),
            end_date=request.POST.get('end_date'),
            description=request.POST.get('description')
        )
        return redirect('home')

    context = {'form': form, 'types': types, 'trip': trip}
    return render(request, 'core/trip_form.html', context)


@login_required(login_url="login")
def update_trip(request, trip_slug):
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    print(trip_slug)
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    trip = Trip.objects.get(slug=trip_slug)
    form = TripForm(instance=trip)
    types = Type.objects.all()

    if request.user != trip.host:
        return HttpResponse('You are not allowed!')

    if request.method == 'POST':
        trip.title = request.POST.get('title')
        type_name = request.POST.get('type')
        type, created = Type.objects.get_or_create(name=type_name)
        trip.type = type
        trip.start_loc = request.POST.get('start_loc')
        trip.end_loc = request.POST.get('end_loc')
        trip.start_date = request.POST.get('start_date')
        trip.end_date = request.POST.get('end_date')
        trip.description = request.POST.get('description')
        trip.save()
        return redirect('home')
    context = {'form': form, 'types': types}
    return render(request, 'core/trip_form.html', context)


@login_required(login_url="login")
def delete_trip(request, trip_slug):
    trip = Trip.objects.get(slug=trip_slug)

    if request.user != trip.host:
        return HttpResponse('You are not allowed!')

    if request.method == 'POST':
        trip.delete()
        return redirect('home')
    return render(request, 'core/delete.html', {'obj': trip})


@login_required(login_url="login")
def delete_message(request, msg_slug):
    message = Message.objects.get(slug=msg_slug)

    if request.user != message.user:
        return HttpResponse('You are not allowed!')

    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request, 'core/delete.html', {'obj': message})


def types_page(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    types = Type.objects.filter(name__icontains=q)
    return render(request, 'core/types.html', {'types': types})


def activity_page(request):
    trip_messages = Message.objects.all()
    return render(request, 'core/activity.html', {'trip_messages': trip_messages})
