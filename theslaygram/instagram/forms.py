from django import forms
from .models import Profile, User, Post


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', )


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('portfolio', 'bio', 'gender')


class NewPostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ['user', 'pub_date']
