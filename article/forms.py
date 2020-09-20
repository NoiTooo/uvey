from django import forms
from .models import Inquiry

"""from .models import Comment, Reply"""


class InquiryCreateForm(forms.ModelForm):
    """問い合わせフォーム"""

    class Meta:
        model = Inquiry
        fields = ('name', 'email', 'inquiry_type', 'inquiry')


"""
class CommentCreateForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('name', 'text')


class ReplyCreateForm(forms.ModelForm):

    class Meta:
        model = Reply
        fields = ('name', 'text')
"""
