from django import forms
from .models import Profile, User, Post, Review


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', )


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
<<<<<<< HEAD
        fields = ('portfolio', 'bio', 'gender',)
=======
        fields = ('portfolio', 'bio', 'gender', 'profile_pic')
>>>>>>> beb04a541bdec91e621c0604f9c264f8495108a0


class NewPostForm(forms.ModelForm):
    class Meta:
        model = Post
<<<<<<< HEAD
        exclude = ['user', 'pub_date', ]
=======
        exclude = ['user', 'pub_date', 'vote_score',
                   'num_vote_up', 'num_vote_down', 'upvote_count', 'downvote_count']
>>>>>>> beb04a541bdec91e621c0604f9c264f8495108a0


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('comment',)
