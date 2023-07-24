from rest_framework.routers import SimpleRouter

from django.urls import include, path

from .views import TaskViewSet, UserViewSet


router = SimpleRouter()

router.register(r'tasks', TaskViewSet)
router.register(r'users', UserViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]
