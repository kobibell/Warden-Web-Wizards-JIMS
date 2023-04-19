from django.core.management.base import BaseCommand
import psycopg2

class Command(BaseCommand):
    help = 'Inserts data into the database'

    def handle(self, *args, **options):
        conn = psycopg2.connect(
            dbname="jims",
            user="postgres",
            password="sheetal",
            host="localhost",
            port="5432"
        )

        cur = conn.cursor()
        # cur.execute("""
        #     CREATE TABLE IF NOT EXISTS mytable (
        #         id SERIAL PRIMARY KEY,
        #         name VARCHAR(255),
        #         age INTEGER
        #     );
        # """)

        cur.execute("INSERT INTO jims_app_accounts (account_number, inmate_id, balance) VALUES (%s, %s, %s)", ("A123", "I121", 200))
        cur.execute("INSERT INTO jims_app_accounts (account_number, inmate_id, balance) VALUES (%s, %s, %s)", ("A124", "I124", 100))
        cur.execute("INSERT INTO jims_app_transactiondetails (account_number_id, transaction_type, transaction_amount, transaction_date) VALUES (%s, %s, %s, %s)", ("A123", 'D', 100, '2021-01-01 12:00:01'))
        
        conn.commit()
        conn.close()

        self.stdout.write(self.style.SUCCESS('Data inserted successfully!'))
