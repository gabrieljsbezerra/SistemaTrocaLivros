from datetime import datetime
from django.forms import ValidationError
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from django.urls import reverse
from usuarios.models import TabelaUsuarios
from .models import TabelaLivros, TabelaCategorias, TabelaTrocas, Troca
from .forms import CadastroLivro
from django.db.models import Q
from datetime import date
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


def home(request):
    if request.session.get('usuarios'):
        usuario = TabelaUsuarios.objects.get(
            id=request.session['usuarios']).nome_usuario
        livros = TabelaLivros.objects.all()
        return render(request, 'home.html', {'livros': livros})

    else:
        return redirect(f"{reverse('login')}?status=2")


def meus_livros(request):
    if request.session.get('usuarios'):
        usuario = TabelaUsuarios.objects.get(id=request.session['usuarios'])
        livros = TabelaLivros.objects.filter(usuario=usuario)
        return render(request, 'meus_livros.html', {'livros': livros})
    else:
        return redirect(f"{reverse('login')}?status=2")


def procura_livros(request):
    if request.session.get('usuarios'):
        usuario = TabelaUsuarios.objects.get(id=request.session['usuarios'])
        query = request.GET.get('q', '')  # Obtém o termo de pesquisa

        # Filtra os livros do usuário atual com base no termo de pesquisa
        procura_livros = TabelaLivros.objects.filter(
            Q(nome_livro__icontains=query) |
            Q(autor__icontains=query) |
            Q(editora__icontains=query),
            usuario=usuario  # Restringe aos livros do usuário logado
        ) if query else TabelaLivros.objects.filter(usuario=usuario)

        return render(request, 'meus_livros.html', {'livros': procura_livros, 'query': query})
    else:
        return redirect(f"{reverse('login')}?status=2")


def ver_livro(request, id):
    if request.session.get('usuarios'):
        livro = TabelaLivros.objects.get(id=id)
        if request.session.get('usuarios') == livro.usuario.id:
            return render(request, 'ver_livro.html', {'livro': livro})
        else:
            return redirect(f"{reverse('home')}?status=1")
    else:
        return redirect(f"{reverse('login')}?status=2")


def editar_livro(request, id):
    if request.session.get('usuarios'):
        livro = TabelaLivros.objects.get(id=id)
        categorias = TabelaCategorias.objects.all()
        if request.session.get('usuarios') == livro.usuario.id:
            return render(request, 'editar_livro.html', {'livro': livro, 'categorias': categorias})
        else:
            return redirect(f"{reverse('home')}?status=1")
    else:
        return redirect(f"{reverse('login')}?status=2")


def alterar_livro(request, id):
    if request.method == 'POST':
        try:
            livro = TabelaLivros.objects.get(id=id)

            # Atualizando os campos do livro com os dados do formulário
            livro.nome_livro = request.POST.get('nome_livro')
            livro.autor = request.POST.get('autor')
            livro.co_autor = request.POST.get('co_autor')
            livro.editora = request.POST.get('editora')

            # Atualizando a categoria
            categoria_id = request.POST.get('categoria')
            livro.categoria_id = categoria_id

            # Atualizando o campo Braile
            livro.braile = 'braile' in request.POST

            # Atualizando o link da imagem
            imagem_link = request.POST.get('imagem_link')
            if imagem_link:
                livro.imagem_link = imagem_link

            # Atualizando a imagem de upload
            if 'imagem_upload' in request.FILES:
                livro.imagem_upload = request.FILES['imagem_upload']

            # Validando e salvando as alterações
            livro.full_clean()  # Valida os campos
            livro.save()

            # Redirecionar para a página de detalhes do livro
            return redirect(reverse('ver_livro', args=[livro.id]))
        except ValidationError as e:
            # Se houver erro de validação, renderize o formulário novamente com os erros
            categorias = TabelaCategorias.objects.all()
            return render(request, 'editar_livro.html', {
                'livro': livro,
                'categorias': categorias,
                'errors': e.message_dict
            })
        except TabelaLivros.DoesNotExist:
            return redirect(reverse('home'))
    else:
        return redirect(reverse('home'))


