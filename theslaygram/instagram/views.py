from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib import messages
from .forms import UserProfileForm, UserForm, NewPostForm
from .models import Profile


# Create your views here.

@login_required(login_url='/accounts/login/')
def index(request):
    return render(request, 'index.html')


@login_required
@transaction.atomic
def update_user_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        user_profile = UserProfileForm(
            request.POST, instance=request.user.profile)

        if user_form.is_valid() and user_profile.is_valid():
            user_form.save()
            user_profile.save()
            messages.success(request, 'Profile successfully updated')
            return redirect(index)
        else:
            messages.error(
                request, 'Error occured while updating,,, try again')

    else:
        user_form = UserForm(instance=request.user)
        user_profile = UserProfileForm(instance=request.user.profile)

    return render(request, 'profiles/profile.html', {'user_form': user_form, 'user_profile': user_profile, })


@login_required
def new_post(request):
    current_user = request.user
    if request.method == 'POST':
        form = NewPostForm(request.POST, request.FILES)
        if current_user.is_authenticated and form.is_valid():
            post = form.save(commit=False)
            post.user = current_user
            post.save()
    else:
        form = NewPostForm()
    return render(request, 'posts/new-post.html', {"form": form})
