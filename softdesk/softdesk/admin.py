from django.contrib import admin
from softdesk.models import User, Project, Contributor, Issue, Comment

admin.site.register([User, Project, Contributor, Issue, Comment])