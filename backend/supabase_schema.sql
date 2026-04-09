-- ============================================================
-- Supabase Schema — Waste Classification Assistant
-- Run these in the Supabase SQL editor
-- ============================================================

-- 1. Users table
CREATE TABLE IF NOT EXISTS users (
  id          BIGSERIAL PRIMARY KEY,
  session_id  TEXT UNIQUE NOT NULL,
  name        TEXT,
  age         TEXT,
  created_at  TIMESTAMPTZ DEFAULT NOW()
);

-- 2. Waste queries table
CREATE TABLE IF NOT EXISTS waste_queries (
  id               BIGSERIAL PRIMARY KEY,
  session_id       TEXT REFERENCES users(session_id) ON DELETE CASCADE,
  waste_item       TEXT NOT NULL,
  waste_type       TEXT NOT NULL,
  disposal_method  TEXT,
  timestamp        TIMESTAMPTZ DEFAULT NOW()
);

-- 3. Rewards table
CREATE TABLE IF NOT EXISTS rewards (
  id          BIGSERIAL PRIMARY KEY,
  session_id  TEXT REFERENCES users(session_id) ON DELETE CASCADE,
  points      INT DEFAULT 0,
  updated_at  TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(session_id)
);

-- ── Optional: enable Row Level Security ──
ALTER TABLE users         ENABLE ROW LEVEL SECURITY;
ALTER TABLE waste_queries ENABLE ROW LEVEL SECURITY;
ALTER TABLE rewards       ENABLE ROW LEVEL SECURITY;

-- Allow anon read/write for demo purposes (tighten in production)
CREATE POLICY "allow_all" ON users         FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "allow_all" ON waste_queries FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "allow_all" ON rewards       FOR ALL USING (true) WITH CHECK (true);
