from django.shortcuts import render, redirect
from django.views.generic import CreateView, ListView, UpdateView
from .form import EmployeeForm, LoginForm
from .models import Employee, Area, Position, Entry_Log
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.db import IntegrityError
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from global_login_required import login_not_required
from datetime import datetime
import json

class AreaView(ListView):
    model = Area

    def get(self, request, *args, **kwargs):
        id = self.kwargs['id']

        positions = [{
            'id': position.id,
            'name': position.name
        } for position in Position.objects.filter(area__id=id).all()]

        return JsonResponse({
            'positions': positions
        })

class EntriesView(LoginRequiredMixin, ListView):
    model = Entry_Log
    template_name = 'entries.html'

    def get(self, request, *args, **kwargs):
        if 'name' in request.GET:
            entries = self.model.objects.filter(employee__name__icontains=request.GET['name']).order_by('-hour').all()
        elif 'id' in request.GET:
            entries = self.model.objects.filter(employee__id=request.GET['id']).order_by('-day').all()
        else:
            entries = self.model.objects.order_by('-day').all()

        paginator = Paginator(entries, 4)
        page = request.GET.get('page')
        result = paginator.get_page(page)

        return render(request, self.template_name, {
            'entries': result,
            'message': None,
            'type': None
        })

@method_decorator(csrf_exempt, name='dispatch')
class EntryView(CreateView):
    model = Entry_Log

    def post(self, request, *args, **kwargs):
        registro = self.kwargs['registro']
        jsonContext = {'msg': 'O campo registro é obrigatório'}
        status = 405

        if registro > 0:
            employee = Employee.objects.filter(registration_code=registro).first()
            if employee:
                ultima = self.model.objects.filter(employee=employee).last()
                tipo = 1
                if datetime.now().date() == ultima.day.date():
                    if ultima.type == 1:
                        tipo = 2

                self.model.objects.create(
                    employee = employee,
                    type=tipo
                )
                jsonContext = {'msg': 'Ponto registrado com sucesso!!!'}
                status = 200
            else:
                jsonContext = {'msg': 'Funcionário não encontrado.'}


        return JsonResponse(jsonContext, status=status)

@method_decorator(csrf_exempt, name='dispatch')
class EmployedHashView(UpdateView):
    model = Employee

    def post(self, request, **kwargs):
        registro = self.kwargs['registro']
        jsonContext = {'msg': 'O campo registro é obrigatório'}
        status = 405

        if registro > 0:
            employee = self.model.objects.filter(registration_code=registro).first()
            if employee:
                try:
                    if employee.digitalHash != digitalHash:
                        employee.digitalHash = digitalHash
                        employee.save()

                    jsonContext = {'msg': 'Hash registrada com sucesso!!!'}
                    status = 200
                except IntegrityError:
                    jsonContext = {'msg': 'Essa hash já pertence a outro usuário!!!'}
                    status = 403
            else:
                jsonContext = {'msg': 'Funcionário não encontrado.'}

        return JsonResponse(jsonContext, status=status)

class EmployeeDeleteView(LoginRequiredMixin, CreateView):
    model = Employee
    template_name = 'employees.html'

    def get(self, request, *args, **kwargs):
        try:
            self.model.objects.filter(id=self.kwargs['id']).delete()
            message = "Usuário deleteado com sucesso!!!"
            type = "success"
        except:
            message = "Erro ao deletar usuário"
            type = "danger"

        employees = self.model.objects.all()
        paginator = Paginator(employees, 4)
        page = request.GET.get('page')
        result = paginator.get_page(page)

        return render(request, self.template_name, {
            'employees': result,
            'message': message,
            'type': type
        })

