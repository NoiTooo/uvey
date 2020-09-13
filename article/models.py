from django.db import models


class Theme(models.Model):
    theme = models.CharField(verbose_name='タグ', max_length=30)

    def __str__(self):
        return self.tag

    class Meta:
        verbose_name = "タグ"
        verbose_name_plural = "タグ"


class Article(models.Model):
    title = models.CharField(verbose_name='タイトル', max_length=30)
    content = models.TextField(verbose_name='記事内容')
    thumbnail = models.ImageField(verbose_name='サムネイル用画像/300pxx300px', upload_to='media/upload/thumbnail/')
    is_published = models.BooleanField(verbose_name='公開設定')
    created_at = models.DateTimeField(verbose_name='登録日', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新日', auto_now=True)
    themes = models.ManyToManyField(Theme, verbose_name='タグ', blank=True)

    def __str__(self):
        return self.tag

    class Meta:
        verbose_name = "記事"
        verbose_name_plural = "記事"
