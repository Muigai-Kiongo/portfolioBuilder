from django.urls import path
from . import views

urlpatterns = [
    # Portfolio List, Detail, Update, Delete (creation uses wizard!)
    path('portfolios/', views.portfolio_list, name='portfolio_list'),
    path('portfolio/<int:pk>/', views.portfolio_detail, name='portfolio_detail'),
    path('portfolio/<int:pk>/edit/', views.portfolio_update, name='portfolio_update'),
    path('portfolio/<int:pk>/delete/', views.portfolio_delete, name='portfolio_delete'),

    

    # Portfolio Wizard Flow & Preview
    path('portfolio/wizard/step1/', views.wizard_step1, name='wizard_step1'),
    path('portfolio/wizard/step2/', views.wizard_step2, name='wizard_step2'),
    path('portfolio/wizard/step3/', views.wizard_step3, name='wizard_step3'),
    path('portfolio/wizard/finalize/', views.wizard_finalize, name='wizard_finalize'),
    path('portfolio/<int:pk>/preview/', views.portfolio_preview, name='portfolio_preview'),

    # Section CRUD
    path('portfolio/<int:portfolio_pk>/section/add/', views.section_create, name='section_create'),
    path('section/<int:pk>/edit/', views.section_update, name='section_update'),
    path('section/<int:pk>/delete/', views.section_delete, name='section_delete'),

    # Media CRUD
    path('portfolio/<int:portfolio_pk>/media/upload/', views.media_upload, name='media_upload'),
    path('media/<int:pk>/delete/', views.media_delete, name='media_delete'),

    # SocialLink CRUD
    path('sociallink/add/', views.sociallink_create, name='sociallink_create'),
    path('sociallink/<int:pk>/edit/', views.sociallink_update, name='sociallink_update'),
    path('sociallink/<int:pk>/delete/', views.sociallink_delete, name='sociallink_delete'),

    # Testimonial CRUD
    path('portfolio/<int:portfolio_pk>/testimonial/add/', views.testimonial_create, name='testimonial_create'),
    path('testimonial/<int:pk>/delete/', views.testimonial_delete, name='testimonial_delete'),

    # Template CRUD (admin only)
    path('templates/', views.template_list, name='template_list'),
    path('template/create/', views.template_create, name='template_create'),
    path('template/<int:pk>/edit/', views.template_update, name='template_update'),
    path('template/<int:pk>/delete/', views.template_delete, name='template_delete'),
]