from django.shortcuts import render,redirect
import cv2
from django.views import View
from django.contrib import messages
from django.contrib.sessions.models import Session
from django.core.files import File
from django.core.files.base import ContentFile
from django.core.files.temp import NamedTemporaryFile
import os
from .models import*
import numpy as np
import face_recognition
from datetime import datetime

# Create your views here.

def base(request):
	return render(request,"base.html",{})

def Home(request):
	return render(request,"Home.html",{})

def Logout(request):
	Session.objects.all().delete()
	return redirect("/")

def Employee_Login(request):
	if request.method == "POST":
		C_name = request.POST['username']
		C_password = request.POST['pass']
		if userDetails.objects.filter(username=C_name, password=C_password).exists():
			users = userDetails.objects.all().filter(username=C_name, password=C_password)
			messages.info(request,C_name +' logged in')
			request.session['UserId'] = users[0].id
			request.session['type_id'] = 'User'
			request.session['UserType'] = C_name
			request.session['login'] = "Yes"
			# request.session['username'] = Username
			return redirect("/")
		else:
			messages.info(request, 'Please Register')
			return redirect("/Registeration")
	else:
		return render(request,'Employee_Login.html',{})
	return render(request,'Employee_Login.html',{})

	return render(request,'Employee_Login.html',{})

def Admin_Login(request):
	if request.method == "POST":
		A_username = request.POST['aname']
		A_password = request.POST['apass']
		if admin_details.objects.filter(aname=A_username,apass=A_password ).exists():
			ad = admin_details.objects.get(aname=A_username,apass=A_password )
			messages.info(request,A_username+ ' login is Sucessfull')
			request.session['type_id'] = 'Admin'
			request.session['UserType'] = 'Admin'
			request.session['login'] = "Yes"
			return redirect("/")
		else:
			print('y')
			messages.error(request, 'Error wrong username/password')
	else:
		return render(request, "Admin_Login.html", {})
	return render(request,'Admin_Login.html',{})

def Registeration(request):
	if request.method == "POST":
		Fname = request.POST['firstname']
		print(Fname)
		age= request.POST['age']
		phone= request.POST['phone']
		address= request.POST['Address']
		email = request.POST['email']
		username= request.POST['username']
		password= request.POST['pass']
		department= request.POST['Department']
		course= request.POST['course']
		Class= request.POST['Class']
		#photo = request.FILES['img']
		# photo_name = username + "_" + str(photo)
		# print(photo_name)
		#photo = os.path.join(path,photo) 
		#print(photo)
		path = 'C:/PythonProjects/Facial_Recognition_Attendance/media/user_images'
		def rename():
			New = username
			print(username)
		photos = "user_images"+"/"+username + '.jpg' 

		obj = userDetails(F_name = Fname
							,age 		= age
							,phone 		= phone
							,address 	= address
							,email 		= email
							,username 	= username
							,password 	= password
							,department = department
							,course 	= course
							,Class 		= Class
							,images 	= photos)
		obj.save()
		#messages.info(request,name +' Registered')
		return redirect('/Employee_Login/')
	else:
		return render(request,"Registeration.html",{})

def Registeration2(request):
	return render(request,'Registeration2.html',{})


	
def capture(request):
	if request.method =="POST":
		username = request.POST['username']
		print(username)
		if userDetails.objects.filter(username=username).exists():
			messages.info(request,'Username Already Exists')
			return redirect('/Registeration2')
		else:
			cam = cv2.VideoCapture(0)

			# title of the app
			# cv2.namedWindow('python webcam screenshot app')

			# let's assume the number of images gotten is 0
			img_counter = 0
			username = username

			# while loop
			while True:
			    # intializing the frame, ret
			    ret, frame = cam.read()
			    # if statement
			    if not ret:
			        print('failed to grab frame')
			        break
			    # the frame will show with the title of test
			    cv2.imshow('test', frame)
			    #to get continuous live video feed from my laptops webcam
			    k  = cv2.waitKey(1)
			    # if the escape key is been pressed, the app will stop
			    if k%256 == 27:
			        print('escape hit, closing the app')
			        break
			    # if the spacebar key is been pressed
			    # screenshots will be taken
			    elif k%256  == 32:
			        # the format for storing the images scrreenshotted
			        img_name = f'{username}'
			        #path to the folder where the screenshit will be saved
			        path = 'C:/Users/Downloads/Facial_Recognition_Attendance/Facial_Recognition_Attendance/media/user_images'
			        # saves the image as a png file
			        cv2.imwrite(os.path.join(path,img_name +".jpg"), frame)
			        #path1 = 'C:/PythonProjects/Facial_Recognition_Attendance/media/'+ img_name + '.jpg'
			        #print(path1)
			        print('screenshot taken')
			        # the number of images automaticallly increases by 1
			        img_counter += 1
			# release the camera
			cam.release()
			# stops the camera window
			cv2.destroyAllWindows()
			return render(request,"Registeration.html",{})
	else:
		return render(request,"Registeration.html",{})


