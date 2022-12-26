from django.contrib import admin
from .models import Post, Tag


class PostAdmin(admin.ModelAdmin):
    fields = ('title', 'tagline', 'body', 'image', 'tags', 'is_published', 'author')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'author':
            if request.path.endswith('add/'):
                kwargs['initial'] = request.user.pk
            kwargs['disabled'] = True
            return db_field.formfield(**kwargs)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
        
    list_display = ('title', 'is_published')
    list_filter = ('is_published',)

class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Post, PostAdmin)
admin.site.register(Tag, TagAdmin)

