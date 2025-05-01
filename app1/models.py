from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.conf import settings  


class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, first_name, last_name, password=None):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            username=username,
            first_name=first_name,
            last_name=last_name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, first_name, last_name, password=None):
        user = self.create_user(
            email=email,
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    password = models.CharField(max_length=255)
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'  # Login by email
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']  # Additional required fields

    def __str__(self):
        return self.email


class Job(models.Model):
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('closed', 'Closed'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='jobs')  # The user who posted the job
    title = models.CharField(max_length=255)  # Job title
    description = models.TextField()  # Job description, can be lengthy
    document = models.FileField(upload_to='job_documents/', blank=True, null=True)  # Optional document attachment
    time_posted = models.DateTimeField(auto_now_add=True)  # Time when the job was posted
    deadline = models.DateField(blank=True, null=True)  # Optional deadline for the job
    budget = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  # Budget for the job
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')  # Job status
    skills_required = models.CharField(max_length=255, blank=True, null=True)  # Skills required for the job
    working_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='working_jobs')  # The user currently working on the job

    def __str__(self):
        return self.title

class JobOutput(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='job_outputs')
    output_file = models.FileField(upload_to='job_outputs/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Output for {self.job.title}"

class Profile(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='profiles')
    introduction=models.TextField(blank=True,null=True)
    profile_pic=models.ImageField(upload_to='profile_pics',blank=True,null=True)

    
    skills = models.CharField(max_length=50,blank=True, null=True)
    experience = models.PositiveIntegerField(default=0, help_text="Years of experience in freelancing or related work.")
    #location = models.CharField(max_length=255, blank=True, null=True, help_text="City, State, or Country of the freelancer.")
    resume = models.FileField(upload_to='profile_resume/', blank=True, null=True)  # Optional document attachment

    
    def __str__(self):
        return f"{self.user.username}'s Profile"
    
class Applications(models.Model):

    sending_user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='sending_user')
    receving_user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='receving_user')
    job=models.ForeignKey(Job,on_delete=models.CASCADE,related_name='job')
    body=models.TextField()
    #time_posted = models.DateTimeField(auto_now_add=True,default=timezone.now)

    STATUS_CHOICES = [
        ('accepted', 'Accepted'),
        ('requested', 'Requested'),
        ('rejected', 'Rejected'),
    
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='requested')  # Job status

    def __str__(self):
        return f"{self.sending_user.username}'s Application for {self.job.title}"


class Message(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_messages')
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender.username} to {self.receiver.username} about {self.job.title}"



    


