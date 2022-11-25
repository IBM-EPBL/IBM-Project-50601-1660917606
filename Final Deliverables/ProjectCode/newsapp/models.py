from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your models here.
class Customer(models.Model):
    user = models.ForeignKey(User, max_length=200, null=True, on_delete = models.SET_NULL)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    date = models.DateTimeField(auto_now_add= True, null=True)
    recent_category = models.CharField(max_length=200, default = 'general')

    ####### displays name in customer table instead of id ---> in admin panel ####
    def __str__(self):
            return self.name

class Article(models.Model):
    url = models.CharField(max_length = 500, null = True)
    title = models.CharField(max_length = 200, null= True)    
    desciption = models.CharField(max_length = 1000, null= True)
    urlToImage = models.CharField(max_length = 500, null= True)
    author = models.CharField(max_length = 200, null= True)
    publishedAt = models.CharField(max_length = 200, null= True)

    def __str__(self):
        return self.title

class SavedArticle(models.Model):
    customer = models.ForeignKey(Customer, null= True, on_delete=models.SET_NULL)
    article = models.ForeignKey(Article, null= True, on_delete=models.SET_NULL)




