import psycopg2

from loguru import logger
from typing import Any, Dict, Tuple


class postgresDB():
    """The PostgreSQL datastore used for the demo application.

    Attributes:
      uri_params: A dictionary with the URI parameters for db connection.
    """

    def __init__(self,
                 uri_params: Dict[str, str]) -> str:
        self.host = uri_params["host"]
        self.dbname = uri_params["dbname"]
        self.password = uri_params["password"]
        self.port = uri_params["port"]
        self.ssl = uri_params["ssl"]
        self.user = uri_params["user"]

    def execute_and_commit(self,
                           cur: Any,
                           conn: Any,
                           sql: str,
                           data: Tuple[str, str] = None
                           ) -> int:
        """Execute a SQL query and commit the current transaction.

        Args:
          cur: connection cursor.
          conn: psycopg2 connection object.
          sql: the SQL statement to execute.
          data: placeholder for values to fill in SQL query.

        Returns:
          rows: number of rows that the last execute call produced
        """
        cur.execute(sql, data)
        rows = cur.rowcount
        cur.close()
        conn.commit()
        return rows

    def create_table(self) -> None:
        """Create the db table if the table did not exist."""
        conn = psycopg2.connect(
            host=self.host, dbname=self.dbname,
            user=self.user, password=self.password,
            port=self.port, sslmode=self.ssl
        )
        try:
            cur = conn.cursor()
            sql = """
              CREATE TABLE IF NOT EXISTS aiven_demo_app (
                      id SERIAL PRIMARY KEY,
                      storage_time TIMESTAMP NOT NULL,
                      item BIGINT NOT NULL,
                      log_time VARCHAR(30) NOT NULL,
                      error VARCHAR(25) NOT NULL
              );"""
            self.execute_and_commit(cur, conn, sql)
            logger.info(
                "Table 'aiven_demo_app' existed or was created in Aiven")
        except psycopg2.DatabaseError as de:
            logger.error(f"Error creating table 'aiven_demo_app': {de}")
        except Exception as e:
            logger.error(f"Error creating table 'aiven_demo_app': {e}")
        finally:
            if conn is not None:
                conn.close()

    def write_data(self, item: str, log_time: str, error: str) -> None:
        """Write data to table.

        Args:
          item: the first element of the Kafka Producer.
          log_time: the second element of the Kafka Producer.
          error: the third element of the Kafka Producer.
        """
        conn = psycopg2.connect(
            host=self.host, dbname=self.dbname,
            user=self.user, password=self.password,
            port=self.port, sslmode=self.ssl
        )
        try:
            cur = conn.cursor()
            sql = ("INSERT INTO aiven_demo_app VALUES (DEFAULT, now(), %s, %s, %s);")
            self.execute_and_commit(cur, conn, sql, (
                item,
                log_time,
                error,
            ))  # data needs to be a tuple!
            logger.info(
                f"Data written for item:{item} - error:{error} with updated status.")
        except psycopg2.DatabaseError as de:
            logger.error(f"Error writing data to table: {de}")
        except Exception as e:
            logger.error(f"Error writing data to table: {e}")
        finally:
            if conn is not None:
                conn.close()

    def get_table_size(self) -> int:
        """Return row count for table."""
        conn = psycopg2.connect(
            host=self.host, dbname=self.dbname,
            user=self.user, password=self.password,
            port=self.port, sslmode=self.ssl
        )
        try:
            cur = conn.cursor()
            sql = "SELECT COUNT(*) FROM aiven_demo_app;"
            cur.execute(sql)
            row_count = cur.fetchone()[0]
            logger.info(f"Table size is {row_count} rows")
            cur.close()
            return row_count
        except psycopg2.DatabaseError as de:
            logger.error(f"Error getting size of table: {de}")
        except Exception as e:
            logger.error(f"Error getting size of table: {e}")
        finally:
            if conn is not None:
                conn.close()
