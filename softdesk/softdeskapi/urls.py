from django.urls import path, include
from . import views

urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('projects/', views.ProjectList.as_view()),
    path('projects/<int:pk>/', views.ProjectDetail.as_view()),
    path('projects/<int:pk>/users/', views.ProjectUserList.as_view()),
    path('projects/<int:pk_project>/users/<int:pk_user>/', views.ProjectUserDelete.as_view()),
    path('projects/<int:pk>/issues/', views.IssueList.as_view()),
    path('projects/<int:pk_project>/issues/<int:pk_issue>/', views.IssueDetail.as_view()),
    # path('users/<int:pk>/', views.UserDetail.as_view()),
    path('signup/', views.Signup.as_view()),
    path('contributor/', views.contributor_list),
    path('users', views.UserList.as_view())
]