class EmployeeEditView(LoginRequiredMixin, CreateView):
    model = Employee
    template_name = 'employee.html'
    form_class = EmployeeForm

    def post(self, request, *args, **kwargs):
        employeeId = self.kwargs['id']
        instance = self.model.objects.filter(id=employeeId).first()

        form = self.form_class(request.POST, instance=instance, employeeId=employeeId)
        try:
            if form.is_valid():
                form.save()
                message = 'Formulário editado com sucesso'
                _type = 'success'
            else:
                message = 'Formulário inválido'
                _type = 'danger'
        except:
            message = 'Um erro inesperado ocorreu'
            _type = 'danger'

        return render(request, self.template_name, {
            'form': form,
            'employed': instance,
            'message': message,
            'type': _type,
            'post_method': 'employee-edit',
            'id': employeeId,
            'title': 'Editar Cadastro',
            'btn': 'Editar'
        })

    def get(self, request, *args, **kwargs):
        employeeId = self.kwargs['id']
        instance = self.model.objects.filter(id=employeeId).first()

        return render(request, self.template_name, {
            'form': self.form_class(instance=instance, employeeId=employeeId),
            'employed': instance,
            'message': None,
            'type': None,
            'post_method': 'employee-edit',
            'id': employeeId,
            'title': 'Editar Cadastro',
            'btn': 'Editar'
        })

class EmployeeView(LoginRequiredMixin, CreateView):
    model = Employee
    template_name = 'employee.html'
    form_class = EmployeeForm

    def get(self, request, *args, **kwargs):
        employeeId = self.kwargs['id']
        instance = self.model.objects.filter(id=employeeId).first()

        return render(request, self.template_name, {
            'form': self.form_class(instance=instance, employeeId=employeeId),
            'employed': instance,
            'message': None,
            'type': None,
            'post_method': None,
            'id': employeeId,
            'title': instance.name,
            'btn': None
        })

class EmployeeNewView(LoginRequiredMixin, CreateView):
    model = Employee
    template_name = 'employee.html'
    form_class = EmployeeForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        employee = Employee.objects.filter(registration_code=request.POST['registration_code']).first()
        if employee:
            return render(request, self.template_name, {
                'form': form,
                'message': 'Essa matrícula já existe',
                'type': 'warning',
                'post_method': 'employee-new',
                'id': None,
                'title': 'Cadastrar Funcionário',
                'btn': 'Salvar'
            })

        try:
            if form.is_valid():
                form.save()
                message = 'Formulário salvo com sucesso'
                _type = 'success'
                form = self.form_class()
            else:
                message = 'Formulário inválido'
                _type = 'danger'
        except IntegrityError as e:
            message = 'Matrícula já existente'
            _type = 'danger'
        except:
            message = 'Um erro inesperado ocorreu'
            _type = 'danger'

        return render(request, self.template_name, {
            'form': form,
            'message': message,
            'type': _type,
            'post_method': 'employee-new',
            'id': None,
            'title': 'Criar employee',
            'btn': 'Salvar'
        })

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {
            'form': self.form_class(),
            'message': None,
            'type': None,
            'post_method': 'employee-new',
            'id': None,
            'title': 'Cadastrar Funcionário',
            'btn': 'Salvar'
        })

class EmployeesView(LoginRequiredMixin, ListView):
    model = Employee
    template_name = 'employees.html'

    def get(self, request, *args, **kwargs):
        if 'name' in request.GET:
            employees = self.model.objects.filter(name__icontains=request.GET['name']).all()
        else:
            employees = self.model.objects.all()

        paginator = Paginator(employees, 4)
        page = request.GET.get('page')
        result = paginator.get_page(page)

        return render(request, self.template_name, {
            'employees': result,
            'message': None,
            'type': None
        })

@login_not_required
def login_view(request):
    loginForm = LoginForm()
    message = None

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        loginForm = LoginForm(request.POST)

        if loginForm.is_valid():
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if 'next' in request.GET:
                    return redirect(request.GET['next'])
                return redirect('/')
            else:
                message = {'type': 'danger','text': 'Dados de usuário incorretos'}

    context = {
        'form': loginForm,
        'message': message,
    }
    return render(request, template_name='login.html', context=context, status=200)

def logout_view(request):
    logout(request)
    return redirect('/login')

def home_view(request):
    return redirect('/employees')
