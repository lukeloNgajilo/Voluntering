import matplotlib.pyplot as plt
import pandas as pd
import xhtml2pdf.pisa as pisa
import csv,os,glob,filecmp,ipinfo,asyncio
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from django.shortcuts import render as render, redirect
from django.template.loader import get_template
from django.views.generic import View
from io import BytesIO
from sklearn.linear_model import LinearRegression
from pyresparser import ResumeParser
from django.core.exceptions import ValidationError
from django.contrib import messages
from tvs.models import *
from tvs import models as models
# class to return data for visual
from tvs.datatype import PtrDetails, UserStatusDetail, ToMap1
from tvs.models import Users,Chart,Region,Push
from .forms import UserForm, CVUpload, UserMoreInfo, UploadData, VolunteerApply, Cancel,LoginForm
from tvs import admin
from django.db.models import Value,Max
from haversine import haversine
import json
from django.core import serializers
# Create your views here.

#loop = asyncio.get_event_loop()


# class to check the highest ptr
class Ptr(object):
    @staticmethod
    def check_ptr():
        module_data = models.Chart.objects.all()

        check = []

        for i in module_data:

            if float(i.ptr) > 50:
                data = PtrDetails(i.region, i.ptr)
                check.append(data)
        return check


class MapTz(object):
    @staticmethod
    def cross_check_map():
        filter_ptr = Ptr.check_ptr()
        patch_data_map = []
        for i in filter_ptr:
            if i.region == 'DODOMA':
                i.region = 'tz-do'
            elif i.region == 'GEITA':
                i.region = 'tz-ge'
            elif i.region == 'KATAVI':
                i.region = 'tz-ka'
            elif i.region == 'KIGOMA':
                i.region = 'tz-km'
            elif i.region == 'MARA':
                i.region = 'tz-ma'
            elif i.region == 'RUKWA':
                i.region = 'tz-rk'
            elif i.region == 'SHINYANGA':
                i.region = 'tz-sh'
            elif i.region == 'SIMIYU':
                i.region = 'tz-si'
            elif i.region == 'SINGIDA':
                i.region = 'tz-sd'
            elif i.region == 'SONGWE':
                i.region = 'nill'
            elif i.region == 'TABORA':
                i.region = 'tz-tb'
            elif i.region == 'MOROGORO':
                i.region = 'tz-mo'
            elif i.region == 'MWANZA':
                i.region = 'tz-mw'
            elif i.region == 'KAGERA':
                i.region = 'tz-kr'
            elif i.region == 'ARUSHA':
                i.region = 'tz-as'
            elif i.region == 'MANYARA':
                i.region = 'tz-my'
            elif i.region == 'KILIMANJARO':
                i.region = 'tz-kl'
            elif i.region == 'TANGA':
                i.region = 'tz-tn'
            elif i.region == 'PWANI':
                i.region = 'tz-pw'
            elif i.region == 'DAR ES SALAAM':
                i.region = 'tz-ds'
            elif i.region == 'LINDI':
                i.region = 'tz-li'
            elif i.region == 'MTWARA':
                i.region = 'tz-mt'
            elif i.region == 'RUVUMA':
                i.region = 'tz-rv'
            elif i.region == 'NJOMBE':
                i.region = 'tz-nj'
            elif i.region == 'MBEYA':
                i.region = 'tz-mb'
            elif i.region == 'IRINGA':
                i.region = 'tz-ir'

            pair_data_map = [i.region, float(i.ptr)]
            data_map = ToMap1(pair_data_map)
            patch_data_map.append(data_map)
        return patch_data_map

# add regions method
def add_regions(data):
        for row in csv.DictReader(open(data)):
            base_data = Region()
            base_data.region = str(row['region']).upper()
            base_data.lat = row['lat']
            base_data.long = row['long']
            base_data.save()

# the first page to see even if user has not logged in
def index(request):
    # total users
    total_user = models.Users.objects.all().count()
    # total volunteers
    total_volunteer = models.Volunteer.objects.all().count()
    #get region co-ordinate data
    region_coordinates = models.Region.objects.all().count()
    # read and save them to a model if not exists
    if region_coordinates == 0:
        data_path = 'media/coordinates/region_cdnts.csv'
        #run async
        loop.run_in_executor(None,add_regions,data_path)

    predict = PTRDataPrediction()
    prediction = int(predict.estimatePrediction())
    # pass_to_html
    pass_data = {
        'username': request.user.username.capitalize(),
        'users': total_user,
        'volunteers' : total_volunteer,
        'predict':prediction
    }
    return render(request, 'index.html',pass_data)

