from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib import messages
from django.http import Http404
from .forms import UserProfileForm, UserForm, NewPostForm
from .models import Profile, Post
from vote.managers import VotableManager

votes = VotableManager()
# Create your views here.


@login_required(login_url='/accounts/login/')
def index(request):
    posts = Post.display_posts()
    return render(request, 'index.html', {"posts": posts})


@login_required(login_url='/accounts/login/')
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


@login_required(login_url='/accounts/login/')
def new_post(request):
    current_user = request.user
    if request.method == 'POST':
        form = NewPostForm(request.POST, request.FILES)
        if current_user.is_authenticated and form.is_valid():
            post = form.save(commit=False)
            post.user = current_user
            post.save()
            return redirect(index)
    else:
        form = NewPostForm()
    return render(request, 'posts/new-post.html', {"form": form})


@login_required(login_url='/accounts/login/')
def posts(request, user_id):
    user_id = request.user.id
    posts = Post.display_users_posts(user_id)
    # return posts
    return render(request, 'profiles/posts.html', {"posts": posts})


@login_required(login_url='/accounts/login/')
def single_post(request, pictures):
    try:
        post = Post.objects.get(id=pictures)
        current_user = request.user
        current_post = post
        if request.method == 'POST':
            review_form = NewReviewForm(request.POST)
            if current_user.is_authenticated and review_form.is_valid():
                review = review_form.save(commit=False)
                review.users = current_user
                review.pictures = current_post
                review.save()
        else:
            review_form = NewReviewForm()
    except DoesNotExist:
        raise Http404
    return render(request, "profiles/post.html", {"post": post, "review_form": review_form})


@login_required(login_url='/accounts/login')
def upvote_post(request, pk):
    post = Post.get_single_post(pk)
    user = request.user
    user_id = user.id

    if user.is_authenticated:
        upvote = post.votes.up(user_id)
        print(upvote)
        post.upvote_count = post.votes.count()
        post.save()
    return redirect(index)
    # return render(request, "profiles/post.html", {"post": post, "upvote": upvote})


@login_required(login_url='/accounts/login')
def downvote_post(request, pk):
    post = Post.get_single_post(pk)
    user = request.user
    user_id = user.id

    if user.is_authenticated:
        downvote = post.votes.down(user_id)
        print(post.id)
        print(downvote)
        print(post.vote_score)
        post.downvote_count = post.votes.count()
        post.save()
    return redirect(index)
