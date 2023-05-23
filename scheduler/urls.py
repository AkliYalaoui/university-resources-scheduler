from django.urls import path

from . import views

# URLConf
urlpatterns = [
    path("", views.home_view, name="home"),
    path("workspaces/students", views.students_home_view, name="students_workspaces"),
    path("workspaces/teachers", views.teachers_home_view, name="teachers_workspaces"),
    path("programs/<int:group_id>", views.programs_view, name="programs"),
    path("students/", views.students_view, name="students"),
    path("students/<int:student_id>", views.student_details_view, name="student_details"),
    path("teachers/", views.teachers_view, name="teachers"),
    path("teachers/<int:teacher_id>", views.teacher_details_view, name="teacher_details"),
    path("formations/", views.formations_view, name="formations"),
    path("sections/", views.sections_view, name="sections"),
    path("groups/", views.groups_view, name="groups"),
    path("semesters/", views.semesters_view, name="semesters"),
    path("salles/", views.salles_view, name="salles"),
    path("modules/", views.modules_view, name="modules"),
    path("accounts/login/", views.login_view, name="login"),
    path('logout/', views.logout_view, name='logout'),
]