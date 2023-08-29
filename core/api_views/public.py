from django.core.exceptions import ObjectDoesNotExist 
from django.contrib.auth.models import User
from django.db import IntegrityError
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token


from core.serialzers import BookSerializer
from core.models import Book 


@api_view(["GET"])
def serve_book(request):

    #diplaying all books or books by name
    if request.method == "GET":

        #filtering by name
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

