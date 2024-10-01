"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from backend.views import *
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('admin/', admin.site.urls),
    #Auth
    #path('', loginuserView, name='loginuserView'),LoginView
    path('', LoginView.as_view(), name='loginuserView'),

    path('signup/', signupuserView, name ='signupuserView'),
    path('logout/',LogoutPageView.as_view(), name ='logoutuserView'),
    path('password/', ChangePasswordView.as_view(), name='change_pass'),

    #List
    # path('', views.home, name ='home'),
    path('list/',login_required(ListUsersView.as_view()), name ='listusersView'),
    path('listratings/<int:pk>', ListRatingsView.as_view(), name ='detail'),
    path('rate/<int:pk>', ChoiseEmp.as_view(), name ='choice'),
    path('tablepoint/',login_required(TablePointView.as_view()), name ='tablepointview'),
    path('newemployed/',login_required(NewEmployedView), name ='newemployedview'),
    path('update-page/<int:pk>',login_required(UpdatePageView), name ='updatepageview'),
    path('delete-data/<int:pk>', login_required(DeletePageView), name='deletepageview'),
]
handler403 = "backend.views.error_403_view"
handler404 = "backend.views.error_404_view"
handler500 = "backend.views.error_500_view"