# populate data from ToChart Model
class ChartData(object):

    # count data from ToChart Model
    @staticmethod
    def get_objects():
        return models.Chart.objects.all()

    @staticmethod
    def check_valve_data():
        data = {'region': [], 'enrolment': [],
                'teacher': [], 'ptr': [],'school':[],'ward':[]}

        datum = models.Chart.objects.all()
      

        for unit in datum:
                data['region'].append(unit.region)
                data['enrolment'].append(unit.enrolment)
                data['teacher'].append(unit.teacher)
                data['ptr'].append(unit.ptr)
        return data

#read data from file and add to model
def read_and_add(file_path):
        for row in csv.DictReader(open(file_path)):
             data = Chart()
             data.region = row['REGION']
             data.enrolment = row['ENROLMENT']
             data.teacher = row['ALL TEACHERS']
             data.ptr = row['PTR']
             data.school = row['SCHOOL']
             data.ward = row['WARD']
             data.save()

# delete the existing table
def delete_table():
    ChartData.get_objects().delete()

@login_required
def home(request, chartID='container', chart_type='column', chart_height=600):
    global x, y, z
    data = ChartData.check_valve_data()
    push_details = Push()
    push_length = models.Push.objects.all().count()
    user = models.Users.objects.all().count()
    volunteer = models.Volunteer.objects.all().count()
    path_filename = "media/doc_usage/used_path.txt"

    # add web push details
    if push_length == 0:
        push_details.userKey = 'MmI2NmU2NjktODNkYS00MjkyLWJhNjgtMDY1OGFiYjliYzg3'
        push_details.appKey = 'MjdkY2FjMTctYTEyMi00MjEzLWJjNWQtMGE0YmU0ZDQxMmIz'
        push_details.appId = '5aa60fa3-6edd-43ff-a55a-e4e03618c388'
        push_details.save()

    #get file list from CVS Model
    filename_list = models.Upload.objects.values('allocations')

    chart_value_list = ChartData.get_objects().count()
    #get list of files
    list_of_files_db = []
    
     
    # add files from db to list
    for files in filename_list:
        list_of_files_db.append(files['allocations'])
    
    # automatically to True used in filecmp
    update_chart = False
    #file path to be uploaded in chart
    chart_path = ''
    # integrate the files from CSV Models with the existing (\documents)
    if filename_list.count() > 1:
        latest_file_from_db = list_of_files_db[list_of_files_db.__len__()-1]
        #dealing with the latest 2 files to be added in database
        for f in range(2):
            #if latest file return to condition
            if list_of_files_db[f] == latest_file_from_db:
                continue
            #if files are the same do not update chart
            file1 = "media/"+list_of_files_db[f]
            file2 = "media/"+latest_file_from_db
            if not filecmp.cmp(file1,file2,shallow=False):
                chart_path = "media/"+latest_file_from_db
                read_saved_path = open(path_filename)
                message = read_saved_path.read()

                #compare the last saved path with the current
                if chart_path != message:
                #update chart
                    update_chart = True
                break


    if chart_value_list == 0 or update_chart:
        if update_chart:
            #help later in judging deleting model data
            file = open(path_filename,"w")
            file.write(chart_path)
            file.close()
            #delete an existing table asynchronously
            loop.run_in_executor(None,delete_table,None)

        else:
            chart_path = 'media/documents/sample.csv'
            #open empty file to store latest db filepath
            open_empty = open(path_filename,"w")
            open_empty.close()

        # add chart data asynchronously
        loop.run_in_executor(None,read_and_add,chart_path)
        

    # load prediction
    predict = PTRDataPrediction()
    prediction = predict.estimatePrediction()

    # username
    username = request.user.username
    

    teach = data['teacher']
    enrol = data['enrolment']
    ptr = data['ptr']
    region = data['region']

    filter_ptr = Ptr.check_ptr()
    filter_map = MapTz.cross_check_map()

    # iterate the list string parse to float
    teach_data = []
    enrol_data = []
    ptr_data = []
    for x in teach:
        y = float(x)
        teach_data.append(y)

    for x in enrol:
        y = float(x)
        enrol_data.append(y)

    for x in ptr:
        y = float(x)
        ptr_data.append(y)

    chart = {"renderTo": chartID, "type": chart_type, "height": chart_height, }
    title = {"text": 'PTR Government school'}
    xAxis = {"title": {"text": 'Region'}, "categories": region}
    yAxis = {"title": {"text": 'Data'}}

    series = [
        {
            "name": 'Teacher',
            "data": teach_data
        }, {
            "name": 'Enrolment',
            "data": enrol_data
        }, {
            "name": 'PTR(Pupil to Teacher Ratio)',
            "data": ptr_data
        }
    ]


    # pair the data for the map needs
    multiple_pair = []
    for i in filter_map:
        multiple_pair.append(i.data_pair)
    
    # verifying the user status
    verify = user_status(request)

    # pass the context
    to_html = {
        'chartID': chartID, 'chart': chart,
        'series': series, 'title': title,
        'xAxis': xAxis, 'yAxis': yAxis,
        'ptr': ptr_data, 'value': filter_ptr,
        'sample': multiple_pair,
        'username': username.capitalize(),
        'status': verify.lower(),
        'predict': int(prediction),
        'users': user,
        'volunteers': volunteer
    }

    return render(request, template_name='home.html', context=to_html)

