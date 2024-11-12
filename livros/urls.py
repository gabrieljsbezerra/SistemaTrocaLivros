from django.urls import path, include
from . import views
from django.conf import settings  # Import settings
from django.conf.urls.static import static  # Import static

urlpatterns = [
    path('home/', views.home, name='home'),
    path('Meus Livros/', views.meus_livros, name='meus_livros'),
    path('Cadastro Livro/', views.cadastro_livro, name='cadastro_livro'),
    path('valida_cadastro_livro/', views.valida_cadastro_livro, name='valida_cadastro_livro'),
    path('ver_livro/<int:id>', views.ver_livro, name='ver_livro'),
    path('Procura Livros/', views.procura_livros, name='procura_livros'),
    path('editar_livro/<int:id>/', views.editar_livro, name='editar_livro'),
    path('alterar_livro/<int:id>/', views.alterar_livro, name='alterar_livro'),
    path('disponibilizar_para_troca/<int:id>/', views.disponibilizar_para_troca, name='disponibilizar_para_troca'),
    path('listar_livros_para_troca/', views.listar_livros_para_troca, name='listar_livros_para_troca'),
    path('propor_troca/<int:id>/', views.propor_troca, name='propor_troca'),
    path('gerenciar_troca/<int:id>/', views.gerenciar_troca, name='gerenciar_troca'),
    path('detalhes_livro/<int:id>/', views.detalhes_livro, name='detalhes_livro')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
