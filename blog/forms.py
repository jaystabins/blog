from django import forms
from tinymce.widgets import TinyMCE
from .models import Post, Tag

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'tagline', 'image', 'body', 'tags', 'is_published')
        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control'}),
            'tagline': forms.TextInput(attrs={'class': 'form-control'}),
            'body': TinyMCE(attrs={'class': 'form-control'}),
            'tags': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tags'] = forms.ModelMultipleChoiceField(
            queryset=Tag.objects.all(),
            widget=forms.CheckboxSelectMultiple(),
        )
