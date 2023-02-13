from django.urls import path
from .import views

urlpatterns=[
    path('index',views.index,name='index'),
    path('register',views.register,name='register'),
    path('login',views.login,name='login'),
    path('logout',views.logout,name='logout'),
    path('inspection',views.inspection,name='inspection'),
    path('email',views.email,name='email')
]


