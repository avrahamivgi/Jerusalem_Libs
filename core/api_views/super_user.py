from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from django.core.exceptions import ObjectDoesNotExist 
from django.db.models import RestrictedError
from django.http import Http404


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
from core.models import Customer , Book , Rent




#funcs for the database:
#customer: (1)display (2)add (3)remove (4)update
#books: (1)display (2)add (3)remove (4)update
#rents: (1)display (2)add (3)remove

#customer funcs:

#CUSTOMER HANDLE
@api_view(["GET","POST","PUT","DELETE"])
def serve_customer(request):

    #diplaying all customers or one customer by id
    if request.method == "GET":
        cust_id = request.query_params.get("id",False) #"False" - if we dont get the query
    
        if not cust_id:
            customers = Customer.objects.all()
            serialzer = CustomerSerializer(instance=customers ,many=True)

        else:

            #validate that there is customer
            try:
                customer = Customer.objects.get(customer_id = cust_id)
            except ObjectDoesNotExist:
                return Response({"info":"no such customer"})
            
            serialzer = CustomerSerializer(instance=customer)

        return Response(serialzer.data)

    #adding a new customer
    if request.method== "POST":
        customer = CustomerSerializer(data = request.data)
        if customer.is_valid():
            try:
                # validate that its 9 digit number(this is hard to do in the regular validator)
                if len(request.data["customer_id"]) != 9 : 
                    raise ValueError("You Need To Provied 9 Digit Number!")
                customer.save()
            except IntegrityError:
                return Response({"info":"There Is Already Customer With This Id"},status=400)
            except ValueError as e:
                return Response({"error": str(e)}, status=400)
            
            return Response({"info":"customer created succsesfuly!", "data":request.data},status=200)

        else:
            return Response({"info":"error!","error": customer.errors} ,status=500)
    
    #changing the name or the age of the customer
    if request.method == "PUT":
        id_ = request.query_params.get("id",False)

        if not id_:
            return Response({"info":"You must specify the id of the customer"}, status=400)
        
        #validating the customer
        try:
            customer = Customer.objects.get(customer_id = id_)
        except ObjectDoesNotExist:
            return Response({"info":"your id not exist in the database"})
        
        serialzer = CustomerMiniSerializer(customer, data = request.data, partial = True)
        
        if serialzer.is_valid():
            updated_customer = serialzer.save()
            return Response({"info":"works. changes saved.","name":updated_customer.name,"age":updated_customer.age,"id":updated_customer.customer_id} )

        return Response({"info":"error!","error":serialzer.errors},status=400)

    #deleting the customer if he dont have any rents
    if request.method == "DELETE":
        id_ = request.query_params.get("id",False)

        if not id_:
            return Response({"info":"You must specify the id of the customer you want to delete"}, status=400)
        
        #validating the Customer
        try:
            customer = Customer.objects.get(customer_id = id_)
        except ObjectDoesNotExist:
            return Response({"info":"your customer id not exist in the database"})
        
        try:
            customer.delete()
        except RestrictedError:
            return Response({"info":"The Customer In Rent And Cant Be Deleted."})
        return Response({"info":"User Deleted Successfully"})























@api_view(["GET","POST","PUT","DELETE"])
def serve_book(request):

    #diplaying all books or one book by id
    if request.method == "GET":
        book_name = request.query_params.get("name",False) #"False" - if we dont get the query
    
        if not book_name:
            books = Book.objects.all()
            serialzer = BookSerializer(instance=books ,many = True)

        else:

            #validate that there is book that contain EVEN PART OF THE STRING
            try:
                book = Book.objects.get(name__icontains = book_name)
            except ObjectDoesNotExist:
                return Response({"info":"no such book"})
            
            serialzer = BookSerializer(instance=book)

        return Response(serialzer.data)

    #adding a new book ^
    if request.method== "POST":
        book = BookSerializer(data = request.data)
        if book.is_valid():
            book.save()
            return Response({"info":"book created succsesfuly!", "data":request.data},status=200)

        else:
            return Response({"info":"error!","error": book.errors} ,status=500)
    
    #changing the return period of the book !!just if the book not in rent..
    if request.method == "PUT":
        id_ = request.query_params.get("id",False) 

        if not id_:
            return Response({"info":"You must specify the id of the book"}, status=400)
        
        #validating the book
        try:
            book = Book.objects.get(id = id_)
        except ObjectDoesNotExist:
            return Response({"info":"your id not exist in the database"})
        
        #checking if the book is not in rent..
        res = Rent.objects.filter(book = id_)
        if res:
            return Response({"info":"The Book Is Rent. So He Cant Be Changed."},400)
        serialzer = BookMiniSerializer(book, data = request.data, partial = True)
        
        if serialzer.is_valid():
            new_book = serialzer.save()
            return Response({"info":"works. changes saved.","book_name":new_book.name,"author":new_book.author,"id":new_book.return_period} )

        return Response({"info":"error!","error":serialzer.errors},status=400)

    #deleting the book !!if he dont have any rents
    if request.method == "DELETE":
        id_ = request.query_params.get("id",False)

        if not id_:
            return Response({"info":"You must specify the id of the book you want to delete"}, status=400)
        
        #validating the book
        try:
            book = Book.objects.get(id = id_)
        except ObjectDoesNotExist:
            return Response({"info":"your book id not exist in the database"})
        try :
            book.delete()
        except RestrictedError:
            return Response({"info":"The Book In Rent And Cant Be Deleted."})
        
        return Response({"info":"Book Deleted Successfully"})