@login_required
def cancelApplication(request):
    sent_data={}
    user_name = request.user.username 
    if request.method == 'POST':
            messages.error(request,'Please Correct All Errors')

    else:
        form = Cancel()
        sent_data = {
            'form':form,
            'username':user_name,
            'users':models.Users.objects.all().count(),
        'volunteers': models.Volunteer.objects.all().count()
            }

    return render(request, template_name='apply/cancel.html', context=sent_data)



class ProfileView(View):
    def get(self, request):
        ##loop through the user data
        user_id = request.user.id
        applied = user_status(request)
        global name, firstname, lastname, email, home, phone, role,subjects
        data = models.User.objects.all()
        data1 = models.Users.objects.get(user=user_id)
        username = request.user.username
        for i in data:
            if i.username == username:
                name = username
                firstname = i.first_name
                lastname = i.last_name
                email = i.email
                home = data1.home_address
                phone = data1.phone_number
                role = data1.role
                subjects = data1.subjects


        user = models.Users.objects.all().count()
        volunteer = models.Volunteer.objects.all().count()

        to_html = {
            'users':user,
            'volunteers':volunteer,
            'applied':applied.lower(),
            'name': name,
            'firstname': firstname,
            'lastname': lastname,
            'email': email,
            'username': username,
            'home': home,
            'phone': phone,
            'role': role,
            'subjects':subjects
        }

        return render(request, 'accounts/profile.html', context=to_html)

    def post(self, request):
        username = request.user.id
        data = models.Users.objects.get(user=username)
        data1 = models.User.objects.get(username=data.user)
        if request.POST:
            login_data = request.POST.dict()
            firstname = login_data.get("firstname")
            lastname = login_data.get("lastname")
            user_name = login_data.get("username")
            email = login_data.get("email")
            name = login_data.get("home")
            phone = login_data.get("phone")
            role = login_data.get("role")
            subjects = login_data.get("subjects")
            data.phone_number = phone
            data.home_address = name
            data1.email = email
            data1.username = user_name
            data1.last_name = lastname
            data1.first_name = firstname
            if role == 'Student' or role == 'Teacher' or role == 'student' or role == 'teacher':
                if role == 'teacher':
                    role = 'Teacher'
                else:
                    role = 'Student'
                if subjects == 'Arts' or subjects == 'arts' or subjects == 'Science' or subjects == 'science':
                    if subjects == 'science':
                        subjects = 'Science'
                    else:
                        subjects = 'Arts'
                    data1.role = role
                    data.role = role
                    data1.subjects = subjects
                    data.subjects = subjects
                    data.save()
                    data1.save()
                    messages.success(request,'Changes Saved Successfully')
                else:
                    messages.error(request,'Subjects can be Arts or Science')
            else:
                messages.error(request,'Role can be a Teacher or Student')

        return redirect('profile')


def user_status(request):
    value=''
    voluntee = models.Volunteer.objects.all()
    name = request.user.username

    for i in voluntee:
        if i.username == name:
            value = i.status_update
            break
    return value



