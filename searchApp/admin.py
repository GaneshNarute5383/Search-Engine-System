from django.contrib import admin

# Register your models here.
from .models import WebContent, Contact, Feedback, SitemapInfo
from . models import Keywords
# @WebContent
class AdminWebComponent(admin.ModelAdmin):
    list_display = ["id","webpage_url","webpage_title","webpage_description","webpage_description"]
admin.site.register(WebContent,AdminWebComponent)

class AdminKeywords(admin.ModelAdmin):
    list_display = ["id","kname"]
admin.site.register(Keywords,AdminKeywords)

class AdminContact(admin.ModelAdmin):
    list_display = ["id","fullname","email","subject","message"]
admin.site.register(Contact,AdminContact)

class AdminFeedback(admin.ModelAdmin):
    list_display = ["id","fullname","email","feedback"]
admin.site.register(Feedback,AdminFeedback)

class AdminSitemapInfo(admin.ModelAdmin):
    list_display = ["id","url","sitemap"]
admin.site.register(SitemapInfo,AdminSitemapInfo)