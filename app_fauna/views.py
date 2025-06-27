from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView, View, TemplateView
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect, get_object_or_404

from .forms import RegistroForm, PerfilUsuarioForm, PublicacionForm
from .models import Publicacion, Especie, Lugar, Comentario, Like, PerfilUsuario
from django.contrib.auth.models import User

class IndexView(TemplateView):
    template_name = 'index.html'

# --- PUBLICACIÓN ---

class PublicacionListView(ListView):
    model = Publicacion
    template_name = 'publicacion/list.html'
    context_object_name = 'publicaciones'

class PublicacionDetailView(DetailView):
    model = Publicacion
    template_name = 'publicacion/detail.html'
    context_object_name = 'publicacion'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        publicacion = self.get_object()
        user = self.request.user
        context['usuario_ya_dio_like'] = False
        if user.is_authenticated:
            context['usuario_ya_dio_like'] = publicacion.likes.filter(usuario=self.request.user).exists()
        return context


class PublicacionCreateView(LoginRequiredMixin, CreateView):
    model = Publicacion
    form_class = PublicacionForm
    template_name = 'publicacion/form.html'

    def form_valid(self, form):
        # Crear o recuperar Especie
        especie_nombre = form.cleaned_data['especie_nombre']
        especie, created = Especie.objects.get_or_create(nombre_comun=especie_nombre)

        # Crear o recuperar Lugar
        lugar_nombre = form.cleaned_data['lugar_nombre']
        lugar, created = Lugar.objects.get_or_create(nombre=lugar_nombre)

        form.instance.especie = especie
        form.instance.lugar = lugar
        form.instance.autor = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        # redirige a detalle de la publicación creada
        return reverse_lazy('publicacion_detail', kwargs={'pk': self.object.pk})


class PublicacionUpdateView(LoginRequiredMixin, UpdateView):
    model = Publicacion
    form_class = PublicacionForm
    template_name = 'publicacion/form.html'

    def form_valid(self, form):
        especie_nombre = form.cleaned_data['especie_nombre']
        especie, created = Especie.objects.get_or_create(nombre_comun=especie_nombre)

        lugar_nombre = form.cleaned_data['lugar_nombre']
        lugar, created = Lugar.objects.get_or_create(nombre=lugar_nombre)

        form.instance.especie = especie
        form.instance.lugar = lugar
        return super().form_valid(form)

    def get_success_url(self):
        # redirige a detalle de la publicación creada
        return reverse_lazy('publicacion_detail', kwargs={'pk': self.object.pk})

class PublicacionDeleteView(LoginRequiredMixin, DeleteView):
    model = Publicacion
    template_name = 'publicacion/confirm_delete.html'
    success_url = reverse_lazy('publicacion_list')


# --- ESPECIE ---

class EspecieListView(ListView):
    model = Especie
    template_name = 'especie/list.html'
    context_object_name = 'especies'

class EspecieCreateView(LoginRequiredMixin, CreateView):
    model = Especie
    template_name = 'especie/form.html'
    fields = ['nombre_comun', 'nombre_cientifico', 'descripcion', 'imagen']

class EspecieUpdateView(LoginRequiredMixin, UpdateView):
    model = Especie
    template_name = 'especie/form.html'
    fields = ['nombre_comun', 'nombre_cientifico', 'descripcion', 'imagen']

class EspecieDeleteView(LoginRequiredMixin, DeleteView):
    model = Especie
    template_name = 'especie/confirm_delete.html'
    success_url = reverse_lazy('especie_list')


# --- LUGAR ---

class LugarListView(ListView):
    model = Lugar
    template_name = 'lugar/list.html'
    context_object_name = 'lugares'

class LugarCreateView(LoginRequiredMixin, CreateView):
    model = Lugar
    template_name = 'lugar/form.html'
    fields = ['nombre', 'ubicacion', 'descripcion', 'imagen']

class LugarUpdateView(LoginRequiredMixin, UpdateView):
    model = Lugar
    template_name = 'lugar/form.html'
    fields = ['nombre', 'ubicacion', 'descripcion', 'imagen']

class LugarDeleteView(LoginRequiredMixin, DeleteView):
    model = Lugar
    template_name = 'lugar/confirm_delete.html'
    success_url = reverse_lazy('lugar_list')


# --- COMENTARIO ---

class ComentarioCreateView(LoginRequiredMixin, CreateView):
    model = Comentario
    template_name = 'comentario/form.html'
    fields = ['contenido']

    def dispatch(self, request, *args, **kwargs):
        self.publicacion = get_object_or_404(Publicacion, pk=self.kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.autor = self.request.user
        form.instance.publicacion = self.publicacion
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('publicacion_detail', kwargs={'pk': self.publicacion.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['publicacion'] = self.publicacion  # 👈 Pasamos el objeto al template
        return context

class ComentarioUpdateView(LoginRequiredMixin, UpdateView):
    model = Comentario
    fields = ['contenido']
    template_name = 'comentario/form.html'

    def get_queryset(self):
        return Comentario.objects.filter(autor=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Agrega la publicación asociada al comentario al contexto
        context['publicacion'] = self.object.publicacion
        return context

    def get_success_url(self):
        return reverse_lazy('publicacion_detail', kwargs={'pk': self.object.publicacion.pk})



class ComentarioDeleteView(LoginRequiredMixin, DeleteView):
    model = Comentario
    template_name = 'comentario/confirm_delete.html'

    def get_queryset(self):
        return Comentario.objects.filter(autor=self.request.user)

    def get_success_url(self):
        return reverse_lazy('publicacion_detail', kwargs={'pk': self.object.publicacion.pk})


# --- LIKE (solo crear y eliminar automáticamente) ---

class LikeToggleView(LoginRequiredMixin, View):
    def post(self, request, pk):
        publicacion = get_object_or_404(Publicacion, pk=pk)
        like, created = Like.objects.get_or_create(publicacion=publicacion, usuario=request.user)
        if not created:
            like.delete()
        return redirect('publicacion_detail', pk=pk)




class RegistroView(CreateView):
    form_class = RegistroForm
    template_name = 'usuarios/registro.html'
    success_url = reverse_lazy('login')

class PerfilView(LoginRequiredMixin, TemplateView):
    template_name = 'usuarios/perfil.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        perfil = PerfilUsuario.objects.filter(user=self.request.user).first()
        context['perfil'] = perfil
        # Agregar publicaciones propias
        context['publicaciones_usuario'] = Publicacion.objects.filter(autor=self.request.user)
        return context


class PerfilEditView(LoginRequiredMixin, UpdateView):
    model = PerfilUsuario
    form_class = PerfilUsuarioForm
    template_name = 'usuarios/perfil_form.html'

    def get_object(self, queryset=None):
        return PerfilUsuario.objects.get(user=self.request.user)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_success_url(self):
        return reverse_lazy('perfil')


class PerfilDeleteView(LoginRequiredMixin, DeleteView):
    model = PerfilUsuario
    template_name = 'usuarios/perfil_confirm_delete.html'
    success_url = reverse_lazy('index')

    def get_object(self, queryset=None):
        return PerfilUsuario.objects.get(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        # Opcional: borrar también el usuario auth para eliminar todo
        user = request.user
        self.object = self.get_object()
        response = super().delete(request, *args, **kwargs)
        user.delete()  # elimina el usuario auth
        return response