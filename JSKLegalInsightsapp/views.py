from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse, JsonResponse, FileResponse
import logging
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib import colors
import requests
from .models import (
    BlogPost, 
    CaseStudy, 
    AboutPage, 
    LegalResource, 
    InteractiveTool, 
    ContactMessage,
    LegalArticle, 
    LegalDocumentTemplate,
    Profile, 
    Education, 
    SkillCategory, 
    Skill, 
    LegalExperience, 
    LegalPublication, 
    LegalAward,
    SocialLink,
    # Resource and LegalDocument are referenced but don't exist in the models
    # Commenting them out to fix the import error
    # Resource,
    # LegalDocument
    Profile, Education, LegalExperience, LegalArticle, LegalDocumentTemplate,
    BlogPost, CaseStudy, LegalAward, LegalPublication
)
from .forms import (
    LegalResourceForm, 
    InteractiveToolForm, 
    CaseLawSearchForm, 
    CitationForm, 
    ContractForm, ProfileForm, EducationForm, LegalExperienceForm, LegalArticleForm,
    LegalDocumentTemplateForm
)
from .utils import fetch_case_law, fetch_legal_news, fetch_legal_articles_from_newsdata
from django.contrib.admin.views.decorators import staff_member_required

# Configure logger
logger = logging.getLogger(__name__)




def home(request):
    """
    Home page view. Displays the latest blog posts, case studies, and about content.
    """
    latest_posts = BlogPost.objects.order_by('-created_at')[:3]
    latest_cases = CaseStudy.objects.order_by('-created_at')[:3]
    about_content = AboutPage.objects.first().content if AboutPage.objects.exists() else "Welcome to JSK Legal Insights"
    
    context = {
        'latest_posts': latest_posts,
        'latest_cases': latest_cases,
        'about_content': about_content
    }
    return render(request, 'home.html', context)


def blog(request):
    """
    Blog page view. Displays a paginated list of all blog posts.
    """
    posts = BlogPost.objects.order_by('-created_at')
    paginator = Paginator(posts, 6)  # 6 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'blog.html', {'page_obj': page_obj})


def blog_detail(request, post_id):
    """
    Blog detail view. Displays a single blog post.
    """
    post = get_object_or_404(BlogPost, id=post_id)
    return render(request, 'blog_detail.html', {'post': post})


def about(request):
    """
    About page view. Displays information about Jasmine S. Khan.
    """
    about_content = AboutPage.objects.first().content if AboutPage.objects.exists() else "Welcome to JSK Legal Insights"
    return render(request, 'about.html', {'about_content': about_content})

def about_view(request):
    # Get Emily's profile - we can identify it by email or name
    profile = get_object_or_404(Profile)
    
    # Get all skill categories
    skill_categories = SkillCategory.objects.all().prefetch_related('skills')
    
    # Create a context dictionary with all the data
    context = {
        'profile': profile,
        'educations': Education.objects.filter(profile=profile).order_by('-start_year'),
        'experiences': LegalExperience.objects.filter(profile=profile).order_by('-start_date'),
        'publications': LegalPublication.objects.filter(profile=profile).order_by('-year'),
        'skill_categories': skill_categories,
        'awards': LegalAward.objects.filter(profile=profile).order_by('-year'),
        'social_links': SocialLink.objects.filter(profile=profile),
    }
    
    
    return render(request, 'about.html', context)

def case_studies(request):
    """
    Case studies page view. Displays a list of all case studies.
    """
    case_studies = CaseStudy.objects.order_by('-created_at')
    return render(request, 'case_studies.html', {'case_studies': case_studies})


def case_study_detail(request, case_id):
    """
    Case study detail view. Displays a single case study.
    """
    case = get_object_or_404(CaseStudy, id=case_id)
    
    # Add this line to provide a default author if needed
    if not hasattr(case, 'author'):
        case.author = None  # Or some default User object
        
    return render(request, 'case_study_detail.html', {'case': case})

