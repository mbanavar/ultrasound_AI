from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('delete/<int:image_id>/', views.delete_image, name='delete_image'),
    path('about/', views.about, name='about'),
    path('process/<int:image_id>/', views.process_image, name='process_image'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

