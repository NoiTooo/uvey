from functools import reduce
from operator import and_
from datetime import datetime

from django.contrib.auth import get_user_model
from django.db.models import Q
from django.urls import reverse_lazy
from django.views import generic

from .models import Article
from .forms import InquiryCreateForm

User = get_user_model()


class Index(generic.ListView):
    """ TOPページ """
    template_name = 'article/index.html'
    queryset = Article.objects.order_by('-created_at').filter(is_published=True)
    context_object_name = 'object_list'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        # topRecommendedArticlesで最新の記事を1つ渡す
        ctx['first'] = Article.objects.filter(is_published=True).order_by('-created_at').first()
        # 2つ目以降の記事をリストで渡す
        ctx['list'] = Article.objects.filter(is_published=True).order_by('-created_at')[1:5]
        # 検索されたクエリを取り出す
        ctx['query'] = self.request.GET.get('q', '')
        # 検索されたクエリを集計する
        query_list = {}
        with open('./article/log/query.csv', encoding='UTF-8')as f:
            for item in f:
                columns = item.rstrip().split(',')
                query = columns[0]
                if query in query_list:
                    query_list[query] += 1
                else:
                    query_list[query] = 1
        # 検索されたクエリでトレンドワード作る
        trend_words = []
        for k, v in sorted(query_list.items(), key=lambda x: x[1], reverse=True):
            trend_words.append(str(k))
        ctx['trend_word1'] = trend_words[0]
        ctx['trend_word2'] = trend_words[1]
        ctx['trend_word3'] = trend_words[2]
        ctx['trend_word4'] = trend_words[3]
        ctx['trend_word5'] = trend_words[4]
        return ctx


class SearchResult(generic.ListView):
    """ 検索結果の表示 """
    template_name = 'article/search_result.html'
    queryset = Article.objects.order_by('-created_at').filter(is_published=True)
    context_object_name = 'object_list'

    def get_queryset(self):
        queryset = Article.objects.order_by('-created_at').filter(is_published=True)
        keyword = self.request.GET.get('q')
        if keyword:
            exclusion = set([' ', '　'])
            q_list = ''
            for i in keyword:
                if i in exclusion:
                    pass
                else:
                    q_list += i
            query = reduce(
                and_, [Q(title__icontains=q) |
                       Q(content__icontains=q) |
                       Q(themes__theme__icontains=q)
                       for q in q_list]
            )
            queryset = queryset.filter(query)
            # 検索されたクエリを書き込む
            with open('./article/log/query.csv', 'a', encoding='UTF-8')as f:
                today = datetime.today()
                f.write(keyword)
                f.write(',')
                f.write(str(today) + '\n')
        return queryset

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        # 検索されたクエリを取り出す
        ctx['query'] = self.request.GET.get('q', '')
        # 検索結果後、記事数をカウントする
        keyword = self.request.GET.get('q', '')
        count = Article.objects.filter(
            Q(title__icontains=keyword) |
            Q(content__icontains=keyword) |
            Q(themes__theme__icontains=keyword)).filter(is_published=True).count()
        ctx['count'] = count
        # 検索されたクエリを集計する
        query_list = {}
        with open('./article/log/query.csv', encoding='UTF-8')as f:
            for item in f:
                columns = item.rstrip().split(',')
                query = columns[0]
                if query in query_list:
                    query_list[query] += 1
                else:
                    query_list[query] = 1
        # 検索されたクエリでトレンドワード作る
        trend_words = []
        for k, v in sorted(query_list.items(), key=lambda x: x[1], reverse=True):
            trend_words.append(str(k))
        ctx['trend_word1'] = trend_words[0]
        ctx['trend_word2'] = trend_words[1]
        ctx['trend_word3'] = trend_words[2]
        ctx['trend_word4'] = trend_words[3]
        ctx['trend_word5'] = trend_words[4]
        return ctx


class Detail(generic.DetailView):
    """ 詳細ページ """
    template_name = 'article/detail.html'
    model = Article

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        # 検索されたクエリを取り出す
        ctx['query'] = self.request.GET.get('q', '')
        # 検索されたクエリを集計する
        query_list = {}
        with open('./article/log/query.csv', encoding='UTF-8')as f:
            for item in f:
                columns = item.rstrip().split(',')
                query = columns[0]
                if query in query_list:
                    query_list[query] += 1
                else:
                    query_list[query] = 1
        # 検索されたクエリでトレンドワード作る
        trend_words = []
        for k, v in sorted(query_list.items(), key=lambda x: x[1], reverse=True):
            trend_words.append(str(k))
        ctx['trend_word1'] = trend_words[0]
        ctx['trend_word2'] = trend_words[1]
        ctx['trend_word3'] = trend_words[2]
        ctx['trend_word4'] = trend_words[3]
        ctx['trend_word5'] = trend_words[4]
        return ctx


class Inquiry(generic.CreateView):
    """問い合わせフォーム"""
    template_name = 'article/inquiry.html'
    form_class = InquiryCreateForm
    success_url = reverse_lazy('article:inquiry_done')


class InquiryDone(generic.TemplateView):
    """問い合わせ完了"""
    template_name = 'article/inquiry_done.html'
