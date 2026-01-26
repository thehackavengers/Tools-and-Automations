CREATE TABLE IF NOT EXISTS adverse_media (
    ARN TEXT PRIMARY KEY,
    date DATE,
    title TEXT,
    article TEXT,
    domain TEXT,
    url TEXT,
    lea TEXT,
    crimes TEXT,
    person TEXT,
    locations TEXT,
    quantum TEXT,
    keywords TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
