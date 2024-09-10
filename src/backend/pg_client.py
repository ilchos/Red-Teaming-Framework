import psycopg
from psycopg.rows import dict_row
from settings import PostgresSettings


class PostgresClient:
    def __init__(self, settings: PostgresSettings):
        self.settings = settings
        self.conn = None

    def connect(self):
        self.conn = psycopg.connect(
            row_factory=dict_row,
            **self.settings.model_dump(),
        )

    def disconnect(self):
        if self.conn:
            self.conn.close()

    def execute_query(self, query: str):
        if not self.conn:
            self.connect()
        with self.conn.cursor() as cur:
            cur.execute(query)
            return cur.fetchall()

    def select_competitors(self):
        query = """
            SELECT
                model_name,
                total,
                passed,
                hit_rate,
                manually_tested,
                high_level_category,
                mid_level_category,
                low_level_category
            FROM leaderboard_competitors
        """
        return self.execute_query(query)

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()
