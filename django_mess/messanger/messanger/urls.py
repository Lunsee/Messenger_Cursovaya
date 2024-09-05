"""
URL configuration for messanger project.

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
from django.views.generic import RedirectView

from messanger_enc.views import login_view
from django.urls import path, include
from messanger_enc.utils.api import submit_data_reg
from messanger_enc.utils.api import submit_data_log
from messanger_enc.views import user_profile
from messanger_enc.utils.api import Send_Message_Control
from messanger_enc.utils.api import check_user
from messanger_enc.utils.api import get_message_history


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', login_view, name='login'),
    path('check_user/', check_user, name='check_user'),
    path('get_message_history/', get_message_history, name='get_message_history'),
    path('Send_Message_Control/', Send_Message_Control, name='Send_Message_Control'),
    path('submit_data_reg/', submit_data_reg, name='submit_data_reg'),
    path('submit_data_log/', submit_data_log, name='submit_data_log'),
    path('<str:username>/', user_profile, name='user_profile'),
    path('', RedirectView.as_view(url='/login/')),

]