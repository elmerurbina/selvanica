from django.db import models
from django.contrib.auth.models import User

# Perfil extendido del usuario
class PerfilUsuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ubicacion = models.CharField(max_length=100)
    foto_perfil = models.ImageField(upload_to='perfiles/', null=True, blank=True)

    def __str__(self):
        return self.user.get_full_name() or self.user.username

# Especie animal exótica
class Especie(models.Model):
    nombre_comun = models.CharField(max_length=100)
    nombre_cientifico = models.CharField(max_length=150, blank=True, null=True)
    descripcion = models.TextField()
    imagen = models.ImageField(upload_to='especies/')

    def __str__(self):
        return self.nombre_comun

# Lugar natural de Nicaragua
class Lugar(models.Model):
    nombre = models.CharField(max_length=100)
    ubicacion = models.CharField(max_length=255)
    descripcion = models.TextField()
    imagen = models.ImageField(upload_to='lugares/')

    def __str__(self):
        return self.nombre

# Publicación del usuario (puede incluir especie o lugar)
class Publicacion(models.Model):
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    especie = models.ForeignKey(Especie, on_delete=models.SET_NULL, null=True, blank=True)
    lugar = models.ForeignKey(Lugar, on_delete=models.SET_NULL, null=True, blank=True)
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    imagen_principal = models.ImageField(upload_to='publicaciones/')
    fecha_publicacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo

# Comentarios a publicaciones
class Comentario(models.Model):
    publicacion = models.ForeignKey(Publicacion, on_delete=models.CASCADE, related_name='comentarios')
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    contenido = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comentario de {self.autor.username}'

# Likes a publicaciones
class Like(models.Model):
    publicacion = models.ForeignKey(Publicacion, on_delete=models.CASCADE, related_name='likes')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('publicacion', 'usuario')

    def __str__(self):
        return f'{self.usuario.username} dio like a {self.publicacion.titulo}'

# Fotos adicionales por publicación
class FotoExtra(models.Model):
    publicacion = models.ForeignKey(Publicacion, on_delete=models.CASCADE, related_name='fotos_extra')
    imagen = models.ImageField(upload_to='fotos_extra/')
    descripcion = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f'Foto adicional para {self.publicacion.titulo}'
