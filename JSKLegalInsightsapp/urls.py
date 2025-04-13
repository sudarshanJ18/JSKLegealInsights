from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    # Existing URLs
    path('', views.home, name='home'),
    path('blog/', views.blog, name='blog'),
    path('blog/<int:post_id>/', views.blog_detail, name='blog_detail'),
    path('about/', views.about_view, name='about'),
    path('case-studies/', views.case_studies, name='case_studies'),
    path('case-studies/<int:case_id>/', views.case_study_detail, name='case_study_detail'),
    path('resources/', views.resources, name='resources'),
    path('contact/', views.contact_view, name='contact'),
    path('login/', views.login_user, name='login'),
    path('register/', views.register, name='register'),
    path('password-reset/', views.password_reset, name='password_reset'),
    path('privacy/', views.privacy, name='privacy'),
    path('analyzer/', views.analyzer, name='analyzer'),
    path('portfolio/', views.portfolio, name='portfolio'),
    path('case-law-search/', views.case_law_search, name='case_law_search'),
    path('citation-generator/', views.citation_generator, name='citation_generator'),
    path('download-contract-pdf/', views.download_contract_pdf, name='download_contract_pdf'),
    path('contract-generator/', views.contract_generator, name='contract_generator'),
    path('legal-articles/', views.legal_articles_list, name='legal_articles_list'),
    path('legal-articles/<int:article_id>/', views.legal_article_detail, name='legal_article_detail'),
    path('legal-documents/', views.legal_documents_list, name='legal_documents_list'),
    path('download-document/<int:document_id>/', views.download_document, name='download_document'),
    path('legal-news/', views.legal_news_view, name='legal_news'),
    path('articles/', views.articles_list, name='articles_list'),
    path('articles/<int:article_id>/', views.article_detail, name='article_detail'),
    
    # New dashboard URLs
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/profile/', views.dashboard_profile, name='dashboard_profile'),
    path('dashboard/profile/<int:profile_id>/', views.dashboard_profile, name='dashboard_profile'),
    path('dashboard/profile/<int:profile_id>/education/', views.dashboard_education, name='dashboard_education'),
    path('dashboard/profile/<int:profile_id>/education/<int:education_id>/', views.dashboard_education, name='dashboard_education'),
    path('dashboard/profile/<int:profile_id>/experience/', views.dashboard_experience, name='dashboard_experience'),
    path('dashboard/profile/<int:profile_id>/experience/<int:experience_id>/', views.dashboard_experience, name='dashboard_experience'),
    path('dashboard/articles/', views.dashboard_articles, name='dashboard_articles'),
    path('dashboard/articles/<int:article_id>/', views.dashboard_articles, name='dashboard_articles'),
    path('dashboard/documents/', views.dashboard_documents, name='dashboard_documents'),
    path('dashboard/documents/<int:document_id>/', views.dashboard_documents, name='dashboard_documents'),
    path('dashboard/delete/<str:model_name>/<int:item_id>/', views.delete_item, name='delete_item'),
]
    


# Serving media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
