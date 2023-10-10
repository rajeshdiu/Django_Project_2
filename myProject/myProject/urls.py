
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from myProject import views 

urlpatterns = [
    path('admin/', admin.site.urls), 
    path('home', views.home,name="home"), 
    path('loginPage', views.loginPage,name="loginPage"), 
    path('', views.signupPage,name="signupPage"), 
    path('myAdmin/home', views.adminPage,name="adminPage"), 
    path('myProfile', views.myProfile,name="myProfile"), 
    path('profile/update', views.profileUpdate,name="profileUpdate"), 
    path('logoutPage', views.logoutPage,name="logoutPage"), 
    
    
    
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
