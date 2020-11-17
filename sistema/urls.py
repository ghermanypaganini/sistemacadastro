"""sistema URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from global_login_required import login_not_required
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from sbadmin.views import (
                            EmployedHashView, EmployeeNewView, EmployeeView, EmployeesView, EmployeeDeleteView, EmployeeEditView,
                            AreaView, EntriesView, EntryView, login_view, logout_view, home_view
                          )

urlpatterns = [
    path('admin/', admin.site.urls), #Acesso Admin
    path('', home_view, name='home'), #Home
    path("login", login_view, name='login'), #Login
    path("logout", logout_view, name='logout'), #Sair
    path('employees/', EmployeesView.as_view(), name='employees'), #Funcionários
    path('employee/new/', EmployeeNewView.as_view(), name='employee-new'), #Novo
    path('employee/delete/<int:id>/', EmployeeDeleteView.as_view(), name='employee-delete'), #Deletar
    path('employee/edit/<int:id>/', EmployeeEditView.as_view(), name='employee-edit'), #Editar
    path('employee/view/<int:id>/', EmployeeView.as_view(), name='employee-view'), #Visualizar
    path('areas/<int:id>', AreaView.as_view(), name='area'), #Areas
    path('entries/', EntriesView.as_view(), name='entries'), #Entradas
    path('entry/<int:registro>', login_not_required(EntryView.as_view()), name='entry'), #Entradas
    path('hash/<int:registro>', login_not_required(EmployedHashView.as_view()), name='entry'), #Entradas
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
