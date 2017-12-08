from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url('^$', views.index, name='slaygram'),
    url('^profiles/edit', views.update_user_profile, name="updateuserprofile"),
    url(r'^upload/new_post', views.new_post, name="new_post"),
    url(r'^profiles/(\d+)/$', views.posts, name="post"),
    url(r'^post/upvote/(\d+)$', views.upvote_post, name="upvote_post"),
    url(r'^post/downvote/(\d+)$', views.downvote_post, name="downvote_post"),
    url(r'^post/comment/(\d+)$', views.post_comment, name="post_comment"),
    url(r'^profile/follow/(\d+)$', views.follow, name="follow"),
    url(r'^post/download/(\d+)$', views.download_image, name="download_image"),
    url(r'^post/comments/(\d+)$', views.get_comments, name="get_comments"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
