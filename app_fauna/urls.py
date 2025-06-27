from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from .views import *

urlpatterns = [
    # Publicación
    path('', PublicacionListView.as_view(), name='publicacion_list'),
    path('publicacion/<int:pk>/', PublicacionDetailView.as_view(), name='publicacion_detail'),
    path('publicacion/nueva/', PublicacionCreateView.as_view(), name='publicacion_create'),
    path('publicacion/<int:pk>/editar/', PublicacionUpdateView.as_view(), name='publicacion_update'),
    path('publicacion/<int:pk>/eliminar/', PublicacionDeleteView.as_view(), name='publicacion_delete'),

    # Especie
    path('especies/', EspecieListView.as_view(), name='especie_list'),
    path('especie/nueva/', EspecieCreateView.as_view(), name='especie_create'),
    path('especie/<int:pk>/editar/', EspecieUpdateView.as_view(), name='especie_update'),
    path('especie/<int:pk>/eliminar/', EspecieDeleteView.as_view(), name='especie_delete'),

    # Lugar
    path('lugares/', LugarListView.as_view(), name='lugar_list'),
    path('lugar/nuevo/', LugarCreateView.as_view(), name='lugar_create'),
    path('lugar/<int:pk>/editar/', LugarUpdateView.as_view(), name='lugar_update'),
    path('lugar/<int:pk>/eliminar/', LugarDeleteView.as_view(), name='lugar_delete'),

    # Comentario
    path('publicacion/<int:pk>/comentar/', ComentarioCreateView.as_view(), name='comentario_create'),

    # Likes
    path('publicacion/<int:pk>/like/', LikeToggleView.as_view(), name='like_toggle'),
    path('', IndexView.as_view(), name='index'),

    path('login/', LoginView.as_view(template_name='usuarios/login.html'), name='login'),
path('perfil/eliminar/', PerfilDeleteView.as_view(), name='perfil_eliminar'),

    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('registro/', RegistroView.as_view(), name='registro'),
    path('perfil/', PerfilView.as_view(), name='perfil'),
    path('perfil/editar/', PerfilEditView.as_view(), name='perfil_editar'),
]
