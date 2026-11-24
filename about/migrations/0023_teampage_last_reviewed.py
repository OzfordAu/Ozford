from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('about', '0022_alter_testimonialpage_testimonial'),
    ]

    operations = [
        migrations.AddField(
            model_name='teampage',
            name='last_reviewed',
            field=models.DateField(
                blank=True,
                null=True,
                verbose_name='Last Reviewed',
                help_text='Date this page was last reviewed. Displayed on the page.'
            ),
        ),
    ]