# apply.html view
@login_required
def apply(request):
    # get an applicant resume data
    resume_data=''
    name = request.user.username
    user_id = request.user.id
    global to_html, voluntee
    voluntee = 0

    #get resume file data
    # the following could be better
    users = models.Users.objects.raw('SELECT resume FROM tvs_users WHERE username = %s',[name])
    registered_users = models.Users.objects.raw('SELECT * FROM tvs_users')
    #store data extracted
    resume_path=''
    # get saved resume path per logged user
    for i in registered_users:
        if str(i.user_id) == user_id:
            resume_path = 'media/'+str(i.resume)
            break

    # check if the user uploaded a resume
    # check if the user has resume data or not
    resume_validator = False
    if resume_path:
        resume_data = ResumeParser
        inner_form = Cancel(request.POST)
        if inner_form.is_valid():
            instance = inner_form.save(commit=False)
            instance.name = name
            models.Volunteer.objects.filter(username=name).delete()
            instance.save()
            messages.success(request,'Operation Executed Successfully')
            return redirect('home')
        else:ResumeParser(resume_path).get_extracted_data()

    int_volunteer_check = user_status(request)

    if str(resume_data):
        resume_validator = True

    # user Co-ords from AS
    # if request.ipinfo:
    #     coord = request.ipinfo.loc
    # else:
    #     coord = '-6.8235,39.2695'
    #
    # if coord:
    #     coord_list = str(coord).split(',')
    #     latitude = float(coord_list[0])
    #     longitude = float(coord_list[1])
    # else:
    #     #default pointing to Dar Es Salaam
    #     latitude = float(-6.8235)
    #     longitude = float(39.2695)
    # # detected user location
    # user_location=(latitude,longitude)
    # distance_storage=[]
    # region_storage=[]
    #shortest distance using haversine 
    #get all data from region model
    # region_data = Region.objects.raw("SELECT * FROM tvs_region")
    # for result in region_data:
    #     # assign each time the coods retrieved
    #     current_cods = (float(result.lat),float(result.long))
    #     # use haversine formula to calculate the current location with each from model
    #     distance = float(haversine(user_location,current_cods))
    #     # store resulted distance
    #     distance_storage.append(distance)
    #     # store respectively region from distance > lat & long
    #     region_storage.append(result.region)
    
    # use built in pyfunction to calculate minimum value
    # shortest_distance = min(distance_storage)
    # # get a region using minimum distance index from a list
    # selected_region = region_storage[distance_storage.index(shortest_distance)]

    # get highest ptr for a chosen region
    # max_ptr = Chart.objects.filter(region=selected_region).aggregate(Max('ptr'))
    # datum = Chart.objects.filter(ptr=max_ptr['ptr__max'])
    # retreive and assign region to a user
    # for i in datum:
    #     region = i.region
    #     ward = i.ward
    #     school = i.school

    if request.method == 'POST': 
        if not resume_validator:
            form = CVUpload(request.POST, request.FILES)
            if int_volunteer_check == 'Rejected' or int_volunteer_check == '' or int_volunteer_check is None:
             if form.is_valid():
                if name:
                    # not empty
                    instance = form.save(commit=False)
                    instance.username = name
                   # request.session['contacts'] =form.cleaned_data['contact']

                    #request.session['aaabbb'] = contact
                 #   instance.location = region
                  #  instance.school = school
                  #  instance.ward = ward
                    instance.status_update = 'Pending'
                    voluntee = voluntee + 1
                    #updateChart(voluntee, region)
                    messages.success(request,'Request Submitted Successfully')
                    instance.save()
                    #send to status page
                return redirect('chooselocation')
            else:
                form.save(commit=False)
            return redirect('chooselocation')
        else:
            form_data = VolunteerApply(request.POST, request.FILES)
            print(form_data)
            if int_volunteer_check == 'Rejected' or  int_volunteer_check == '' or int_volunteer_check is None:
                if form_data.is_valid():
                    instance = form_data.save(commit=False)
                    instance.username = name
                    print(instance)
                    #instance.location = region
                    instance.school = school
                    instance.ward = ward
                    instance.status_update = 'Pending'
                    instance.full_name = str(resume_data['name'])
                    if resume_data['mobile_number']:
                        contacts = resume_data['mobile_number']
                        print(resume_data['mobile_number'])
                    elif resume_data['email']:
                        contacts = resume_data['email']

                    instance.contact = contacts

                    instance.carrier =  resume_data['designation']
                    instance.experience = resume_data['company_names']
                    instance.skills = resume_data['skills']
                    instance.education = resume_data['degree']
                    voluntee = voluntee + 1
                    updateChart(voluntee, region)
                    instance.save()
                    messages.success(request,'Request Submitted Successfully')
                    return redirect('chooselocation')
                else:
                    form_data.save(commit=False)
            return redirect('chooselocation')
    else:
        final_form=''
        if resume_validator:
            final_form = VolunteerApply()
        else:
            final_form = CVUpload()


        to_html = {
          #  'data': region,
            'form': final_form,
            'name': name,
        }
    return render(request, 'apply/apply.html', context=to_html)

