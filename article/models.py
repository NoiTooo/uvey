from django.db import models


class Theme(models.Model):
    """ テーマタグ """
    theme = models.CharField(verbose_name='タグ', max_length=30)

    def __str__(self):
        return self.theme

    class Meta:
        verbose_name = "テーマタグ"
        verbose_name_plural = "テーマタグ"


class UploadImg(models.Model):
    """ 記事挿入用の画像保管場所 """
    name = models.CharField(verbose_name='名前', max_length=100)
    img = models.ImageField(verbose_name='イメージファイル', upload_to='article/static/article/img/',
                            help_text='「static/article/img」に格納されます。')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "イメージ"
        verbose_name_plural = "イメージ"


class Article(models.Model):
    """ コンテンツ記事 """
    title = models.CharField(verbose_name='タイトル', max_length=30)
    content = models.TextField(verbose_name='記事内容')
    thumbnail = models.ImageField(verbose_name='サムネイル用画像', upload_to='article/media/thumbnail/')
    is_published = models.BooleanField(verbose_name='公開設定')
    created_at = models.DateTimeField(verbose_name='登録日', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新日', auto_now=True)
    themes = models.ManyToManyField(Theme, verbose_name='タグ', blank=True)
    views = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "記事"
        verbose_name_plural = "記事"


INQUIRY_TYPE = (('【Uvey】サービスに関するお問い合わせ', '【Uvey】サービスに関するお問い合わせ'),
                ('【Uvey】サービスに関するご意見・ご要望', '【Uvey】サービスに関するご意見・ご要望'),
                ('その他', 'その他'))


class Inquiry(models.Model):
    """ 問合せフォーム """
    name = models.CharField(verbose_name='お名前', max_length=30)
    email = models.EmailField(verbose_name='メールアドレス')
    inquiry_type = models.CharField(verbose_name='概要する問合せ', max_length=100, choices=INQUIRY_TYPE)
    inquiry = models.TextField(verbose_name='お問合せ内容')
    created_at = models.DateTimeField(verbose_name='登録日', auto_now_add=True)

    def __str__(self):
        return self.inquiry_type

    class Meta:
        verbose_name = "お問合せ"
        verbose_name_plural = "お問合せ"


"""
お悩み投稿機能
"""


class Post(models.Model):
    """お悩み"""
    name = models.CharField(verbose_name='お名前', max_length=10)
    title = models.CharField(verbose_name='タイトル', max_length=45)
    text = models.TextField(verbose_name='投稿内容')
    created_at = models.DateTimeField(verbose_name='登録日', auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "投稿"
        verbose_name_plural = "投稿"


class Comment(models.Model):
    """コメント."""
    name = models.CharField(max_length=255, blank=True)
    text = models.TextField()
    target = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(verbose_name='登録日', auto_now_add=True)
    is_public = models.BooleanField(default=True)  # コメント承認機能実装のときに利用

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "コメント"
        verbose_name_plural = "コメント"


class Reply(models.Model):
    """返信コメント."""
    name = models.CharField(max_length=255, blank=True)
    text = models.TextField()
    target = models.ForeignKey(Comment, on_delete=models.CASCADE)
    created_at = models.DateTimeField(verbose_name='登録日', auto_now_add=True)
    is_public = models.BooleanField(default=True)  # コメント承認機能実装のときに利用

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "返信コメント"
        verbose_name_plural = "返信コメント"