def resources(request):
    """
    Resources page view. Displays legal resources, tools, articles, and documents.
    Also fetches legal news to display as resources (limited to 3).
    """
    # Get database objects
    db_resources = LegalResource.objects.all()
    tools = InteractiveTool.objects.all()
    articles = LegalArticle.objects.all()
    documents = LegalDocumentTemplate.objects.all()
    
    # Fetch legal news articles
    news_articles = fetch_legal_news()
    
    # Transform news articles into resources format for display in resource cards
    news_resources = [
        {
            "title": article["title"],
            "summary": article["description"] or "No description available",
            "link": article["url"],
            "image": article.get("urlToImage") or "/static/images/default_news.jpg"
        }
        for article in news_articles  # We'll slice in the template
    ]
    
    # Form handling for admin users
    if request.method == "POST":
        resource_form = LegalResourceForm(request.POST, request.FILES)
        tool_form = InteractiveToolForm(request.POST)
        if resource_form.is_valid():
            resource_form.save()
            return redirect('resources')
        if tool_form.is_valid():
            tool_form.save()
            return redirect('resources')
    else:
        resource_form = LegalResourceForm()
        tool_form = InteractiveToolForm()

    context = {
        'db_resources': db_resources,  # Resources from database
        'news_resources': news_resources,  # Resources from news API
        'tools': tools,
        'articles': articles,
        'documents': documents,
        'resource_form': resource_form,
        'tool_form': tool_form
    }
    
    return render(request, 'resources.html', context)

def legal_news_view(request):
    """
    Full page view for legal news articles.
    Shows all available news articles.
    """
    try:
        # Fetch all legal news articles
        news_articles = fetch_legal_news()
        
        # Transform all news articles into resources format
        all_news = []
        for article in news_articles:
            if article:  # Make sure the article is not None
                all_news.append({
                    "title": article.get("title", "Untitled"),
                    "summary": article.get("description", "No description available"),
                    "content": article.get("content", ""),
                    "link": article.get("url", "#"),
                    "image": article.get("urlToImage") or "/static/images/default_news.jpg",
                    "source": article.get("source", {}).get("name", "Unknown Source"),
                    "published_at": article.get("publishedAt", "")
                })
        
        context = {
            'news_articles': all_news,
        }
        
        return render(request, 'legal_news.html', context)
    except Exception as e:
        # Log the error (you would want proper logging in production)
        print(f"Error in legal_news_view: {e}")
        # Return a simple error page or redirect back to resources
        context = {
            'error_message': "Unable to fetch news articles at this time."
        }
        return render(request, 'legal_news.html', context)

def contact(request):
    """
    Contact page view. Displays a contact form or information.
    """
    return render(request, 'contact.html')


def dashboard(request):
    """
    Dashboard view. Displays an admin dashboard for authenticated users.
    """
    return render(request, 'dashboard.html')


def login_user(request):
    """
    Login view. Displays a login form for users.
    """
    return render(request, 'login.html')


def register(request):
    """
    Registration view. Displays a registration form for new users.
    """
    return render(request, 'register.html')


def password_reset(request):
    """
    Password reset view. Displays a password reset form.
    """
    return render(request, 'password_reset.html')


def privacy(request):
    """
    Privacy policy view. Displays the privacy policy.
    """
    return render(request, 'privacy.html')


def analyzer(request):
    """
    Analyzer tool view. Displays a legal analysis tool.
    """
    return render(request, 'analyzer.html')


def portfolio(request):
    """
    Portfolio view. Displays the user's legal projects and achievements.
    """
    return render(request, 'portfolio.html')


def case_law_search(request):
    """
    Case law search view. Searches for legal cases based on query.
    """
    query = request.GET.get("q", "")
    results = {}

    if query:
        results = fetch_case_law(query)

    return render(request, "case_law_search.html", {"results": results, "query": query})


def contact_view(request):
    """
    Contact form processing view. Handles form submission and sends email.
    """
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip()
        message = request.POST.get("message", "").strip()

        # Log the received form data
        logger.info(f"Received Form Data: Name={name}, Email={email}, Message={message}")

        # Basic field validation
        if not name or not email or not message:
            messages.error(request, "All fields are required!")
            return redirect("contact")

        # Save the contact message to the database
        ContactMessage.objects.create(name=name, email=email, message=message)

        # Email Configuration
        subject = f"New Contact Message from {name}"
        email_body = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"
        recipient_email = "sreelakshmijalla@gmail.com"

        try:
            send_mail(
                subject=subject,
                message=email_body,
                from_email=settings.DEFAULT_FROM_EMAIL,  # Use email from settings
                recipient_list=[recipient_email],
                fail_silently=False,
            )
            messages.success(request, "Your message has been sent successfully!")
            logger.info("✅ Email Sent Successfully!")
        except Exception as e:
            messages.error(request, "There was an issue sending your message. Please try again later.")
            logger.error(f"❌ Email Sending Error: {e}")

        return redirect("contact")

    return render(request, "contact.html")


