import psycopg
from fastapi import Depends
from loguru import logger
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
                score,
                high_level_category,
                low_level_category,
                lang,
                manually_tested,
                benchmark_version
            FROM leaderboard_competitors
        """
        return self.execute_query(query)

    def select_users(self, username: str):
        query = "SELECT * FROM users WHERE username = %s"
        params = (username,)
        result = self.execute_query(query, params)
        return result

    def insert_user(self, user, hashed_password):
        query = "INSERT INTO users (username, password_hash) VALUES \
            (%s, %s) RETURNING id"
        params = (user.username, hashed_password)
        user_id = self.execute_query(query, params)[0]["id"]
        print(f"USER_ID: {user_id}")
        return user_id

    def insert_competitors(self, competitors):
        if not self.conn:
            self.connect()
        try:
            for data in competitors:
                data_dict = data.model_dump()

                columns = ", ".join(data_dict.keys())
                placeholders = ", ".join(["%s"] * len(data_dict))
                query = f"INSERT INTO leaderboard_competitors ({columns}) VALUES ({placeholders})"

                with self.conn.cursor() as cur:
                    cur.execute(query, list(data_dict.values()))

        except psycopg.errors.UniqueViolation as exc:
            logger.info(f"Exception: {exc}")
            raise exc

        self.conn.commit()


def get_settings():
    return Settings()


def get_postgres_client(settings: Settings = Depends(get_settings)):
    return PostgresClient(settings=settings.postgres_settings)
