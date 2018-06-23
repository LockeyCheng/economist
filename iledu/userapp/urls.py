"""app_with_vue URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^login/', views.LoginManager.as_view(), name='login'),
    url(r'^logout/$', views.LogoutManager.as_view(), name='logout'),
    url(r'^uprofile/$', views.UserProfile.as_view(), name='uprofile'),
    url(r'^avatar_upload/$', views.Useravatar.as_view(), name='avatar'),
    url(r'^user_list$', views.UserList.as_view(), name='users'),
    url(r'^uadmin/$', views.UserAdmin.as_view(), name='uadmin'),
    url(r'^library_admin/$', views.libraryAdmin.as_view(), name='library_admin'),
    ]
