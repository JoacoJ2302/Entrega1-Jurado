from django.shortcuts import get_object_or_404, redirect, render
from .models import *
from .forms import PostForm, UserRegisterForm, SearchProfile, UserEditionForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


def feed(request):
    posts = Post.objects.all()
    context = {'posts' : posts,}
    return render (request, 'social/feed.html', context)

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            messages.success(request, f'Usuario {username} ha sido creado') 
            return redirect('feed')
    else:
        form = UserRegisterForm()
    context = {'form' : form,}
    return render (request, 'social/register.html', context)

def profile(request, username=None):
    current_user = request.user
    if username and username != current_user.username:
        user = User.objects.get(username=username)
        posts = user.posts.all()
    else:
        posts = current_user.posts.all()
        user = current_user
    return render (request, 'social/profile.html', {'user':user, 'posts':posts})

def about(request):
    return render (request, 'social/about.html')


@login_required
def post(request):
    current_user = get_object_or_404(User, pk=request.user.pk)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = current_user
            post.save()
            messages.success(request, 'Post enviado')
            return redirect('feed')
    else:
        form = PostForm()
    return render (request, 'social/post.html', {'form' : form,})

def follow(request, username):
    current_user = request.user
    to_user = User.objects.get(username=username)
    to_user_id = to_user
    rel = Relationship(from_user = current_user, to_user=to_user_id)
    rel.save()
    messages.success(request, f'Sigues a {username}')
    return redirect('feed')

def unfollow(request, username):
    current_user = request.user
    to_user = User.objects.get(username=username)
    to_user_id = to_user.id
    rel = Relationship.objects.filter(from_user=current_user.id, to_user=to_user_id).get()
    rel.delete()
    messages.success(request, f'Ya no sigues a {username}')
    return redirect('feed')

def search(request):
    user_search = request.GET.get('username', None)
    if user_search is not None:
        users = User.objects.filter(username__icontains = user_search)
    else:
        users = User.objects.all()
    form = SearchProfile()
    return render (request, 'social/search.html', {'form':form, 'users':users})

def edit(request):
    if request.method == 'POST':
        form = UserEditionForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            logued_user = request.user
            if data.get('password1') == data.get('password2') and len(data.get('password1')) > 8:
                logued_user.set_password(data.get('password1'))
                messages.success(request, f'Contrase??a modificada - Vuelve a iniciar sesion') 
                logued_user.save()
                return redirect('login')
            else:
                messages.error(request, f'No se puedo modificar la contrase??a')
    else:
        form = UserEditionForm()
    context = {'form' : form,}
    return render (request, 'social/edit.html', context)