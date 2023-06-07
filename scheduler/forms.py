from django import forms
from .models import Etudiant, Formation, Section, Groupe, Semestre, Salle, Module, Seance


class StudentForm(forms.ModelForm):
    class Meta:
        model = Etudiant
        fields = ('user', 'groupe')


class FormationForm(forms.ModelForm):
    class Meta:
        model = Formation
        fields = "__all__"

class SectionForm(forms.ModelForm):
    class Meta:
        model = Section
        fields = ("name",)
class GroupForm(forms.ModelForm):
    class Meta:
        model = Groupe
        fields = "__all__"

class ModuleForm(forms.ModelForm):
    class Meta:
        model = Module
        fields = "__all__"

class SemestreForm(forms.ModelForm):
    class Meta:
        model = Semestre
        fields = "__all__"

# class GradeForm(forms.ModelForm):
#     class Meta:
#         model = Grade
#         fields = "__all__"
# class TypeSalleForm(forms.ModelForm):
#     class Meta:
#         model = TypeSalle
#         fields = "__all__"

class SalleForm(forms.ModelForm):
    class Meta:
        model = Salle
        fields = ["name", "capacity", "type"]

class ProgramForm(forms.ModelForm):
    class Meta:
        model = Seance
        fields = "__all__"