from django.contrib.auth.models import User
from django.db.utils import IntegrityError 
from django.core.exceptions import ObjectDoesNotExist , ValidationError
from django.db.models import RestrictedError
from django.http import Http404


from rest_framework.decorators import (api_view,
                                       authentication_classes,
                                       permission_classes)
from rest_framework.authentication import BasicAuthentication , TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from datetime import timedelta , datetime

from core.serialzers import CustomerSerializer , CustomerMiniSerializer , BookSerializer ,BookMiniSerializer, RentSerializer , RentMiniSerializer ,UserSerializer
from core.models import Customer , Book , Rent,Worker
from core.permissions import IsLibraryWorker




#funcs for the database:
#customer: (1)display (2)add (3)remove (4)update
#books: (1)display (2)add (3)remove (4)update
#rents: (1)display (2)add (3)remove

#customer funcs:

#CUSTOMER HANDLE
@api_view(["GET","POST","PUT","DELETE"])
@authentication_classes([BasicAuthentication , TokenAuthentication])
@permission_classes([IsAuthenticated,IsLibraryWorker])
def serve_customer(request):

    #diplaying all customers or one customer by id
    if request.method == "GET":
        cust_id = request.query_params.get("id",False) #"False" - if we dont get the query
        worker = Worker.objects.get(user = request.user)

        if  not cust_id or cust_id == "null":
            customers = Customer.objects.filter(lib = worker.lib.id)
            serialzer = CustomerSerializer(instance=customers ,many=True)
        else:
            #validate that there is customer
            try:
                customer = Customer.objects.get(customer_id = cust_id)
            except ObjectDoesNotExist:
                return Response({"info":"no such customer"})
            
            serialzer = CustomerSerializer(instance=customer )

            return Response([serialzer.data])

        return Response(serialzer.data)

    #adding a new customer ONLY TO THEIR LIB!
    if request.method== "POST":
        print(f"\n\n\n{request.data}\n\n\n")
        
        # import IPython; IPython.embed()
        customer = CustomerSerializer(data=request.data)
        if customer.is_valid():
            try:
                # validate that its 9 digit number(this is hard to do in the regular validator)
                if len(request.data["customer_id"]) != 9 : 
                    raise ValueError("You Need To Provied 9 Digit Number!")

                #validate that the lib of the customer is the lib of the worker:
                
                if request.data["lib"] != str(request.user.worker.lib.id):
                    raise ValueError("You not allowed to add customer to another lib..")
                
                customer.save()
            except IntegrityError as e:
                return Response({"info":"There Is Already Customer With This Id", "error":{str(e)}},status=400)
            except ValueError as e:
                return Response({"error": str(e)}, status=400)

            return Response({"info":"customer created succsesfuly!"},status=200)

        else:
            return Response({"error": customer.errors} ,status=500)
    


    #deleting the customer if he dont have any rents
    if request.method == "DELETE":
        id_ = request.query_params.get("id",False)

        if not id_:
            return Response({"info":"You must specify the id of the customer you want to delete"}, status=400)
        
        #validating the Customer
        try:
            customer = Customer.objects.get(customer_id = id_)
            #validate that the lib of the customer is the lib of the worker:
            if User.objects.get(customer= id_).customer.lib.id != request.user.worker.lib.id:
               raise ValueError(f"You not allowed to delete customer from another lib..")
                
        except ObjectDoesNotExist:
            print("\n\n\n\n\n")
            print(request.query_params)
            return Response({f"info":"your customer id not exist in the database"},400)
        except ValueError as e:
            return Response({"info":str(e)},400)
        
        try:
            customer.delete()
        except RestrictedError:
            return Response({"info":"The Customer In Rent And Cant Be Deleted."},400)
        return Response({"info":"User Deleted Successfully"})
















