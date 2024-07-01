from pgvector.django import VectorExtension
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
#        ("csvapp", "0022_delete_classificationembeddings"),
    ]
    operations = [
        VectorExtension(),
        migrations.RunSQL(
            """
            -- Create the tsvector column
            ALTER TABLE class_embedding ADD COLUMN content_tsvector TSVECTOR;

            -- Populate the tsvector column with data
            UPDATE class_embedding
            SET content_tsvector = to_tsvector('yiddish', classification_id);
            
            -- Create a GIN index on the tsvector column for faster full-text search
            CREATE INDEX class_embedding_content_tsvector_idx ON class_embedding USING GIN(content_tsvector);
            """,
            reverse_sql=migrations.RunSQL.noop  # Reverse operation is a no-op
        )

    ]
