<<<<<<< HEAD
# Generated by Django 4.2.4 on 2023-09-13 17:22
=======
# Generated by Django 4.2.4 on 2023-09-14 10:14
>>>>>>> 53653ba071b9153eadc5a72ec2b8fd7d2648e424

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendors', '0002_alter_vendor_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vendor',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='warranty_period',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
