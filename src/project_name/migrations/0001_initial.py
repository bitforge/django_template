from django.db import migrations, models
import imagefield.fields
import sugus.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100, verbose_name='Title')),
                ('slug', models.SlugField(max_length=100, verbose_name='Slug')),
                ('image', imagefield.fields.ImageField(blank=True, height_field='image_height', null=True, upload_to=sugus.models.entry_upload_path, verbose_name='Image', width_field='image_width')),
                ('website', models.URLField(blank=True, null=True, verbose_name='Website')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('image_width', models.PositiveIntegerField(blank=True, editable=False, null=True)),
                ('image_height', models.PositiveIntegerField(blank=True, editable=False, null=True)),
            ],
            options={
                'verbose_name': 'Entry',
                'verbose_name_plural': 'Entries',
                'ordering': ('title',),
            },
        ),
    ]
