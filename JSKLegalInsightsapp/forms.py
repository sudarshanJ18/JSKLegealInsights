from django import forms
from .models import (
    LegalResource, InteractiveTool, LegalArticle, LegalDocumentTemplate,
    ContactMessage, Citation, Contract, Profile, Education, LegalExperience
)


class LegalResourceForm(forms.ModelForm):
    class Meta:
        model = LegalResource
        fields = ['title', 'summary', 'image', 'link']
        widgets = {
            'summary': forms.Textarea(attrs={'rows': 4}),
        }


class InteractiveToolForm(forms.ModelForm):
    class Meta:
        model = InteractiveTool
        fields = ['name', 'description', 'icon', 'link']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }


class LegalArticleForm(forms.ModelForm):
    class Meta:
        model = LegalArticle
        fields = ['title', 'category', 'content', 'author']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'rich-text-editor'}),
        }


class LegalDocumentTemplateForm(forms.ModelForm):
    class Meta:
        model = LegalDocumentTemplate
        fields = ['title', 'description', 'document_file', 'content']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'content': forms.Textarea(attrs={'rows': 10}),
        }


class ContactMessageForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 4}),
        }


class CitationForm(forms.Form):
    case_name = forms.CharField(max_length=255)
    court = forms.CharField(max_length=100)
    year = forms.IntegerField(min_value=1700, max_value=2100)
    volume = forms.IntegerField(min_value=1)
    reporter = forms.CharField(max_length=50)
    page = forms.IntegerField(min_value=1)


class ContractForm(forms.Form):
    party_one = forms.CharField(max_length=255, label="First Party Name")
    party_two = forms.CharField(max_length=255, label="Second Party Name")
    contract_type = forms.ChoiceField(choices=[
        ('nda', 'Non-Disclosure Agreement'),
        ('employment', 'Employment Contract'),
        ('rental', 'Rental Agreement'),
        ('sales', 'Sales Agreement'),
    ])
    contract_terms = forms.CharField(widget=forms.Textarea, label="Contract Terms")
    effective_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'degree', 'email', 'location', 'profile_image', 
                  'about_me', 'career_goal', 'title', 'resume_file']
        widgets = {
            'about_me': forms.Textarea(attrs={'rows': 5}),
            'career_goal': forms.Textarea(attrs={'rows': 3}),
        }


class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = ['degree', 'institution', 'start_year', 'end_year', 
                  'gpa', 'description', 'is_current', 'honors']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'honors': forms.Textarea(attrs={'rows': 3}),
        }


class LegalExperienceForm(forms.ModelForm):
    class Meta:
        model = LegalExperience
        fields = ['position', 'organization', 'location', 'start_date', 
                  'end_date', 'is_current', 'description']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }


class CaseLawSearchForm(forms.Form):
    query = forms.CharField(max_length=255, label="Search Case Law")