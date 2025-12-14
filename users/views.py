from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.contrib.auth import login, authenticate, logout
from django.views import View
from users.forms import RegisterForm,CustomRegistrationForm,LoginForm,AssignRoleForm,CreateGroupForm,CustomPasswordChangeForm,CustomPasswordResetForm,CustomPasswordResetConfirmForm,EditProfileForm
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required,user_passes_test
from django.db.models import Prefetch
from django.contrib.auth.views import LoginView,PasswordChangeView,PasswordChangeDoneView,PasswordResetView,PasswordResetConfirmView,PasswordResetDoneView,PasswordResetCompleteView
from django.views.generic import TemplateView,UpdateView,ListView,CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator

User = get_user_model()

# Test for user
"""
class EditProfileView(UpdateView):
    model = User
    form_class = EditProfileForm
    template_name = 'accounts/update_profile.html'
    context_object_name = 'form'
    
    def get_object(self):
        return self.request.user
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['userprofile'] = UserProfile.objects.get(user= self.request.user)
        return kwargs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_profile = UserProfile.objects.get(user=self.request.user) 
        print('views', user_profile)
        context["form"] = self.form_class(instance = self.object, userprofile=user_profile)
        return context
    
    def form_valid(self, form):
        form.save(commit=True)
        return redirect('profile')
"""    
class EditProfileView(UpdateView):
    model = User
    form_class = EditProfileForm
    template_name = 'accounts/update_profile.html'
    context_object_name = 'form'
    
    def get_object(self):
        return self.request.user
    
    def form_valid(self, form):
        form.save()
        return redirect('profile')

 
def is_admin(user):
    return user.groups.filter(name="Admin").exists()


# Create your views here.
def sign_up(request):
    form = CustomRegistrationForm()
    if request.method == 'POST': 
        form = CustomRegistrationForm(request.POST)
        if form.is_valid():
            # username = form.cleaned_data.get('username')
            # password = form.cleaned_data.get('password1')
            # confirm_password = form.cleaned_data.get('password2')
            
            # if password == confirm_password:
            #     User.objects.create(username=username,password= password)   
            # else:
            #     print("Password are not same")
            user  = form.save(commit=False)
            print('user' , user)
            user.set_password(form.cleaned_data.get('password1'))
            print(form.cleaned_data)
            user.is_active = False
            user.save()

            messages.success(request,"A Confirmation mail sent. Please check the email")
            
            return redirect('sign-in')      
        else:
            print("Form is not valid")
    return render(request,'registration/register.html',{'form':form})

class SignUpView(CreateView):
    context_object_name = 'form'
    template_name = 'registration/register.html'
    form_class = CustomRegistrationForm
    
    def post(self,request,*args, **kwargs):
        form = CustomRegistrationForm(request.POST)
        if form.is_valid():
            user  = form.save(commit=False)
            user.set_password(form.cleaned_data.get('password1'))
            print(form.cleaned_data)
            user.is_active = False
            user.save()
            messages.success(request,"A Confirmation mail sent. Please check the email")
            return redirect('sign-in')
        else:
            print("Form is not valid")
            return redirect('sign-up')

def sign_in(request):
    form = LoginForm()
    if request.method == "POST":
        # username = request.POST.get('username')
        # password = request.POST.get('password')
        # user = authenticate(username=username, password=password)
        # print('doc',username,password)
        # print(user)
        # if user is not None:
        #     login(request,user)
        #     return redirect('home')
        form = LoginForm(data=request.POST)
        if form.is_valid():    
            user = form.get_user()
            login(request,user)
            return redirect('home')
    return render(request,"registration/login.html",{'form':form})

class CustomLoginView(LoginView):
    form_class = LoginForm
    
    
class ChangePassword(PasswordChangeView):
    template_name = "accounts/password_change.html"
    form_class = CustomPasswordChangeForm

@login_required
def sign_out(request):
    if request.method == 'POST':
        logout(request)
        return redirect('sign-in')    


def activate_user(request,user_id,token):
    try:
        user = User.objects.get(id=user_id)
        if default_token_generator.check_token(user,token):
            user.is_active = True
            user.save()
            return redirect('sign-in')
        else:
            return HttpResponse('Invalid Id or token')
    except User.DoesNotExist:
        return HttpResponse('User not found')

@user_passes_test(is_admin,login_url='no-permission')
def admin_dashboard(request):
    users = User.objects.prefetch_related(
            Prefetch('groups',queryset=Group.objects.all(),
            to_attr='all_groups')
        ).all()
    
    for user in users:
        if user.all_groups:
            user.group_name = user.all_groups[0].name
        else:
            user.group_name = 'No Group assigned'
    return render(request,'admin/dashboard.html',{'users':users})

