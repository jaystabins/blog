from django import forms
from .models import Post, Tag

# cat = Tag.objects.all().values('name', 'name')
# cat_list = []

# for item in cat:
#     cat_list.append(item)

class PostForm(forms.ModelForm):
    tag = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(), widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-control',}))

    class Meta:
        model = Post
        fields = ('title', 'body', 'tag')

        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control'}),
        }