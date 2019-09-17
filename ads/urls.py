"""ads URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path

from projects.views import AddOriginatorView, AddProjectDetailView, SummaryView, EditProjectDetailView, \
    EditOriginatorView, ProjectView, ProjectDetailView, AddCostView, LoginView, LogoutView, VoteView, VoteConfirmView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('add_project/', AddOriginatorView.as_view(), name='add_project'),
    path('edit_project/', EditOriginatorView.as_view(), name='edit_project'),
    path('add_project/details/', AddProjectDetailView.as_view(), name='add_project_details'),
    path('edit_project/details/', EditProjectDetailView.as_view(), name='edit_project_details'),
    path('add_project/costs/', AddCostView.as_view(), name='add_project_costs'),
    path('add_project/summary/', SummaryView.as_view(), name='summary_view'),
    path('projects', ProjectView.as_view(), name='projects'),
    re_path(r'project/(?P<id>(\d)+)', ProjectDetailView.as_view(), name='project_detail'),
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('vote', VoteView.as_view(), name='vote'),
    path('vote/confirm', VoteConfirmView.as_view(), name='vote_confirm'),
]
