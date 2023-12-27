"""
URL configuration for djangoProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from ASKII import views
urlpatterns = [
    path('', views.index, name='index'),
    path('ask', views.ask, name='ask'),
    path('settings', views.settings, name='settings'),
    path('login', views.login, name='login'),
    path('signup', views.signup, name='signup'),
    path('tag/<tag_name>', views.tag, name='tag'),
    path('question/<question_id>', views.question, name='question'),
    path('hot', views.hot, name='hot'),
    path('admin/', admin.site.urls),
    path('profile/<int:profile_id>/', views.profile, name='profile'),
]
