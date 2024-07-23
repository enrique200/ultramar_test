from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookingViewSet, VehicleViewSet, BookingListView, BookingCreateView, BookingUpdateView, BookingDeleteView, export_bookings_to_xls, import_bookings_from_xls, associate_vehicle, disassociate_vehicle

router = DefaultRouter()
router.register(r'bookings', BookingViewSet)
router.register(r'vehicles', VehicleViewSet)

urlpatterns = [
    path('', BookingListView.as_view(), name='booking_list'),
    path('new/', BookingCreateView.as_view(), name='booking_new'),
    path('edit/<int:pk>/', BookingUpdateView.as_view(), name='booking_edit'),
    path('delete/<int:pk>/', BookingDeleteView.as_view(), name='booking_delete'),
    path('export-xls/', export_bookings_to_xls, name='export_bookings_to_xls'),
    path('import-xls/', import_bookings_from_xls, name='import_bookings_from_xls'),
    path('booking/<int:booking_id>/associate_vehicle/<int:vehicle_id>/', associate_vehicle, name='associate_vehicle'),
    path('booking/<int:booking_id>/disassociate_vehicle/<int:vehicle_id>/', disassociate_vehicle, name='disassociate_vehicle'),
]