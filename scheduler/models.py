from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime
from django.core.exceptions import ValidationError

class Semestre(models.Model):
    name = models.CharField(max_length=100)
    start = models.CharField(max_length=100)
    end = models.CharField(max_length=100)

    SESSION_CHOICES = (
        ('février', 'Février'),
        ('juin', 'Juin'),
    )

    session = models.CharField(max_length=10, choices=SESSION_CHOICES, default="février")

class Formation(models.Model):
    name = models.CharField(max_length=100, unique=True)
    niveau = models.CharField(max_length=100)
    nb_semestre = models.IntegerField(default=2)

class Module(models.Model):
    name = models.CharField(max_length=100, unique=True)
    weekly_volume = models.IntegerField(default=5)
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
    name = models.CharField(max_length=200, unique=True)
    
    def __str__(self) -> str:
        return self.name

class Enseignant(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    daily_load = models.IntegerField(default=6)
    modules = models.ManyToManyField(Module)
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE)

class Etudiant(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    groupe = models.ForeignKey(Groupe, on_delete=models.CASCADE)

# class TypeSalle(models.Model):
#     name = models.CharField(max_length=200)
#     def __str__(self) -> str:
#         return self.name

class Salle(models.Model):
    name = models.CharField(max_length=100, unique=True)
    # type = models.ForeignKey(TypeSalle, on_delete=models.CASCADE)
    TYPE_CHOICES = (
        ('td', 'TD'),
        ('tp', 'TP'),
        ('amphitheater', 'Amphitheater'),
    )

    type = models.CharField(max_length=15, choices=TYPE_CHOICES)
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
    start_time = models.TimeField(default=datetime.time(8, 00))
    end_time = models.TimeField(default=datetime.time(10, 00))

    TYPE_CHOICES = (
        ('td', 'TD'),
        ('tp', 'TP'),
        ('cours', 'Cours'),
    )

    type = models.CharField(max_length=10, choices=TYPE_CHOICES)


    def clean(self): pass

        # existing_seances = Seance.objects.filter(
        #     enseignant=self.enseignant,
        #     day=self.day,
        #     start_time__lt=self.end_time,
        #     end_time__gt=self.start_time
        # ).exclude(pk=self.pk)
        # if existing_seances.exists():
        #     raise ValidationError('Enseignant est déjà occupé à ce créneau horaire')
        
        # conflicting_seances = Seance.objects.filter(
        #     salle=self.salle,
        #     day=self.day,
        #     start_time__lt=self.end_time,
        #     end_time__gt=self.start_time
        # )
        # if conflicting_seances.exists():
        #     raise ValidationError('la salle est déjà occupée à ce créneau horaire')
        
        # daily_load = Seance.objects.filter(enseignant=self.enseignant, day=self.day).exclude(pk=self.pk).aggregate(total=models.Sum(models.F('end_time') - models.F('start_time')))['total']
        # MAX_DAILY_LOAD = 12
        # if daily_load and (daily_load + (self.end_time - self.start_time)) > MAX_DAILY_LOAD:
        #     raise ValidationError("la charge journalière maximale de l'enseignant est atteinte")

        # if self.type == 'tp' and self.salle.type in ['amphitheater', 'td']:
        #     raise ValidationError('A TP session cannot be scheduled in an amphitheater or TD room.')
        
        # if self.type in ['td', 'cours'] and self.salle.type == 'tp':
        #     raise ValidationError('A td or course session cannot be scheduled in a TP room.')
        
        # if self.salle.capacity < Etudiant.objects.filter(groupe=self.groupe).count():
        #     raise ValidationError('The capacity of the room is insufficient for the group size.')
        
        # assigned_modules = self.enseignant.modules.all()
        # if self.subject not in assigned_modules:
        #     raise ValidationError('The teacher is not assigned to this module.')
        

        # Check if the session type is TD or TP and validate the group and section assignment
        # if self.type in ['td', 'tp']:
        #     group_section = self.groupe.section

        #     # Check if a course session is assigned to the section of the group
        #     conflicting_sessions = Seance.objects.filter(
        #         type='cours',
        #         groupe__section=group_section,
        #         start_time__lt=self.end_time,
        #         end_time__gt=self.start_time
        #     )

        #     if conflicting_sessions.exists():
        #         raise ValidationError('A course session is already assigned to the section of this group.')

        # elif self.type == 'cours':
        #     section = self.groupe.section

        #     # Check if a TD or TP session is assigned to any group within the section
        #     conflicting_sessions = Seance.objects.filter(
        #         type__in=['td', 'tp'],
        #         groupe__section=section,
        #     )

        #     if conflicting_sessions.exists():
        #         raise ValidationError('A TD or TP session is already assigned to a group within this section.')