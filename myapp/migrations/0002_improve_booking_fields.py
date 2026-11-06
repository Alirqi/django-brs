from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("myapp", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="book",
            name="userid",
            field=models.PositiveIntegerField(db_index=True),
        ),
        migrations.AlterField(
            model_name="book",
            name="busid",
            field=models.PositiveIntegerField(db_index=True),
        ),
        migrations.AlterField(
            model_name="bus",
            name="nos",
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name="bus",
            name="rem",
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name="book",
            name="nos",
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name="bus",
            name="price",
            field=models.DecimalField(decimal_places=2, max_digits=8),
        ),
        migrations.AlterField(
            model_name="book",
            name="price",
            field=models.DecimalField(decimal_places=2, max_digits=8),
        ),
    ]