def cadastro_livro(request):
    if request.session.get('usuarios'):
        status = request.GET.get('status')
        if status is not None:
            status = int(status)
        categorias = TabelaCategorias.objects.all()
        form = CadastroLivro()
        return render(request, 'cadastro_livro.html', {'status': status, 'categorias': categorias, 'form': form})
    else:
        return redirect(f"{reverse('login')}?status=2")


def valida_cadastro_livro(request):
    if request.method == "POST":
        form = CadastroLivro(request.POST, request.FILES)
        if form.is_valid():
            # Obter a data do formulário
            data_cadastro_str = form.data.get('data_cadastro')

            # Verificar se a data foi preenchida, caso contrário usar a data atual
            if data_cadastro_str:
                try:
                    data_cadastro = datetime.strptime(
                        data_cadastro_str, "%d/%m/%Y").date()
                except ValueError:
                    return redirect("cadastro_livro", status=5)
            else:
                data_cadastro = date.today()

            # Criar o objeto livro com os dados do formulário
            livro = TabelaLivros(
                nome_livro=form.data['nome_livro'],
                autor=form.data['autor'],
                co_autor=form.data.get('co_autor', ''),
                editora=form.data['editora'],
                categoria_id=form.data['categoria'],
                braile=form.data.get('braile', False),
                data_cadastro=data_cadastro,
                usuario_id=request.session.get('usuarios'),
                imagem_link=form.data['imagem_link'],
                imagem_upload=form.files.get('imagem_upload')
            )

            # Salvar o livro no banco de dados
            livro.save()
            return redirect("meus_livros")
        else:
            return redirect("cadastro_livro", status=1)
    else:
        return redirect("cadastro_livro")

# Trocas


def disponibilizar_para_troca(request, id):
    if request.session.get('usuarios'):
        livro = get_object_or_404(TabelaLivros, id=id)
        if request.session.get('usuarios') == livro.usuario.id:
            livro.disponivel_para_troca = True
            livro.save()
            return redirect('meus_livros')
    return redirect('login')


def detalhes_livro(request, id):
    livro = get_object_or_404(TabelaLivros, id=id)
    return render(request, 'detalhes_livro.html', {'livro': livro})

def listar_livros_para_troca(request):
    usuario = TabelaUsuarios.objects.get(id=request.session['usuarios'])

    # Livros do próprio usuário
    livros_usuario = TabelaLivros.objects.filter(usuario=usuario, disponivel_para_troca=True)

    # Livros de outros usuários disponíveis para troca
    livros_outros = TabelaLivros.objects.filter(disponivel_para_troca=True).exclude(usuario=usuario)

    # Obter todas as trocas onde o usuário é o oferecedor ou o solicitante
    trocas_oferecidas = TabelaTrocas.objects.filter(usuario_oferecedor=usuario)
    trocas_recebidas = TabelaTrocas.objects.filter(usuario_solicitante=usuario)

    # Criar um dicionário para armazenar o status e o ID da troca
    trocas_dict = {}
    for troca in trocas_oferecidas:
        trocas_dict[troca.livro_oferecido_id] = {
            'status': troca.status,
            'troca_id': troca.id
        }

    for troca in trocas_recebidas:
        trocas_dict[troca.livro_solicitado_id] = {
            'status': troca.status,
            'troca_id': troca.id
        }

    # Adicionar o status de troca aos livros de outros usuários
    for livro in livros_outros:
        if livro.id in trocas_dict:
            livro.status_troca = trocas_dict[livro.id]['status']
            livro.troca_id = trocas_dict[livro.id]['troca_id']
        else:
            # Verificar se o usuário atual já propôs uma troca para este livro
            troca_existente = TabelaTrocas.objects.filter(
                livro_solicitado=livro, usuario_oferecedor=usuario, status='Pendente'
            ).first()
            if troca_existente:
                livro.status_troca = 'Pendente'
                livro.troca_id = troca_existente.id
            else:
                livro.status_troca = None
                livro.troca_id = None

    # Adicionar o status de troca aos livros do próprio usuário
    for livro in livros_usuario:
        livro.status_troca = trocas_dict.get(livro.id, {}).get('status', None)
        livro.troca_id = trocas_dict.get(livro.id, {}).get('troca_id', None)

    # Obter o histórico de trocas aceitas
    trocas_aceitas = TabelaTrocas.objects.filter(
        (Q(usuario_oferecedor=usuario) | Q(usuario_solicitante=usuario)),
        status='Aceita'
    )

    context = {
        'livros_usuario': livros_usuario,
        'livros_outros': livros_outros,
        'trocas_aceitas': trocas_aceitas,
    }

    return render(request, 'listar_livros_para_troca.html', context)



