from django.db import models
from django.contrib.auth.models import User

class Template(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    preview_image = models.ImageField(upload_to="template_previews/", blank=True, null=True)

    def __str__(self):
        return self.name

class Portfolio(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="portfolios")
    title = models.CharField(max_length=200)
    bio = models.TextField(blank=True)
    template = models.ForeignKey(Template, on_delete=models.SET_NULL, null=True, blank=True)
    published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.user.username})"

class Section(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name="sections")
    title = models.CharField(max_length=100)
    content = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.title} ({self.portfolio.title})"

class Media(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name="media", null=True, blank=True)
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name="portfolio_media")
    file = models.FileField(upload_to="portfolio_media/")
    media_type = models.CharField(max_length=50)  # image, video, document, etc.
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.media_type}: {self.file.name}"

class SocialLink(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="social_links")
    platform = models.CharField(max_length=50)
    url = models.URLField()

    def __str__(self):
        return f"{self.user.username} - {self.platform}"

class Testimonial(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name="testimonials")
    name = models.CharField(max_length=100)
    feedback = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} on {self.portfolio.title}"