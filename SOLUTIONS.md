# ------------------- Project Logistics_ultramar ------------------- 

This document outlines the technical solutions and decisions made during the development of the logistics application for managing bookings and vehicles. The application includes functionalities such as user authentication, CRUD operations on bookings, export/import of booking data to/from XLS files, and a REST API.

# Models

- **Booking**: Stores details about bookings including a unique booking number, ports, and ship dates.
- **Vehicle**: Linked to bookings with details like VIN, make, model, and weight.
- **Port**: Stores information about ports which are used in the booking details.

### User Authentication

- Implemented using Django's built-in authentication system to ensure that all pages are accessible only to authenticated users.

### SITE GENERAL

- Built using Django Rest Framework (DRF).
- Endpoints for `Booking` and `Vehicle` models allowing CRUD operations.

### Import/Export Functionality

- Implemented file upload functionality to import booking details from an XLS file using pandas.
- Integrated `django-import-export` for admin actions to easily import and export data directly from the Django admin interface.
- Date Handling: Faced issues with date formats during import/export. Resolved by enforcing strict date formats using `pandas` during import and careful data handling in export.
- File Validation: Ensured robust server-side validation to handle incorrect file formats and missing columns in the uploaded files.
- 
### Middleware

- Developed command to automatically delete vehicles linked to bookings older than six months.

### Frontend

- Used Bootstrap 5 to style the frontend.
- JavaScript 

## Details

I have added date_created and date_update fields in the models
I add select ports in form add and edit bookings

## Conclusion

I have made the entire site protected by user. Created different html for the CRUD of bookings and associating/disassociating vehicles.
Use of Modal to confirm the deletion of bookings
