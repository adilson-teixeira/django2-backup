#from pyexpat.errors import messages
from django.shortcuts import redirect, render
from django.contrib import messages
from .forms import ContatoForm, ProdutoModelForm
from .models import Produto
from django.shortcuts import redirect #usado para redirecionar usuário anonimo.

def index(request):
    context = {
        'produtos': Produto.objects.all()
    }
    return render(request, 'index.html', context)


def contato(request):
    form = ContatoForm(request.POST or None)

    if str(request.method) == 'POST':
        if form.is_valid():
            form.send_mail()

            messages.success(request, 'E-mail enviado com sucesso!')
            form =  ContatoForm()
        else:
            messages.error(request, 'Erro ao enviar e-mail')

    context = {
        'form': form
    }
    return render(request, 'contato.html', context)


def produto(request):
    if str(request.user) != 'AnonymousUser': # verifica se o usuário está logado
        if str(request.method) == 'POST':
            form = ProdutoModelForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request, 'Produto salvo com sucesso.')
                form = ProdutoModelForm() # limpa as entradas do form na página
            else:
                messages.error(request, 'Erro ao salvar o produto.')

        else:
            form = ProdutoModelForm()
        context = {
            'form': form
        }
        return render(request, 'produto.html', context )
    else:
        return redirect('index')

