from rest_framework import serializers
from datetime import date
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError


from .models import Customer ,Book , Rent ,Library
from .validators import validate_id

#serilazers for models:

#user
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

#lib
class LibSerializer(serializers.ModelSerializer):
    class Meta:
        model = Library
        fields = "__all__"


#customer
class CustomerSerializer(serializers.ModelSerializer):
    customer_id = serializers.CharField(validators=[validate_id])
    lib_details = LibSerializer(source="lib", read_only=True)
    password = serializers.CharField(write_only=True)  

    class Meta:
        model = Customer
        fields = "__all__"

    def create(self, validated_data):
        print('XXXXXXXXXXXXXXXXXXXXX\n\n')
        #password = validated_data.pop('password')  
        # create new user instance
        user = User(username=validated_data['customer_id'])
        user.set_password(validated_data.pop('password') )
        user.save()

        # Link the User instance to the Customer
        validated_data['user'] = user
        print(user)

        customer = Customer.objects.create(**validated_data)
        return customer

class CustomerMiniSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = ['name','birth_date',"lib"]

#book
class BookSerializer(serializers.ModelSerializer):

    lib_details= LibSerializer(source="lib" , read_only=True)
    
    class Meta:
        model = Book
        fields = "__all__"

class BookMiniSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = ['return_period']    
#rent
class RentSerializer(serializers.ModelSerializer):
    #Checking If The Rent Is Late
    is_late = serializers.SerializerMethodField(source="get_is_late")
    def get_is_late(self,rent_object):
        return rent_object.return_end_date < date.today()

    #adding additonal details about the books rented for display purpose
    book_details = BookSerializer(source="book", read_only=True)

    #and also the lib details
    lib_details = LibSerializer(source="lib", read_only=True)
    #when i use source - "lib" i use the exist attrbiute in my model.

    class Meta:
        model = Rent
        fields = "__all__"


class RentMiniSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rent
        fields = "return_start_date"