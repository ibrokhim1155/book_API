# Generated by Django 5.1.1 on 2024-09-27 17:42

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_attributekey_attributevalue_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_comments', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='product',
            name='users_like',
            field=models.ManyToManyField(blank=True, related_name='products_likes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='productattributevalue',
            name='key',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='attribute_keys', to='product.attributekey'),
        ),
        migrations.AlterField(
            model_name='productattributevalue',
            name='value',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='attribute_values', to='product.attributevalue'),
        ),
        migrations.AlterField(
            model_name='productimage',
            name='image',
            field=models.ImageField(blank=True, upload_to='product'),
        ),
    ]
