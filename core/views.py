from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .models import Portfolio, Section, Media, Template, SocialLink, Testimonial
from .forms import PortfolioForm, SectionForm, MediaForm, TemplateForm, SocialLinkForm, TestimonialForm

# --- Portfolio Wizard Flow ---
@login_required
def wizard_step1(request):
    # Clear wizard session for new portfolio
    for key in ['wizard_title', 'wizard_bio', 'wizard_template_id', 'wizard_portfolio_pk']:
        request.session.pop(key, None)
    if request.method == "POST":
        title = request.POST.get("title")
        request.session['wizard_title'] = title
        return redirect("wizard_step2")
    return render(request, "core/wizard_step1.html", {'step': 1})

@login_required
def wizard_step2(request):
    if request.method == "POST":
        bio = request.POST.get("bio")
        request.session['wizard_bio'] = bio
        return redirect("wizard_step3")
    return render(request, "core/wizard_step2.html", {'step': 2})

@login_required
def wizard_step3(request):
    templates = Template.objects.all()
    if request.method == "POST":
        template_id = request.POST.get("template_id")
        request.session['wizard_template_id'] = template_id
        return redirect("wizard_finalize")
    return render(request, "core/wizard_step3.html", {"templates": templates, 'step': 3})

@login_required
def wizard_finalize(request):
    title = request.session.get("wizard_title", "")
    bio = request.session.get("wizard_bio", "")
    template_id = request.session.get("wizard_template_id")
    template = Template.objects.filter(id=template_id).first() if template_id else None

    # Save Portfolio only if not already saved in this session
    if not request.session.get("wizard_portfolio_pk"):
        portfolio = Portfolio.objects.create(
            user=request.user,
            title=title,
            bio=bio,
            template=template,
            published=False
        )
        request.session['wizard_portfolio_pk'] = portfolio.pk
    else:
        portfolio = Portfolio.objects.get(pk=request.session["wizard_portfolio_pk"])

    # Redirect to preview
    return redirect("portfolio_preview", pk=portfolio.pk)

@login_required
def portfolio_preview(request, pk):
    portfolio = get_object_or_404(Portfolio, pk=pk, user=request.user)
    sections = portfolio.sections.all()
    testimonials = portfolio.testimonials.all()
    return render(request, "core/portfolio_preview.html", {
        "portfolio": portfolio,
        "sections": sections,
        "testimonials": testimonials,
    })

# --- Portfolio CRUD (create removed, now use wizard) ---
@login_required
def portfolio_list(request):
    portfolios = Portfolio.objects.filter(user=request.user)
    return render(request, "core/portfolio_list.html", {"portfolios": portfolios})

@login_required
def portfolio_detail(request, pk):
    portfolio = get_object_or_404(Portfolio, pk=pk, user=request.user)
    sections = portfolio.sections.all()
    testimonials = portfolio.testimonials.all()
    return render(request, "core/portfolio_detail.html", {
        "portfolio": portfolio,
        "sections": sections,
        "testimonials": testimonials,
    })

@login_required
def portfolio_update(request, pk):
    portfolio = get_object_or_404(Portfolio, pk=pk, user=request.user)
    if request.method == "POST":
        form = PortfolioForm(request.POST, instance=portfolio)
        if form.is_valid():
            form.save()
            return redirect("portfolio_detail", pk=portfolio.pk)
    else:
        form = PortfolioForm(instance=portfolio)
    return render(request, "core/portfolio_form.html", {
        "form": form,
        "portfolio": portfolio  # <<< ADD THIS LINE!
    })

@login_required
def portfolio_delete(request, pk):
    portfolio = get_object_or_404(Portfolio, pk=pk, user=request.user)
    if request.method == "POST":
        portfolio.delete()
        return redirect("portfolio_list")
    return render(request, "core/portfolio_confirm_delete.html", {"portfolio": portfolio})

# --- Section CRUD ---
@login_required
def section_create(request, portfolio_pk):
    portfolio = get_object_or_404(Portfolio, pk=portfolio_pk, user=request.user)
    if request.method == "POST":
        form = SectionForm(request.POST)
        if form.is_valid():
            section = form.save(commit=False)
            section.portfolio = portfolio
            section.save()
            return redirect("portfolio_detail", pk=portfolio.pk)
    else:
        form = SectionForm()
    return render(request, "core/section_form.html", {"form": form, "portfolio": portfolio})

