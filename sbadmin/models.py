from django.db import models

TYPE = (
        (1, 'Entrada'),
        (2, 'Saída'),
    )

class Area(models.Model): #Área
    name = models.CharField(max_length=20, null=False, verbose_name='Área')

    def __str__(self):
        return self.name

class Position(models.Model): #Cargo
    name = models.CharField(max_length=20, null=False, verbose_name='Cargo')
    area = models.ForeignKey(Area, null=True, on_delete=models.SET_NULL, verbose_name='Área')

    def __str__(self):
        return self.name

class Employee(models.Model): #Funcionário
    name = models.CharField(max_length=50, null=False, verbose_name='Nome')
    registration_code = models.IntegerField(null=False, unique=True, verbose_name='Matrícula')
    position = models.ForeignKey(Position, null=True, verbose_name='Cargo', on_delete=models.SET_NULL)

    def __str__(self):
        return self.name

class Entry_Log(models.Model): #Registro de Entradas
    employee = models.ForeignKey(Employee, null=True, on_delete=models.SET_NULL)
    day = models.DateTimeField(auto_now_add=True, blank=True)
    type = models.IntegerField(choices=TYPE, default=1)

    def __str__(self):
        return "{} - {}".format(self.employee.name, self.day)

    def getType(self):
        return TYPE[self.type - 1][1]