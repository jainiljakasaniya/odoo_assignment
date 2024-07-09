from django.shortcuts import render, HttpResponse, redirect
from .models import Sessions, Rooms, Tags, Booking
from datetime import datetime, timedelta, timezone
import jwt

SECRET_KEY = "RoomBooking12345678"

def is_valid(token):
    try:
        token_obj = jwt.decode(str(token).encode(), SECRET_KEY, ["HS256"])
        expiration_time = datetime.fromtimestamp(token_obj["exp"], tz=timezone.utc)
        return expiration_time >= datetime.now(tz=timezone.utc)
    except:
        return False

def index(request):
    # return HttpResponse('Jainil')
    if request.method == "POST":
        name = request.POST["name"]
        session = Sessions()
        now = datetime.now()
        session.name = name
        session.start = now
        session.end = now + timedelta(minutes=30)
        session.save()
        curr_session=Sessions.objects.get(start=session.start)
        data = {
            "id": session.id,
            "name": name,
            "exp": (datetime.now() + timedelta(minutes=30)).timestamp(),
        }
        encoded_jwt = jwt.encode(data, SECRET_KEY, algorithm="HS256")
        rooms = Rooms.objects.all()
        bookings = Booking.objects.all()
        context = {"rooms": rooms, "bookings": '', "token": str(encoded_jwt),"selected_room":-1,"day":0}
        return render(request, "index.html", context=context)
    return render(request, "login.html")

def room_page(request, date, selected_room, slot_start, token):
    # if request.method == "POST":
    #     room, date, slot_start, token = (
    #         request.POST["room"],
    #         request.POST["date"],
    #         request.POST["slot_start"],
    #         request.POST["auth_token"],
    #     )
    if is_valid(token):
        # print(int(selected_room))
        time_obj = datetime.strptime(slot_start, '%H:%M')
        delta = timedelta(minutes=30)
        new_time_obj = time_obj + delta
        slot_end = new_time_obj.strftime('%H:%M')
        booking = Booking()
        token_obj = jwt.decode(str(token).encode(), SECRET_KEY, ["HS256"])
        booking.date = date
        booking.start_time = slot_start
        booking.end_time = slot_end
        room=Rooms.objects.get(id=int(selected_room)+1)
        print(token_obj, type(token_obj['id']))
        session=Sessions.objects.get(id=token_obj['id'])
        booking.session_id = session
        booking.room_id = room
        print(booking)
        booking.save()
        rooms = Rooms.objects.all()
        bookings = Booking.objects.all()
        context = {"rooms": rooms, "bookings": '', "token": token,"selected_room":-1, "day":date}
        return render(request, "index.html", context=context)
    else:
        return render(request, "login.html")

def search_booking(request, filter, token):
    if is_valid(token):
        rooms = Rooms.objects.filter(name__icontains=filter).all()
        bookings = []
        for room in rooms:
            booking_indi = Booking.objects.filter(room_id=room.id).all()
            bookings.extend(booking_indi)
        context = {"rooms": rooms, "bookings": '', "token": token,"selected_room":-1,"day":0}
        return render(request, "index.html", context=context)
    else:
        return render(request, "login.html")

def day_select(request,day,selected_room,token):
    if is_valid(token):
        rooms = Rooms.objects.all()
        # bookings = []
        # for room in rooms:
        #     booking_indi = Booking.objects.filter(room_id=room.id).all()
        #     bookings.extend(booking_indi)
        bookings = Booking.objects.filter(room_id=int(selected_room)+1,date=day)
        # print(bookings[])
        bookings_list = [booking.start_time for booking in bookings]
        print(bookings_list)
        context = {"rooms": rooms, "bookings": bookings_list, "token": token,"selected_room":int(selected_room),"day":day}
        print(context)
        return render(request, "index.html", context=context)
    else:
        return render(request, "login.html")
## hmo@odoo.com