def citation_generator(request):
    """
    Citation generator view. Displays a tool for generating legal citations.
    """
    citation_result = None

    if request.method == "POST":
        form = CitationForm(request.POST)
        if form.is_valid():
            case_name = form.cleaned_data['case_name']
            court = form.cleaned_data['court']
            year = form.cleaned_data['year']
            volume = form.cleaned_data['volume']
            reporter = form.cleaned_data['reporter']
            page = form.cleaned_data['page']

            # Generate legal citation format
            citation_result = f"{case_name}, {volume} {reporter} {page} ({court} {year})"
            
            # Store citation in session for PDF generation
            request.session['citation_text'] = citation_result

    else:
        form = CitationForm()

    return render(request, 'citation_generator.html', {'form': form, 'citation_result': citation_result})


def download_contract_pdf(request):
    """
    Download contract as PDF. Generates a well-formatted PDF of the contract.
    """
    contract_text = request.POST.get('contract_text', "No contract available") if request.method == "POST" else "No contract available"

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="contract.pdf"'

    doc = SimpleDocTemplate(response, pagesize=letter)
    styles = getSampleStyleSheet()
    
    content = []
    
    # Title
    title_style = styles["Title"]
    title_style.textColor = colors.darkblue
    title = Paragraph("Legal Contract", title_style)
    content.append(title)

    # Space after title
    content.append(Paragraph("<br/><br/>", styles["Normal"]))

    # Contract text with proper formatting
    contract_paragraph = Paragraph(contract_text.replace("\n", "<br/>"), styles["Normal"])
    content.append(contract_paragraph)
    
    doc.build(content)
    
    return response


def contract_generator(request):
    """
    Contract generator view. Displays a tool for generating legal contracts.
    """
    contract_text = None

    if request.method == "POST":
        form = ContractForm(request.POST)
        if form.is_valid():
            party_one = form.cleaned_data['party_one']
            party_two = form.cleaned_data['party_two']
            contract_type = form.cleaned_data['contract_type']
            contract_terms = form.cleaned_data['contract_terms']
            effective_date = form.cleaned_data['effective_date']

            # Generate contract text
            contract_templates = {
                "nda": f"This Non-Disclosure Agreement (NDA) is made between {party_one} and {party_two} on {effective_date}. {contract_terms}",
                "employment": f"This Employment Contract is made between {party_one} (Employer) and {party_two} (Employee) on {effective_date}. {contract_terms}",
                "rental": f"This Rental Agreement is between {party_one} (Landlord) and {party_two} (Tenant), effective {effective_date}. {contract_terms}",
                "sales": f"This Sales Agreement is entered into by {party_one} (Seller) and {party_two} (Buyer) on {effective_date}. {contract_terms}",
            }

            contract_text = contract_templates.get(contract_type, "Invalid contract type selected.")

    else:
        form = ContractForm()

    return render(request, 'contract_generator.html', {'form': form, 'contract_text': contract_text})


def legal_articles_list(request):
    """
    Legal articles list view. Displays a list of articles, optionally filtered by category.
    """
    category = request.GET.get('category', '')
    if category:
        articles = LegalArticle.objects.filter(category=category)
    else:
        articles = LegalArticle.objects.all()
    
    return render(request, "legal/articles_list.html", {"articles": articles})


def legal_article_detail(request, article_id):
    """
    Legal article detail view. Displays a single article.
    """
    article = get_object_or_404(LegalArticle, id=article_id)
    return render(request, "legal/article_detail.html", {"article": article})


def legal_documents_list(request):
    """
    Legal documents list view. Displays a list of all document templates.
    """
    documents = LegalDocumentTemplate.objects.all()
    return render(request, "legal/documents_list.html", {"documents": documents})


def download_document(request, document_id):
    """
    Download document view. Allows downloading a legal document template.
    """
    document = get_object_or_404(LegalDocumentTemplate, id=document_id)
    return FileResponse(document.document_file.open(), as_attachment=True)


