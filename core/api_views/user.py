from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from django.core.exceptions import ObjectDoesNotExist 
from django.db.models import RestrictedError
from django.http import Http404
from django.shortcuts import get_object_or_404

from rest_framework.decorators import (api_view,
                                       authentication_classes,
                                       permission_classes)
from rest_framework.authentication import BasicAuthentication , TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.authtoken.models import Token
from datetime import timedelta , datetime

from core.serialzers import CustomerSerializer , CustomerMiniSerializer , BookSerializer ,BookMiniSerializer, RentSerializer , RentMiniSerializer
from core.models import Customer , Book , Rent , Library
from core.permissions import IsCustomer




#funcs for the database:
#customer: (1)display (2)add (3)remove (4)update
#books: (1)display (2)add (3)remove (4)update
#rents: (1)display (2)add (3)remove

#customer funcs:


@api_view(["GET"])
@authentication_classes([BasicAuthentication , TokenAuthentication])
@permission_classes([IsAuthenticated , IsCustomer])
def serve_book(request):

    #diplaying all books or books by name
    if request.method == "GET":
        book_name = request.query_params.get("name",False) #"False" - if we dont get the query
        all_libs_books = request.query_params.get("external",False)

        #multipy queris handeling
        if book_name and all_libs_books:
            return Response({"error":"you can enter only on query at a time"})

        #checking what the library of the user

        #customer
        customer= Customer.objects.get(user = request.user)


        #display all books by user library catalog
        if not book_name and not all_libs_books:
            books = Book.objects.filter(lib  = customer.lib)
            serialzer = BookSerializer(instance=books ,many = True)

        elif all_libs_books:
            books = Book.objects.all()
            serialzer = BookSerializer(instance=books ,many = True)
        else:

            #validate that there is book that contain EVEN PART OF THE STRING on all LIBS
            try:
                book = Book.objects.filter(name__icontains = book_name ,lib = customer.lib)
            except ObjectDoesNotExist:
                return Response({"info":"no such book"})
            
            serialzer = BookSerializer(instance=book , many = True)

        return Response(serialzer.data)

#checking his own rents(JUST SHOW)
@api_view(["GET"])
@authentication_classes([BasicAuthentication , TokenAuthentication])
@permission_classes([IsAuthenticated, IsCustomer])
def serve_rent(request):
    
    user = request.user

    #checking the rents of the user by his Token..
    try:
        rents = Rent.objects.filter(cust__user=user)
        serializer = RentSerializer(instance=rents, many=True)
    except Exception as e:            
        return Response({"info":e})
    return Response(serializer.data)

        

@api_view(["POST"])
@authentication_classes([BasicAuthentication , TokenAuthentication])
@permission_classes([IsAuthenticated , IsCustomer])
#changing his password
def change_password(request):

    user = request.user

    try:
        if request.data.get("password") == None:
            raise ValueError("please enter password")
        if len(request.data.get("password")) <= 3:
            raise ValueError("your password are too short..")
        user.set_password(request.data.get("password"))
        user.save()
    except ValueError as e:
        return Response({"error":f"{e}"})
    return Response({"info":"your password changed succesfuly!"})