from django.db import migrations


def create_superuser(apps, schema_editor):
    User = apps.get_model("auth", "User")
    User.objects.create_superuser("test", "test@gmail.com", "test")


def reverse_func(apps, schema_editor):
    User = apps.get_model("auth", "User")
    User.objects.get(username="test").delete()


class Migration(migrations.Migration):
    # dependencies = [
    #     ('main', '0001_initial'),
    # ]

    operations = [
        migrations.RunPython(create_superuser, reverse_func),
    ]
