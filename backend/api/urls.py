from django.conf.urls import include, url
from django.conf.urls.static import static
from rest_framework import routers
from .api import (UserViewSet)
from django.urls import path

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Talana Challenge REST API Documentation",
      default_version='v1',
      description="Talana Swagger REST API",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

router = routers.DefaultRouter()
router.register('api/user', UserViewSet, 'user')

urlpatterns = [
    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    url(r'^api/user/create_account/', UserViewSet.as_view({'post': 'create_account'}), name='create_account'),
    url(r'^api/user/verify_account/<int:user_id>', UserViewSet.as_view({'post': 'verify_account'}), name='verify_account'),
    url(r'^api/user/generate_password/(?P<pk>\d+)$', UserViewSet.as_view({'post': 'generate_password'}), name='generate_password'),
    url(r'^api/user/choose_winner/', UserViewSet.as_view({'get': 'choose_winner'}), name='choose_winner')
]

urlpatterns += router.urls
