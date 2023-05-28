from django.urls import path

from .views.auth import login_view, logout_view, profile_view
from .views.students import students_home_view, students_view, student_details_view
from .views.teachers import teachers_home_view, teachers_view, teacher_details_view
from .views.grades import grades_view, grade_details_view
from .views.admins import admins_view, admin_details_view
from .views.formations import formations_view, formation_details_view
from .views.home import home_view
from .views.sections import sections_view, section_details_view
from .views.groups import groups_view, group_details_view, allowed_sessions_view
from .views.semesters import semesters_view, semester_details_view
from .views.salles import salles_view, salle_details_view
# from .views.type_salles import type_salles_view, type_salle_details_view
from .views.modules import modules_view, module_details_view

urlpatterns = [
    path("", home_view, name="home"),
    path("workspaces/students", students_home_view, name="students_workspaces"),
    path("workspaces/teachers", teachers_home_view, name="teachers_workspaces"),
    path("admins/", admins_view, name="admins"),
    path("admins/<int:admin_id>", admin_details_view, name="admin_details"),
    path("students/", students_view, name="students"),
    path("students/<int:student_id>", student_details_view, name="student_details"),
    path("teachers/", teachers_view, name="teachers"),
    path("teachers/<int:teacher_id>", teacher_details_view, name="teacher_details"),
    path("grades/", grades_view, name="grades"),
    path("grades/<int:grade_id>", grade_details_view, name="grade_details"),
    path("formations/", formations_view, name="formations"),
    path("formations/<int:formation_id>", formation_details_view, name="formation_details"),
    path("sections/", sections_view, name="sections"),
    path("sections/<int:section_id>", section_details_view, name="section_details"),
    path("groups/", groups_view, name="groups"),
    path("groups/<int:group_id>", group_details_view, name="group_details"),
    path("sessions/<int:group_id>/<int:semester_id>", allowed_sessions_view, name="allowed_sessions"),
    path("semesters/", semesters_view, name="semesters"),
    path("semesters/<int:semester_id>", semester_details_view, name="semester_details"),
    path("salles/", salles_view, name="salles"),
    path("salles/<int:salle_id>", salle_details_view, name="salle_details"),
    # path("type-salles/", type_salles_view, name="type_salles"),
    # path("type-salles/<int:type_id>", type_salle_details_view, name="type_salle_details"),
    path("modules/", modules_view, name="modules"),
    path("modules/<int:module_id>", module_details_view, name="module_details"),
    path("accounts/profile/", profile_view, name="profile"),
    path("accounts/login/", login_view, name="login"),
    path('logout/', logout_view, name='logout'),
]