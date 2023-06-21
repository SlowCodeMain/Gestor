from django.shortcuts import render, redirect
from django.views import View

from django.contrib.auth import authenticate, login, logout

from core.models import Directivo


class DirectivosLoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('directivos_home')
        return render(request, 'directivos/login/view_login_directivos.html')

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')

        login_user = authenticate(request, email=email, password=password)
        if login_user is not None:
            login(request, login_user)
            return redirect('directivos_home')

        return render(request, 'directivos/login/view_login_directivos.html', {'error': 'Correo o contraseña incorrectos'})


class DirectivosLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('directivos_login')


class DirectivosHomeView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('directivos_login')
        return render(request, 'directivos/home/view_home_directivos.html')


class DirectivosCrearView(View):

    def get(self, request):
        return render(request, 'directivos/crear/view_crear_directivos.html')

    def post(self, request):
        # campos
        # nombre, email, apellidos, fecha_nacimiento, direccion, numero_telefono, imagen, puesto
        nombre = request.POST.get('nombres')
        apellidos = request.POST.get('apellidos')
        email = request.POST.get('email')
        numero_telefono = request.POST.get('numero_telefono')
        direccion = request.POST.get('direccion')
        fecha_nacimiento = request.POST.get('fecha_nacimiento')
        puesto = request.POST.get('puesto')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        imagen = request.FILES.get('imagen')

        if password1 != password2:
            return render(request, 'directivos/crear/view_crear_directivos.html', {'error': 'Las contraseñas no coinciden'})
        if Directivo.objects.filter(email=email).exists():
            return render(request, 'directivos/crear/view_crear_directivos.html',
                          {'error': 'Este correo ya esta registrado'})

        directivo = Directivo.objects.create(
            email=email,
            nombre=nombre,
            apellidos=apellidos,
            numero_telefono=numero_telefono,
            direccion=direccion,
            fecha_nacimiento=fecha_nacimiento,
            puesto=puesto,
            imagen=imagen,
        )
        directivo.set_password(password1)
        directivo.save()
        directivo.crearCredencial()

        print('deberia de llegar aqui')

        return render(request, 'directivos/crear/view_crear_directivos.html', context={'success': 'Directivo creado con exito, iniciar sesion: '})
