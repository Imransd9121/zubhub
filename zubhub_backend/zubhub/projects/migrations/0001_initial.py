# Generated by Django 2.2.7 on 2021-05-16 03:47

from django.conf import settings
import django.contrib.postgres.indexes
import django.contrib.postgres.search
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True,
                                        primary_key=True, serialize=False, verbose_name='ID')),
                ('path', models.CharField(max_length=255, unique=True)),
                ('depth', models.PositiveIntegerField()),
                ('numchild', models.PositiveIntegerField(default=0)),
                ('name', models.CharField(max_length=100, unique=True)),
                ('description', models.CharField(
                    blank=True, max_length=1000, null=True)),
                ('slug', models.SlugField(max_length=1000, unique=True)),
                ('search_vector',
                 django.contrib.postgres.search.SearchVectorField(null=True)),
            ],
            options={
                'verbose_name_plural': 'categories',
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False,
                                        primary_key=True, serialize=False, unique=True)),
                ('title', models.CharField(max_length=1000)),
                ('description', models.CharField(
                    blank=True, max_length=10000, null=True)),
                ('video', models.URLField(blank=True, max_length=1000, null=True)),
                ('materials_used', models.CharField(max_length=5000)),
                ('views_count', models.IntegerField(blank=True, default=0)),
                ('likes_count', models.IntegerField(blank=True, default=0)),
                ('comments_count', models.IntegerField(blank=True, default=0)),
                ('slug', models.SlugField(max_length=1000, unique=True)),
                ('created_on', models.DateTimeField(
                    default=django.utils.timezone.now)),
                ('published', models.BooleanField(default=True)),
                ('search_vector',
                 django.contrib.postgres.search.SearchVectorField(null=True)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL,
                                               related_name='projects', to='projects.Category')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                              related_name='projects', to=settings.AUTH_USER_MODEL)),
                ('likes', models.ManyToManyField(blank=True,
                                                 related_name='projects_liked', to=settings.AUTH_USER_MODEL)),
                ('saved_by', models.ManyToManyField(blank=True,
                                                    related_name='saved_for_future', to=settings.AUTH_USER_MODEL)),
                ('views', models.ManyToManyField(blank=True,
                                                 related_name='projects_viewed', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True,
                                        primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('slug', models.SlugField(max_length=150, unique=True)),
                ('search_vector',
                 django.contrib.postgres.search.SearchVectorField(null=True)),
                ('projects', models.ManyToManyField(blank=True,
                                                    related_name='tags', to='projects.Project')),
            ],
        ),
        migrations.CreateModel(
            name='StaffPick',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False,
                                        primary_key=True, serialize=False, unique=True)),
                ('title', models.CharField(max_length=1000)),
                ('description', models.CharField(max_length=1000)),
                ('slug', models.SlugField(max_length=1000, unique=True)),
                ('created_on', models.DateTimeField(
                    default=django.utils.timezone.now)),
                ('is_active', models.BooleanField(default=True)),
                ('projects', models.ManyToManyField(
                    related_name='staff_picks', to='projects.Project')),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True,
                                        primary_key=True, serialize=False, verbose_name='ID')),
                ('image_url', models.URLField(max_length=1000)),
                ('public_id', models.CharField(
                    blank=True, max_length=1000, null=True)),
                ('project', models.ForeignKey(blank=True, null=True,
                                              on_delete=django.db.models.deletion.CASCADE, related_name='images', to='projects.Project')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True,
                                        primary_key=True, serialize=False, verbose_name='ID')),
                ('path', models.CharField(max_length=255, unique=True)),
                ('depth', models.PositiveIntegerField()),
                ('numchild', models.PositiveIntegerField(default=0)),
                ('text', models.CharField(max_length=10000)),
                ('created_on', models.DateTimeField(
                    default=django.utils.timezone.now)),
                ('published', models.BooleanField(default=True)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                              related_name='comments', to=settings.AUTH_USER_MODEL)),
                ('profile', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE,
                                              related_name='profile_comments', to=settings.AUTH_USER_MODEL)),
                ('project', models.ForeignKey(blank=True, null=True,
                                              on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='projects.Project')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddIndex(
            model_name='category',
            index=django.contrib.postgres.indexes.GinIndex(
                fields=['search_vector'], name='projects_ca_search__4ee9e0_gin'),
        ),
        migrations.AddIndex(
            model_name='tag',
            index=django.contrib.postgres.indexes.GinIndex(
                fields=['search_vector'], name='projects_ta_search__4852a3_gin'),
        ),
        migrations.AddIndex(
            model_name='project',
            index=django.contrib.postgres.indexes.GinIndex(
                fields=['search_vector'], name='projects_pr_search__1d35f9_gin'),
        ),
    ]
