from django.shortcuts import render, redirect, get_object_or_404 # importa funções para renderizar templates, redirecionar e obter obj do db ou gerar erro 404
from .models import Usuario # importa o modelo 'usuario' definido no arquivo atual
from django.urls import reverse #importa a função 'reverse' para construir urls reversas
from django.core import serializers #importa um mecanismo para serializar/deserializar dados do django
from .serializers import UsuarioSerializer,UsuarioUpdateSerializer #importa serializadores definidos no arquivo atual
from rest_framework.renderers import TemplateHTMLRenderer #importa o renderizador de templates do django rest framework
from rest_framework.response import Response #importa a classe de resposta do django rest framework
from rest_framework import status, generics #importa codigos de status do http e classes genéricas do django rest framework
from django.contrib import messages

class CadastrarUsuario(generics.CreateAPIView): 
   
    serializer_class = UsuarioSerializer  # define o serializador a ser utilizado para criar um novo usuário

  
    def get(self, request, *args, **kwargs):   #metodo GET para exibir o formulário de cadastro do usuário

        serializer= self.serializer_class()         #inicializa o seriador vazio
      
        return render(request, 'cadastrousuario.html', {'serializer': serializer})   #rendereiza o template 'cadastrousuario.html', passando o serializador como contexto
    
   
    def post(self, request, *args, **kwargs):  #metodo POST para processar o form de cadastro do ususario
      
        serializer = self.serializer_class(data=request.data)   #inicializa o serializador com os dados de requisição

        
        if serializer.is_valid(): #verifica se os dados do form são váliddos
            
            serializer.save() #salva o usuario no bd
          
            return redirect('listar')   #redirecionapara pag de cadastro bem sucedida
       

    def validar(request):
        if  request.method == "get" :
           return render(request, 'cadastrousuario.html')

        elif request.method == "post":
            nome = request.POST.get('nome')
            sobrenome = request.POST.get('sobrenome')
            idade = request.POST.get('idade')
            foto = request.FILES.get('foto')

            usuario = Usuarios(nome=nome, sobrenome=sobrenome, idade=idade, foto=foto)
            usuario.save()
            messages.sucess(request, 'usuario cadastrado' ,extra_tags='sucess-message')
            return render(request, 'cadastrousuario.html', {'usuario' : usuario})
        
class ListarUsuario(generics.ListAPIView):
   
    queryset = Usuario.objects.all()  #define a consulta para recuperar todos os usuários do db

 
    serializer_class = UsuarioSerializer     #define o serializador a ser utilizado para serializar e desserializar os dados do usuário

  
    def get(self, request, *args, **kwargs):   #metodo GET para exibir lista de usuarios
       
        usuarios = self.get_queryset()  #obtem a lista de usuarios do db
       
        return render(request, 'listarusuario.html', {'usuarios' : usuarios})  #renderiza o template 'listarusuario.html', passando a lista de usuários como contexto
    
   
def post(self, request, *args, **kwargs):  #metodo POST para processar o form da criação de usuario
       
        serializer = self.serializer_class(data=request.data)  #inicializa o serializador com os dados de requisição
        
   
        if serializer.is_valid():  #verifica se os dados do form são váliddos
           
            return redirect('listar')    #redirecionapara pag de listagem de usuarios apos criação bem sucedida

class UpdateUsuario(generics.UpdateAPIView):

    queryset = Usuario.objects.all()  #define a consulta para recuperar todos os usuários do db
    serializer_class = UsuarioSerializer  #define o serializador a ser utilizado para serializar e desserializar os dados do usuario


    def get(self, request, *args, **kwargs): #metodo GET para exibir lista de usuarios
        user_id = kwargs.get('pk') #obtem o id do usuario a ser atualizado dos parâmetros da URL
        usuario = get_object_or_404(Usuario, pk=user_id)  #obtem o id do usuario do bd ou retorna um erro 404 se não encontrado
        serializer = self.serializer_class(instance=usuario)  #inicializa o serializador com a instância do usuário
        return render(request, 'atualizarusuario.html', {'serializer': serializer, 'usuario': usuario})   #renderiza o template 'atualizarusuario.html' , passando o usuario e o serializador como contexto
    
    def post(self, request, *args, **kwargs): #metodo POST para processar o form do update de usuario
        user_id = kwargs.get('pk')   #obtem o id do usuario a ser atualizado dos parâmetros da URL
        
        usuario = get_object_or_404(Usuario, pk=user_id)   #obtem o id do usuario do bd ou retorna um erro 404 se não encontrado
        serializer = UsuarioUpdateSerializer(instance=usuario, data=request.data, partial=True)  #inicializa o serializador de autualização com a instancia do usuario e os dados da requisição

         
        if serializer.is_valid(): #verifica se os dados do form são váliddos
            serializer.save()   #salva as alterações no db
            return redirect('listar')   #redirecionapara pag de listagem de usuarios apos atualização bem sucedida
        return render(request, 'listarusuario.html', {'serializer': serializer, 'usuario': usuario})   #renderiza o template, 'atualizarusuario.html' com o serializador e o usuario como contexo

class DeleteUsuario(generics.DestroyAPIView): #define uma classe de visualização baseada em genéricos para excluir um usuario

    queryset = Usuario.objects.all() #consuta para recuperar todos os usuarios do db
    
 
    serializer_class = UsuarioSerializer  #define o serializador a ser utilizado para serializar e desserializar os dados do usuário


    def get(self, request, *args, **kwargs):  #metodo GET para exibir pagina de  confirmação de exclusão de usuario

        user_id = kwargs.get('pk') #obtem o id do usuario a ser excluido dos parâmetros da URL
     
        usuario = get_object_or_404(Usuario, pk=user_id)   #obtem o usuario do bd ou retorna um erro 404 se não encontrado
    
        serializer = self.serializer_class(instance=usuario)  #inicializa o serializador com a instância do usuário

        return render(request, 'listarusuario.html', {'serializer': serializer, 'usuario': usuario})   #renderiza o template 'listarusuarios.html' , passando o usuario e o serializador como contexto

   
    def post(self, request, *args, **kwargs): #metodo POST para processara exclusão do usuario
        
        user_id = kwargs.get('pk') #obtem o id do usuario a ser atualizado dos parâmetros da URL
       
        usuario = get_object_or_404(Usuario, pk=user_id)  #obtem o usuario do bd ou retorna um erro 404 se não encontrado
        
        usuario.delete()    #exclui o usuario do db
        
        return redirect('listar')  #redirecionapara pag de listagem de usuarios apos a exclusão bem sucedida