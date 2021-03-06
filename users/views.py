"""Django Views for Users."""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.core.files.storage import FileSystemStorage
from .forms import UserRegisterForm, UserCreateMeetForm

from .forms import UserRegisterForm, UserCreateMeetForm, UserUpdateDetailForm, ProfileUpdateForm


from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from appointment.models import UserMeeting


def register(request):
    """Render to register page if user is already logged in, redirect to home page."""
    if request.user.is_authenticated:
        messages.info(request, 'You have to logout before make a new register')
        return redirect('appointment:home_page')
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'{username} has been created!!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


class LoginFormView(SuccessMessageMixin, LoginView):
    """User login page."""

    template_name = 'users/login.html'
    success_url = 'appointment:home_page'
    success_message = "You were successfully logged in."


@login_required
def profile(request):
    """Render to profile.html."""
    if request.method == 'POST':
        user_update_form = UserUpdateDetailForm(request.POST, instance=request.user)
        profile_update_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if user_update_form.is_valid() and profile_update_form.is_valid():
            user_update_form.save()
            profile_update_form.save()
            messages.success(request, f'Your profile has been update!!')
            return redirect('profile')
    else:
        user_update_form = UserUpdateDetailForm(instance=request.user)
        profile_update_form = ProfileUpdateForm(instance=request.user.profile)
    context = {'user_update_form': user_update_form, 'profile_update_form': profile_update_form}
    return render(request, 'users/profile.html', context)


@login_required
def create_meet(request):
    """Create meeting form."""
    if request.method == 'POST':
        form = UserCreateMeetForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            subject = form.cleaned_data.get('subject')
            start_time = form.cleaned_data.get('start_time').strftime('%d %B %Y')
            messages.success(request, f'{subject} start at {start_time} has been created!!')
            return redirect('appointment:home_page')
    else:
        form = UserCreateMeetForm()
    return render(request, 'users/create_meeting.html', {'form': form})

def other_profiles(request, user_id):
    """View the other profiles."""
    specific_user = get_object_or_404(User, pk=user_id)
    joining_meet = UserMeeting.objects.filter(user=specific_user, is_join=True)
    return render(request, 'users/other_profiles.html', {'specific_user': specific_user, 'joining_meet': joining_meet})

