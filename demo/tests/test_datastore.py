import os
import psycopg2
import pytest


class TestPsqlDatasore():

    TEST_HOST = os.environ["TEST_HOST"]
    TEST_PASSWORD = os.environ["TEST_PASSWORD"]
    TEST_DB_NAME = os.environ["TEST_DB_NAME"]
    TEST_PORT = os.environ["TEST_PORT"]
    TEST_USER = os.environ["TEST_USER"]

    def test_db_connection(self):
        """Test the user can connect to database."""
        assert TestPsqlDatasore.TEST_HOST is not None
        assert TestPsqlDatasore.TEST_DB_NAME is not None
        assert TestPsqlDatasore.TEST_PASSWORD is not None
        assert TestPsqlDatasore.TEST_PORT is not None
        assert TestPsqlDatasore.TEST_USER is not None

        conn = psycopg2.connect(
            host=TestPsqlDatasore.TEST_HOST,
            dbname=TestPsqlDatasore.TEST_DB_NAME,
            user=TestPsqlDatasore.TEST_USER,
            password=TestPsqlDatasore.TEST_PASSWORD,
            port=TestPsqlDatasore.TEST_PORT,
            sslmode="require"
        )
        cur = conn.cursor()
        cur.execute("SELECT 1;")
        conn.commit()
        assert cur.fetchone()[0] == 1
        cur.close()

    def test_table_exists(self):
        """Test the user can read table."""
        conn = psycopg2.connect(
            host=TestPsqlDatasore.TEST_HOST,
            dbname=TestPsqlDatasore.TEST_DB_NAME,
            user=TestPsqlDatasore.TEST_USER,
            password=TestPsqlDatasore.TEST_PASSWORD,
            port=TestPsqlDatasore.TEST_PORT,
            sslmode="require"
        )

        cur = conn.cursor()
        cur.execute("SELECT * FROM aiven_demo_app LIMIT 1;")
        conn.commit()
        assert cur.fetchone()[0] == 1
        cur.close()