def legal_news_view(request):
    """
    Legal news view. Displays news articles fetched from an external API.
    """
    articles = fetch_legal_news()
    return render(request, 'legal/news.html', {'articles': articles})


def resources_view(request):
    """
    Resources view. Displays and searches resources, articles, and documents.
    """
    query = request.GET.get("q", "")
    
    articles = LegalArticle.objects.all()
    # Using LegalDocumentTemplate instead of LegalDocument
    documents = LegalDocumentTemplate.objects.all()
    # Using LegalResource instead of Resource
    db_resources = LegalResource.objects.all()

    if query:
        articles = articles.filter(title__icontains=query)
        documents = documents.filter(title__icontains=query)
        db_resources = db_resources.filter(title__icontains=query)

    context = {
        "articles": articles,
        "documents": documents,
        "db_resources": db_resources,
        "query": query,
    }
    return render(request, "resources.html", context)


def fetch_legal_cases(request):
    """
    Fetch legal cases view. Fetches case data from Court Listener API.
    """
    url = "https://www.courtlistener.com/api/rest/v4/opinions/"
    search_query = request.GET.get("search", "intellectual property")  # Default search term
    params = {"search": search_query}

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        return render(request, "legal/case_law_search.html", {"cases": data["results"]})
    except requests.RequestException as e:
        logger.error(f"API Request Error: {e}")
        return JsonResponse({"error": "Failed to fetch legal cases"}, status=500)


def articles_list(request):
    """
    Articles list view. Displays a list of all legal articles ordered by date.
    """
    articles = LegalArticle.objects.all().order_by("-published_date")
    return render(request, "legal/articles_list.html", {"articles": articles})


def article_detail(request, article_id):
    """
    Article detail view. Displays a single legal article.
    """
    article = get_object_or_404(LegalArticle, id=article_id)
    return render(request, "legal/article_detail.html", {"article": article})

def articles_home(request):
    articles = fetch_legal_articles_from_newsdata()
    print("Fetched Articles:", articles)  # <-- Add this
    return render(request, 'legals/articles_list.html', {'articles': articles})

@staff_member_required
def dashboard(request):
    """
    Dashboard view. Displays admin options for authenticated staff users.
    """
    # Count various entities for dashboard stats
    stats = {
        'blog_posts': BlogPost.objects.count(),
        'case_studies': CaseStudy.objects.count(),
        'legal_articles': LegalArticle.objects.count(),
        'legal_documents': LegalDocumentTemplate.objects.count(),
        'contact_messages': ContactMessage.objects.count(),
        'profiles': Profile.objects.count(),
    }
    
    return render(request, 'dashboard/index.html', {'stats': stats})

@staff_member_required
def dashboard_profile(request, profile_id=None):
    """
    Edit profile in dashboard.
    """
    if profile_id:
        profile = get_object_or_404(Profile, id=profile_id)
        title = "Edit Profile"
    else:
        profile = None
        title = "Create New Profile"
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            profile = form.save()
            messages.success(request, f"Profile '{profile.name}' saved successfully!")
            return redirect('dashboard_profile', profile_id=profile.id)
    else:
        form = ProfileForm(instance=profile)
    
    profiles = Profile.objects.all()
    return render(request, 'dashboard/profile.html', {
        'form': form, 
        'profile': profile,
        'profiles': profiles,
        'title': title
    })

@staff_member_required
def dashboard_education(request, profile_id, education_id=None):
    """
    Edit education in dashboard.
    """
    profile = get_object_or_404(Profile, id=profile_id)
    
    if education_id:
        education = get_object_or_404(Education, id=education_id, profile=profile)
        title = "Edit Education"
    else:
        education = None
        title = "Add Education"
    
    if request.method == 'POST':
        form = EducationForm(request.POST, instance=education)
        if form.is_valid():
            education = form.save(commit=False)
            education.profile = profile
            education.save()
            messages.success(request, f"Education '{education.degree}' saved successfully!")
            return redirect('dashboard_profile', profile_id=profile.id)
    else:
        form = EducationForm(instance=education)
    
    educations = Education.objects.filter(profile=profile)
    return render(request, 'dashboard/education.html', {
        'form': form, 
        'profile': profile,
        'education': education,
        'educations': educations,
        'title': title
    })

