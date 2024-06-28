from django.contrib import admin
from .models import Tag, Author, Articles, Biography
from .forms import ArticleForm, BiographyForm_
from .models import ClickLog

# Register your models here.

class ArticlesAdmin(admin.ModelAdmin):
    form = ArticleForm 
    list_filter = ("tags", "title", "created_at", "updated_at")
    list_display = ("title", "tags_list", "created_at", "updated_at")
    prepopulated_fields = {"slug": ("title",)}
       
    def tags_list(self, obj):
        return ", ".join([tag.caption for tag in obj.tags.all()])
    tags_list.short_description = "Tags"
    
class ArticleAdmin(admin.ModelAdmin):
    form = ArticleForm
    
class BiographyAdmin(admin.ModelAdmin):
    form = BiographyForm_
    
  
admin.site.register(Articles, ArticlesAdmin)
admin.site.register(Tag)
admin.site.register(Author)
admin.site.register(Biography, BiographyAdmin)    
admin.site.register(ClickLog)


