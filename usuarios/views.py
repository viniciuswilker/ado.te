from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.messages import constants
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import auth


def cadastro(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('/divulgar/novo_pet')
        return render(request, 'cadastro.html')
    elif request.method == 'POST':  
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')

        if len(nome.strip()) == 0 or len(email.strip()) == 0 or len(senha.strip()) == 0 or len(confirmar_senha.strip()) == 0:
            messages.add_message(request, constants.ERROR, 'Preencha todos os dados')
            return redirect('/auth/cadastro')
        
        if senha != confirmar_senha:
            messages.add_message(request, constants.ERROR, 'Senhas não coincidem')
            return redirect('/auth/cadastro')
        
        try:
            user = User.objects.create_user(
                username=nome,
                email=email,
                password=senha)
            user.save()
            return render(request, 'cadastro.html')
        except:
            messages.add_message(request, constants.ERROR, 'Erro interno do sistema')
            print('Erro interno do sistema')
            return render(request, 'login.html')


def login(request):
        if request.method == 'GET':
            if request.user.is_authenticated:
                return redirect('/divulgar/novo_pet')
            return render(request,'login.html')
        
        elif request.method == 'POST':
            nome = request.POST.get('nome')
            senha = request.POST.get('senha')
            user = authenticate(username=nome, password=senha)

            if len(nome.strip()) == 0 or len(senha.strip()) == 0:
                messages.add_message(request, constants.ERROR, 'Preencha todos os dados')
                return redirect('/auth/login')


            if not user:
                messages.add_message(request, constants.ERROR, 'Usuário não encontrado')
                return redirect('/auth/login')
            else:
                auth.login(request, user)
                return redirect('/divulgar/novo_pet')
    
            


def sair(request):
    logout(request)
    return redirect('/auth/login')