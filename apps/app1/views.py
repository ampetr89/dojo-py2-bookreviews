from django.shortcuts import render, redirect
from .models import User 
from .models import Book
from .models import Author 
from .models import Review 
from django.contrib import messages

def is_logged_in(request):
    if 'logged-in' not in request.session:
        request.session['logged-in'] = False

    return request.session['logged-in']

def index(request):
    if is_logged_in(request):
        return redirect('/books')
    else:
        return render(request, 'app1/login.html')

def books(request):
    print('going to books')
    if is_logged_in(request):
        context = {
            'reviews': Review.objects.all(),
            'all_reviewed_books': list(set(Book.objects.filter(review__rating__isnull=False)))
        }
        return render(request, 'app1/index.html', context)
    else:
        return redirect('/')

def book_show(request, book_id):
    context = {
        'book': Book.objects.get(id=book_id)
    }
    return render(request, 'app1/book-show.html', context)
def login(request):
    if is_logged_in(request):
        return redirect('/')
    else:
        return render(request, 'app1/login.html')

def register(request):
    if is_logged_in(request):
        return redirect('/')
    else:
        return render(request, 'app1/register.html')

def logout(request):
    if request.method=='POST':
        request.session.clear()
        return redirect('/')
    else:
        return redirect('/')

def process_registration(request):
    if request.method == 'GET':
        return redirect('/')
    
    data = request.POST
    reg_errors = []
    if data['password'] != data['password2']:
        reg_errors.append("Supplied passwords don't match")
    
    test_user = User(first_name=data['first_name'], last_name=data['last_name'],
            email=data['email'], username=data['username'], password_plaintext=data['password'])
    reg_errors += test_user.registration_errors()

    for err_msg in reg_errors:
        messages.add_message(request, messages.ERROR, err_msg)

    if len(reg_errors) == 0:
        test_user.encrypt_pw()
        test_user.save() # create the user in the database
        messages.add_message(request, messages.SUCCESS, "Registration successful! Please log in")
        return redirect('/login')
    else:
        return redirect('/register')


def process_login(request):
    if request.method == 'GET':
        return redirect('/')
    
    data = request.POST
    login_errors = []

    test_user = User(username=data['username'], password_plaintext=data['password'])
    test_user, login_errs = test_user.login_errors()

    for err_msg in login_errs:
        messages.add_message(request, messages.ERROR, err_msg)

    if len(login_errs) == 0:
        request.session['logged-in'] = True
        request.session['user_id'] = test_user.id
        request.session['first_name'] = test_user.first_name
        print(request.session)
        return redirect('/')
    else:
        return redirect('/login')

def add(request):
    if is_logged_in(request):
        context = {
            'authors': [str(obj) for obj in Author.objects.all()]
        }
        return render(request, 'app1/add.html', context)
    else:
        return redirect("/")

def create_book(request):
    if request.method=='GET':
        return redirect('/')

    data = request.POST
    if 'author' not in data:
        if 'other-author' in data and data['other-author']=='':
            messages.add_message(request, messages.ERROR, "Must specify author name if none selected from list")
            return redirect('/add')
        else:
            author_name = data['other-author']
    else:
        author_name = data['author']

    book = Book.lookup(data['title'], author_name) 
    # if not found will create a new one, otherwise returns existing. 
    # also does the same for the author

    user = User.objects.get(id=request.session['user_id'])
    review = Review.objects.create(
        book=book, user=user,
        rating=data['rating'], content=data['content']
        )
    
    return redirect('/books/'+str(book.id))

def user_show(request, user_id):
    user = User.objects.filter(id=user_id)
    if len(user)==0:
        return redirect('/')
    user = user[0]
    reviewed = [rev.book for rev in user.review_set.all()]
    user_unique_books = list(set(reviewed))
    context = {
        'user':  user,
        'user_unique_books': user_unique_books
    }
    return render(request, 'app1/user-show.html', context)