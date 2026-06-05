 CREATE TABLE IF NOT EXISTS users (
  user_id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password_hash TEXT NOT NULL,
  has_voted BOOLEAN NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS candidates (
  candidate_id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  votes_count INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS votes (
  vote_id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  candidate_id INTEGER NOT NULL,
  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(user_id),
  FOREIGN KEY (candidate_id) REFERENCES candidates(candidate_id)
);

-- Insert default candidates
INSERT INTO candidates (name, votes_count) VALUES ('Red', 0), ('Blue', 0), ('Green', 0);