# applicant status
class Status(object):
    @staticmethod
    def status(request):
        global status_update, location, school, ward, reason
        name = request.user.username
        voluntee = models.Volunteer.objects.all()
        user_status_info = user_status(request)

        detail = []

        if user_status_info == '' or user_status_info is None:
            status = 'not present, please apply'
            reason = 'please apply first'
            region = 'not allocated'
            school = 'not applied'
            ward = 'not allocated'
            length = 'not specified'
            data = UserStatusDetail(status,reason, region, school,ward,length)
            detail.append(data)
            return detail
        else:
            for i in voluntee:
                if i.username == name:
                    status_update = i.status_update
                    location = i.location
                    school = i.school
                    ward = i.ward
                    reason = i.reason
                    period = str(i.length) + ' Months'

                    if i.status_update == 'Pending':
                        change_to = 'Pending approval'
                        reasoning  = 'Please be patient, we are processing your request'
                        data = UserStatusDetail(change_to, reasoning, i.location,i.school,i.ward, period)
                        detail.append(data)
                    elif i.status_update == 'Approved':
                        data = UserStatusDetail(i.status_update, i.reason,i.location,i.school,i.ward, period)
                        detail.append(data)
                    else:
                        data = UserStatusDetail(i.status_update, i.reason, i.location,i.school,i.ward, period)
                        detail.append(data)
            return detail



# view user status
@login_required
def status_view(request):
    name = request.user.username
    voluntee_status = Status.status(request)
    applied = user_status(request)
    user = models.Users.objects.all().count()
    volunteer = models.Volunteer.objects.all().count()

    to_html = {
        'users':user,
        'volunteers':volunteer,
        'applied':applied.lower(),
        'status': voluntee_status,
        'username': name
    }
    return render(request, template_name='apply/status.html', context=to_html)


# to be finished i.e update chart data
def updateChart(increment, region):
    chartUpdate = models.Chart.objects.get(region=region)

    old = chartUpdate.teacher
    new = float(old) + float(increment)
    # chartUpdate.teacher =


# manage.html view
# approve or reject volunteers
@user_passes_test(lambda u: u.is_superuser)
def approveVolunteer(request):
    global fname, to_html
    name = request.user.username
    user_id = request.user.id
    volunteer = models.Volunteer.objects.all()
    files = models.Upload.objects.all()
    
    # queries for all education level
    cert = models.Volunteer.objects.filter(education='Certificate Level')
    cert1 = models.Volunteer.objects.filter(education='Certificate Level', status_update=str(1))
    dipl = models.Volunteer.objects.filter(education='Diploma Level')
    dipl1 = models.Volunteer.objects.filter(education='Diploma Level', status_update=str(1))
    degr = models.Volunteer.objects.filter(education='Degree Level')
    degr1 = models.Volunteer.objects.filter(education='Degree Level', status_update=str(1))
    mast = models.Volunteer.objects.filter(education='Masters Level')
    mast1 = models.Volunteer.objects.filter(education='Masters Level', status_update=str(1))

    paginator = Paginator(files, 5)

    page = request.GET.get('page')

    try:
        # create Page object for the given page
        files = paginator.page(page)
    except PageNotAnInteger:
        # if page parameter in the query string is not available, return the first page
        files = paginator.page(1)
    except EmptyPage:
        # if the value of the page parameter exceeds num_pages then return the last page
        files = paginator.page(paginator.num_pages)

    # Get the index of the current page
    index = files.number - 1  # edited to something easier without index
    # This value is maximum index of your pages, so the last page - 1
    max_index = len(paginator.page_range)
    # You want a range of 7, so lets calculate where to slice the list
    start_index = index - 3 if index >= 3 else 0
    end_index = index + 3 if index <= max_index - 3 else max_index
    # Get our new page range. In the latest versions of Django page_range returns
    # an iterator. Thus pass it to list, to make our slice possible again.
    page_range = list(paginator.page_range)[start_index:end_index]

    if request.method == 'POST':
        form = UploadData(request.POST, request.FILES)

        data = request.POST.dict()
        filename = data.get("file-name")

        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            return redirect('clean')

        # clean and upload file
        if str(filename) == "":
            messages.error(request,"Please attach a PTR File")
        else:
            if str(filename).endswith('.csv'):
                file = models.Upload.objects.all()
                for i in file:
                    if str(filename) == str(i.filename):
                    # print(i.uploadcvs)
                        AutoClean.clean_data(i.allocations)
                    # print(filename)
                        redirect('clean')
                redirect('clean')
            else:
                messages.error(request,"Please upload a CSV File")
        redirect('clean')

    else:
        form = UploadData()
        to_html = {
            'name': volunteer,
            'form': form,
            'file': files,
            'page': page_range,
            'cert': cert,
            'cert1': cert1,
            'dipl': dipl,
            'dipl1': dipl1,
            'degr': degr,
            'degr1': degr1,
            'mast': mast,
            'mast1': mast1
        }

    return render(request, template_name='admin/manage.html', context=to_html)


