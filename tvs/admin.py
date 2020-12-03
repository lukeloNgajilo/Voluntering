from django.contrib import admin
from django.contrib.auth.models import Group
from django.urls import path
from tvs import models as models


admin.site.site_header = 'Volunteer Management System'
admin.site.unregister(Group)

class UserField(admin.ModelAdmin):
    list_display = ('user', 'home_address', 'phone_number', 'role','subjects','resume')
admin.site.register(models.Users, UserField)

class VolunteerField(admin.ModelAdmin):
    list_display = ('username','full_name', 'contact', 'location', 'education', 'experience'
                    , 'why_volunteer', 'status_update', 'reason','length','school','ward')
admin.site.register(models.Volunteer, VolunteerField)

class UploadCvs(admin.ModelAdmin):
    list_display = ('filename','year','allocations')
admin.site.register(models.Upload, UploadCvs)

class ToChart(admin.ModelAdmin):
    list_display = ('region', 'enrolment', 'teacher', 'ptr','ward','school')
admin.site.register(models.Chart, ToChart)

class RegionCoordinates(admin.ModelAdmin):
    list_display = ('region','lat','long')
admin.site.register(models.Region, RegionCoordinates)

class CancelledApplicantions(admin.ModelAdmin):
    list_display = ('name','canceling_reason')
admin.site.register(models.CancelledApplication,CancelledApplicantions)

class WebPushDetails(admin.ModelAdmin):
    list_display = ('userKey','appKey','appId')
admin.site.register(models.Push, WebPushDetails)


# custom clean button
class MyModelAdmin(admin.ModelAdmin):
    def get_urls(self):
        urls = super(MyModelAdmin, self).get_urls()
        my_urls = [
            path('admin/list', self.my_view, name="custom_view")
        ]
        return my_urls + urls

    def my_view(self, request):
        # custom view which should return an HttpResponse
        pass

    # In case your template resides in a non-standard location
    change_list_template = "volunteer/tvs/templates/admin/change_list.html"
