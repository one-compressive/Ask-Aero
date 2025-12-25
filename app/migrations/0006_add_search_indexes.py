from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_remove_question_is_correct_answer_is_correct'),
    ]

    operations = [
        migrations.RunSQL(
            sql=[
                "CREATE INDEX IF NOT EXISTS app_question_title_idx ON app_question(title);",
                "CREATE INDEX IF NOT EXISTS app_question_text_idx ON app_question(text);",
            ],
            reverse_sql=[
                "DROP INDEX IF EXISTS app_question_title_idx;",
                "DROP INDEX IF EXISTS app_question_text_idx;",
            ]
        ),
    ]
