"""
URL configuration for scholarsgig project.

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
from app1.views import *
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('',Homeview.as_view(),name="home"),
    path('login/',Loginview.as_view(),name="login"),
    path('signup/',Signupview.as_view(),name="signup"),
    path('job_input/',Jobinputview.as_view(),name="job_input"),
    path('job/<int:id>',Jobview.as_view(),name="job"),
    path('profiles/',ProfileView.as_view(),name="profiles"),
    path('profile_input',Profile_input_view.as_view(),name="profile_input"),
    path('user_profile/<int:pk>',User_Profile_View.as_view(),name="user_profile"),
    path('myjobs/',Myjobs.as_view(),name="myjobs"),
    path('applications/<int:id>',Applicationview.as_view(),name="applications"),
    path('work_dashboard/<int:id>',WorkDashboard.as_view(),name="work_dashboard"),
]
if settings.DEBUG:  # Serve media files in development
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
