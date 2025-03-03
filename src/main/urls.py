from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('posts/tag/<str:tagname>/', views.posts_by_tag, name="posts-by-tag"),

    path('post/<int:post_id>/', views.get_post, name="post"),
    path('post/<int:post_id>/like', views.like, name="like"),
    path('post/<int:post_id>/entry/<int:entry_id>/', views.post_entry, name="entry"),

    path('create/', views.create_post, name="create_post"),
    path('profile/<str:username>', views.profile, name="profile"),
]