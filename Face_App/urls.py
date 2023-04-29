from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .import views
from Face_App.views import capture
# from Face_App.views import Demo2

urlpatterns = [
				path('base/',views.base,name="base"),
				path('Employee_Login/',views.Employee_Login,name="Employee_Login"),
				path('Registeration/',views.Registeration,name="Registeration"),
				path('capture/',views.capture,name="capture"),
				path('Admin_Login/',views.Admin_Login,name="Admin_Login"),
				path('demo/',views.demo,name="demo"),
				path('',views.Home,name="Home"),
				path('Attendance/',views.Attendance,name="Attendance"),
				path('Edit_Profile/',views.Edit_Profile,name="Edit_Profile"),
				path('update/',views.update,name='update'),
				path('View_Employees/',views.View_Employees,name="View_Employees"),
				path('View_Attendance/',views.View_Attendance,name="View_Attendance"),
				path('Employee_Details2/<int:id>',views.Employee_Details2,name="Employee_Details2"),
				path('Employee_Details/',views.Employee_Details,name="Employee_Details"),
				path('Registeration2/',views.Registeration2,name="Registeration2,"),
				path('View_Attendance_User/',views.View_Attendance_User,name="View_Attendance_User"),
				path('Logout/',views.Logout,name='Logout'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 