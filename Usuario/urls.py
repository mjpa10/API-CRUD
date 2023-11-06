from django.urls import path #Importa a função path de do modulo 'django.urls'
from . import views # Importa as visualizações definidas no arquivo atual
from django.conf import settings #Inporta as configs do django
from django.conf.urls.static import static #Importa a função 'static' para servir arquivos estáticos durante o desenvolvimento

urlpatterns = [
    path('',views.CadastrarUsuario.as_view(),name='cadastro'),
    path('listar_usuarios',views.ListarUsuario.as_view(),name='listar'),
    path('usuario/<int:pk>/atualizar',views.UpdateUsuario.as_view(),name='update'),
    path('usuario/<int:pk>/deletar',views.DeleteUsuario.as_view(),name='deletar')
 ]

if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT) # para acessar as midias via url