class AdminDashboard(ListView):
    model = User
    context_object_name = 'users'
    template_name = 'admin/dashboard.html'
    
    def get_queryset(self):
        users = User.objects.prefetch_related(
            Prefetch('groups',queryset=Group.objects.all(),
            to_attr='all_groups')
        ).all()
        for user in users:
            if user.all_groups:
                user.group_name = user.all_groups[0].name
            else:
                user.group_name = 'No Group assigned'    
        return users

    
@user_passes_test(is_admin,login_url='no-permission')
def assign_role(request,user_id):
    user = User.objects.get(id=user_id)
    form = AssignRoleForm()
    if request.method=='POST':
        form = AssignRoleForm(request.POST)
        if form.is_valid():
            role = form.cleaned_data.get('role')
            user.groups.clear()
            user.groups.add(role)
            messages.success(request,f"User {user.username} has been assigned to the {role.name} role")
            return redirect('admin-dashboard')
    return render(request,'admin/assign_role.html',{'form': form})

class AssignRole(UpdateView):
    context_object_name = 'form'
    template_name = 'admin/assign_role.html'
    pk_url_kwarg = 'user_id'
    form_class = AssignRoleForm
    
    def get_queryset(self):
        queryset = User.objects.prefetch_related(
            Prefetch('groups',queryset=Group.objects.all(),
            to_attr='all_groups')
        ).all()
        return queryset
    
    def get_initial(self):
        initial = super().get_initial()
        group = self.object.groups.first()
        if group:
            initial['role'] = group
        return initial
    
    def form_valid(self, form):
        user = self.object
        role = form.cleaned_data.get('role')
        user.groups.clear()
        if role:
            user.groups.add(role)
        messages.success(self.request,f"User {user.username} has been assigned to the {role.name} role")
        return redirect('admin-dashboard')

@user_passes_test(is_admin,login_url='no-permission')
def create_group(request):
    form = CreateGroupForm()
    if request.method=='POST':
        form = CreateGroupForm(request.POST)
        if form.is_valid():
            group = form.save()
            messages.success(request,f"Group {group.name} has been created successfully")
            return redirect('create-group')
    return render(request,'admin/create_group.html',{'form':form})

class CreateGroup(CreateView):
    template_name = 'admin/create_group.html'
    context_object_name = 'form'
    form_class = CreateGroupForm
    
    # def get(self,request,*args, **kwargs):
    #     form = CreateGroupForm()
    #     return render(request,self.template_name,{'form':form})
    
    def post(self,request,*args, **kwargs):
        form = CreateGroupForm(request.POST)
        if form.is_valid():
            group = form.save()
            messages.success(request,f"Group {group.name} has been created successfully")
            return redirect('create-group')        

@user_passes_test(is_admin,login_url='no-permission')
def group_list(request):
    groups = Group.objects.prefetch_related('permissions')
    return render(request,'admin/group_list.html',{'groups':groups})

group_decorator = [login_required,user_passes_test(is_admin,login_url='no-permission')]
@method_decorator(group_decorator,name='dispatch')
class ViewGroup(ListView):
    model = Group
    context_object_name = 'groups'
    template_name = "admin/group_list.html"

class ProfileView(LoginRequiredMixin,TemplateView):
    template_name = 'accounts/profile.html'
    
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        user = self.request.user
        context['username'] = user.username
        context['email'] = user.email
        context['name'] = user.get_full_name()
        context['bio'] = user.bio
        context['profile_image'] = user.profile_image
        context['member_since'] = user.date_joined
        context['last_login'] = user.last_login

        return context
    
class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm
    template_name = "registration/reset_password.html"
    success_url = reverse_lazy('sign-in')
    html_email_template_name = 'registration/reset_email.html'
    
    def form_valid(self, form):
        messages.success(self.request,"A reset email has been sent. Please check your email")
        return super().form_valid(form)
    
class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = CustomPasswordResetConfirmForm
    template_name = "registration/reset_password.html"
    success_url = reverse_lazy('sign-in')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["protocol"] = "https" if self.request.is_secure() else 'http'
        context['domain'] = self.request.get_host()
        print(context)
        return context
    
    def form_valid(self, form):
        messages.success(self.request,"Password reset successfully")
        return super().form_valid(form)
        
"""
    Admin 
        - shobkichu
    Manager
        - project
        - task create
    Employee
        - Task read
        - Task update
    
    Role Based Access Control(RBAC)
""" 