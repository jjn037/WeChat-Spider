from django.contrib import admin
from wechat_gzh.models import GZH, Article


class ArticleAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('gzh',)}

admin.site.register(GZH)
admin.site.register(Article)
# admin.site.register(GZH_paper_list)

