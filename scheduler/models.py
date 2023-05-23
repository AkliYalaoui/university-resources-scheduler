from django.db import models
from django.contrib.auth.models import AbstractUser

class Semestre(models.Model):
    name = models.CharField(max_length=100)
    start = models.CharField(max_length=100)
    end = models.CharField(max_length=100)

class Formation(models.Model):
    name = models.CharField(max_length=100)
    niveau = models.CharField(max_length=100)
    nb_semestre = models.IntegerField(default=2)

class Module(models.Model):
    name = models.CharField(max_length=100)
    volume = models.CharField(max_length=100)
    semester = models.ForeignKey(Semestre, on_delete=models.CASCADE)
    formation = models.ForeignKey(Formation, on_delete=models.CASCADE)

class Section(models.Model):
    name = models.CharField(max_length=100)
    formation = models.ForeignKey(Formation, on_delete=models.CASCADE)

class Groupe(models.Model):
    name = models.CharField(max_length=100)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('admin', 'Admin'),
    )
    
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)


class Enseignant(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    modules = models.ManyToManyField(Module)
    grade = models.CharField(max_length=200)

class Etudiant(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    groupe = models.ForeignKey(Groupe, on_delete=models.CASCADE)

class Salle(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    capacity = models.IntegerField()

class Seance(models.Model):
    DAY_CHOICES = (
        ('dimanche', 'Dimanche'),
        ('lundi', 'Lundi'),
        ('mardi', 'Mardi'),
        ('mercredi', 'Mercredi'),
        ('jeudi', 'Jeudi'),
    )
    enseignant = models.ForeignKey(Enseignant, on_delete=models.CASCADE)
    subject = models.ForeignKey(Module, on_delete=models.CASCADE)
    groupe = models.ForeignKey(Groupe, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semestre, on_delete=models.CASCADE)
    salle = models.ForeignKey(Salle, on_delete=models.CASCADE)
    day = models.CharField(max_length=10, choices=DAY_CHOICES)
    time = models.TimeField()
    type = models.CharField(max_length=100)

