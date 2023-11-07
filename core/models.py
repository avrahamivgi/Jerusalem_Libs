from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Library(models.Model):
    #(default id..)
    name = models.CharField(max_length=40)
    address = models.CharField(max_length=100 , blank=True, null=True)
    def __str__(self):
        return f"{self.name} , {self.id}"

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer',blank=True)
    lib = models.ForeignKey(Library , on_delete = models.CASCADE)
    name = models.CharField(max_length=40)
    birth_date = models.DateField(null=True, blank=True)   
    phone = models.IntegerField(blank= True , null= True)
    customer_id = models.CharField(primary_key=True, max_length=9) #its on purpose char field and not integar..
    
    def __str__(self):
        return f"{self.name} , {self.customer_id}"

class Worker(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='worker')
    lib = models.ForeignKey(Library , on_delete = models.CASCADE)
    name = models.CharField(max_length=40)
    phone = models.IntegerField()
    
    def __str__(self):
        return f"{self.name}"

class Manager(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='manager')
    lib = models.ForeignKey(Library , on_delete = models.CASCADE)
    name = models.CharField(max_length=40)
    phone = models.IntegerField()
    
    def __str__(self):
        return f"{self.name}"


class Book(models.Model):
    lib = models.ForeignKey(Library , on_delete = models.CASCADE )
    name = models.CharField(max_length=40)
    author = models.CharField(max_length=40)
    cover_img = models.ImageField(upload_to="book_covers/" , null=True , blank= True ,default="book_covers\\jru_cover.png")
    numbers_choise = ((1,"10 days"), (2,"20 days"), (3,"30 days"))
    return_period = models.IntegerField(choices=numbers_choise, default= 2)

    def __str__(self):
        return f"{self.name}"

class Rent(models.Model):
    lib = models.ForeignKey(Library , on_delete = models.CASCADE )
    book = models.ForeignKey(Book,on_delete=models.RESTRICT)
    cust = models.ForeignKey(Customer,on_delete=models.RESTRICT , default=1)
    return_start_date = models.DateField(null=True , blank= True)
    return_end_date = models.DateField(null = True , blank=True)

    def __str__(self):
        return f"{self.book} , {self.cust} ,{self.return_end_date}"
    
