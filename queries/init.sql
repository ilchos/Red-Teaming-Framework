CREATE TABLE leaderboard_competitors (
    id SERIAL PRIMARY KEY,
    model_name TEXT NOT NULL,
    score DOUBLE PRECISION NOT NULL,
    low_level_category TEXT NOT NULL,
    high_level_category TEXT NOT NULL,
    lang TEXT NOT NULL,
    manually_tested boolean NOT NULL,
    benchmark_version TEXT NOT NULL,
    UNIQUE (model_name, low_level_category, high_level_category, lang, manually_tested, benchmark_version)
);
INSERT INTO leaderboard_competitors 
(model_name, score, low_level_category, high_level_category, lang, manually_tested, benchmark_version) VALUES
    ('gpt-4o', 0.87, 'HARMFUL_ILLEGAL_DRUGS', 'Jailbreak', 'en', FALSE, '1.0'),
    ('gpt-4o', 0.99, 'HARMFUL_VIOLENT_CRIME', 'Jailbreak', 'en', FALSE, '1.0'),
    ('mistral', 0.79, 'SOME_DEEP_EVAL_CAT_1', 'Encoding', 'en', FALSE, '1.0'),
    ('mistral', 0.71, 'SOME_DEEP_EVAL_CAT_2', 'Suffix', 'en', FALSE, '1.0'),
    ('gemini', 0.94, 'SOME_DEEP_EVAL_CAT_3', 'Injection', 'en', FALSE, '1.0'),
    ('gemini', 0.91, 'SOME_DEEP_EVAL_CAT_4', 'Injection', 'en', TRUE, '1.0');

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL
);