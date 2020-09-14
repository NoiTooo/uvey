# Generated by Django 3.1.1 on 2020-09-14 07:33

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Theme',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('theme', models.CharField(max_length=30, verbose_name='タグ')),
            ],
            options={
                'verbose_name': 'テーマタグ',
                'verbose_name_plural': 'テーマタグ',
            },
        ),
        migrations.CreateModel(
            name='UploadImg',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='名前')),
                ('img', models.ImageField(help_text='「static/article/img」に格納されます。', upload_to='article/static/article/img/', verbose_name='イメージファイル')),
            ],
            options={
                'verbose_name': 'イメージ',
                'verbose_name_plural': 'イメージ',
            },
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30, verbose_name='タイトル')),
                ('content', models.TextField(verbose_name='記事内容')),
                ('thumbnail', models.ImageField(upload_to='article/media/thumbnail/', verbose_name='サムネイル用画像')),
                ('is_published', models.BooleanField(verbose_name='公開設定')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='登録日')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新日')),
                ('themes', models.ManyToManyField(blank=True, to='article.Theme', verbose_name='タグ')),
            ],
            options={
                'verbose_name': '記事',
                'verbose_name_plural': '記事',
            },
        ),
    ]
