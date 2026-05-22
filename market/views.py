from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Student, Course, Teacher, Enrollment
from rest_framework.authtoken.models import Token

@login_required
def home(request):
    students = Student.objects.all()
    courses = Course.objects.all()
    teachers = Teacher.objects.all()
    return render(request, 'home.html', {
        'students': students,
        'courses': courses,
        'teachers': teachers,
    })

@login_required
def student_filter(request):
    level = request.GET.get('level', '')
    students = Student.objects.all()
    if level:
        students = students.filter(level=level)
    return render(request, 'student_list.html', {'students': students, 'level': level})

@login_required
def course_filter(request):
    hours = request.GET.get('hours', '')
    courses = Course.objects.all()
    if hours:
        courses = courses.filter(hours=hours)
    return render(request, 'course_list.html', {'courses': courses, 'hours': hours})

@login_required
def teacher_filter(request):
    teachers = Teacher.objects.all()
    return render(request, 'teacher_list.html', {'teachers': teachers})

@login_required
def assign_teacher(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    teachers = Teacher.objects.all()
    if request.method == 'POST':
        teacher_id = request.POST.get('teacher_id')
        teacher = get_object_or_404(Teacher, id=teacher_id)
        course.teacher = teacher
        course.save()
        return redirect('course_filter')
    return render(request, 'assign_teacher.html', {'course': course, 'teachers': teachers})

@login_required
def add_student(request):
    if request.method == 'POST':
        name = request.POST['name']
        phone = request.POST['phone']
        age = request.POST['age']
        gender = request.POST['gender']
        address = request.POST['address']
        level = request.POST['level']
        image = request.FILES.get('image')
        Student.objects.create(name=name, phone=phone, age=age, gender=gender, address=address, level=level, image=image)
        return redirect('student_filter')
    return render(request, 'student_add.html')

@login_required
def edit_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if request.method == 'POST':
        student.name = request.POST['name']
        student.phone = request.POST['phone']
        student.age = request.POST['age']
        student.gender = request.POST['gender']
        student.address = request.POST['address']
        student.level = request.POST['level']
        if request.FILES.get('image'):
            student.image = request.FILES['image']
        student.save()
        return redirect('student_filter')
    return render(request, 'student_add.html', {'student': student})

@login_required
def delete_student(request, student_id):
    get_object_or_404(Student, id=student_id).delete()
    return redirect('student_filter')

@login_required
def add_teacher(request):
    if request.method == 'POST':
        Teacher.objects.create(
            name=request.POST['name'],
            age=request.POST['age'],
            salary=request.POST['salary'],
        )
        return redirect('teacher_filter')
    return render(request, 'teacher_add.html')

@login_required
def edit_teacher(request, teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id)
    if request.method == 'POST':
        teacher.name = request.POST['name']
        teacher.age = request.POST['age']
        teacher.salary = request.POST['salary']
        teacher.save()
        return redirect('teacher_filter')
    return render(request, 'teacher_add.html', {'teacher': teacher})

@login_required
def delete_teacher(request, teacher_id):
    get_object_or_404(Teacher, id=teacher_id).delete()
    return redirect('teacher_filter')

@login_required
def add_course(request):
    teachers = Teacher.objects.all()
    if request.method == 'POST':
        teacher_id = request.POST.get('teacher_id')
        Course.objects.create(
            name=request.POST['name'],
            hours=request.POST['hours'],
            level=request.POST['level'],
            teacher_id=teacher_id if teacher_id else None,
        )
        return redirect('course_filter')
    return render(request, 'course_add.html', {'teachers': teachers})

@login_required
def edit_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    teachers = Teacher.objects.all()
    if request.method == 'POST':
        course.name = request.POST['name']
        course.hours = request.POST['hours']
        course.level = request.POST['level']
        teacher_id = request.POST.get('teacher_id')
        course.teacher_id = teacher_id if teacher_id else None
        course.save()
        return redirect('course_filter')
    return render(request, 'course_add.html', {'course': course, 'teachers': teachers})

@login_required
def delete_course(request, course_id):
    get_object_or_404(Course, id=course_id).delete()
    return redirect('course_filter')

@login_required
def add_course_to_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    courses = Course.objects.all()
    error = ''
    if request.method == 'POST':
        course_id = request.POST.get('course_id')
        grade = request.POST.get('grade', '')
        course = get_object_or_404(Course, id=course_id)
        if student.level != course.level:
            error = f"Student level ({student.level}) does not match course level ({course.level})"
        elif not course.teacher:
            error = f"Course '{course.name}' has no teacher assigned yet"
        elif Enrollment.objects.filter(student=student, course=course).exists():
            error = f"Student is already enrolled in '{course.name}'"
        else:
            Enrollment.objects.create(student=student, course=course, grade=grade)
            return redirect('student_filter')
    return render(request, 'enroll_student.html', {'student': student, 'courses': courses, 'error': error})
