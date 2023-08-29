from rest_framework import serializers
from datetime import date
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError


from .models import Customer ,Book , Rent 
from .validators import validate_id

#serilazers for models:

#user
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

#customer
class CustomerSerializer(serializers.ModelSerializer):
    customer_id = serializers.CharField(validators = [validate_id])
    username = serializers.CharField(write_only=True)  # "write only" means that its will not be included in the response
    user = UserSerializer(read_only=True)  # in order to prevent query call for this

    class Meta:
        model = Customer
        fields = "__all__"

    #in order to connect the customer to the user
    #with a name and not with id - we overide the create func
    #thank for chat gpt :)
    def create(self, validated_data):
        username = validated_data.pop('username')  # extracting the username from the request
        #validate that there is user
        try:
            user = User.objects.get(username=username)  # get the user instance
        except User.DoesNotExist:
            raise ValidationError("There Is Not Such A User..")
        customer = Customer.objects.create(user=user, **validated_data)
        return customer

class CustomerMiniSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = ['name','age',"lib"]

#book
class BookSerializer(serializers.ModelSerializer):

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
    
    class Meta:
        model = Rent
        fields = "__all__"


class RentMiniSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rent
        fields = "return_start_date"