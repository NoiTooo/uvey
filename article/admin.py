from django.contrib import admin
from .models import Article, Theme, UploadImg


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_published', 'updated_at', 'created_at')
    ordering = ('-updated_at',)
    list_filter = ('is_published', 'themes')
    search_fields = ('title', 'content')
    filter_horizontal = ['themes']

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "tags":
            kwargs["queryset"] = Theme.objects.order_by('theme')
        return super().formfield_for_manytomany(db_field, request, **kwargs)


admin.site.register(Article, ArticleAdmin)
admin.site.register(Theme)
admin.site.register(UploadImg)
