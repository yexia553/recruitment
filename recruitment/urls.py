from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from django.conf.urls import include
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from rest_framework import permissions
from interview.serializer import CandidateViewSet
from jobs.serializer import JobViewSet
from jobs.serializer import ResumeViewSet
from rest_framework.schemas import get_schema_view
from rest_framework_swagger.renderers import SwaggerUIRenderer, OpenAPIRenderer


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff']


class UserViewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


router = routers.DefaultRouter()
router.register('users', UserViewset)
router.register('jobs', JobViewSet)
router.register('resumes', ResumeViewSet)
router.register('candidates', CandidateViewSet)

schema_view = get_schema_view(title='API DOC',
                              renderer_classes=[SwaggerUIRenderer,
                                                OpenAPIRenderer]
                              )

urlpatterns = [
    url(r'^', include('jobs.urls')),
    path('grappelli/', include('grappelli.urls')),
    path('admin/', admin.site.urls),
    url(r'^accounts/', include('registration.backends.simple.urls')),
    # rest framework url
    path(r'api-auth/', include('rest_framework.urls')),
    path(r'api/', include(router.urls)),
    path('api/docs/', schema_view, name='docs'),
]
