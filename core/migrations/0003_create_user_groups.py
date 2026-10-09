from django.db import migrations


ORGANIZER = 'Организатор выставки'
CHAIRMAN = 'Председатель клуба'


def create_groups(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Group.objects.get_or_create(name=ORGANIZER)
    Group.objects.get_or_create(name=CHAIRMAN)


def remove_groups(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Group.objects.filter(name__in=[ORGANIZER, CHAIRMAN]).delete()


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0002_alter_medal_breed'),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]
    operations = [
        migrations.RunPython(create_groups, remove_groups),
    ]