@staff_member_required
def dashboard_experience(request, profile_id, experience_id=None):
    """
    Edit legal experience in dashboard.
    """
    profile = get_object_or_404(Profile, id=profile_id)
    
    if experience_id:
        experience = get_object_or_404(LegalExperience, id=experience_id, profile=profile)
        title = "Edit Legal Experience"
    else:
        experience = None
        title = "Add Legal Experience"
    
    if request.method == 'POST':
        form = LegalExperienceForm(request.POST, instance=experience)
        if form.is_valid():
            experience = form.save(commit=False)
            experience.profile = profile
            experience.save()
            messages.success(request, f"Experience '{experience.position}' saved successfully!")
            return redirect('dashboard_profile', profile_id=profile.id)
    else:
        form = LegalExperienceForm(instance=experience)
    
    experiences = LegalExperience.objects.filter(profile=profile)
    return render(request, 'dashboard/experience.html', {
        'form': form, 
        'profile': profile,
        'experience': experience,
        'experiences': experiences,
        'title': title
    })

@staff_member_required
def dashboard_articles(request, article_id=None):
    """
    Manage legal articles in dashboard.
    """
    if article_id:
        article = get_object_or_404(LegalArticle, id=article_id)
        title = "Edit Legal Article"
    else:
        article = None
        title = "Create New Legal Article"
    
    if request.method == 'POST':
        form = LegalArticleForm(request.POST, instance=article)
        if form.is_valid():
            article = form.save()
            messages.success(request, f"Article '{article.title}' saved successfully!")
            return redirect('dashboard_articles')
    else:
        form = LegalArticleForm(instance=article)
    
    articles = LegalArticle.objects.all().order_by('-published_date')
    return render(request, 'dashboard/articles.html', {
        'form': form, 
        'article': article,
        'articles': articles,
        'title': title
    })

@staff_member_required
def dashboard_documents(request, document_id=None):
    """
    Manage legal document templates in dashboard.
    """
    if document_id:
        document = get_object_or_404(LegalDocumentTemplate, id=document_id)
        title = "Edit Document Template"
    else:
        document = None
        title = "Create New Document Template"
    
    if request.method == 'POST':
        form = LegalDocumentTemplateForm(request.POST, request.FILES, instance=document)
        if form.is_valid():
            document = form.save()
            messages.success(request, f"Document template '{document.title}' saved successfully!")
            return redirect('dashboard_documents')
    else:
        form = LegalDocumentTemplateForm(instance=document)
    
    documents = LegalDocumentTemplate.objects.all().order_by('-created_at')
    return render(request, 'dashboard/documents.html', {
        'form': form, 
        'document': document,
        'documents': documents,
        'title': title
    })

@staff_member_required
def delete_item(request, model_name, item_id):
    """
    Generic view to delete items from the dashboard.
    """
    models_map = {
        'profile': Profile,
        'education': Education,
        'experience': LegalExperience,
        'article': LegalArticle,
        'document': LegalDocumentTemplate,
        'award': LegalAward,
        'publication': LegalPublication,
    }
    
    model = models_map.get(model_name)
    if not model:
        messages.error(request, f"Invalid model name: {model_name}")
        return redirect('dashboard')
    
    try:
        item = model.objects.get(id=item_id)
        item_name = getattr(item, 'title', getattr(item, 'name', f"Item #{item_id}"))
        item.delete()
        messages.success(request, f"{model_name.capitalize()} '{item_name}' deleted successfully!")
    except model.DoesNotExist:
        messages.error(request, f"{model_name.capitalize()} with ID {item_id} does not exist.")
    
    # Redirect based on the model
    if model_name == 'profile':
        return redirect('dashboard')
    elif model_name == 'education' or model_name == 'experience':
        # Assumes we have the profile ID in the URL
        profile_id = request.GET.get('profile_id')
        if profile_id:
            return redirect('dashboard_profile', profile_id=profile_id)
    elif model_name == 'article':
        return redirect('dashboard_articles')
    elif model_name == 'document':
        return redirect('dashboard_documents')
    
    # Default fallback
    return redirect('dashboard')

def case_study_list(request):
    case_studies = CaseStudy.objects.all().order_by('-created_at')
    return render(request, 'case_study_list.html', {'case_studies': case_studies})
