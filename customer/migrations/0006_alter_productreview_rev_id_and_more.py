# Generated by Django 4.2.4 on 2023-09-28 14:57

from django.db import migrations, models
import shortuuid.django_fields


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0005_alter_productreview_review_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productreview',
            name='rev_id',
            field=shortuuid.django_fields.ShortUUIDField(alphabet='0123456789abcdefABCDEF', length=10, max_length=20, prefix='review-', unique=True),
        ),
        migrations.AlterField(
            model_name='productreview',
            name='review_rating',
            field=models.CharField(choices=[('⭐⭐⭐⭐⭐', 5), ('⭐⭐⭐', 3), ('⭐', 1), ('⭐⭐', 2), ('⭐⭐⭐⭐', 4)], default='--NONE---', max_length=50),
        ),
    ]
