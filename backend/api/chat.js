import express from 'express';
import { createClient } from '@supabase/supabase-js';

const router = express.Router();
const supabase = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_SERVICE_ROLE_KEY);

router.post('/query-chatbot', async (req, res) => {
  const { targetUserId, messageText } = req.body;

  try {
    // Generate match embedding space tracking array (In production, parse messageText using text-embedding-3-small)
    const mockQueryEmbedding = Array.from({ length: 1536 }, () => Math.random());

    // Execute isolation search function bypassing risk of overlapping tenant contexts
    const { data: matchedContext, error } = await supabase.rpc('match_user_documents', {
      query_embedding: mockQueryEmbedding,
      match_threshold: 0.60,
      match_count: 3,
      filter_user_id: parseInt(targetUserId)
    });

    if (error) throw error;

    const contextContextString = matchedContext.map(doc => doc.content_chunk).join("\n\n");
    
    // Send background facts back up to the frontend UI layer
    return res.status(200).json({ 
      context: contextContextString,
      systemPromptHint: `Answer the user prompt truthfully using only the facts here:\n${contextContextString}`
    });

  } catch (err) {
    return res.status(500).json({ error: "Failed to evaluate semantic database vectors." });
  }
});

export default router;
