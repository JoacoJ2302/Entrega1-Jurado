from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(label='Email (Opcional)')
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirma contraseña', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        help_texts = {k:'' for k in fields}
        

class PostForm(forms.ModelForm):
    content = forms.CharField(label='', widget=forms.Textarea(attrs={'rows':2, 'placeholder':'Escribe tu post / Write your post'}), required=True)
 
    class Meta:
        model = Post
        fields = ['content']
        
        
class SearchProfile(forms.Form):
    username = forms.CharField(max_length=20)
    
    
class UserEditionForm(forms.Form):
    password1 = forms.CharField(label='Nueva contraseña', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirma nueva contraseña', widget=forms.PasswordInput)