from django.contrib import messages, auth
from django.contrib.messages import constants

from django.contrib.auth.models import User
from django.shortcuts import render, redirect

def logar(request):
    if request.method == "GET":
        return render(request, 'logar.html')
    elif request.method == "POST":
        username = request.POST.get('username')
        senha = request.POST.get('senha')
        user = auth.authenticate(request, username=username, password=senha)
    if user:
        auth.login(request, user)
        return redirect('/home') # Vai dar erro
    messages.add_message(
        request,
        constants.ERROR,
        'Usuario ou senha inválidos'
    )
    return redirect('/usuarios/logar')


def cadastro(request):
    if request.method == "GET":
        return render(request, 'cadastro.html')
    elif request.method == "POST":
        username = request.POST.get('username')
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')
        if not senha == confirmar_senha:
            messages.add_message(
                request,
                constants.ERROR,
                'As senhas não coincidem'
            )
            return redirect('/usuarios/cadastro')
        if len(senha) < 6:
            messages.add_message(
                request,
                constants.ERROR,
                'A senha deve possuir pelo menos 6 caracteres'
            )
            return redirect('/usuarios/cadastro')
        users = User.objects.filter(username=username)
        if users.exists():
            messages.add_message(
                request,
                constants.ERROR,
                'Já existe um usuário com esse username'
            )
            return redirect('/usuarios/cadastro')
        user = User.objects.create_user(
            username=username,
            password=senha
        )
        return redirect('/usuarios/logar')
