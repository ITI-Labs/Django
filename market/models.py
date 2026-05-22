from django.db import models

LEVEL_CHOICES = [
    ('L1', 'Level 1'),
    ('L2', 'Level 2'),
    ('L3', 'Level 3'),
    ('L4', 'Level 4'),
    ('L5', 'Level 5'),
    ('L6', 'Level 6'),
]

GENDER_CHOICES = [
    ('M', 'Male'),
    ('F', 'Female'),
]

class Teacher(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    salary = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class Course(models.Model):
    name = models.CharField(max_length=100)
    hours = models.IntegerField()
    level = models.CharField(max_length=2, choices=LEVEL_CHOICES)
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True, related_name='courses')

    def __str__(self):
        return self.name

class Student(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    image = models.ImageField(upload_to='students/', null=True, blank=True)
    age = models.IntegerField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    address = models.TextField()
    level = models.CharField(max_length=2, choices=LEVEL_CHOICES)
    courses = models.ManyToManyField(Course, through='Enrollment', related_name='students')

    def __str__(self):
        return self.name

class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    grade = models.CharField(max_length=2, blank=True, null=True)

    class Meta:
        unique_together = ('student', 'course')

    def __str__(self):
        return f"{self.student.name} - {self.course.name}"
