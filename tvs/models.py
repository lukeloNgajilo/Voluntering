from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator,RegexValidator, FileExtensionValidator
from django.db import models,connection
import os
from django.core.exceptions import ValidationError


# Create your models here.
# To be used in database (AutoGenerated)

CERT = (
    ('None','None'),
        ('Certificate level', 'Certificate level'), ('Diploma level', 'Diploma level'), ('Degree level', 'Degree level')
        , ('Masters level', 'Masters level'))

def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.pdf','.docx']
    if not ext in valid_extensions:
        raise ValidationError('Unsupported file extension, Only PDF or DOCX allowed.')


class Regions(models.Model):
    RegionCode = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20)

    def __str__(self):
         return self.name

class Council(models.Model):
    name = models.CharField(max_length=20 ,default="none")
    CouncilCode = models.IntegerField(primary_key=True)
    Regions = models.ForeignKey(Regions,on_delete=models.CASCADE)

    def __str__(self):
         return self.name

class Ward(models.Model):
      name = models.CharField(max_length=20)
      WardCode = models.IntegerField(primary_key=True)
      Council = models.ForeignKey(Council,on_delete=models.CASCADE)

      def __str__(self):
            return self.name

class School(models.Model):
    name = models.CharField(max_length=20)
    ward = models.ForeignKey(Ward,on_delete=models.CASCADE)

    def __str__(self):
        return self.name

# Volunteer details on Applying
class Volunteer(models.Model):
    reg = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    username = models.CharField(max_length=50, null=False)
    full_name = models.CharField(max_length=100,default='None')
    location = models.CharField(max_length=100, null=False)
    contact = models.CharField(validators=[reg], max_length=17, blank=True,default='None')
    carrier = models.TextField(default='None',null = True)
    experience = models.TextField(default='None',null = True)
    skills = models.TextField(default='None',null = True)
    why_volunteer = models.TextField()
    STATUS = (('Approved','Approved'),('Rejected','Rejected'),('Pending','Pending'))
    status_update = models.CharField(max_length=20,choices=STATUS,null=True)
    reason = models.TextField(default='Did not approved',null = True)
    length = models.PositiveIntegerField(default=3, validators=[MinValueValidator(3), MaxValueValidator(12)])
    education = models.CharField(max_length=20, choices=CERT,default='None',null = True)
    school = models.CharField(max_length=100,blank=True,default='None')
    ward = models.CharField(max_length=150,blank=True,default='Dar Es Salaam')
    city1 = models.ForeignKey(Regions, on_delete=models.CASCADE, related_name='city', null=True)
    council1 = models.ForeignKey(Council, on_delete=models.CASCADE, related_name='council', null=True)
    ward1 = models.ForeignKey(Ward, on_delete=models.CASCADE, related_name='ward', null=True)
    School1 = models.ForeignKey(School, on_delete=models.CASCADE, related_name='school45', null=True)
    city2 = models.ForeignKey(Regions, on_delete=models.CASCADE, related_name='city1', null=True)
    council2 = models.ForeignKey(Council, on_delete=models.CASCADE, related_name='council1', null=True)
    School2 = models.ForeignKey(School, on_delete=models.CASCADE, related_name='school1', null=True)
    ward2 = models.ForeignKey(Ward, on_delete=models.CASCADE, related_name='ward1', null=True)
    city3 = models.ForeignKey(Regions, on_delete=models.CASCADE, related_name='city2', null=True)
    council3 = models.ForeignKey(Council, on_delete=models.CASCADE, related_name='council2', null=True)
    ward3 = models.ForeignKey(Ward, on_delete=models.CASCADE, related_name='ward2', null=True)
    School3 = models.ForeignKey(School, on_delete=models.CASCADE, related_name='school2', null=True)

    def __str__(self):
        return self.full_name
# files to upload for chart population
class Upload(models.Model):
    year_validator = RegexValidator(regex=r'^[0-9]+$', message="Only numbers are allowed")
    file_name_validator =  RegexValidator(regex=r'(?!sample\b)\b\w+',message="sample is a reserved name")
    filename = models.CharField(max_length=50,primary_key = True)
    year = models.CharField(validators=[year_validator],max_length=4)
    allocations = models.FileField(upload_to="documents/")

    # return file name of the csv file
    def __str__(self):
        return self.filename


# data used in chart
#todo add other fileds such as school,+ward
class Chart(models.Model):
    region = models.CharField(max_length=20)
    enrolment = models.CharField(max_length=20)
    teacher = models.CharField(max_length=20)
    ptr = models.CharField(max_length=20)
    ward = models.CharField(max_length=50)
    school = models.CharField(max_length=65)

    # used in production (Large data)
    # @classmethod
    # def truncate(cls):
    #     with connection.cursor() as cursor:
    #         cursor.execute('TRUNCATE TABLE "{0}" CASCADE'.format(cls._meta.db_table))


# Used to store user details
class Users(models.Model):
    reg = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    home_address = models.CharField(max_length=100, null=True)
    phone_number = models.CharField(validators=[reg], max_length=17, blank=True)
    POSITION = (('Student', 'Student'), ('Teacher', 'Teacher'))
    role = models.CharField(max_length=10, choices=POSITION)
    SUBJECT = (('Arts','Arts'),('Science','Science'))
    subjects = models.CharField(max_length=10, choices=SUBJECT)
    resume = models.FileField(upload_to="resume/",null=True, blank=True,
    validators=[validate_file_extension],
    help_text=('Please upload a PDF File'))

# Used in controling  volunteer allocation (short distance)
class Region(models.Model):
     id = models.AutoField(primary_key=True)
     region = models.CharField(max_length=100, null=True)
     lat = models.CharField(max_length=10, null=True)
     long = models.CharField(max_length=10, null=True)

# containing web_push details
class Push(models.Model):
    id = models.AutoField(primary_key=True)
    userKey = models.CharField(max_length=400, null=True)
    appKey = models.CharField(max_length=400, null=True)
    appId = models.CharField(max_length=400, null=True)

# store all the canceled applications
class CancelledApplication(models.Model):
    name = models.CharField(max_length=100, null=True)
    canceling_reason = models.TextField()
