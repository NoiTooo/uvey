from django import forms
from .models import Article, Inquiry, Comment, Reply


class InquiryCreateForm(forms.ModelForm):
    """問い合わせフォーム"""

    class Meta:
        model = Inquiry
        fields = ('name', 'email', 'inquiry_type', 'inquiry')


class CommentCreateForm(forms.ModelForm):
    """コメント投稿"""

    class Meta:
        model = Comment
        fields = ('name', 'text')


class ReplyCreateForm(forms.ModelForm):
    """返信投稿"""

    class Meta:
        model = Reply
        fields = ('name', 'text')
