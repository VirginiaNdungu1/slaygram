from django.db import models
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from django.db.models import Q, signals
from django.dispatch import receiver
from tinymce.models import HTMLField
from vote.models import VoteModel
from vote.managers import VotableManager
# Create your models here.
Gender_Choices = (
    ('F', 'female'),
    ('M', 'male'),
    ('Both', 'both'),
    ('None', 'non-specified'),
)


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile')
    portfolio = models.CharField(max_length=500, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    gender = models.CharField(
        max_length=30, choices=Gender_Choices, default='None', blank=True)
    philosophy = models.TextField(max_length=500, blank=True)


User.profile = property(lambda u: Profile.objects.get_or_create(user=u)[0])


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


post_save.connect(create_user_profile, sender=User)


class Post(VoteModel, models.Model):
    votes = VotableManager()

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='post')

    picture = models.ImageField(upload_to='pictures/', blank=True)
    caption = models.TextField(max_length=140)
    upvote_count = models.PositiveIntegerField(default=0)
    downvote_count = models.PositiveIntegerField(default=0)
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['pub_date']

    def save_post(self):
        self.save()

    @classmethod
    def display_users_posts(cls, id):
        posts = cls.objects.filter(user_id=id)
        return posts

    @classmethod
    def display_posts(cls):
        posts = cls.objects.all()
        return posts

    @property
    def image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url

    @classmethod
    def get_single_post(cls, pk):
        post = cls.objects.get(pk=pk)
        # upvote = post.votes.up(id=id)
        return post


class Review(models.Model):
    users = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="vote")
    pictures = models.ForeignKey(Post, related_name="vote")
    created_at = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(max_length=140, blank=True)

    class Meta:
        ordering = ['created_at']

    def save_review(self):
        self.save()

    @classmethod
    def get_single_comment(cls, id):
        comment = cls.objects.get(id=pk)
        return comment

    @classmethod
    def get_comments(cls, id):
        comments = cls.objects.all()
        return comments
