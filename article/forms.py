from django import forms
from .models import Article, Inquiry


class InquiryCreateForm(forms.ModelForm):
    """問い合わせフォーム"""

    class Meta:
        model = Inquiry
        fields = ('name', 'email', 'inquiry_type', 'inquiry')
