#from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth import login,authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404

from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib import messages
from .models import *

class Homeview(LoginRequiredMixin,View):
    login_url='login'
    def get(self,request):
        jobs=Job.objects.all().order_by('-time_posted')
        for job in jobs:
            if job.skills_required:
                job.skills_required = job.skills_required.split(',') 
        return render(request,'home.html',{'jobs':jobs})

class Loginview(View):
    def get(self,request):
        return render(request,'login_page.html')
    
    def post(self,request):
        email=request.POST['email']
        password=request.POST['password']
        user=authenticate(request,email=email,password=password)
        if user:
            login(request,user)
        else:
            return render(request,'login_page.html',{'error':'Invalid Credentials '})
        return redirect('home')
    



class Signupview(View):
    def get(self, request):
        return render(request, 'signup.html')  # Custom form without Django forms

    def post(self, request):
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')

        
        if not email or not first_name or not last_name or not username or not password:
            messages.error(request, "All fields are required!")
            return render(request, 'signup.html',{'error':'All fields are required!'})

    
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username already taken!")
            return render(request, 'signup.html',{'error':'Username already taken!'})

        
        elif CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email already taken!")
            return render(request, 'signup.html',{'error':'Email already taken!'})
        
        else:
            # Create the user if no issues
            user = CustomUser.objects.create_user(
                username=username, 
                email=email, 
                first_name=first_name, 
                last_name=last_name, 
                password=password
            )
            login(request, user)  # Log the user in immediately after signup
            messages.success(request, "Signup successful!")
            return redirect('profile_input')  # Redirect to the home page or dashboard

class Jobinputview(LoginRequiredMixin,View):
    login_url='login'

    def get(self,request):
        return render(request,'job_input.html')
    
    def post(self,request):
        title=request.POST['title']
        description=request.POST['description']
        document = request.FILES.get('document')
        deadline = request.POST.get('deadline')
        budget = request.POST['budget']
        skills = ','.join(request.POST.getlist('skills'))  # Combine selected skills

        Job.objects.create(
            user=request.user,  # Assuming the user is logged in
            title=title,
            description=description,
            document=document,
            deadline=deadline,
            budget=budget,
            skills_required=skills,
            
        )
        return redirect('home')

class Jobview(LoginRequiredMixin,View):
    login_url='login'
    def get(self,request,id):
        c_job=Job.objects.get(id=id)
        application = Applications.objects.filter(sending_user=request.user, job=c_job).first()

        if c_job.skills_required:
            c_job.skills_required = c_job.skills_required.split(',') 
        return render(request,'job.html',{'job':c_job,'application':application})
    
    def post(self,request,id):
    
        c_job=Job.objects.get(id=id)
        Applications.objects.create(
            sending_user=request.user,
            receving_user=c_job.user,
            job=c_job,
            body=f'requested for your job',
        )
        return redirect('job',id=c_job.id)
        

class ProfileView(View):
    def get(self,request):
        profile=Profile.objects.all()
        for pro in profile:
            if pro.skills:
                pro.skills = pro.skills.split(',') 
        return render(request,'profiles.html',{'profile':profile})
    
class Profile_input_view(View):
    def get(self,request):
        profile = get_object_or_404(Profile, user=request.user)
        context = {
                'introduction': profile.introduction,
                'skills': profile.skills.split(',') if profile.skills else [],  # Split skills into a list
                'resume':profile.resume,
                'experience':profile.experience
            }
        return render(request, 'profile_input.html', context)

    def post(self,request):
        profile=get_object_or_404(Profile,user=request.user)

        intro=request.POST['intro']
        skills = ','.join(request.POST.getlist('skills'))
        resume=request.FILES.get('resume')
        experience=request.POST['experience']
        profile.introduction=intro
        profile.skills=skills 
        profile.experience=experience

        #if profile.resume:

        profile.resume=resume
        profile.save()
        return redirect('home')

class User_Profile_View(View):
    def get(self,request,pk):
        profile=get_object_or_404(Profile,user_id=pk)
        
        return render(request,'user_profile.html',{'profile':profile})

class Myjobs(View):
    def get(self,request):
        posted_jobs=Job.objects.filter(user=request.user)
        assigned_jobs=Job.objects.filter(working_user=request.user)
        for job in posted_jobs:
            if job.skills_required:
                job.skills_required = job.skills_required.split(',') 
        for job in assigned_jobs:
            if job.skills_required:
                job.skills_required = job.skills_required.split(',') 
        return render(request,'myjobs.html',{'posted_jobs':posted_jobs,'assigned_jobs':assigned_jobs})

class Applicationview(View):
    def get(self,request,id):
        job=get_object_or_404(Job,id=id)
        application=Applications.objects.filter(receving_user=request.user,job=job)
        return render(request,'applications.html',{'application':application,'job':job})
    
    def post(self,request,id):
        action=request.POST.get('action')
        job = get_object_or_404(Job, id=id)

        application = Applications.objects.filter(receving_user=request.user, job=job).first()  # Use .first() to get the application object

        if action == "accept":
            application.status= "accepted"
            job.working_user=request.user
            job.save()

        
        elif action =="reject":
            application.status= "rejected"
        
        application.save()

        return redirect('job',id=job.id)