CREATE TABLE leaderboard_competitors (
    record_id SERIAL PRIMARY KEY,
    id DOUBLE PRECISION NOT NULL,
    agent_name TEXT NOT NULL,
    score DOUBLE PRECISION NOT NULL,
    vul_deepeval TEXT NOT NULL,
    type_general TEXT NOT NULL,
    lang TEXT NOT NULL,
    manually_tested boolean NOT NULL,
    benchmark_version TEXT NOT NULL,
    reason TEXT NOT NULL,
    UNIQUE (agent_name, vul_deepeval, type_general, lang, manually_tested, benchmark_version, reason)
);

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL
);