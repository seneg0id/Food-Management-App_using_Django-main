from django.urls import path , include
from . import views
from .views import (PostListView,PostDetailView,PostCreateView,PostUpdateView,PostDeleteView,UserPostListView)


urlpatterns = [
    path('',views.open,name='openpage'),
    path('home', PostListView.as_view(), name='blog-home'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('post/new/', PostCreateView.as_view(),name='post-create'),
    path('request/<int:id>/',views.food,name='request-food'),
    path('cancel/<int:id>/',views.cancel,name='cancel-request'),
    path('requestedorders/',views.requested,name='requested-orders'),
    path('about/', views.about, name='about-blog'),
    path('search/',views.search,name='search'),
]