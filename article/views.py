from django.contrib.auth import get_user_model
from django.views import generic

from .models import Article

User = get_user_model()


class Index(generic.ListView):
    template_name = 'article/index.html'
    queryset = Article.objects.all()