class UserFormView(View):
    form_class = UserForm

    # form_class_info=UserMoreInfo

    # blank form
    def get(self, request):
        form = self.form_class(None)
        return render(request, 'registration/signup-form.html', {'form': form})

    # process form data
    def post(self, request): # initial I thought it could be this method then tried to add some message to return but didn't work, Let me read some thing one minute an we resume    back...okay brother
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)

            # clean data
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            # return user objects if is valid
            user = authenticate(username=username, password=password)

            if user is not None:

                if user.is_active:
                    login(request, user)
                    user = user.username
                    to_html = {
                        'user': user
                    }
                    return redirect('complete_signup')
        return render(request, 'registration/signup-form.html', {'form': form})


def userLogout(request):
    logout(request)
    print("Output : ",request)
    return redirect('index')


def my_view(request):

    if request.method == 'POST':

        login_form = LoginForm(request.POST)

        if login_form.is_valid():

            username = request.POST['username']
            password = request.POST['password']

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                # Redirect to a success page.
                return redirect('home')
            else:
                # return HttpResponse("<h2>Good</h2>")
                # Return an 'invalid login' error message.
                error_msg = "Wrong Password or Username"
                return render(request, 'registration/login.html', {'loginform': login_form, 'error_msg': error_msg})

        form = LoginForm()
        return render(request, 'registration/login.html', {'loginform':form})

    form = LoginForm()
    return render(request, 'registration/login.html', {'loginform':form})


# signup proceed page
class UserCompleteSignUp(View):
    form_class = UserMoreInfo
    country_origin=''

    # blank form
    def get(self, request):
        country_origin = request.ipinfo.country
        messages.info(request,'Complete Your Profile Information')
        form = self.form_class(None)
        return render(request, 'registration/complete-signup.html', {'form': form})

    # process form data
    def post(self, request):
        country_origin = request.ipinfo.country
        username = request.user
        form = self.form_class(request.POST)
        
        if form.is_valid():
            resume = request.FILES['resume']
            if country_origin != None and country_origin == 'TZ':
                if resume:
                    validate = str(resume)
                    # validate for PDF & DOCX
                    if validate.endswith('.pdf') or validate.endswith('.docx'):
                        home_address = form.cleaned_data['home_address']
                        phone_number = form.cleaned_data['phone_number']
                        role = form.cleaned_data['role']
                        subjects = form.cleaned_data['subjects']
                        userInfo = Users(user=username, home_address=home_address, phone_number=phone_number, role=role, subjects=subjects, resume=resume)
                        userInfo.save()
                        return redirect('home')
                    else:
                        messages.error(request, "Unsupported File, please upload only PDF or DOCX Files")
                        return render(request, 'registration/complete-signup.html', {'form': form})
                else:
                    messages.error(request,'Please Attach Your Recent Resume')
                    return render(request, 'registration/complete-signup.html', {'form': form})
            else:
                messages.error(request,"Sorry Only Tanzanians are permitted")
                return render(request, 'registration/complete-signup.html', {'form': form})
                
        return render(request, 'registration/signup-form.html', {'form': form})


# predict the PTR using linear regression
class PTRDataPrediction:
    # read the file
    def readFile(self):       
        filePath = "media/documents/sample.csv"
        data = pd.read_csv(filePath)
        data = data[['REGION', 'PTR']]
        # changing the region name to number for prediction
        data['REGION'] = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26]
        return data

    def prediction(self):
        data = self.readFile()
        X = data['REGION'].values.reshape(-1, 1)
        y = data['PTR'].values.reshape(-1, 1)
        reg = LinearRegression()
        reg.fit(X, y)
        predictions = reg.predict(X)
        return predictions

    def plotingGraph(self):
        data = self.readFile()
        predictions = self.prediction()
        plt.figure(figsize=(16, 8))
        plt.scatter(
            data['REGION'],
            data['PTR'],
            c='black'
        )
        plt.plot(
            data['REGION'],
            predictions,
            c='blue',
            linewidth=2
        )
        plt.xlabel("Money spent on TV ads ($)")
        plt.ylabel("Sales ($)")
        # plt.show()

    def estimatePrediction(self):
        predictions = self.prediction()
        total = 0
        for i in predictions:
            for j in i:
                total += j

        sizeOfData = len(predictions)

        estimation = total / sizeOfData

        return estimation


class Render:
    @staticmethod
    def render(path: str, params: dict):
        template = get_template(path)
        html = template.render(params)
        response = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), response)
        if not pdf.err:
            return HttpResponse(response.getvalue(), content_type='application/pdf')
        else:
            return HttpResponse("Error Rendering PDF", status=400)


