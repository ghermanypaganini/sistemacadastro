from django.forms import ModelForm
from django import forms
from .models import Employee, Area, Position

class EmployeeForm(ModelForm):
    area = forms.ModelChoiceField(
        queryset=Area.objects.all(),
        widget=forms.Select(attrs={
            'class': 'form-control'
        }))

    def __init__(self, *args, **kwargs):
        try:
            id = kwargs['employeeId']
            emp = Employee.objects.filter(id=id).first()
            area = emp.position.area.id
            position = emp.position.id
            kwargs.pop('employeeId', None)
        except:
            area = None
            position = None

        super(EmployeeForm, self).__init__(*args, **kwargs)
        if kwargs.get('instance'):
            self.fields['area'].initial = area
            self.fields['position'].queryset = Position.objects.filter(area__id=area).all()
            self.fields['position'].initial = position

    class Meta:
        model = Employee
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': "form-control"}),
            'registration_code': forms.TextInput(attrs={'class': "form-control"}),
            'position': forms.Select(attrs={'class': "form-control"}),
            'digitalHash': forms.TextInput(attrs={'class': "form-control"}),
        }

class LoginForm(forms.Form):
    username = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}), label='Usuário')
    password = forms.CharField(max_length=32, widget=forms.PasswordInput(attrs={'class': 'form-control'}), required=True, label='Senha')

