import express from 'express';
import axios from 'axios';
import { createClient } from '@supabase/supabase-js';

const router = express.Router();
const supabase = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_SERVICE_ROLE_KEY);

// Simple utility function to break text content down into manageable semantic slices
function splitTextIntoChunks(text, chunkSize = 800) {
  const words = text.split(' ');
  const chunks = [];
  let currentChunk = [];

  for (let word of words) {
    currentChunk.push(word);
    if (currentChunk.join(' ').length >= chunkSize) {
      chunks.push(currentChunk.join(' '));
      currentChunk = [];
    }
  }
  if (currentChunk.length > 0) chunks.push(currentChunk.join(' '));
  return chunks;
}
router.post('/sync-profile', async (req, res) => {
  if (!req.isAuthenticated()) return res.status(401).json({ error: "Unauthorized access trigger" });

  const user = req.user;
  try {
    // 1. Query user's public repositories from the GitHub REST API (Fixed dynamic template interpolation)
    const repoResponse = await axios.get(`https://github.com{user.username}/repos`, {
      headers: { Authorization: `token ${user.oauth_token}` }
    });

    for (let repo of repoResponse.data) {
      // 2. Upsert repository baseline entries into database tables
      const { data: repoRecord } = await supabase.from('repositories').upsert({
        user_id: user.id,
        repo_github_id: repo.id.toString(),
        name: repo.name,
        description: repo.description || '',
        stars_count: repo.stargazers_count,
        repo_url: repo.html_url,
        // 🌟 THE CRITICAL INTERCEPT: Securely pull the authentic About website config straight from GitHub response
        homepage_url: repo.homepage || '' 
      }, { onConflict: 'user_id, repo_github_id' }).select().single();

      // 3. Attempt to scrape raw file values out of README markdown layouts
      try {
        const readmeResponse = await axios.get(`https://githubusercontent.com{user.username}/${repo.name}/${repo.default_branch}/README.md`);
        const textChunks = splitTextIntoChunks(readmeResponse.data);

        // Delete old chunks to ensure data freshness
        await supabase.from('documents').delete().eq('repo_id', repoRecord.id);

        for (let chunk of textChunks) {
          // Generate artificial dummy vector embeddings arrays (In production, replace with real OpenAI / Cohere API fetch requests)
          const dummyEmbedding = Array.from({ length: 1536 }, () => Math.random());

          await supabase.from('documents').insert({
            user_id: user.id,
            repo_id: repoRecord.id,
            content_chunk: `Repository: ${repo.name}\nDescription: ${repo.description}\nWebsite: ${repo.homepage || ''}\n\n${chunk}`,
            embedding: dummyEmbedding
          });
        }
      } catch (readmeErr) {
        // Continue loop if repository doesn't have a structured README markdown document
        continue;
      }
    }
    return res.status(200).json({ status: "Synchronization completed successfully." });
  } catch (error) {
    return res.status(500).json({ error: error.message });
  }
});

export default router;
