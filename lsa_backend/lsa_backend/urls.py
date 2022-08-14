"""lsa_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import include, path
from django.urls import path
from rest_framework import routers, serializers, viewsets
from login.models import Usuario
from django.contrib import admin
from rest_framework.authtoken import views
from login.views import *
from rest_framework.permissions import IsAuthenticated
from aprendizaje.viewset import SenaViewset, UsuarioSenaViewset
from django.config import settings
from django.config.urls.static import static
# Serializers define the API representation.

class UsuarioSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Usuario
        fields = ['url', 'email', 'nombre', 'apellido',]

# ViewSets define the view behavior.
class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [IsAuthenticated]


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'usuario', UsuarioViewSet)
router.register(r'senas', SenaViewset)
router.register(r'usuario_senas', UsuarioSenaViewset)



# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),
    path('api-token-auth/', views.obtain_auth_token),
    path('login/', login),
    path('senas/get_senas_categoria', SenaViewset.get_senas_categoria),
    path('usuario/get_senas_usuario', UsuarioSenaViewset.get_senas_usuario),
    path('usuario/post_sena_usuario', UsuarioSenaViewset.post_sena_usuario),
]+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
