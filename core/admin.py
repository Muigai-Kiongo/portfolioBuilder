from django.contrib import admin
from .models import Template, Portfolio, Section, Media, SocialLink, Testimonial


admin.site.site_header = "PortfolioCraft Admin"
admin.site.site_title = "PortfolioCraft Admin Portal"
admin.site.index_title = "Welcome to PortfolioCraft Administration"

@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)
    verbose_name = "Portfolio Template"
    verbose_name_plural = "Portfolio Templates"

@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'published', 'created_at')
    list_filter = ('published', 'created_at')
    search_fields = ('title', 'user__username')
    verbose_name = "Portfolio"
    verbose_name_plural = "Portfolios"

@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'portfolio', 'order')
    search_fields = ('title', 'portfolio__title')
    list_filter = ('portfolio',)
    verbose_name = "Portfolio Section"
    verbose_name_plural = "Portfolio Sections"

@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    list_display = ('media_type', 'file', 'portfolio', 'section', 'uploaded_at')
    list_filter = ('media_type', 'portfolio', 'section')
    search_fields = ('media_type', 'file')
    verbose_name = "Portfolio Media"
    verbose_name_plural = "Portfolio Media Files"

@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ('user', 'platform', 'url')
    search_fields = ('user__username', 'platform', 'url')
    list_filter = ('platform',)
    verbose_name = "Social Link"
    verbose_name_plural = "Social Links"

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'portfolio', 'created_at')
    search_fields = ('name', 'portfolio__title', 'feedback')
    list_filter = ('portfolio',)
    verbose_name = "Portfolio Testimonial"
    verbose_name_plural = "Portfolio Testimonials"