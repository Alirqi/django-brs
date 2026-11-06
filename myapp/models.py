from django.db import models


class Bus(models.Model):
    bus_name = models.CharField(max_length=30)
    source = models.CharField(max_length=30)
    dest = models.CharField(max_length=30)
    nos = models.PositiveIntegerField()
    rem = models.PositiveIntegerField()
    price = models.DecimalField(decimal_places=2, max_digits=8)
    date = models.DateField()
    time = models.TimeField()

    class Meta:
        verbose_name_plural = "List of Buses"
        ordering = ["date", "time"]

    def __str__(self):
        return self.bus_name


class User(models.Model):
    """Legacy profile model retained for compatibility; Django auth handles passwords."""
    user_id = models.AutoField(primary_key=True)
    email = models.EmailField()
    name = models.CharField(max_length=30)
    password = models.CharField(max_length=128)

    class Meta:
        verbose_name_plural = "List of Users"

    def __str__(self):
        return self.email


class Book(models.Model):
    BOOKED = "B"
    CANCELLED = "C"
    TICKET_STATUSES = (
        (BOOKED, "Booked"),
        (CANCELLED, "Cancelled"),
    )

    email = models.EmailField()
    name = models.CharField(max_length=30)
    userid = models.PositiveIntegerField(db_index=True)
    busid = models.PositiveIntegerField(db_index=True)
    bus_name = models.CharField(max_length=30)
    source = models.CharField(max_length=30)
    dest = models.CharField(max_length=30)
    nos = models.PositiveIntegerField()
    price = models.DecimalField(decimal_places=2, max_digits=8)
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(
        choices=TICKET_STATUSES,
        default=BOOKED,
        max_length=2,
    )

    class Meta:
        verbose_name_plural = "List of Bookings"
        ordering = ["-date", "-time"]

    def __str__(self):
        return f"{self.email} - {self.bus_name} ({self.get_status_display()})"
