from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class AboutPage(models.Model):
    title = models.CharField(max_length=255, default="About Us")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "About Page"
        verbose_name_plural = "About Page"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    name = models.CharField(max_length=100)
    degree = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    location = models.CharField(max_length=100)
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)
    about_me = models.TextField()
    career_goal = models.TextField()
    # New fields for Emily's profile
    title = models.CharField(max_length=255, blank=True)  # e.g., "J.D. Candidate | Constitutional Law Focus"
    resume_file = models.FileField(upload_to='resumes/', null=True, blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"

class Education(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='education')
    degree = models.CharField(max_length=200)
    institution = models.CharField(max_length=200)
    start_year = models.PositiveIntegerField()
    end_year = models.PositiveIntegerField(null=True, blank=True)
    gpa = models.CharField(max_length=10, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    # New fields for Emily's education
    is_current = models.BooleanField(default=False)
    honors = models.TextField(blank=True, null=True)
    
    @property
    def date_range(self):
        end = 'Present' if self.is_current else str(self.end_year)
        return f"{self.start_year} - {end}"

    def __str__(self):
        return f"{self.degree} at {self.institution}"
    
    class Meta:
        verbose_name = "Education"
        verbose_name_plural = "Education History"
        ordering = ['-end_year', '-start_year']

class SkillCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Skill Category"
        verbose_name_plural = "Skill Categories"

class Skill(models.Model):
    category = models.ForeignKey(SkillCategory, on_delete=models.CASCADE, related_name='skills')
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Skill"
        verbose_name_plural = "Skills"

# New model for Legal Experience
class LegalExperience(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='legal_experiences')
    position = models.CharField(max_length=200)
    organization = models.CharField(max_length=200)
    location = models.CharField(max_length=100, blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_current = models.BooleanField(default=False)
    description = models.TextField()
    
    @property
    def date_range(self):
        if self.is_current:
            return f"{self.start_date.strftime('%B %Y')} - Present"
        elif self.end_date:
            # For seasonal positions like "Summer 2024"
            if self.start_date.month in [6, 7, 8] and self.end_date.month in [8, 9] and self.start_date.year == self.end_date.year:
                return f"Summer {self.start_date.year}"
            # For academic year positions
            elif (self.start_date.month in [8, 9] and self.end_date.month in [5, 6] and 
                  self.end_date.year - self.start_date.year == 1):
                return f"{self.start_date.year}-{self.end_date.year}"
            else:
                return f"{self.start_date.strftime('%B %Y')} - {self.end_date.strftime('%B %Y')}"
        return f"{self.start_date.strftime('%B %Y')}"
    
    def __str__(self):
        return f"{self.position} at {self.organization}"
    
    
        
    class Meta:
        verbose_name = "Legal Experience"
        verbose_name_plural = "Legal Experiences"
        ordering = ['-start_date']

# New model for Publications/Research
class LegalPublication(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='legal_publications')
    title = models.CharField(max_length=200)
    publication_type = models.CharField(max_length=100)  # e.g., "Published in Columbia Law Review"
    year = models.IntegerField()
    description = models.TextField()
    image = models.ImageField(upload_to='research_images/', blank=True, null=True)
    link = models.URLField(null=True, blank=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Legal Publication"
        verbose_name_plural = "Legal Publications"
        ordering = ['-year']

# New model for Awards
class LegalAward(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='legal_awards')
    title = models.CharField(max_length=200)
    description = models.TextField()
    year = models.CharField(max_length=20)  # Using CharField to allow ranges like "2023-2024"
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Legal Award"
        verbose_name_plural = "Legal Awards"
        ordering = ['-year']

# New model for Social Links
class SocialLink(models.Model):
    PLATFORM_CHOICES = [
        ('linkedin', 'LinkedIn'),
        ('twitter', 'Twitter'),
        ('facebook', 'Facebook'),
        ('portfolio', 'Portfolio'),
    ]
    
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='social_links')
    platform = models.CharField(max_length=50, choices=PLATFORM_CHOICES)
    url = models.URLField()
    
    def __str__(self):
        return f"{self.profile.name}'s {self.platform}"
    
    class Meta:
        verbose_name = "Social Link"
        verbose_name_plural = "Social Links"

class BlogPost(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # Directly linked to Django's built-in User model
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  # Tracks last modification time
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Blog Post"
        verbose_name_plural = "Blog Posts"
        ordering = ['-created_at']

class CaseStudy(models.Model):
    title = models.CharField(max_length=255)  # Title of the case study
    summary = models.TextField()  # Short description of the case study
    content = models.TextField()  # Detailed content of the case study
    image = models.ImageField(upload_to='case_studies/', blank=True, null=True)  # Optional image
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='case_studies', null=True)  # Author of the case study
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when created
    updated_at = models.DateTimeField(auto_now=True)  # Timestamp when updated

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Case Study"
        verbose_name_plural = "Case Studies"
        ordering = ['-created_at']
        
class ContactMessage(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name} - {self.email}"
    
    class Meta:
        verbose_name = "Contact Message"
        verbose_name_plural = "Contact Messages"
        ordering = ['-created_at']


class LegalResource(models.Model):
    title = models.CharField(max_length=255)
    summary = models.TextField()
    image = models.ImageField(upload_to='resources/')
    link = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Legal Resource"
        verbose_name_plural = "Legal Resources"
        ordering = ['-created_at']


class InteractiveTool(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    icon = models.CharField(max_length=100, help_text="FontAwesome icon class (e.g., 'fas fa-balance-scale')")
    link = models.URLField()

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Interactive Tool"
        verbose_name_plural = "Interactive Tools"

class LegalNews(models.Model):
    title = models.CharField(max_length=255)
    summary = models.TextField()
    link = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Legal News"
        verbose_name_plural = "Legal News"
        ordering = ['-created_at']
    
class CaseLaw(models.Model):
    title = models.CharField(max_length=255)
    summary = models.TextField()
    full_text = models.TextField()
    citation = models.CharField(max_length=255, blank=True, null=True)
    date_decided = models.DateField()
    court = models.CharField(max_length=255)
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Case Law"
        verbose_name_plural = "Case Law"
        ordering = ['-date_decided']
    
class Citation(models.Model):
    citation_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.citation_text[:50] 
    
    class Meta:
        verbose_name = "Citation"
        verbose_name_plural = "Citations"
        ordering = ['-created_at']
    
class Contract(models.Model):
    contract_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Contract {self.id} - {self.created_at.strftime('%Y-%m-%d')}"
    
    class Meta:
        verbose_name = "Contract"
        verbose_name_plural = "Contracts"
        ordering = ['-created_at']

class LegalArticle(models.Model):
    title = models.CharField(max_length=255)
    category = models.CharField(max_length=100, choices=[
        ("rights", "Understanding Your Rights"),
        ("contract", "Contract Law Basics"),
        ("ip", "Intellectual Property Law"),
        ("employment", "Employment & Labor Laws"),
        ("criminal", "Criminal Law & Procedure"),
        ("family", "Family & Divorce Law"),
        ("business", "Business & Corporate Law"),
    ])
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.CharField(max_length=255, default="Unknown")  # Set default value
    published_date = models.DateTimeField(default=timezone.now)  # Set default to now

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Legal Article"
        verbose_name_plural = "Legal Articles"
        ordering = ['-published_date']

class LegalDocumentTemplate(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    document_file = models.FileField(upload_to="legal_documents/")
    content = models.TextField(blank=True, null=True)  # Ensure content is optional
    created_at = models.DateTimeField(auto_now_add=True)  # Ensure this field exists

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Legal Document Template"
        verbose_name_plural = "Legal Document Templates"
        ordering = ['-created_at']
    
class Resource(models.Model):
    # Check if this model exists
    title = models.CharField(max_length=255)
    content = models.TextField()
    
    def __str__(self):
        return self.title
class SiteConfiguration(models.Model):
    """Global site configuration and theme settings"""
    site_title = models.CharField(max_length=100, default="Portfolio", help_text="Title that appears in browser tab")
    primary_color = models.CharField(max_length=20, default="#4b6cb7", help_text="Primary color for the site (hex code)")
    secondary_color = models.CharField(max_length=20, default="#2c3e50", help_text="Secondary color for the site (hex code)")
    show_resume_button = models.BooleanField(default=True, help_text="Show or hide the resume download button")
    footer_text = models.TextField(blank=True, null=True, help_text="Text to appear in the footer")
    meta_description = models.TextField(blank=True, null=True, help_text="Site description for SEO")
    google_analytics_id = models.CharField(max_length=50, blank=True, null=True, help_text="Google Analytics tracking ID")

    def __str__(self):
        return "Site Configuration"
    
    class Meta:
        verbose_name_plural = "Site Configuration"
        verbose_name = "Site Configuration"

    def save(self, *args, **kwargs):
        # Ensure only one instance of SiteConfiguration
        self.__class__.objects.exclude(id=self.id).delete()
        super().save(*args, **kwargs)

    @classmethod
    def get_solo(cls):
        """Get or create the singleton configuration instance"""
        obj, created = cls.objects.get_or_create(pk=1)
        return obj