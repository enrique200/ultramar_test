from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Port, Booking, Vehicle

class BookingAdmin(ImportExportModelAdmin):
    list_display = ('booking_number', 'loading_port', 'discharge_port', 'ship_arrival_date', 'ship_departure_date')
    pass

admin.site.register(Booking, BookingAdmin)
admin.site.register(Port)
admin.site.register(Vehicle)