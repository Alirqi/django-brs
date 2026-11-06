from datetime import datetime
from decimal import Decimal, InvalidOperation

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render

from .models import Book, Bus


def home(request):
    if request.user.is_authenticated:
        return render(request, "myapp/home.html")
    return redirect("signin")


@login_required(login_url="signin")
def findbus(request):
    if request.method != "POST":
        return render(request, "myapp/findbus.html")

    source = (request.POST.get("source") or "").strip()
    destination = (request.POST.get("destination") or "").strip()
    date_value = request.POST.get("date") or ""

    try:
        travel_date = datetime.strptime(date_value, "%Y-%m-%d").date()
    except ValueError:
        return render(request, "myapp/findbus.html", {
            "data": request.POST,
            "error": "Please enter a valid travel date.",
        })

    bus_list = Bus.objects.filter(
        source__iexact=source,
        dest__iexact=destination,
        date=travel_date,
        rem__gt=0,
    ).order_by("time")

    if bus_list.exists():
        return render(request, "myapp/list.html", {
            "bus_list": bus_list,
            "source_r": source,
            "dest_r": destination,
            "date_r": travel_date,
        })

    return render(request, "myapp/findbus.html", {
        "data": request.POST,
        "error": "No available bus schedule for the selected route and date.",
    })


@login_required(login_url="signin")
def bookings(request):
    if request.method != "POST":
        return redirect("findbus")

    try:
        bus_id = int(request.POST.get("bus_id", ""))
        seats = int(request.POST.get("no_seats", ""))
    except (TypeError, ValueError):
        return render(request, "myapp/error.html", {
            "error": "Please select a valid bus and number of seats.",
        })

    if seats < 1:
        return render(request, "myapp/error.html", {
            "error": "The number of seats must be at least one.",
        })

    with transaction.atomic():
        bus = get_object_or_404(Bus.objects.select_for_update(), pk=bus_id)
        if seats > bus.rem:
            return render(request, "myapp/findbus.html", {
                "error": "Not enough seats are available. Please choose fewer seats.",
            })

        bus.rem -= seats
        bus.save(update_fields=["rem"])

        total_cost = Decimal(seats) * bus.price
        booking = Book.objects.create(
            name=request.user.username,
            email=request.user.email,
            userid=request.user.pk,
            busid=bus.pk,
            bus_name=bus.bus_name,
            source=bus.source,
            dest=bus.dest,
            nos=seats,
            price=total_cost,
            date=bus.date,
            time=bus.time,
            status=Book.BOOKED,
        )

    return render(request, "myapp/bookings.html", {
        "book": booking,
        "bus": bus,
        "name_r": bus.bus_name,
        "source_r": bus.source,
        "dest_r": bus.dest,
        "nos_r": seats,
        "price_r": total_cost,
        "date_r": bus.date,
        "time_r": bus.time,
    })


@login_required(login_url="signin")
def cancellings(request):
    if request.method != "POST":
        return redirect("seebookings")

    try:
        booking_id = int(request.POST.get("bus_id", ""))
    except (TypeError, ValueError):
        return render(request, "myapp/error.html", {
            "error": "Please select a valid booking.",
        })

    with transaction.atomic():
        booking = get_object_or_404(
            Book.objects.select_for_update(),
            pk=booking_id,
            userid=request.user.pk,
        )

        if booking.status == Book.CANCELLED:
            messages.info(request, "This booking has already been cancelled.")
            return redirect("seebookings")

        bus = get_object_or_404(Bus.objects.select_for_update(), pk=booking.busid)
        bus.rem = min(bus.nos, bus.rem + booking.nos)
        bus.save(update_fields=["rem"])

        booking.status = Book.CANCELLED
        booking.save(update_fields=["status"])

    messages.success(request, "Your booking has been cancelled successfully.")
    return redirect("seebookings")


@login_required(login_url="signin")
def seebookings(request, new=None):
    book_list = Book.objects.filter(userid=request.user.pk).order_by("-date", "-time")
    return render(request, "myapp/booklist.html", {"book_list": book_list})


def signup(request):
    if request.method != "POST":
        return render(request, "myapp/signup.html")

    username = (request.POST.get("name") or "").strip()
    email = (request.POST.get("email") or "").strip()
    password = request.POST.get("password") or ""

    if not username or not email or not password:
        return render(request, "myapp/signup.html", {
            "error": "Please complete all fields.",
        })
    if User.objects.filter(username=username).exists():
        return render(request, "myapp/signup.html", {
            "error": "This username is already registered.",
        })
    if User.objects.filter(email__iexact=email).exists():
        return render(request, "myapp/signup.html", {
            "error": "This email is already registered.",
        })

    user = User.objects.create_user(username=username, email=email, password=password)
    login(request, user)
    return render(request, "myapp/thank.html")


def signin(request):
    if request.method != "POST":
        return render(request, "myapp/signin.html")

    username = (request.POST.get("name") or "").strip()
    password = request.POST.get("password") or ""
    user = authenticate(request, username=username, password=password)

    if user is None:
        return render(request, "myapp/signin.html", {
            "error": "Invalid username or password.",
        })

    login(request, user)
    return redirect("success")


@login_required(login_url="signin")
def signout(request):
    if request.method != "POST":
        return redirect("home")
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect("signin")


@login_required(login_url="signin")
def success(request):
    return render(request, "myapp/success.html", {"user": request.user})
