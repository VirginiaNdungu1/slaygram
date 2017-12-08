from django import forms
from .models import Profile, User, Post, Review


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', )


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('portfolio', 'bio', 'gender', 'profile_pic')


class NewPostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ['user', 'pub_date', 'vote_score',
                   'num_vote_up', 'num_vote_down', 'upvote_count', 'downvote_count']


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('comment',)