def demo(request):
	return render(request,"demo.html",{})




def Attendance(request):
	path = 'media/user_images'
	images = []
	personName = []
	myList = os.listdir(path)
	print(myList)
	#To split or to extract the username 
	for img in myList:
		#Reading our images from the folder
		current_img = cv2.imread(f'{path}/{img}')
		#Insering images inside images list 
		images.append(current_img)
		#splitting Username and extention
		personName.append(os.path.splitext(img)[0])
	print(personName)
	def faceEncodings(images):
		encodeList = []
		for img in images:
			img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
			encode = face_recognition.face_encodings(img)[0]
			encodeList.append(encode)
		return encodeList
	encodeListKnown = faceEncodings(images)
	print("Encoding Complete")


	cap = cv2.VideoCapture(0)

	while True:
		ret,frame = cap.read()
		faces = cv2.resize(frame,(0,0),None,0.25,0.25)
		faces = cv2.cvtColor(faces,cv2.COLOR_BGR2RGB)

		facesCurrentFrame = face_recognition.face_locations(faces)
		encodesCurrentFrame = face_recognition.face_encodings(faces,facesCurrentFrame)

		for encodeFace,faceLoc in zip(encodesCurrentFrame,facesCurrentFrame):
			matches = face_recognition.compare_faces(encodeListKnown,encodeFace)
			faceDis = face_recognition.face_distance(encodeListKnown,encodeFace)

			matchIndex = np.argmin(faceDis)

			if matches[matchIndex]:
				name = personName[matchIndex].upper()
				# print(name)
				y1,x2,y2,x1 = faceLoc
				y1,x2,y2,x1 = y1*4,y2*4,x2*4,x1*4
				cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),2)
				cv2.rectangle(frame, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
				cv2.putText(frame, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
				time_now = datetime.now()
				dStr = time_now.strftime('%d/%m/%Y')
				if attendance.objects.filter(name = name,date=dStr).exists():
					# messages.info(request,'OK')
					break
				# else:
				time_now = datetime.now()
				tStr = time_now.strftime('%H:%M:%S')
				dStr = time_now.strftime('%d/%m/%Y')
				obj = attendance(name = name,date = dStr,time = tStr)
				obj.save()
				messages.info(request,'Attendance Marked Sucessfully')
		print("out of for loop")			
		cv2.imshow("Camera",frame)
		# if attendance.objects.filter(name = personName).exists():
		# 	messages.info(request,'Already logged')
		# else:
		# 	obj = attendance()


		if cv2.waitKey(10) == 13:#if enter key is pressed
			break
	print("out of while")
	cap.release()
	cv2.destroyAllWindows()

	return redirect('/')

def Edit_Profile(request):
	User_id =request.session['UserId']
	details = userDetails.objects.all().filter(id=User_id)
	return render(request,'Edit_Profile.html',{'details':details})

def update(request):
	if request.method == "POST":
		User_id = request.POST['UserId']
		Fname = request.POST['firstname']
		age= request.POST['age']
		phone= request.POST['phone']
		address= request.POST['Address']
		email = request.POST['email']
		department= request.POST['Department']
		course= request.POST['course']
		Class= request.POST['Class']
		userDetails.objects.filter(id=User_id).update(F_name 	= Fname
													,age 		= age
													,phone 		= phone
													,address 	= address
													,email 		= email
													,department = department
													,course 	= course
													,Class 		= Class
			)
		messages.info(request,'Profile Updated Sucessfully')
		return redirect('/Edit_Profile')
	else:
		details = userDetails.objects.all().filter(id=User_id)
		return render(request,'Edit_Profile.html',{'details':details})




def View_Employees(request):
	return render(request,'View_Employees.html',{})

def View_Attendance(request):
	if request.method == "POST":
		searched = request.POST['searched']
		details = attendance.objects.filter(name__icontains=searched)
		return render(request,'View_Attendance.html',{'details':details})
	else:
		details = attendance.objects.all()
		return render(request,'View_Attendance.html',{'details':details})

def Employee_Details2(request,id):
	details = userDetails.objects.filter(id=id)
	return render(request,'Employee_Details2.html',{'details':details})

def Employee_Details(request):
	details = userDetails.objects.all()
	return render(request,'Employee_Details.html',{'details':details})

def View_Attendance_User(request):
	User_id =request.session['UserId']
	details = attendance.objects.filter(id = User_id)
	C_name=request.session['UserType']
	details = attendance.objects.filter(name = C_name)
	print(C_name)
	return render(request,'View_Attendance_User.html',{'details':details})