@api_view(["GET","POST","PUT","DELETE"])
@authentication_classes([BasicAuthentication , TokenAuthentication])
@permission_classes([IsAuthenticated,IsLibraryWorker])
def serve_book(request):


    #diplaying all books or one book by id
    if request.method == "GET":
        #There is opition to view books from another librarys with query:
        external_lib = request.query_params.get("external",False)
        #Searching for one book:
        book_name = request.query_params.get("name",False) #"False" - if we dont get the query

        #showing books only from the worker lib(DEFAULT)
        if not book_name and not external_lib:
           books = Book.objects.filter(lib = request.user.customer.lib.id)
           serialzer = BookSerializer(instance=books , many = True)

        #showing books from all libs
        elif not book_name and external_lib:
            books = Book.objects.all()
            serialzer = BookSerializer(instance=books ,many = True)

        #showing search for spesific book
        else:
            #validate that there is book that contain EVEN PART OF THE STRING
            try:
                book = Book.objects.get(name__icontains = book_name)
            except ObjectDoesNotExist:
                return Response({"info":"no such book"})
            
            serialzer = BookSerializer(instance=book)

        #if there is no books found - wiil be a proper message
        if not serialzer.data:
            return Response({"info":"no books found"})
        
        return Response(serialzer.data)

    #adding a new book only for the worker library..
    if request.method== "POST":
        book = BookSerializer(data = request.data)
        if book.is_valid():
            try:
                #validate the book add to the lib of the worker:
                if request.data["lib"] != str(request.user.customer.lib.id):
                    raise ValueError("You are not allowed to add book to another lib..")
            except ValueError as e:
                return Response({"info":str(e)}) 
            book.save()
            return Response({"info":"book created succsesfuly!", "data":request.data},status=200)

        else:
            return Response({"info":"error!","error": book.errors} ,status=500)
    
    #changing the RETURN PERIOD of the book just if the book not in rent.. and the lib of the worker its the lib of the book
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
        try:
        #validate that book is in the lib of the worker:
            if book.lib.id != request.user.customer.lib.id:
                raise ValueError("You are not allowed to add book to another lib..")         
        except ValueError as e:
            return Response({"info":str(e)})
        
        if serialzer.is_valid():
            new_book = serialzer.save()
            return Response({"info":"works. changes saved.","book_name":new_book.name,"author":new_book.author,"return_period":new_book.return_period} )

        return Response({"info":"error!","error":serialzer.errors},status=400)

    #deleting the book if he dont have any rents and he in the lib of the worker
    if request.method == "DELETE":
        id_ = request.query_params.get("id",False)

        if not id_:
            return Response({"info":"You must specify the id of the book you want to delete"}, status=400)
        
        #validating the book
        try:
            book = Book.objects.get(id = id_)
        except ObjectDoesNotExist:
            return Response({"info":"your book id not exist in the database"})
        
        try:
        #validate that book is in the lib of the worker:
            if book.lib.id != request.user.customer.lib.id:
                raise ValueError("You are not allowed to add book to another lib..")         
        except ValueError as e:
            return Response({"info":str(e)})
        try :
            book.delete()
        except RestrictedError:
            return Response({"info":"The Book In Rent And Cant Be Deleted."})
        
        return Response({"info":"Book Deleted Successfully"})




@api_view(["GET","POST","PUT","DELETE"])
@authentication_classes([BasicAuthentication , TokenAuthentication])
@permission_classes([IsAuthenticated])
def serve_rent(request):

    #diplaying all rents or rents by customer id
    #displaying only rents of the worker lib
    if request.method == "GET":
        #optional querys
        cust_id = request.query_params.get("id",False) 

        #check for query 'cust_id'
        if not cust_id:
            rents = Rent.objects.filter(lib = request.user.worker.lib.id)
            serialzer = RentSerializer(instance=rents ,many = True)

        else:
            #validate that there is rent associated with a customer 
            rent = Rent.objects.filter(cust= cust_id , lib = request.user.worker.lib.id)
            if not rent:
                return Response()
            
            serialzer = RentSerializer(instance=rent , many = True)

        #return message if there is no rents in general:
        if not serialzer.data:
            return Response({"info":"Not Found Any Rents "})
        return Response(serialzer.data)

    #adding a new rent !!validate that the book is not already in use..
    if request.method== "POST":
        rent = RentSerializer(data = request.data)

        #Check if the book havent rented alerady
        # & check that the rent is on the worker lib
        try:
            if Rent.objects.filter(book = request.data["book"]):
                return Response({"info":"The Book Already Rented.. come in another time.."})
            
            if request.data["lib"]!= str(request.user.customer.lib.id):
                raise ValueError("you cant make rent in another library")
        except KeyError:
            return Response({"info":"error: you need to pass th book id.."})
        except ValueError as e:
            return Response({"info":str(e)})
        if rent.is_valid():
        
            rent_start_date = rent.validated_data["return_start_date"] = datetime.now()
            
            #check what the period time of the book
            my_book = Book.objects.get(id=request.data["book"])
            if my_book.return_period == 1:
                rent.validated_data["return_end_date"] = rent_start_date + timedelta(days = 10)

            if my_book.return_period == 2:
                rent.validated_data["return_end_date"] = rent_start_date + timedelta(days = 20)

            if my_book.return_period == 3:
                rent.validated_data["return_end_date"] = rent_start_date + timedelta(days = 30)
            try:
                rent.save()
            except IntegrityError as e:
                return Response({"info":"you need to enter the customer id","error":str(e)})
            return Response({"info":"rent created succsesfuly!", "data":request.data},status=200)

        else:
            return Response({"info":"error!","error": rent.errors} ,status=500)
    
    #sending error message for trying to edit
    if request.method == "PUT":
        return Response({"info":"error! you can't change rent. its immutable."},status=400)


    #deleting a rent only in the library of the worker
    if request.method == "DELETE":
        id_ = request.query_params.get("id",False)

        if not id_:
            return Response({"info":"You must specify the id of the rent you want to delete"}, status=400)
        
        #validating that the rent exist & in the lib of the worker
        try:
            rent = Rent.objects.get(id = id_)
            if rent.lib.id != request.user.worker.lib.id:
                raise ValueError(f"you cant delete rents of another lib.. The Rent Lib:{rent.lib.id}  Your Lib:{request.user.customer.lib.id}")
        except ObjectDoesNotExist:
            return Response({"info":"your id of the rent not exist in the database"})
        except ValueError as e:
            return Response({"info":str(e)})
        rent.delete()
        return Response({"info":"Rent Deleted Successfully"})



    