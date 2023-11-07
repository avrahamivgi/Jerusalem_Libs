from django.core.exceptions import ObjectDoesNotExist 
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.views.decorators.cache import cache_page
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token


from core.serialzers import BookSerializer
from core.models import Book ,Worker


@api_view(["GET"])
def serve_book(request):

    #diplaying all books or books by name
    if request.method == "GET":
        #filtering by name
        book_name = request.query_params.get("name",False) #"False" - if we dont get the query
        lib = request.data.get("lib",False)
        print(book_name , lib , request.data)
        if not book_name and not lib:
            books = Book.objects.all()
            serialzer = BookSerializer(instance=books ,many = True)
            
        elif book_name and not lib:

            #validate that there is book that contain EVEN PART OF THE STRING
            try:
                book = Book.objects.filter(name__icontains = book_name)
                serialzer = BookSerializer(instance=book,many = True)
                if not book:
                    return Response({"no such book"})

            except ObjectDoesNotExist:
                return Response({"no such book"})
        
        elif book_name and lib:
            try:
                book = Book.objects.filter(name__icontains = book_name , lib=lib)
            except ObjectDoesNotExist:
                return Response({"info":"no such book"})
            
            serialzer = BookSerializer(instance=book,many = True)

        return Response(serialzer.data)
    


@api_view(["POST"])
def signup(request):
    try:
    
        username = request.data.get("username")
        password = request.data.get("password")
        
        user = User.objects.create_user(username=username , password=password)
        token = Token.objects.create(user = user)
    except IntegrityError as e:
        return Response({"info":"This username is in use. pick another one.","error":str(e)})
    except Exception as e :
        return Response({"info":"you have not provided all the details","error":str(e)})
 

    return Response({"Token" : token.key , "info": f"new user created! id : {user.id}"})

