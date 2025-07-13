from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout

from accounts.models import User


class LoginView(View):
    template_name = 'account.html'
    def get(self,request):
        return render(request,self.template_name)
    
    def post(self,request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = authenticate(request,email=email,password=password)
        if user is not None:
            login(request,user)
            messages.success(request,'Logged in successfully')
            if user.is_customer:
                return redirect('website:home')
            elif user.is_admin:
                pass
            else:
                messages.info(request,'Unauthorized user')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            messages.info(request,'Invalid email or password')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
class RegisterView(View):
    template_name = 'register.html'

    def get(self, request):
        context = {}
        return render(request, self.template_name, context)

    def post(self, request):
        first_name = request.POST.get('fname')
        last_name = request.POST.get('lname')
        gender = request.POST.get('gender')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.info(request, 'Passwords do not match')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


        email_exists = User.objects.filter(email=email).exists()
        print(email_exists)
        if email_exists:
            messages.info(request, 'User already exists')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        user = User.objects.create(
            first_name=first_name,
            last_name =last_name,
            email=email,
            phone_number=phone_number,
            gender=gender,
        )
        user.set_password(password)
        user.is_customer = True
        user.save()

        # Authenticate and log in the user
        user = authenticate(request, email=email, password=password)
        login(request, user)
        messages.success(request, 'Account created successfully')
        return redirect('website:home')
    
class LogoutView(View):
    def get(self,request):
        logout(request)
        messages.success(request,'Logged out successfully')
        return redirect('website:home')
