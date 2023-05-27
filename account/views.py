from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db.utils import IntegrityError

from django.contrib.auth.decorators import login_required
from django.contrib import messages


def login_view(request):
    """
    Vista para iniciar sesión.
    """
    error_message = None

    # Si la solicitud es POST, procesar el formulario de inicio de sesión
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Si el usuario es válido, iniciar sesión y redirigir a la página de inicio
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            # Mostrar un mensaje de error si el nombre de usuario o la contraseña son incorrectos
            error_message = "El nombre de usuario o la contraseña son incorrectos. Por favor inténtalo de nuevo."

    # Si la solicitud no es POST o hay un mensaje de error, renderizar el formulario de inicio de sesión
    return render(request, "login.html", {"error_message": error_message})


def logout_view(request):
    """
    Vista para cerrar sesión.
    """
    logout(request)
    return redirect("home")


def signup_view(request):
    """
    Vista para registrarse.
    """
    error_message = None

    # Si la solicitud es POST, procesar el formulario de registro
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]

        # Verificar si las contraseñas coinciden
        if password1 == password2:
            try:
                # Crear un nuevo usuario y redirigir a la página de inicio
                user = User.objects.create_user(
                    username=username, email=email, password=password1
                )
                login(request, user)
                return redirect("home")
            except IntegrityError:
                # Mostrar un mensaje de error si el nombre de usuario ya existe
                error_message = "El nombre de usuario ya existe. Por favor elige otro."
        else:
            # Mostrar un mensaje de error si las contraseñas no coinciden
            error_message = (
                "Las contraseñas no coinciden. Por favor inténtalo de nuevo."
            )

    # Si la solicitud no es POST o hay un mensaje de error, renderizar el formulario de registro
    return render(request, "signup.html", {"error_message": error_message})


@login_required
def edit_user_view(request):
    """
    Vista para actualizar la información del usuario.
    """
    error_message = None
    success_message = None

    # Si la solicitud es POST, procesar el formulario y guardar los cambios en el usuario actual
    if request.method == "POST":
        username = request.POST["username"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        email = request.POST["email"]
        password = request.POST["password"]

        # Verificar si el nombre de usuario ya existe
        if (
            username != request.user.username
            and User.objects.filter(username=username).exists()
        ):
            error_message = "El nombre de usuario ya está en uso."
        else:
            # Actualizar los campos en el usuario y guardar los cambios
            user = request.user
            user.username = username
            user.first_name = first_name
            user.last_name = last_name
            user.email = email

            if password:
                user.set_password(password)

            user.save()

            # Actualizar la sesión del usuario para mantenerlo autenticado después de cambiar su contraseña
            login(request, user)

            # Establecer el mensaje de éxito
            success_message = "Los cambios han sido guardados."

    # Renderizar el formulario con los datos actuales del usuario (actualizados o no)
    return render(
        request,
        "edit_user.html",
        {
            "user": request.user,
            "error_message": error_message,
            "success_message": success_message,
        },
    )
