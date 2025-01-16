from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_alter_solardate_solar_day_and_more'),
    ]

    operations = [
        migrations.RunSQL("""
            SET FOREIGN_KEY_CHECKS = 0;

            DROP TABLE IF EXISTS core_eventtype;
            DROP TABLE IF EXISTS core_event_new;

            CREATE TABLE core_eventtype (
                id bigint NOT NULL AUTO_INCREMENT PRIMARY KEY,
                name varchar(50) NOT NULL UNIQUE,
                slug varchar(50) NOT NULL UNIQUE,
                description text NOT NULL,
                color varchar(20) NOT NULL,
                icon varchar(20) NOT NULL,
                `order` integer NOT NULL DEFAULT 0
            );

            CREATE TABLE core_event_new (
                id bigint NOT NULL AUTO_INCREMENT PRIMARY KEY,
                title varchar(200) NOT NULL,
                description text NOT NULL,
                gregorian_date date NOT NULL,
                is_holy_day bool NOT NULL,
                sunset_start bool NOT NULL,
                solar_date_id bigint NOT NULL,
                event_type varchar(20) NOT NULL DEFAULT 'historical',
                event_type_new_id bigint NULL,
                FOREIGN KEY (solar_date_id) REFERENCES core_solardate(id),
                FOREIGN KEY (event_type_new_id) REFERENCES core_eventtype(id) ON DELETE SET NULL
            );

            INSERT INTO core_event_new (
                id, title, description, gregorian_date, is_holy_day, 
                sunset_start, solar_date_id
            ) 
            SELECT 
                id, title, description, gregorian_date, is_holy_day, 
                sunset_start, solar_date_id 
            FROM core_event;

            DROP TABLE core_event;
            RENAME TABLE core_event_new TO core_event;

            SET FOREIGN_KEY_CHECKS = 1;
        """, """
            SET FOREIGN_KEY_CHECKS = 0;
            DROP TABLE IF EXISTS core_eventtype;
            DROP TABLE IF EXISTS core_event_new;
            CREATE TABLE core_event_new LIKE core_event;
            INSERT INTO core_event_new SELECT * FROM core_event;
            DROP TABLE core_event;
            RENAME TABLE core_event_new TO core_event;
            SET FOREIGN_KEY_CHECKS = 1;
        """)
    ]
