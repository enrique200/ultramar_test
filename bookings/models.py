from django.db import models


class Port(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Booking(models.Model):
    booking_number = models.CharField(max_length=100, unique=True)
    loading_port = models.ForeignKey(Port, on_delete=models.CASCADE, related_name='loading_bookings')
    discharge_port = models.ForeignKey(Port, on_delete=models.CASCADE, related_name='discharge_bookings')
    ship_arrival_date = models.DateField()
    ship_departure_date = models.DateField()
    date_create = models.DateTimeField("Date Create", auto_now=False, auto_now_add=True)
    date_update = models.DateTimeField("Date Update", auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.booking_number


class Vehicle(models.Model):
    vin = models.CharField(max_length=100, unique=True)
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    weight = models.FloatField()
    booking = models.ForeignKey(Booking, related_name='vehicles', on_delete=models.CASCADE, null=True, blank=True)
    date_create = models.DateTimeField("Date Create", auto_now=False, auto_now_add=True)
    date_update = models.DateTimeField("Date Update", auto_now=True, auto_now_add=False)

    def __str__(self):
        return f"{self.make} {self.model} ({self.vin})"
