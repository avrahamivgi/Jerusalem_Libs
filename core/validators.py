from django.core.exceptions import ValidationError


#Validate That The Id Is A Number
def validate_id(id_):
    if not id_.isdigit():
        raise ValidationError(f'Please enter a 9-digit number. you enter {id_}')
#The Validation Of Nine Numbers - I Will Do In The Api Views
#(There Is A Problem Of Saving Leading Zeros In Django..)

#
