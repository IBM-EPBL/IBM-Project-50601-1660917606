from django.http import HttpResponse
import requests
from django.shortcuts import render, redirect
from django.contrib.auth.models import auth, User
from django.contrib import messages
from .models import *
from django.http import HttpResponseRedirect

################################### NEWS API #################################

##9c9e6c74b22c4507896ae130faf78c07
##d8949839bf404020a17399d10c47f690
API_KEY = 'd8949839bf404020a17399d10c47f690'


def home(request):

    if not request.user.is_authenticated:
        return redirect('/login')

    country = None
    category = None
    arr1 = request.GET.get('category')
    arr2 = request.GET.get('country')

    if arr1 is not None:
        category, country = arr1.split(',')
        print("category : ", category, "   country : ", country)

    elif arr2 is not None:
        country, category = arr2.split(',')

    customer = Customer.objects.get(user = request.user)
    if country is None:
        country = 'us'
    if category is None:
        category = customer.recent_category
    
    url = f"https://newsapi.org/v2/top-headlines?country={country}&category={category}&apiKey={API_KEY}"
    response = requests.get(url)
    data = response.json()
    articles = data['articles']

    return render(request, 'home.html', {
        'articles' : articles, 
        'data' : data, 
        'country' : country, 
        'category': category,
        'customer' : customer
    })

############################# LOGIN #############################

def register(request):
    return render(request, 'register.html')

def login_page(request):
    return render(request, 'login.html')

def create_account(request):
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    username = request.POST['username']
    email = request.POST['email']
    password1 = request.POST['password1']
    password2 = request.POST['password2']

    if User.objects.filter(username = username).exists():
        messages.info(request, "Username taken")
        return redirect(register)

    elif User.objects.filter(email = email).exists():
        messages.info(request, "Email exists")
        return redirect(register)

    elif password1 != password2:
        messages.info(request, "Password doesnt match")
        return redirect(register)

    else:
        user = User.objects.create_user(username = username, password = password1, email = email, first_name = first_name, last_name = last_name)
        user.save()

        customer = Customer(
            user = user, 
            name = first_name,
            email = email, 
        )
        customer.save()
    
    return redirect(login_page)

def verify_login(request):
    username = request.POST['username']
    password = request.POST['password']

    user = auth.authenticate(username = username, password = password)

    if user is not None:
        auth.login(request, user)
        str = '/newsapp/' + username
        return redirect('/')
    
    messages.info(request, 'Invalid credentials')
    return redirect(login_page)

def logout(request):
    auth.logout(request)
    return redirect('/login')


######################## saved articles ###########################


def saved_articles(request, cust_id):
    customer = Customer.objects.get(id=cust_id)
    saved_articles = customer.savedarticle_set.all()

    return render(request, 'saved_articles.html', {'saved_articles' : saved_articles, 'cust_id' : cust_id, 'customer' : customer})


####################### save an article ##############################

def save_article(request, cust_id):
    ######## put record into Article model and get the id of the article
    url = request.GET.get('url', False)
    total_splits = len(url.split('~'))
    if total_splits is not 7:
        return redirect('/')

    url1, url2, author, publishedAt, description, title, category = url.split('~')

    a = Article(
        title = title, 
        url = url1,
        desciption = description,
        urlToImage = url2,
        author = author,
        publishedAt = publishedAt
    )
    a.save()
   
    ######## put record into SavedArticle model with the customer id and article id
    c = Customer.objects.get(user = request.user)
    c.recent_category = category
    c.save()
    
    print("Recent Category is ", c.recent_category)

    s = SavedArticle(
        customer = c,
        article = a
    )

    s.save()

    return redirect('/')


def delete_saved_article(request, saved_article_id, cust_id):
    instance = SavedArticle.objects.get(id=saved_article_id)
    instance.delete()
    str = '/saved_articles/'+ cust_id
    return redirect(str)
