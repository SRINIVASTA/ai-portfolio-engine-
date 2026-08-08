-- Enable the vector extension for AI similarity lookups
CREATE EXTENSION IF NOT EXISTS vector;

-- Users Table: Core tenant profiles
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    github_id VARCHAR(50) UNIQUE NOT NULL,
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(255),
    avatar_url TEXT,
    oauth_token TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Repositories Table: Metadata for tracked developer apps
CREATE TABLE IF NOT EXISTS repositories (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    repo_github_id VARCHAR(50) NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    stars_count INT DEFAULT 0,
    repo_url TEXT NOT NULL,
    UNIQUE(user_id, repo_github_id)
);

-- Documents Table: Split text chunks and high-dimensional vector embeddings
CREATE TABLE IF NOT EXISTS documents (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    repo_id INT REFERENCES repositories(id) ON DELETE CASCADE,
    content_chunk TEXT NOT NULL,
    embedding VECTOR(1536), -- 1536 matches standard OpenAI / Cohere models
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Generate spatial HNSW index for ultra-fast matching speeds
CREATE INDEX ON documents USING hnsw (embedding vector_cosine_ops);

-- Stored Procedure: Executes isolated RAG vector searches scoped by user ID
CREATE OR REPLACE FUNCTION match_user_documents (
  query_embedding VECTOR(1536),
  match_threshold FLOAT,
  match_count INT,
  filter_user_id INT
)
RETURNS TABLE (
  id INT,
  content_chunk TEXT,
  similarity FLOAT
)
LANGUAGE plpgsql AS $$
BEGIN
  RETURN QUERY
  SELECT
    documents.id,
    documents.content_chunk,
    1 - (documents.embedding <=> query_embedding) AS similarity
  FROM documents
  WHERE documents.user_id = filter_user_id
    AND 1 - (documents.embedding <=> query_embedding) > match_threshold
  ORDER BY documents.embedding <=> query_embedding
  LIMIT match_count;
END;
$$;
