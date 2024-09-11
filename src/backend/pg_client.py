import psycopg
from fastapi import Depends
from psycopg.rows import dict_row
from settings import PostgresSettings, Settings


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

    def execute_query(self, query: str, params=None):
        if not self.conn:
            self.connect()
        with self.conn.cursor() as cur:
            cur.execute(query, params)
            self.conn.commit()
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

    def select_users(self, email: str):
        query = "SELECT * FROM users WHERE email = %s"
        params = (email,)
        result = self.execute_query(query, params)
        return result

    def insert_user(self, user, hashed_password):
        query = "INSERT INTO users (email, password_hash, full_name) VALUES \
            (%s, %s, %s) RETURNING id"
        params = (user.email, hashed_password, user.full_name)
        user_id = self.execute_query(query, params)[0]["id"]
        print(f"USER_ID: {user_id}")
        return user_id

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()


def get_settings():
    return Settings()


def get_postgres_client(settings: Settings = Depends(get_settings)):
    return PostgresClient(settings=settings.postgres_settings)
