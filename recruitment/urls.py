from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from django.conf.urls import include
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from jobs.models import Job
from jobs.models import Resume


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff']


class UserViewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class JobSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Job
        fields = '__all__'


class JobViewset(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer


class ResumeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Resume
        fields = '__all__'


class ResumeViewset(viewsets.ModelViewSet):
    queryset = Resume.objects.all()
    serializer_class = ResumeSerializer


router = routers.DefaultRouter()
router.register('users', UserViewset)
router.register('jobs', JobViewset)
router.register('resumes', ResumeViewset)

urlpatterns = [
    url(r'^', include('jobs.urls')),
    path('grappelli/', include('grappelli.urls')),
    path('admin/', admin.site.urls),
    url(r'^accounts/', include('registration.backends.simple.urls')),
    # rest framework url
    path(r'api-auth/', include('rest_framework.urls')),
    path(r'api/', include(router.urls)),
]
