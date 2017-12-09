from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib import messages
from django.http import Http404
from .forms import UserProfileForm, UserForm, NewPostForm, ReviewForm
from django.contrib.auth.models import User, Group
from .models import Profile, Post, Review
from vote.managers import VotableManager
from theslaygram import settings
votes = VotableManager()
import os
from wsgiref.util import FileWrapper
import mimetypes
# Create your views here.


@login_required(login_url='/accounts/login/')
def index(request):

    # posts = Post.display_posts()
    form = ReviewForm()
    current_user = request.user
    follows = current_user.profile.followers.all()

    posts = []
    comments = []

    for following in follows:
        all_posts = Post.objects.filter(user_id=following.user.id).all()
        posts += all_posts

    return render(request, 'index.html', {"posts": posts, "form": form})


@login_required(login_url='/accounts/login/')
@transaction.atomic
def update_user_profile(request):
    user_id = request.user.id
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        user_profile = UserProfileForm(
            request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and user_profile.is_valid():
            user_form.save()
            user_profile.save()
            messages.success(request, 'Profile successfully updated')
            return redirect(posts, user_id)
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
    current_user = request.user
    user_id = current_user.id
    posts = Post.display_users_posts(user_id)
    form = ReviewForm()
    follows = current_user.profile.followers.all()
    # followers = current_user.profile.followed_by.all()
# return posts
    return render(request, 'profiles/posts.html', {"posts": posts, "form": form, "follows": follows})


@login_required(login_url='/accounts/login')
def post_comment(request, pk):
    post = Post.get_single_post(pk)
    # comment = Review.get_single_comment(id)
    user = request.user
    current_user = request.user.id
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if user.is_authenticated and form.is_valid():
            comment = form.save(commit=False)
            comment.users_id = current_user
            comment.pictures_id = post.id

            comment.save()
            # comment.save_m2m()
            return redirect(index)
    else:
        form = ReviewForm()
    return render(request, 'profiles/posts.html', {"post": post, "form": form})


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


def get_user(request, id):
    user = User.objects.get(id=2)
    print(user.username)
    return user


@login_required(login_url='/accounts/login')
def follow(request, pk):
    post = Post.get_single_post(pk)
    current_user = request.user
    user = post.user
    print(current_user.username)
    following_profile = current_user.profile.followers.add(user.profile)
    # follows = current_user.profile.followers.all()
    print(following_profile)
    return redirect(index)


@login_required(login_url='/accounts/login')
def get_followers(request, id):
    current_user = request.user
    follows = current_user.profile.followers.all()
    for following in follows:
        posts = Post.objects.filter(user_id=following.user.id).all()


@login_required(login_url='/accounts/login')
def download_image(request, pk):
    post = Post.get_single_post(pk)
    # post.picture.file returns full path to the image
    wrapper = FileWrapper(post.picture.file)
    # Use mimetypes to get file type
    content_type = mimetypes.guess_type(
        str(post.picture.file))[0]
    response = HttpResponse(wrapper, content_type=content_type)
    response['Content-Length'] = os.path.getsize(str(post.picture.file))
    response['Content-Disposition'] = "attachment; filename=%s" % post.picture
    return response


@login_required(login_url='/accounts/login')
def get_comments(request, pk):
    comments = []
    user = request.user
    post = Post.get_single_post(pk)
    all_comments = Review.objects.filter(pictures_id=post.id).all()
    comments += all_comments
    comment_count = len(comments)
    return render(request, 'index.html', {"comments": comments})


@login_required(login_url='/accounts/login')
def get_users(request):
    users = User.objects.all()

    return render(request, 'discover.html', {"users": users})


@login_required(login_url='/accounts/login')
def discover(request, id):
    current_user = request.user
    user = User.objects.get(id=pk)
    following_profile = current_user.profile.followers.add(user.profile)
    return redirect(get_users)
