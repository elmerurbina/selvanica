from .models import PerfilUsuario

def perfil_usuario(request):
    perfil = None
    if request.user.is_authenticated:
        perfil = PerfilUsuario.objects.filter(user=request.user).first()
    return {
        'perfil_usuario': perfil
    }
