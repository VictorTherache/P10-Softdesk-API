from rest_framework.permissions import SAFE_METHODS, BasePermission
from rest_framework import permissions
from .models import Contributor, Issue, Projet
import re


class IsOwnerorContributor(permissions.BasePermission):
    """
    Check if the user is an author or a contributor of a project
    """
    message = 'You must be a contributor or an owner of this project'
    def has_permission(self, request, view):
        url_path = request.get_full_path()
        project_id = re.search("(?<=projets/)(.*)(?=/)", url_path)
        if "issues" in url_path:
            project_id = re.search("(?<=projets/)(.*)(?=/issues)", url_path)
        if "comments" in url_path:
            project_id = re.search("(?<=projets/)(.*)(?=/issues)", url_path)
        project_id = project_id.group()
        author_projects = Projet.objects.filter(author=request.user, id=project_id)
        contributor_projects = Contributor.objects.filter(user = request.user, projet = project_id)
        if (author_projects or contributor_projects):
            return True
        else:
            return False

class IsProjectOwner(permissions.BasePermission):
    """
    Check if user is the projects owner
    """
    message = 'You must be an owner'

    def has_permission(self, request, view):
        url_path = request.get_full_path()
        print(url_path)
        project_id = re.search("(?<=projets/)(.*)(?=/)", url_path)
        project_id = project_id.group()
        if "contributors" in url_path:
            project_id = re.search("(?<=projets/)(.*)(?=/contributor)", url_path)
            project_id = project_id.group()
        author_projects = Projet.objects.filter(author=request.user, id=project_id)
        if (author_projects):
            return True
        else:
            return False


class IsIssueOwner(permissions.BasePermission):
    """
    Check if the user is the issues author
    """
    message = 'You must be an owner'
    def has_object_permission(self, request, view, obj):
        print(obj.author_user_id_id)
        print(request.user.id)
        return True if int(obj.author_user_id_id) == int(request.user.id) else False



class IsCommentOwner(permissions.BasePermission):
    """
    Check if current user is the author of the comment
    """
    message = 'You must be the owner'

    def has_object_permission(self, request, view, obj):
        print(obj.author_id)
        print('WOOF')
        if (obj.author_id == request.user.id):
            return True
        else:
            return False