# preview a pdf plus downloading it
class Pdf(View):
    def get(self, request, full_name):
        global fname, params
        name = models.Users.objects.all()
        name1 = models.User.objects.all()
        volunteer = models.Volunteer.objects.get(full_name=full_name)

        for i in name:
            for j in name1:
                if str(volunteer.username) == str(i.user) == str(j.username):
                    params = {
                        'name': volunteer.full_name,
                        'address': i.home_address,
                        'contact': volunteer.contact,
                        'carrier': volunteer.carrier,
                        'experience': volunteer.experience,
                        'skill': volunteer.skills,
                        'why': volunteer.why_volunteer,
                        'role': i.role,
                        'email': j.email
                    }

        return Render.render('previewPDF.html', params)
        # return render(request,template_name='test.html',context=None)


# auto clean data
class AutoClean:
    @staticmethod
    def clean_data(filepath):
        global new_data, group_data
        path = "media/documents/"

        # var = input("Please enter the file name for data cleaning: ")

        data = pd.read_csv(filepath, encoding='latin1')

        data1 = data[['REGION', 'ENROLMENT', 'ALL TEACHERS', 'PTR','WARD','SCHOOL']]

        # check if null or missing data
        check_null = data1.isnull().values.any()

        if check_null:
            # data has a null or empty field
            # then interpolate estimates
            new_data = data1.interpolate()
            group_data = new_data.groupby('REGION').mean()
            group_data.to_csv(path + 'sample.csv')
            handle()
        else:
            # data has no null or empty field
            group_data = data1.groupby('REGION').mean()
            group_data.to_csv(path + 'sample.csv')
            handle()

# handling with id
num = 0
def handling_model(serial):
        for row in csv.DictReader(open('media/documents/sample.csv')):
            data = models.Chart.objects.get(id=serial)
            data.region = row['REGION']
            data.enrolment = row['ENROLMENT']
            data.teacher = row['ALL TEACHERS']
            data.ward = row['WARD']
            data.school = row['SCHOOL']
            data.ptr = row['PTR']
            data.save()
            num = num + 1

# read, upload, update csv data
def handle():
    global v
    if models.Chart.objects.exists():
        global row_id, num
        # retrieve the data
        row_id = []
        data = models.Chart.objects.all()
        # loop to append ids for incremental
        for c in data:
            row_id.append(c.id)

        # asynch
        loop.run_in_executor(None,handling_model,row_id[num])
        return
        loop.run_in_executor(None,read_and_add,'media/documents/sample.csv')


# update user status i.e approve 1 or 0
def updateStatus(request, full_name):
    global data

    num = 1
    num1 = 0

    volunteer = models.Volunteer.objects.get(full_name=full_name)
    v = models.Volunteer.objects.get(id=volunteer.id)
    # name = models.User.objects.get(id=volunteer.id)

    # for i in name:
    # if v.username == request.user.username:
    if v.status_update == 0:
        v.status_update = num
        v.save()
        data = {
            'value': 1
        }
    elif v.status_update == 1:
        v.status_update = num1
        v.save()
        data = {
            'value': 0
        }

    return redirect('manage_applicant', v.certificate)
    # return JsonResponse(data)


# manage specific applicant i.e. certificate, diploma
@user_passes_test(lambda u: u.is_superuser)
def manage_applicant(request, education):
    volunteer = models.Volunteer.objects.filter(education=education).order_by('status_update').all()

    to_html = {
        'applicant': volunteer
    }

    return render(request, template_name='admin/manageApplicant.html', context=to_html)


def load_cities(request):
    country_id = request.POST['Region']
    request.session['sregion'] = country_id

    cities=[]
    aa=test.objects.filter(region=country_id).values('council').order_by('council').distinct()
    cities=list(aa)


   # response = str(list(aa))
    #cities = Council.objects.filter(Regions=country_id).order_by('name')
    context={'cities': cities,
                  'tap':len(aa)
             }
    return HttpResponse(json.dumps({'context': context}), content_type="application/json")



def load_ward(request):
    council_id = request.POST['District']
    country_id = request.session.get('sregion')
    request.session['scouncil'] = council_id
    ward = []
    bb=test.objects.filter(region=country_id,council=council_id).order_by('ward').values('ward').distinct()
    ward = list(bb)
    
    context={'ward': ward,
             'taps':len(bb)
             }
    return HttpResponse(json.dumps({'context': context}), content_type="application/json")


