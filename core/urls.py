from django.contrib import admin
from django.urls import path,include,re_path
# swagger
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
# media files
from django.views.static import serve
from django.conf import settings
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path("auth/", include("account.urls")),
    path('chat/',include("chat.urls")),
    path("user/",include("user.urls")),
    path("group/",include("group.urls")),
    re_path(r"^media/(?P<path>.*)$",serve,{"document_root":settings.MEDIA_ROOT}),
]
