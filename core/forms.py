from django import forms
from .models import Portfolio, Section, Media, Template, SocialLink, Testimonial

class PortfolioForm(forms.ModelForm):
    class Meta:
        model = Portfolio
        fields = ['title', 'bio', 'template', 'published']

class SectionForm(forms.ModelForm):
    class Meta:
        model = Section
        fields = ['title', 'content', 'order']

class MediaForm(forms.ModelForm):
    class Meta:
        model = Media
        fields = ['section', 'file', 'media_type']

class TemplateForm(forms.ModelForm):
    class Meta:
        model = Template
        fields = ['name', 'description', 'preview_image']

class SocialLinkForm(forms.ModelForm):
    class Meta:
        model = SocialLink
        fields = ['platform', 'url']

class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = ['name', 'feedback']