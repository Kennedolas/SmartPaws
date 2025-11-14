from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('pets/', include('pets.urls')),
    path('produtos/', include('produtos.urls')),
    path('usuarios/', include('usuarios.urls')),
    path('servicos/', include('servicos.urls')),
    path('', include('core.urls')), 
    path('carrinho/', include('carrinho.urls')),
]

# Servir arquivos de mídia e estáticos em desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
