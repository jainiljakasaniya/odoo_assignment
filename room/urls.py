from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search/<filter>/<slot>/<token>", views.search_booking, name="search"),
    path(
        "room-page/<date>/<selected_room>/<slot_start>/<token>",
        views.room_page,
        name="room",
    ),
    path("day_select/<day>/<selected_room>/<token>", views.day_select, name="room"),
]