def load_school(request):
    ward_id = request.POST['Ward']
    school = []
    country_id = request.session.get('sregion')
    council_id = request.session.get('scouncil')
    cc = test.objects.filter(region=country_id, council=council_id ,ward=ward_id).values('schoolname')
    school=list(cc)

    context = {'school':  school,
               'tass':len(cc)
               }
    return HttpResponse(json.dumps({'context': context}), content_type="application/json")


def chooselocation(request):



   # regions= Regions.objects.all();
    regions= test.objects.values('region').distinct()

    context={'regions':regions}
    return render(request, 'apply/location.html',context)

def savelocation(request):

    if request.method == 'POST':
        username = request.user.username
        Wards = request.POST['Ward']
        School11 = request.POST['School13']
        School12 = request.POST['School11']
        School13 = request.POST['School12']
        District= request.POST['District']
        Region = request.POST['Region']
        cc = test.objects.filter(schoolname=School11).values('ptr')
        cd = test.objects.filter(schoolname=School12).values('ptr')
        ce = test.objects.filter(schoolname=School13).values('ptr')
        print(cc)
        Ward1 = request.POST['Ward1']
        District1 = request.POST['District1']
        Region1 = request.POST['Region1']
        Ward2 = request.POST['Ward2']
        District2 = request.POST['District2']
        Region2 = request.POST['Region2']

        Volunta=Volunteer.objects.get(username=username)
       # Voluntz=Volunta(city1=r1,city2=r2,city3=r3,council1=c1,council2=c2,council3=c3,
      #  ward1=w,ward2=w1,ward3=w2,School1=ss,School2=ssc,School3=sscw )
        Volunta.city1 = Region
        Volunta.city2 = Region1
        Volunta.city3 = Region2
        Volunta.council1 = District
        Volunta.council2 =District1
        Volunta.council3 =District2
        Volunta.ward1 = Wards
        Volunta.ward2 = Ward1
        Volunta.ward3 = Ward2
        Volunta.ptr1= cc
        Volunta.ptr2 = cd
        Volunta.ptr3 = ce
        Volunta.School1 = School11
        Volunta.School2 = School12
        Volunta.School3 = School13
        Volunta.save()
      #  max_ptr = Chart.objects.filter(ward=w)
       # print(max_ptr)
        #datum = Chart.objects.filter(ptr=max_ptr['ptr__max'])
        return redirect('status')


   # return HttpResponse("asdasdas")































#TODO: nOTIFICATION
#import onesignal as onesignal_sdk

#You can create a OneSignal Client as shown below. You can find your user_auth_key and REST API Key (app_auth_key) on OneSignal Account & API Keys page.
# onesignal_client = onesignal_sdk.Client(user_auth_key="XXXXX",
#                                     app_auth_key="XXXX",
#                                     app_id="APPID")
# new_notification = onesignal_sdk.Notification(post_body={"contents": {"en": "Message", "tr": "Mesaj"}})


# #PUSH SEND
# # create a onesignal client
# onesignal_client = onesignal_sdk.Client(app_auth_key="XXXX", app_id="APPID")

# # create a notification
# new_notification = onesignal_sdk.Notification(post_body={
#     "contents": {"en": "Message", "tr": "Mesaj"},
#     "included_segments": ["Active Users"],
#     "filters": [{"field": "tag", "key": "level", "relation": "=", "value": "10"}]
# })

# # send notification, it will return a response
# onesignal_response = onesignal_client.send_notification(new_notification)
# print(onesignal_response.status_code)
# print(onesignal_response.json())

# #SPECIFIC DEVICES
# onesignal_client = onesignal_sdk.Client(app_auth_key="XXXX", app_id="APPID")
# new_notification = onesignal_sdk.Notification(post_body={
#     "contents": {"en": "Message"},
#     "include_player_ids": ["id1", "id2"],
# })

# # send notification, it will return a response
# onesignal_response = onesignal_client.send_notification(new_notification)
# print(onesignal_response.status_code)
# print(onesignal_response.json())


# #CANCELLING
# onesignal_client = onesignal_sdk.Client(user_auth_key="XXXXX",
#                                     app_auth_key="XXXX",
#                                     app_id="APPID")

# onesignal_response = onesignal_client.cancel_notification("notification_id")
# print(onesignal_response.status_code)
# print(onesignal_response.json())

# #VIEW NOTIFICATIONS
# onesignal_response = onesignal_client.view_notifications(query={"limit": 30, "offset": 0})
# if onesignal_response.status_code == 200:
#     print(onesignal_response.json())

# #VIEW BY ID
# onesignal_response = onesignal_client.view_notification("notification_id")
# if onesignal_response.status_code == 200:
#     print(onesignal_response.json())