@login_required
def section_update(request, pk):
    section = get_object_or_404(Section, pk=pk, portfolio__user=request.user)
    if request.method == "POST":
        form = SectionForm(request.POST, instance=section)
        if form.is_valid():
            form.save()
            return redirect("portfolio_detail", pk=section.portfolio.pk)
    else:
        form = SectionForm(instance=section)
    return render(request, "core/section_form.html", {"form": form, "portfolio": section.portfolio})

@login_required
def section_delete(request, pk):
    section = get_object_or_404(Section, pk=pk, portfolio__user=request.user)
    portfolio_pk = section.portfolio.pk
    if request.method == "POST":
        section.delete()
        return redirect("portfolio_detail", pk=portfolio_pk)
    return render(request, "core/section_confirm_delete.html", {"section": section})

# --- Media CRUD ---
@login_required
def media_upload(request, portfolio_pk):
    portfolio = get_object_or_404(Portfolio, pk=portfolio_pk, user=request.user)
    if request.method == "POST":
        form = MediaForm(request.POST, request.FILES)
        if form.is_valid():
            media = form.save(commit=False)
            media.portfolio = portfolio
            media.save()
            return redirect("portfolio_detail", pk=portfolio.pk)
    else:
        form = MediaForm()
    return render(request, "core/media_form.html", {"form": form, "portfolio": portfolio})

@login_required
def media_delete(request, pk):
    media = get_object_or_404(Media, pk=pk, portfolio__user=request.user)
    portfolio_pk = media.portfolio.pk
    if request.method == "POST":
        media.delete()
        return redirect("portfolio_detail", pk=portfolio_pk)
    return render(request, "core/media_confirm_delete.html", {"media": media})

# --- SocialLink CRUD ---
@login_required
def sociallink_create(request):
    if request.method == "POST":
        form = SocialLinkForm(request.POST)
        if form.is_valid():
            sociallink = form.save(commit=False)
            sociallink.user = request.user
            sociallink.save()
            return redirect("profile") # Or another suitable page
    else:
        form = SocialLinkForm()
    return render(request, "core/sociallink_form.html", {"form": form})

@login_required
def sociallink_update(request, pk):
    sociallink = get_object_or_404(SocialLink, pk=pk, user=request.user)
    if request.method == "POST":
        form = SocialLinkForm(request.POST, instance=sociallink)
        if form.is_valid():
            form.save()
            return redirect("profile")
    else:
        form = SocialLinkForm(instance=sociallink)
    return render(request, "core/sociallink_form.html", {"form": form})

@login_required
def sociallink_delete(request, pk):
    sociallink = get_object_or_404(SocialLink, pk=pk, user=request.user)
    if request.method == "POST":
        sociallink.delete()
        return redirect("profile")
    return render(request, "core/sociallink_confirm_delete.html", {"sociallink": sociallink})

# --- Testimonial CRUD ---
@login_required
def testimonial_create(request, portfolio_pk):
    portfolio = get_object_or_404(Portfolio, pk=portfolio_pk, user=request.user)
    if request.method == "POST":
        form = TestimonialForm(request.POST)
        if form.is_valid():
            testimonial = form.save(commit=False)
            testimonial.portfolio = portfolio
            testimonial.save()
            return redirect("portfolio_detail", pk=portfolio.pk)
    else:
        form = TestimonialForm()
    return render(request, "core/testimonial_form.html", {"form": form, "portfolio": portfolio})

@login_required
def testimonial_delete(request, pk):
    testimonial = get_object_or_404(Testimonial, pk=pk, portfolio__user=request.user)
    portfolio_pk = testimonial.portfolio.pk
    if request.method == "POST":
        testimonial.delete()
        return redirect("portfolio_detail", pk=portfolio_pk)
    return render(request, "core/testimonial_confirm_delete.html", {"testimonial": testimonial})

# --- Template CRUD (admin only) ---
@login_required
def template_list(request):
    templates = Template.objects.all()
    return render(request, "core/template_list.html", {"templates": templates})

@login_required
def template_create(request):
    if request.method == "POST":
        form = TemplateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("template_list")
    else:
        form = TemplateForm()
    return render(request, "core/template_form.html", {"form": form})

@login_required
def template_update(request, pk):
    template = get_object_or_404(Template, pk=pk)
    if request.method == "POST":
        form = TemplateForm(request.POST, request.FILES, instance=template)
        if form.is_valid():
            form.save()
            return redirect("template_list")
    else:
        form = TemplateForm(instance=template)
    return render(request, "core/template_form.html", {"form": form})

@login_required
def template_delete(request, pk):
    template = get_object_or_404(Template, pk=pk)
    if request.method == "POST":
        template.delete()
        return redirect("template_list")
    return render(request, "core/template_confirm_delete.html", {"template": template})