def propor_troca(request, id):
    if request.session.get('usuarios'):
        livro_solicitado = get_object_or_404(TabelaLivros, id=id)
        usuario_id = request.session.get('usuarios')

        # Filtrar os livros do usuário que estão disponíveis para troca e não estão em trocas pendentes
        meus_livros = TabelaLivros.objects.filter(
            usuario_id=usuario_id,
            disponivel_para_troca=True
        ).exclude(
            id__in=TabelaTrocas.objects.filter(
                usuario_oferecedor_id=usuario_id,
                status='Pendente'
            ).values_list('livro_oferecido_id', flat=True)
        )

        if request.method == 'POST':
            livro_oferecido_id = request.POST.get('livro_oferecido')
            livro_oferecido = TabelaLivros.objects.get(id=livro_oferecido_id)

            # Criar uma nova troca
            nova_troca = TabelaTrocas(
                livro_oferecido=livro_oferecido,
                livro_solicitado=livro_solicitado,
                usuario_oferecedor=livro_oferecido.usuario,
                usuario_solicitante=livro_solicitado.usuario,
                data_proposta=date.today(),
                status='Pendente'
            )
            nova_troca.save()

            messages.success(request, 'Troca proposta com sucesso!')
            return redirect('listar_livros_para_troca')

        return render(request, 'propor_troca.html', {
            'livro_solicitado': livro_solicitado,
            'meus_livros': meus_livros
        })
    return redirect('login')
def gerenciar_troca(request, id):
    troca = get_object_or_404(TabelaTrocas, id=id)

    # Verificar se o usuário logado é o oferecedor ou o solicitante
    usuario = TabelaUsuarios.objects.get(id=request.session['usuarios'])
    if usuario != troca.usuario_oferecedor and usuario != troca.usuario_solicitante:
        return redirect('listar_livros_para_troca')

    if request.method == 'POST':
        acao = request.POST.get('acao')
        if acao == 'aceitar':
            troca.status = 'Aceita'
            troca.save()

            # Transferir a propriedade dos livros
            troca.livro_oferecido.usuario = troca.usuario_solicitante
            troca.livro_oferecido.disponivel_para_troca = False
            troca.livro_oferecido.save()

            troca.livro_solicitado.usuario = troca.usuario_oferecedor
            troca.livro_solicitado.disponivel_para_troca = False
            troca.livro_solicitado.save()

            messages.success(request, 'Troca aceita e propriedade dos livros atualizada com sucesso!')

        elif acao == 'recusar':
            # Marcar os livros como disponíveis para troca
            troca.livro_oferecido.disponivel_para_troca = True
            troca.livro_solicitado.disponivel_para_troca = True
            troca.livro_oferecido.save()
            troca.livro_solicitado.save()

            # Deletar a troca
            troca.delete()
            messages.info(request, 'Troca rejeitada e a solicitação foi removida.')

        return redirect('listar_livros_para_troca')

    return render(request, 'gerenciar_troca.html', {'troca': troca})
