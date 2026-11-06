from datetime import date, time
from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Book, Bus


class BusReservationFlowTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="rider",
            email="rider@example.com",
            password="Strong-test-pass-123",
        )
        self.bus = Bus.objects.create(
            bus_name="Test Bus",
            source="Taiz",
            dest="Sanaa",
            nos=10,
            rem=10,
            price=Decimal("12.50"),
            date=date(2030, 5, 20),
            time=time(9, 30),
        )
        self.client.force_login(self.user)

    def test_search_returns_matching_available_bus(self):
        response = self.client.post(reverse("findbus"), {
            "source": "Taiz",
            "destination": "Sanaa",
            "date": "2030-05-20",
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Bus")

    def test_booking_reduces_available_seats_and_saves_total(self):
        response = self.client.post(reverse("bookings"), {
            "bus_id": self.bus.pk,
            "no_seats": "3",
        })
        self.assertEqual(response.status_code, 200)
        self.bus.refresh_from_db()
        booking = Book.objects.get()
        self.assertEqual(self.bus.rem, 7)
        self.assertEqual(booking.nos, 3)
        self.assertEqual(booking.price, Decimal("37.50"))
        self.assertEqual(booking.userid, self.user.pk)

    def test_booking_rejects_more_seats_than_available(self):
        response = self.client.post(reverse("bookings"), {
            "bus_id": self.bus.pk,
            "no_seats": "11",
        })
        self.assertEqual(response.status_code, 200)
        self.bus.refresh_from_db()
        self.assertEqual(self.bus.rem, 10)
        self.assertEqual(Book.objects.count(), 0)

    def test_cancellation_restores_seats_only_once(self):
        booking = Book.objects.create(
            email=self.user.email,
            name=self.user.username,
            userid=self.user.pk,
            busid=self.bus.pk,
            bus_name=self.bus.bus_name,
            source=self.bus.source,
            dest=self.bus.dest,
            nos=2,
            price=Decimal("25.00"),
            date=self.bus.date,
            time=self.bus.time,
            status=Book.BOOKED,
        )
        self.bus.rem = 8
        self.bus.save(update_fields=["rem"])

        response = self.client.post(reverse("cancellings"), {"bus_id": booking.pk})
        self.assertRedirects(response, reverse("seebookings"))
        self.bus.refresh_from_db()
        booking.refresh_from_db()
        self.assertEqual(self.bus.rem, 10)
        self.assertEqual(booking.status, Book.CANCELLED)

        self.client.post(reverse("cancellings"), {"bus_id": booking.pk})
        self.bus.refresh_from_db()
        self.assertEqual(self.bus.rem, 10)

    def test_user_cannot_cancel_another_users_booking(self):
        other = User.objects.create_user(
            username="other",
            email="other@example.com",
            password="Another-strong-pass-123",
        )
        booking = Book.objects.create(
            email=other.email,
            name=other.username,
            userid=other.pk,
            busid=self.bus.pk,
            bus_name=self.bus.bus_name,
            source=self.bus.source,
            dest=self.bus.dest,
            nos=1,
            price=Decimal("12.50"),
            date=self.bus.date,
            time=self.bus.time,
            status=Book.BOOKED,
        )
        response = self.client.post(reverse("cancellings"), {"bus_id": booking.pk})
        self.assertEqual(response.status_code, 404)
        self.bus.refresh_from_db()
        self.assertEqual(self.bus.rem, 10)
