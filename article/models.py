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
