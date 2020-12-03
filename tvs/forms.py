from django import forms
import csv
from django.contrib.auth.models import User

from tvs.models import Volunteer, Users, Upload, CancelledApplication


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class' : 'form-control'})
        self.fields['first_name'].widget.attrs.update({'class' : 'form-control'})
        self.fields['last_name'].widget.attrs.update({'class' : 'form-control'})
        self.fields['email'].widget.attrs.update({'class' : 'form-control'})
        self.fields['password'].widget.attrs.update({'class' : 'form-control'})

POSITION = (('Student', 'Student'), ('Teacher', 'Teacher'))
SUBJECT = (('Arts', 'Arts'), ('Science', 'Science'))

class LoginForm(forms.Form):
    username = forms.CharField(max_length=20, widget=(forms.TextInput(attrs={'class': 'form-control', 'placeholedr': 'Emai or Username','id':'fi'})))
    password = forms.CharField(max_length=20, widget=(forms.PasswordInput(attrs={'class': 'form-control', 'placeholedr': 'Password','id':'si'})))

#validate file size !> 9MB
def file_size(value):
    limit = 9 * 1024 * 1024
    if value.size > limit:
        raise forms.ValidationError('File too large. Size not more than 9 MiB')

# user more info in completing sign up
class UserMoreInfo(forms.ModelForm):
    resume = forms.FileField(label='Upload a Resume', validators=[file_size])
    class Meta:
        model = Users
        fields = ['home_address', 'phone_number', 'role','subjects','resume']
        widgets = {'role': forms.Select(choices=POSITION),'subjects':forms.Select(choices=SUBJECT)}



    def __init__(self, *args, **kwargs):
        super(UserMoreInfo, self).__init__(*args, **kwargs)
        self.fields['resume'].required = False
        self.fields['home_address'].widget.attrs.update({'class' : 'form-control'})
        self.fields['phone_number'].widget.attrs.update({'class' : 'form-control'})
        self.fields['role'].widget.attrs.update({'class' : 'form-control'})
        self.fields['subjects'].widget.attrs.update({'class' : 'form-control'})
        self.fields['resume'].widget.attrs.update({'class' : 'form-control'})
 
LEVELS = (('None','None'),
        ('certificate', 'Certificate Level'), 
        ('diploma', 'Diploma Level'),
         ('degree', 'Degree Level')
        , ('master', 'Masters Level'))

# apply form fields
class CVUpload(forms.ModelForm):
    length = forms.IntegerField(label='Length (in months)', min_value=3, max_value=12)

    class Meta:
        model = Volunteer
        fields = ['full_name', 'contact', 'education', 'carrier'
            , 'experience', 'skills', 'why_volunteer', 'length']
        widgets = {'education': forms.Select(choices=LEVELS)}
        required = 'length'
    
    def __init__(self, *args, **kwargs):
        super(CVUpload, self).__init__(*args, **kwargs)
        self.fields['full_name'].widget.attrs.update({'class' : 'form-control'})
        self.fields['contact'].widget.attrs.update({'class' : 'form-control'})
        self.fields['education'].widget.attrs.update({'class' : 'form-control'})
        self.fields['carrier'].widget.attrs.update({'class' : 'form-control'})
        self.fields['experience'].widget.attrs.update({'class' : 'form-control'})
        self.fields['skills'].widget.attrs.update({'class' : 'form-control'})
        self.fields['why_volunteer'].widget.attrs.update({'class' : 'form-control'})
        self.fields['length'].widget.attrs.update({'class' : 'form-control'})


# cancel from fields
class Cancel(forms.ModelForm):
    class Meta:
        model = CancelledApplication
        fields = ['canceling_reason']
        required = 'canceling_reason'

    def __init__(self, *args, **kwargs):
        super(Cancel, self).__init__(*args, **kwargs)
        self.fields['canceling_reason'].widget.attrs.update({'class' : 'form-control'})

# when a user has uploaded resume
class VolunteerApply(forms.ModelForm):
    length = forms.IntegerField(label='Length (in months)', min_value=3, max_value=12)

    class Meta:
        model = Volunteer
        fields = ['why_volunteer','length']
        required = 'length'

    def __init__(self, *args, **kwargs):
        super(VolunteerApply, self).__init__(*args, **kwargs)
        self.fields['why_volunteer'].widget.attrs.update({'class' : 'form-control'})
        self.fields['length'].widget.attrs.update({'class' : 'form-control'})



# validate csv file
def validate_csv_file_extension(value):
    if not value.name.endswith('.csv'):
        raise forms.ValidationError("Only CSV file is accepted")



# manage, data upload
class UploadData(forms.ModelForm):
    allocations = forms.FileField(label='Upload Teachers Data', validators=[validate_csv_file_extension])

    class Meta:
        model = Upload
        fields = ['filename', 'year', 'allocations']
        required = ['filename', 'allocations']
    
    def __init__(self, *args, **kwargs):
        super(UploadData, self).__init__(*args, **kwargs)
        self.fields['filename'].widget.attrs.update({'class' : 'form-control'})
        self.fields['year'].widget.attrs.update({'class' : 'form-control'})
        self.fields['allocations'].widget.attrs.update({'class' : 'form-control'})




