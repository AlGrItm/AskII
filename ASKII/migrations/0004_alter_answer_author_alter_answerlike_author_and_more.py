# Generated by Django 4.2.7 on 2023-12-27 13:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ASKII', '0003_alter_answerlike_managers_alter_question_managers_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='ASKII.profile'),
        ),
        migrations.AlterField(
            model_name='answerlike',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ASKII.profile'),
        ),
        migrations.AlterField(
            model_name='question',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='ASKII.profile'),
        ),
        migrations.AlterField(
            model_name='question',
            name='tag',
            field=models.ManyToManyField(related_name='questions', to='ASKII.tag'),
        ),
        migrations.AlterField(
            model_name='questionlike',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ASKII.profile'),
        ),
    ]
