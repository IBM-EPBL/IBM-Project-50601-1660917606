from django.urls import path
from . import views
urlpatterns = [
    path('login', views.login_page, name='login_page'),
    path('register/create_account', views.create_account, name = 'create_account'),
    path('verify_login', views.verify_login, name = 'verify_login'),
    path('register/', views.register, name='register'),
    path('saved_articles/<str:cust_id>/', views.saved_articles, name = 'saved_articles'),
    path('save_article/<str:cust_id>/', views.save_article, name = 'save_article'),
    path('delete_saved_article/<str:saved_article_id>/<str:cust_id>', views.delete_saved_article, name = 'delete_saved_article'),
    path('logout', views.logout, name = 'logout'),
    path('', views.home, name='home'),
]


