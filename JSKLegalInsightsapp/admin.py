from django.contrib import admin
from .models import (
    AboutPage, Profile, Education, SkillCategory, Skill, LegalExperience,
    LegalPublication, LegalAward, SocialLink, BlogPost, CaseStudy,
    ContactMessage, LegalResource, InteractiveTool, LegalNews, CaseLaw,
    Citation, Contract, LegalArticle, LegalDocumentTemplate, SiteConfiguration
)

# Register basic models with minimal customization
admin.site.register(AboutPage)
admin.site.register(SkillCategory)
admin.site.register(Skill)
admin.site.register(SocialLink)
admin.site.register(CaseLaw)
admin.site.register(Citation)
admin.site.register(Contract)
admin.site.register(LegalNews)


# Custom admin classes for more complex models
class EducationInline(admin.TabularInline):
    model = Education
    extra = 1

class LegalExperienceInline(admin.TabularInline):
    model = LegalExperience
    extra = 1

class LegalPublicationInline(admin.TabularInline):
    model = LegalPublication
    extra = 1

class LegalAwardInline(admin.TabularInline):
    model = LegalAward
    extra = 1

class SocialLinkInline(admin.TabularInline):
    model = SocialLink
    extra = 1


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    inlines = [EducationInline, LegalExperienceInline, LegalPublicationInline, LegalAwardInline, SocialLinkInline]
    list_display = ('name', 'email', 'degree', 'title')
    search_fields = ('name', 'email', 'about_me')


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'updated_at')
    search_fields = ('title', 'content')
    list_filter = ('created_at', 'author')
    date_hierarchy = 'created_at'


@admin.register(CaseStudy)
class CaseStudyAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'updated_at')
    search_fields = ('title', 'summary', 'content')
    list_filter = ('created_at',)
    date_hierarchy = 'created_at'


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at')
    search_fields = ('name', 'email', 'message')
    list_filter = ('created_at',)
    readonly_fields = ('name', 'email', 'message', 'created_at')  # Make read-only since these are submissions


@admin.register(LegalResource)
class LegalResourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    search_fields = ('title', 'summary')


@admin.register(InteractiveTool)
class InteractiveToolAdmin(admin.ModelAdmin):
    list_display = ('name', 'link')
    search_fields = ('name', 'description')


@admin.register(LegalArticle)
class LegalArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'author', 'published_date')
    search_fields = ('title', 'content', 'author')
    list_filter = ('category', 'published_date')
    date_hierarchy = 'published_date'


@admin.register(LegalDocumentTemplate)
class LegalDocumentTemplateAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    search_fields = ('title', 'description')


@admin.register(SiteConfiguration)
class SiteConfigurationAdmin(admin.ModelAdmin):
    list_display = ('site_title', 'primary_color', 'secondary_color')
    fieldsets = (
        ('Site Information', {
            'fields': ('site_title', 'meta_description', 'footer_text')
        }),
        ('Appearance', {
            'fields': ('primary_color', 'secondary_color', 'show_resume_button')
        }),
        ('Analytics', {
            'fields': ('google_analytics_id',),
            'classes': ('collapse',)
        }),
    )

    def has_add_permission(self, request):
        # Prevent creating multiple configurations
        return not SiteConfiguration.objects.exists()