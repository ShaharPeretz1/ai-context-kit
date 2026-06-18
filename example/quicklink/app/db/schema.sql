-- quicklink schema. One store for links + click events (see decisions.md Decision 002).

CREATE TABLE IF NOT EXISTS links (
    slug        TEXT PRIMARY KEY,
    url         TEXT NOT NULL,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS click_events (
    id          BIGSERIAL PRIMARY KEY,
    slug        TEXT NOT NULL REFERENCES links(slug),
    clicked_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_click_events_slug ON click_events(slug);
