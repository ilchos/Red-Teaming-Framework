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
-- INSERT INTO leaderboard_competitors 
-- (id, agent_name, score, vul_deepeval, type_general, lang, manually_tested, benchmark_version, reason) VALUES
--     (1.0, 'gpt-4o', 0.81, 'HARMFUL_ILLEGAL_DRUGS', 'Jailbreak', 'en', FALSE, '1.0', 'reason'),
--     (2.0, 'gpt-4o', 0.82, 'HARMFUL_VIOLENT_CRIME', 'Jailbreak', 'en', FALSE, '1.0', 'reason'),
--     (1.0, 'mistral', 0.83, 'HARMFUL_ILLEGAL_DRUGS', 'Jailbreak', 'en', FALSE, '1.0', 'reason'),
--     (1.0, 'mistral', 0.84, 'HARMFUL_VIOLENT_CRIME', 'Jailbreak', 'en', FALSE, '1.0', 'reason'),
--     (1.0, 'gemini', 0.85, 'HARMFUL_ILLEGAL_DRUGS', 'Jailbreak', 'en', FALSE, '1.0', 'reason'),
--     (1.0, 'gemini', 0.86, 'HARMFUL_VIOLENT_CRIME', 'Jailbreak', 'en', TRUE, '1.0', 'reason'),
--     (1.0, 'gpt-4o', 0.87, 'HARMFUL_ILLEGAL_DRUGS', 'Encoding', 'en', FALSE, '1.0', 'reason'),
--     (1.0, 'gpt-4o', 0.88, 'HARMFUL_VIOLENT_CRIME', 'Encoding', 'en', FALSE, '1.0', 'reason'),
--     (1.0, 'mistral', 0.89, 'HARMFUL_ILLEGAL_DRUGS', 'Encoding', 'en', FALSE, '1.0', 'reason'),
--     (1.0, 'mistral', 0.9, 'HARMFUL_VIOLENT_CRIME', 'Encoding', 'en', FALSE, '1.0', 'reason'),
--     (1.0, 'gemini', 0.91, 'HARMFUL_ILLEGAL_DRUGS', 'Encoding', 'en', FALSE, '1.0', 'reason'),
--     (1.0, 'gemini', 0.92, 'HARMFUL_VIOLENT_CRIME', 'Encoding', 'en', TRUE, '1.0', 'reason');

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL
);