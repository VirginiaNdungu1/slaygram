from django.conf.urls import url
from . import views

urlpatterns = [
    url('^$', views.index, name='slaygram'),
    url('^profiles/edit', views.update_user_profile, name="updateuserprofile")
]
