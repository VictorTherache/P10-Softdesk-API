from django.urls import include, path
from rest_framework_nested import routers
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


router = routers.SimpleRouter()
router.register(r'projets', views.ProjetViewSet, basename='projets')
# router.register(r'issues', views.IssueViewSet)
router.register(r'users', views.UserViewSet)
# router.register(r'contributor', views.ContributorViewSet)

projet_router = routers.NestedSimpleRouter(router, r'projets', lookup='projet')
projet_router.register(r'issues', views.IssueViewSet, basename='projet-issues')
projet_router.register(r'contributors', views.ContributorViewSet, basename='projet-contributors')

issue_router = routers.NestedSimpleRouter(projet_router, r'issues', lookup='issue')
issue_router.register(r'comments', views.CommentsViewSet, basename='comments')
# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path(r'', include(projet_router.urls)),
    path(r'', include(issue_router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # path('user/', views.UserAPIView.as_view(), name='user'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('signup/', views.RegisterView.as_view(), name='auth_register'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]