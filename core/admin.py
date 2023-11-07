from django.contrib import admin

from .models import  Manager,Worker, Customer , Book , Rent ,Library


# Register your models here.
admin.site.register(Library)
admin.site.register(Customer)
admin.site.register(Book)
admin.site.register(Manager)
admin.site.register(Worker)



#If You Want To Make Rents You Must SPECIFY The Start Date
#And The Return Date Explicity Because That The Auto Date
#Procces Is In The api_view.py - And The Admin Not Use It
admin.site.register(Rent)