#For Practice I Request For User
@api_view(["GET","POST","PUT","DELETE"])
@authentication_classes([BasicAuthentication , TokenAuthentication])
@permission_classes([IsAuthenticated])
def serve_rent(request):

    #diplaying all rents or rents by customer id
    #there is opiton to show just the lated rents by specifing lated = True
    if request.method == "GET":
        #optional querys
        cust_id = request.query_params.get("id",False) 
        lated = request.query_params.get("lated",False)

        #check for query 'lated'
        if lated:
            serialzer = Rent.objects.filter(is_late = True)
            return Response({"info":"filter"},serialzer.date,status=200)
        #check for query 'cust_id'
        if not cust_id:
            rents = Rent.objects.all()
            serialzer = RentSerializer(instance=rents ,many = True)

        else:
            #validate that there is rent associated with a customer 
            rent = Rent.objects.filter(cust= cust_id)
            if not rent:
                return Response({"info":"no rents"})
            
            serialzer = RentSerializer(instance=rent , many = True)

        return Response(serialzer.data)

    #adding a new rent !!validate that the book is not already in use..
    if request.method== "POST":
        rent = RentSerializer(data = request.data)

        #Check if the book havent rented alerady
        if Rent.objects.filter(book = request.data["book"]):
            return Response({"info":"The Book Already Rented.. come in another time.."})
        
        if rent.is_valid():
        
            rent_start_date = rent.validated_data["return_start_date"] = datetime.datetime.now().date()
            
            #check what the period time of the book
            my_book = Book.objects.get(id=request.data["book"])
            if my_book.return_period == 1:
                rent.validated_data["return_end_date"] = rent_start_date + timedelta(days = 10)

            if my_book.return_period == 2:
                rent.validated_data["return_end_date"] = rent_start_date + timedelta(days = 20)

            if my_book.return_period == 3:
                rent.validated_data["return_end_date"] = rent_start_date + timedelta(days = 30)

            rent.save()
            return Response({"info":"rent created succsesfuly!", "data":request.data},status=200)

        else:
            return Response({"info":"error!","error": rent.errors} ,status=500)
    
    #sending error message for trying to edit
    if request.method == "PUT":
        return Response({"info":"error! you can't change rent. its immutable."},status=400)

    #deleting the rent
    if request.method == "DELETE":
        id_ = request.query_params.get("id",False)

        if not id_:
            return Response({"info":"You must specify the id of the rent you want to delete"}, status=400)
        
        #validating that the rent exist
        try:
            rent = Rent.objects.get(id = id_)
        except ObjectDoesNotExist:
            return Response({"info":"your id of the rent not exist in the database"})
        
        rent.delete()
        return Response({"info":"Rent Deleted Successfully"})



        



#lets make users!!!!!
#sign-up function
@api_view(["POST"])
def signup(request):
    try:
        
        age = request.data.get("age")
        user_id = request.data.get("user_id")
        username = request.data.get("username")
        password = request.data.get("password")
        email = request.data.get("email")

        user = User.objects.create_user(username=username , password=password, 
                                        email=email , user_id= user_id , age = age)
        token = Token.objects.create(user = user)
    except Exception as e :
        return Response({"info":"you have not provided all the details","error":e})
 

    return Response({"Token" : token.key , "info": f"new user created! id : {user.id}"})


#Defining the calls that can be made
@api_view(["GET"])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def private_call(request):

    return Response({"info":"Your Secret Key - @#FDgt#4h"})

#Basic YXZyYWhhbTowODkyMDI2ODQ=

@api_view(["GET"])
def handle_404(request):
    raise Http404()