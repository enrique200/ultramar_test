from django import forms
from .models import Booking, Port

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['booking_number', 'loading_port', 'discharge_port', 'ship_arrival_date', 'ship_departure_date']
        widgets = {
            'ship_arrival_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'ship_departure_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'booking_number': forms.TextInput(attrs={'class': 'form-control'}),
        }

    loading_port = forms.ModelChoiceField(queryset=Port.objects.all(), empty_label=None, widget=forms.Select(attrs={'class': 'form-control'}))
    discharge_port = forms.ModelChoiceField(queryset=Port.objects.all(), empty_label=None, widget=forms.Select(attrs={'class': 'form-control'}))