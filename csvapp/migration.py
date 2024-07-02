from pgvector.django import VectorExtension
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
    ('csvapp', '0001_initial')
    ]
    operations = [
        VectorExtension(),
        migrations.RunSQL(
            """
            -- Create the tsvector column
            ALTER TABLE class_embedding ADD COLUMN content_tsvector TSVECTOR;

            -- Populate the tsvector column with data
            UPDATE class_embedding
            SET content_tsvector = to_tsvector('yiddish', content_id);
            
            -- Create a GIN index on the tsvector column for faster full-text search
            CREATE INDEX class_embedding_content_tsvector_idx ON class_embedding USING GIN(content_tsvector);
            """,
            reverse_sql=migrations.RunSQL.noop  # Reverse operation is a no-op
        ),
       migrations.RunSQL(
            """
            -- Create the tsvector column
            ALTER TABLE input_embedding ADD COLUMN content_tsvector TSVECTOR;

            -- Populate the tsvector column with data
            UPDATE input_embedding
            SET content_tsvector = to_tsvector('yiddish', content_id);

            -- Create a GIN index on the tsvector column for faster full-text search
            CREATE INDEX input_embedding_content_tsvector_idx ON input_embedding USING GIN(content_tsvector);
            """,
            reverse_sql=migrations.RunSQL.noop  # Reverse operation is a no-op
        ),
       
       migrations.RunSQL(
            """
		create or replace view v_category_hint as
		 (
		    SELECT category, array_to_string(ARRAY_AGG(ts_word::VARCHAR), '|') AS ts_words_string
		    FROM category_hint
		    GROUP BY category
		)
            """,
            reverse_sql=migrations.RunSQL.noop  # Reverse operation is a no-op
       ),       
       migrations.RunSQL(
            """
            create or replace view v_input_embedding_with_category as (
            SELECT id, ie.content_id, COALESCE(a.category, 'Other') as category, model_id,embedding, content_tsvector
            FROM input_embedding ie
            left JOIN v_category_hint a ON ie.content_tsvector @@ to_tsquery('yiddish', a.ts_words_string)
            ORDER BY ie.content_id)    

            """,
            reverse_sql=migrations.RunSQL.noop  # Reverse operation is a no-op

       ),
       migrations.RunSQL(
            """
            create or replace view v_class_embedding_with_category as (
            SELECT id, ie.content_id, COALESCE(a.category, 'Other') as category, model_id, embedding, content_tsvector
            FROM class_embedding ie
            left JOIN v_category_hint a ON ie.content_tsvector @@ to_tsquery('yiddish', a.ts_words_string)
            ORDER BY ie.content_id)            
            """,
            reverse_sql=migrations.RunSQL.noop  # Reverse operation is a no-op

       ),
       

    ]
