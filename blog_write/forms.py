from django import forms 
from django_summernote.widgets import SummernoteWidget
from .models import Articles, Biography


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Articles
        fields = ['title', 'excerpt', 'image', 'slug', 'content', 'author', 'tags']
        widgets = {'content': SummernoteWidget(),}
        
class BiographyForm_(forms.ModelForm):
    class Meta:
        model = Biography
        fields = "__all__"
        widgets = {'ContentBiography': SummernoteWidget(),}
         
class UsernameForm(forms.Form):
    username = forms.CharField(label='Username', max_length = 100)
    
    