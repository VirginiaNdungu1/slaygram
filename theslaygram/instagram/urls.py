from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url('^$', views.index, name='slaygram'),
    url('^profiles/edit', views.update_user_profile, name="updateuserprofile"),
    url('^upload/new_post', views.new_post, name="new_post"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
