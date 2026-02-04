"""
URL configuration for softdesk_API project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.urls import include, path
from rest_framework import routers

from authentication import views as auth_views
from support_API import views as support_views

router = routers.DefaultRouter()

router.register(r"users", auth_views.UserViewSet)
router.register(r"groups", auth_views.GroupViewSet)

router.register(r"projects", support_views.ProjectViewSet)
router.register(r"issues", support_views.IssueViewSet)
router.register(r"comments", support_views.CommentViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include(router.urls)),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path('hello/', support_views.HelloView.as_view(), name='hello'),
]

