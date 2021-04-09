from django.db import models
import re


class UserManager(models.Manager):
    def create_validator(self,form):
        errors = {}
        if len(form['first_name']) <2:
            errors['first_name'] = 'First name needs to be at least 8 characters long'
        if len(form['last_name']) <2:
            errors['last_name'] = 'Last name needs to be at least 8 characters long'
        if len(form['email']) < 6:
            errors['email'] = 'email is to short'
        if len(form['password']) < 8:
            errors['password']= 'Password needs to be at least 8 characters long'
        if form['password'] != form['confirm_password']:
            errors['match'] = 'password and pw confirmation do not match'
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(form['email']):
            errors['regex'] = 'email in wrong format'
        users_with_email = User.objects.filter(email=form['email'])
        if len(users_with_email) >=1:
            errors['dup'] = 'email already taken'
        return errors 

class User(models.Model):
    first_name = models.TextField()
    last_name = models.TextField()
    email = models.TextField()
    password = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class DogManager(models.Manager):
    def create_validator(self,form):
        errors = {}
        if len(form['name']) <2:
            errors['name'] = 'Name must be at least 2 characters'
        if len(form['age']) != 0:
            errors['age'] 
        return errors 

class Dog(models.Model):
    name = models.TextField()
    breed = models.TextField()
    age = models.IntegerField()
    gender = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User,related_name='dog_owner',on_delete=models.CASCADE)
    likes = models.ManyToManyField(User,related_name='dogs_liked')
    objects = DogManager()


