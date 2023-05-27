from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime
from django.core.exceptions import ValidationError

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


class Grade(models.Model):
    name = models.CharField(max_length=200)
    
    def __str__(self) -> str:
        return self.name

class Enseignant(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    modules = models.ManyToManyField(Module)
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE)

class Etudiant(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    groupe = models.ForeignKey(Groupe, on_delete=models.CASCADE)

class TypeSalle(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self) -> str:
        return self.name

class Salle(models.Model):
    name = models.CharField(max_length=100)
    type = models.ForeignKey(TypeSalle, on_delete=models.CASCADE)
    capacity = models.IntegerField()

    def is_available(self, day, start_time, end_time):
        conflicting_seances = Seance.objects.filter(
            salle=self,
            day=day,
            start_time__lt=end_time,
            end_time__gt=start_time,
        )
        return not conflicting_seances.exists()

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
    start_time = models.TimeField(default=datetime.time(8, 00))
    end_time = models.TimeField(default=datetime.time(10, 00))
    type = models.CharField(max_length=100)


    # def clean(self):
    #     assigned_modules = self.enseignant.modules.all()
    #     if self.subject not in assigned_modules:
    #         raise ValidationError('The teacher is not assigned to this module.')
        
    #     conflicting_seances = Seance.objects.filter(
    #         enseignant=self.enseignant,
    #         groupe=self.groupe,
    #         day=self.day
    #     ).exclude(pk=self.pk)

    #     module_volume = int(self.subject.volume)
    #     total_volume = sum(int(seance.subject.volume) for seance in conflicting_seances)
    #     if total_volume + module_volume > 1:
    #         raise ValidationError('The module exceeds the hourly volume limit for the group.')
        
    #     conflicting_seances = Seance.objects.filter(
    #         enseignant=self.enseignant,
    #         day=self.day,
    #         start_time__lt=self.end_time,
    #         end_time__gt=self.start_time
    #     )
    #     if conflicting_seances.exists():
    #         raise ValidationError('The teacher is already scheduled to teach during this time.')
        
    #     if not self.salle.is_available(self.day, self.start_time, self.end_time):
    #         raise ValidationError('The salle is already booked for another seance during this time.')
