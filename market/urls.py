from django.urls import path, include
from rest_framework.routers import DefaultRouter
from market import views
from market.api_views import StudentViewSet, CourseViewSet, TeacherViewSet, EnrollmentViewSet, SignupView, login_view, signup_view, logout_view

router = DefaultRouter()
router.register(r'api/students', StudentViewSet)
router.register(r'api/courses', CourseViewSet)
router.register(r'api/teachers', TeacherViewSet)
router.register(r'api/enrollments', EnrollmentViewSet)

urlpatterns = [
    path('', views.home, name='home_page'),
    path('students/', views.student_filter, name='student_filter'),
    path('students/add/', views.add_student, name='add_student'),
    path('courses/', views.course_filter, name='course_filter'),
    path('courses/add/', views.add_course, name='add_course'),
    path('teachers/', views.teacher_filter, name='teacher_filter'),
    path('teachers/add/', views.add_teacher, name='add_teacher'),
    path('assign-teacher/<int:course_id>/', views.assign_teacher, name='assign_teacher'),
    path('enroll/<int:student_id>/', views.add_course_to_student, name='enroll_student'),
    path('students/edit/<int:student_id>/', views.edit_student, name='edit_student'),
    path('students/delete/<int:student_id>/', views.delete_student, name='delete_student'),
    path('teachers/edit/<int:teacher_id>/', views.edit_teacher, name='edit_teacher'),
    path('teachers/delete/<int:teacher_id>/', views.delete_teacher, name='delete_teacher'),
    path('courses/edit/<int:course_id>/', views.edit_course, name='edit_course'),
    path('courses/delete/<int:course_id>/', views.delete_course, name='delete_course'),
    path('login/', login_view, name='login_view'),
    path('signup/', signup_view, name='signup_view'),
    path('logout/', logout_view, name='logout_view'),
    path('api/signup/', SignupView.as_view(), name='api_signup'),
    path('api-auth/', include('rest_framework.urls')),
    path('', include(router.urls)),
]
