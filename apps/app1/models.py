import re
import bcrypt
from django.db import models

class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=12)
    email = models.CharField(max_length=30)
    password = models.CharField(max_length=255)
    password_plaintext = models.CharField(max_length=32, null=True)
    pw_salt = models.CharField(max_length=255)

    def __str__(self):
        return self.first_name+' '+self.last_name

    def registration_errors(self):
        errors = []
        if len(self.first_name) > 50 or len(self.last_name) > 50:
            errors.append('First and last name must be less than 50 characters each.')
        if len(self.username) > 12:
            errors.append('Username must not exceed 12 characters in length.')

        if len(self.password_plaintext) < 8:
            errors.append('Password must be at least 8 characters in length.')

        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
        if not EMAIL_REGEX.match(self.email):
            errors.append('Invalid email format.')

        return errors

    def encrypt_pw(self):
        self.pw_salt = bcrypt.gensalt()
        self.password = bcrypt.hashpw(self.password_plaintext.encode(), self.pw_salt)
        self.password_plaintext = None

    def login_errors(self):
        errors = []
        db_user = User.objects.filter(username=self.username)
        
        if len(db_user) == 0:
            errors.append('No user exists with this username.')
            return self, errors 

        db_user = db_user[0]
        check_password = bcrypt.hashpw(self.password_plaintext.encode(), db_user.pw_salt.encode())
        check_password = check_password.decode()
        
        if db_user.password != check_password:
            errors.append('Invalid password supplied for this user')

        return db_user, errors


class Author(models.Model):
    full_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name

    def lookup(full_name):
        db_author = Author.objects.filter(full_name=full_name)
        if len(db_author) == 0:
            new_author = Author.objects.create(full_name=full_name)
            return new_author
        else:
            return db_author[0]

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Author)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def lookup(book_title, author_full_name):
        db_book = Book.objects.filter(title=book_title).filter(author__full_name=author_full_name)
        if len(db_book) == 0:
            author = Author.lookup(author_full_name)
            new_book = Book.objects.create(title=book_title, author=author)
            return new_book
        else:
            return db_book[0]
        

class Review(models.Model):
    book = models.ForeignKey(Book)
    user = models.ForeignKey(User)
    rating = models.IntegerField()
    content = models.TextField(max_length=300)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{} gave {} {} star(s)'.format(
            str(self.user), str(self.book), str(self.rating))
    
