from rest_framework import viewsets
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import RetrieveAPIView
from rest_framework import generics

from .serializers import ContributorSerializer, ProjetSerializer, IssueSerializer, UserSerializer, CommentsSerializer
from .models import Projet, Issue, User, Contributor, Comments
from .permissions import IsOwnerorContributor, IsProjectOwner, IsCommentOwner, IsIssueOwner


class UserViewSet(viewsets.ModelViewSet):
    """
    UserViewset to get info of the users in the app
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        """
        Sets the permissions for the actions
        """
        if self.request.method == 'POST':
            self.permission_classes = (IsAuthenticated,)

        return super(UserViewSet, self).get_permissions()


class RegisterView(generics.CreateAPIView):
    """
    Register View to register a new user
    """
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer


class ProjetViewSet(viewsets.ModelViewSet):
    """
    Project ViewSet with custom permissions 
    """
    serializer_class = ProjetSerializer
    queryset = Projet.objects.all().order_by('title')


    def get_permissions(self):
        """
        Sets the permissions for the actions
        """
        if self.action == 'list':
            permission_classes = [IsAuthenticated]
        if self.action == 'retrieve':
            print('retrieve')
            permission_classes = [IsOwnerorContributor]
        if self.action == 'update':
            permission_classes = [IsProjectOwner]
        if self.action == 'create':
            permission_classes = [IsAuthenticated]
        if self.action == 'destroy':
            permission_classes = [IsProjectOwner]
        return [permission() for permission in permission_classes]


    def get_queryset(self):
        """
        Returns a list of filtered objects based on if the user
        is a contributor or an author
        """
        result_list = []
        my_projects = Contributor.objects.filter(user = self.request.user.id)
        all_projects = Projet.objects.all()
        for project in all_projects:
            for my_project in my_projects:
                if project.id == int(my_project.projet_id):
                    result_list.append(project.id)
        author_projects = Projet.objects.filter(author = self.request.user.id)
        for author_project in author_projects:
            result_list.append(author_project.id)
        return Projet.objects.filter(pk__in=result_list)


    def perform_create(self, serializer):
        """
        Action to perform before displaying the object
        """
        serializer.save(author = self.request.user)


class IssueViewSet(viewsets.ModelViewSet):
    """
    IssueViewSet with custom permissions
    """
    serializer_class = IssueSerializer
    queryset = Issue.objects.all()

    def get_permissions(self):
        """
        Sets the permissions for the actions
        """
        if self.action == 'list':
            print('list')
            permission_classes = [IsAuthenticated]
        if self.action == 'retrieve':
            print('retrieve')
            permission_classes = [IsOwnerorContributor]
        if self.action == 'update':
            permission_classes = [IsIssueOwner]
        if self.action == 'create':
            permission_classes = [IsOwnerorContributor]
        if self.action == 'destroy':
            permission_classes = [IsIssueOwner]
        return [permission() for permission in permission_classes]


    def get_queryset(self):
        """
        Returns a list of filtered objects based on if the user
        is a contributor or an author
        """
        my_projects = []
        contrib_projects = Contributor.objects.filter(user = self.request.user.id)
        for project in contrib_projects:
            my_projects.append(project.projet_id)
        author_projects = Projet.objects.filter(author = self.request.user.id)
        for project in author_projects:
            my_projects.append(project.id)
        for project_id in my_projects:
            if int(project_id) == int(self.kwargs['projet_pk']):
                return Issue.objects.filter(projet__in=self.kwargs['projet_pk'])
        return []


    def perform_create(self, serializer):
        """
        Action to perform before displaying the object
        """
        serializer.save(author_user_id = self.request.user, assigned_user = self.request.user)


class ContributorViewSet(viewsets.ModelViewSet):

    queryset = Contributor.objects.all()
    serializer_class = ContributorSerializer


    def get_permissions(self):
        """
        Sets the permissions for the actions
        """
        if self.action == 'list':
            print('list')
            permission_classes = [IsOwnerorContributor]
        if self.action == 'retrieve':
            print('retrieve')
            permission_classes = [IsOwnerorContributor]
        if self.action == 'update':
            permission_classes = [IsProjectOwner]
        if self.action == 'create':
            permission_classes = [IsProjectOwner]
        if self.action == 'destroy':
            permission_classes = [IsProjectOwner]
        return [permission() for permission in permission_classes]


    def get_queryset(self):
        """
        Returns a list of filtered objects based on if the user
        is a contributor or an author
        """
        return Contributor.objects.filter(projet=self.kwargs['projet_pk'])


class CommentsViewSet(viewsets.ModelViewSet):
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer


    def get_permissions(self):
        """
        Sets the permissions for the actions
        """
        if self.action == 'list':
            print('list')
            permission_classes = [IsAuthenticated]
        if self.action == 'retrieve':
            print('retrieve')
            permission_classes = [IsOwnerorContributor]
        if self.action == 'create':
            print('commentaire')
            permission_classes = [IsOwnerorContributor]
        if self.action == 'destroy':
            permission_classes = [IsCommentOwner]
        if self.action == 'update':
            print('ees')
            permission_classes = [IsCommentOwner]
        return [permission() for permission in permission_classes]
    

    def get_queryset(self):
        """
        Returns a list of filtered objects based on if the user
        is a contributor or an author
        """
        my_projects = []
        contrib_projects = Contributor.objects.filter(user = self.request.user.id)
        for project in contrib_projects:
            my_projects.append(project.projet_id)
        author_projects = Projet.objects.filter(author = self.request.user.id)
        for project in author_projects:
            my_projects.append(project.id)
        # print(my_projects)
        if int(self.kwargs['projet_pk']) in my_projects:
            comment_queryset =  Comments.objects.filter(issue_id=self.kwargs['issue_pk'])
            return comment_queryset

    def perform_create(self, serializer):
        """
        Action to perform before displaying the object
        """
        serializer.save(author=self.request.user)
