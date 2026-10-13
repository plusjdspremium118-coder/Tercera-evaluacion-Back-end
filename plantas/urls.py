from django.urls import path
from . import views
from django.conf import settings
from django.contrib.staticfiles.urls import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('nosotros', views.nosotros, name='nosotros'),
    path('plantas', views.plantas, name='plantas'),
    path('plantas/crear', views.crear, name='crear'),
    path('plantas/editar/<int:id>', views.editar, name='editar'),
    path('eliminar/<int:id>', views.eliminar, name='eliminar'),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/plantas/', views.PlantaList.as_view(), name='api_plantas_list'),
    path('api/plantas/<int:pk>/', views.PlantaDetail.as_view(), name='api_plantas_detail'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)