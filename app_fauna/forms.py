from django import forms
from django.contrib.auth.models import User
from .models import PerfilUsuario, Publicacion


class RegistroForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    first_name = forms.CharField(label='Nombre')
    last_name = forms.CharField(label='Apellido')
    ubicacion = forms.CharField(label='Ubicación')

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            PerfilUsuario.objects.create(
                user=user,
                ubicacion=self.cleaned_data['ubicacion']
            )
        return user



class PerfilUsuarioForm(forms.ModelForm):
    first_name = forms.CharField(label='Nombre', max_length=30)
    last_name = forms.CharField(label='Apellido', max_length=30)

    class Meta:
        model = PerfilUsuario
        fields = ['ubicacion', 'foto_perfil']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name

    def save(self, commit=True):
        perfil = super().save(commit=False)
        user = perfil.user
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
            perfil.save()
        return perfil

class PublicacionForm(forms.ModelForm):
    especie_nombre = forms.CharField(label='Especie', max_length=255)
    lugar_nombre = forms.CharField(label='Lugar', max_length=255)

    class Meta:
        model = Publicacion
        fields = ['titulo', 'descripcion', 'imagen_principal']  # quitar FK

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Si instancia con objeto, inicializa con los nombres FK actuales
        if self.instance and self.instance.pk:
            if self.instance.especie:
                self.fields['especie_nombre'].initial = self.instance.especie.nombre_comun
            if self.instance.lugar:
                self.fields['lugar_nombre'].initial = self.instance.lugar.nombre

    def clean_especie_nombre(self):
        nombre = self.cleaned_data['especie_nombre'].strip()
        if not nombre:
            raise forms.ValidationError("Debe ingresar un nombre para la especie.")
        return nombre

    def clean_lugar_nombre(self):
        nombre = self.cleaned_data['lugar_nombre'].strip()
        if not nombre:
            raise forms.ValidationError("Debe ingresar un nombre para el lugar.")
        return nombre