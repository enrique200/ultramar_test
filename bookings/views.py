import pandas as pd
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.http import HttpResponse
from rest_framework import viewsets
from .models import Booking, Vehicle
from .serializers import BookingSerializer, VehicleSerializer
from .forms import BookingForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.permissions import IsAuthenticated

@login_required
class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

@login_required
class VehicleViewSet(viewsets.ModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    permission_classes = [IsAuthenticated]

class BookingListView(LoginRequiredMixin, ListView):
    model = Booking
    context_object_name = 'bookings'

class BookingCreateView(LoginRequiredMixin, CreateView):
    model = Booking
    form_class = BookingForm
    template_name = 'bookings/booking_form.html'
    success_url = reverse_lazy('booking_list')

class BookingUpdateView(LoginRequiredMixin, UpdateView):
    model = Booking
    form_class = BookingForm
    template_name = 'bookings/booking_form.html'
    success_url = reverse_lazy('booking_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Supongamos que quieres excluir los vehículos ya asignados a la reserva actual
        context['other_vehicles'] = Vehicle.objects.exclude(booking=self.object)
        return context

class BookingDeleteView(LoginRequiredMixin, DeleteView):
    model = Booking
    context_object_name = 'booking'
    success_url = reverse_lazy('booking_list')

def export_bookings_to_xls(request):
    bookings = Booking.objects.all()
    df = pd.DataFrame(list(bookings.values()))

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="bookings.xls"'

    with pd.ExcelWriter(response) as writer:
        df.to_excel(writer, index=False)

    return response

def export_bookings_to_xls(request):
    bookings = Booking.objects.all()
    df = pd.DataFrame(list(bookings.values()))

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="bookings.xls"'

    with pd.ExcelWriter(response) as writer:
        df.to_excel(writer, index=False)

    return response


def import_bookings_from_xls(request):
    if request.method == 'POST':
        excel_file = request.FILES.get('excel_file')

        if not excel_file:
            messages.error(request, "No file was selected.")
            return render(request, 'bookings/importxls.html')

        try:
            df = pd.read_excel(excel_file)
        except Exception as e:
            messages.error(request, f"Error reading the Excel file: {str(e)}")
            return render(request, 'bookings/importxls.html')

        required_columns = {'booking_number', 'loading_port', 'discharge_port', 'ship_arrival_date',
                            'ship_departure_date'}
        if not required_columns.issubset(df.columns):
            missing_cols = required_columns - set(df.columns)
            messages.error(request, f"Missing columns in Excel file: {', '.join(missing_cols)}")
            return render(request, 'bookings/importxls.html')

        # Procesa cada fila del DataFrame
        for index, row in df.iterrows():
            try:
                _, created = Booking.objects.update_or_create(
                    booking_number=row['booking_number'],
                    defaults={
                        'loading_port': row['loading_port'],
                        'discharge_port': row['discharge_port'],
                        'ship_arrival_date': pd.to_datetime(row['ship_arrival_date']),
                        'ship_departure_date': pd.to_datetime(row['ship_departure_date'])
                    }
                )
            except Exception as e:
                messages.error(request, f"Error processing row {index + 1}: {str(e)}")
                return render(request, 'bookings/importxls.html')

        messages.success(request, "Bookings imported successfully")
        return redirect('booking_list')
    return render(request, 'bookings/importxls.html')

@login_required
def associate_vehicle(request, booking_id, vehicle_id):
    booking = get_object_or_404(Booking, id=booking_id)
    vehicle = get_object_or_404(Vehicle, id=vehicle_id)
    vehicle.booking = booking
    vehicle.save()
    messages.success(request, "Vehicle associated successfully.")
    return redirect('booking_edit', pk=booking_id)

@login_required
def disassociate_vehicle(request, booking_id, vehicle_id):
    vehicle = get_object_or_404(Vehicle, id=vehicle_id)
    vehicle.booking = None
    vehicle.save()
    messages.success(request, "Vehicle disassociated successfully.")
    return redirect('booking_edit', pk=booking_id)