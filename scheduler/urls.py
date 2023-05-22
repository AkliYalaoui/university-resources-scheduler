from django.urls import path

from . import views

# URLConf
urlpatterns = [
    path("home/", views.home_view, name="home"),
    path("programs/", views.programs_view, name="programs"),
    path("students/", views.students_view, name="students"),
    path("teachers/", views.teachers_view, name="teachers"),
    path("formations/", views.formations_view, name="formations"),
    path("sections/", views.sections_view, name="sections"),
    path("groups/", views.groups_view, name="groups"),
    path("semesters/", views.semesters_view, name="semesters"),
    path("salles/", views.salles_view, name="salles"),
    path("modules/", views.modules_view, name="modules"),
    path("login/", views.login_view, name="login"),
    path('logout/', views.logout_view, name='logout'),
]