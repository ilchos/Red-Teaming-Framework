CREATE TABLE leaderboard_competitors (
    model_name TEXT NOT NULL,
    total INTEGER NOT NULL,
    passed INTEGER NOT NULL,
    hit_rate DOUBLE PRECISION NOT NULL,
    low_level_category TEXT NOT NULL,
    mid_level_category TEXT NOT NULL,
    high_level_category TEXT NOT NULL,
    manually_tested boolean NOT NULL
);
INSERT INTO leaderboard_competitors 
(model_name, total, passed, hit_rate, manually_tested, high_level_category, mid_level_category, low_level_category) VALUES
    ('gpt-4o', 10, 7, 0.7, FALSE, 'Injection', 'DeepEval_cat_1', 'garak_cat_1'),
    ('gpt-4o', 10, 7, 0.7, FALSE, 'Injection', 'DeepEval_cat_1', 'garak_cat_2'),
    ('mistral', 10, 7, 0.7, FALSE, 'Injection', 'DeepEval_cat_2', 'garak_cat_2'),
    ('gpt-4o', 10, 7, 0.7, FALSE, 'Injection', 'DeepEval_cat_1', 'garak_cat_2'),
    ('mistral', 10, 5, 0.5, FALSE, 'Encoding', 'DeepEval_cat_2', 'garak_cat_2'),
    ('gemini', 10, 9, 0.9, FALSE, 'Adversarial Suffix', 'DeepEval_cat_3', 'garak_cat_10'),
    ('gpt-3.5', 10, 9, 0.9, TRUE, 'Jailbrake', 'DeepEval_cat_15', 'garak_cat_21');