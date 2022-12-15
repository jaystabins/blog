from django import forms
from .models import Post, Tag

# cat = Tag.objects.all().values('name', 'name')
# cat_list = []

# for item in cat:
#     cat_list.append(item)

class PostForm(forms.ModelForm):
    # tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all())

    class Meta:
        model = Post
        fields = ('title', 'body', 'tags')

        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control'}),
            'tags': forms.CheckboxSelectMultiple(attrs={'class': 'form-control'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tags'] = forms.ModelMultipleChoiceField(
            queryset=Tag.objects.all()
        )