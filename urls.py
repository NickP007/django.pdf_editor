from django.urls import path
from . import views

app_name = 'pdf_editor'

urlpatterns = [
#    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('upload/', views.UploadFile, name='UploadFile'),
]

