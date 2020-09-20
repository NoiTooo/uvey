from datetime import datetime
from functools import reduce
from operator import and_
from urllib import request

from django.contrib.auth import get_user_model
from django.db.models import Q
from django.http import Http404
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse_lazy
from django.views import generic

from .forms import InquiryCreateForm
"""from .forms import CommentCreateForm, ReplyCreateForm"""
from .models import Article
"""from .models import Post, Comment, Reply"""

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
        """
        # Postモデルから値を貰う
        post = Post.objects.order_by('-created_at')
        ctx['post'] = post
        """
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
        # 記事ランキングを作る
        ranking = Article.objects.filter(is_published=True).order_by('-views')[:5]
        ctx['ranking'] = ranking
        return ctx


class SearchResult(generic.ListView):
    """ 検索結果の表示 """
    template_name = 'article/search_result.html'
    queryset = Article.objects.order_by('-created_at').filter(is_published=True)
    context_object_name = 'object_list'
    paginate_by = 8

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
        """
        # Postモデルから値を貰う
        post = Post.objects.order_by('-created_at')
        ctx['post'] = post
        """
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
        # ページネーション「●件ー●件の表示」
        page = self.request.GET.get('page')
        ctx['page'] = page
        if page is None or int(page) == 1:
            if count < 8:
                ctx['pagecountstart'] = 1
                ctx['pagecountend'] = count
            else:
                ctx['pagecountstart'] = 1
                ctx['pagecountend'] = 8
        else:
            ctx['pagecountstart'] = int(page) * 8 - 8
            ctx['pagecountend'] = int(page) * 8
        # 記事ランキングを作る
        ranking = Article.objects.filter(is_published=True).order_by('-views')[:5]
        ctx['ranking'] = ranking
        return ctx


class Detail(generic.DetailView):
    """ 詳細ページ """
    template_name = 'article/detail.html'
    model = Article

    def get_context_data(self, **kwargs):
        # オーバーライド
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
        # カウンターをつける
        pk = self.kwargs['pk']  # PKを取得する
        count = Article.objects.get(pk=pk)
        count.views += 1
        count.save()
        # 記事ランキングを作る
        ranking = Article.objects.filter(is_published=True).order_by('-views')[:5]
        ctx['ranking'] = ranking
        return ctx


class Inquiry(generic.CreateView):
    """問い合わせフォーム"""
    template_name = 'article/inquiry.html'
    form_class = InquiryCreateForm
    success_url = reverse_lazy('article:inquiry_done')


class InquiryDone(generic.TemplateView):
    """問い合わせ完了"""
    template_name = 'article/inquiry_done.html'


class PrivacyPolicy(generic.TemplateView):
    """ プライバシーポリシー """
    template_name = 'article/privacy_policy.html'


"""
お悩み相談機能
"""

"""
class PostListView(generic.ListView):
    # post/ でアクセス記事一覧.
    template_name = 'article/posting/post_list.html'
    model = Post
    paginate_by = 8

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
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
        # 記事ランキングを作る
        ranking = Article.objects.filter(is_published=True).order_by('-views')[:5]
        ctx['ranking'] = ranking
        return ctx


class PostDetailView(generic.DetailView):
    # post//detail/post_pk でアクセス。記事詳細.
    template_name = 'article/posting/post_detail.html'
    model = Post

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
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
        # 記事ランキングを作る
        ranking = Article.objects.filter(is_published=True).order_by('-views')[:5]
        ctx['ranking'] = ranking
        return ctx


class CommentView(generic.CreateView):
    # comment/post_pk コメント投稿.
    model = Comment
    template_name = 'article/posting/comment_form.html'
    form_class = CommentCreateForm
    success_url = reverse_lazy('article:post_list')

    def form_valid(self, form):
        post_pk = self.kwargs['pk']
        post = get_object_or_404(Post, pk=post_pk)

        # 紐づく記事を設定する
        comment = form.save(commit=False)
        comment.target = post
        comment.save()

        # 記事詳細にリダイレクト
        return redirect('article:post_detail', pk=post_pk)


class ReplyView(generic.CreateView):
    # /reply/comment_pk 返信コメント投稿.
    model = Reply
    template_name = 'article/posting/comment_form.html'
    form_class = ReplyCreateForm
    success_url = reverse_lazy('article:post_list')

    def form_valid(self, form):
        comment_pk = self.kwargs['pk']
        comment = get_object_or_404(Comment, pk=comment_pk)

        # 紐づくコメントを設定する
        reply = form.save(commit=False)
        reply.target = comment
        reply.save()

        # 記事詳細にリダイレクト
        return redirect('article:post_detail', pk=comment.target.pk)

"""