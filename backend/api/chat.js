import fs from 'fs';
import { GoogleGenAI } from '@google/genai';
import { createClient } from '@supabase/supabase-js';

// Read incoming payload matrix from Streamlit's stdin pipe wrapper
const inputPayload = fs.readFileSync(0, 'utf-8');

async function processChatPipeline() {
  try {
    const { username, prompt, apiKey, systemInstruction, vaultContext } = JSON.parse(inputPayload);

    // Initialize Supabase Contextual Memory
    const supabaseUrl = process.env.SUPABASE_URL || "";
    const supabaseKey = process.env.SUPABASE_SERVICE_ROLE_KEY || "";
    let contextString = "";

    if (supabaseUrl && supabaseKey) {
      const supabase = createClient(supabaseUrl, supabaseKey);
      const mockQueryEmbedding = Array.from({ length: 1536 }, () => Math.random());
      const targetUserId = parseInt(username) || 0;

      const { data: matchedContext, error } = await supabase.rpc('match_user_documents', {
        query_embedding: mockQueryEmbedding,
        match_threshold: 0.60,
        match_count: 3,
        filter_user_id: targetUserId
      });

      if (!error && matchedContext) {
        contextString = matchedContext.map(doc => doc.content_chunk).join("\n\n");
      }
    }

    // Fall back to Streamlit memory buffer if database vectors are empty
    const finalContext = contextString || vaultContext || "No custom repository documentation indexed.";

    // 🎯 THE GOOGLE GENAI LIVE PROCESS PIPELINE:
    // Initializes the official SDK using the key you provided in the UI input box
    const ai = new GoogleGenAI({ apiKey: apiKey });
    
    // Execute a live chat completion query targeting the fast Gemini Flash model
    const aiResponse = await ai.models.generateContent({
      model: 'gemini-2.5-flash',
      contents: [
        { role: 'user', parts: [{ text: `${systemInstruction}\n\nContextual repository documentation facts:\n${finalContext}\n\nUser Question: ${prompt}` }] }
      ]
    });

    const assistantOutput = aiResponse.text || "Unable to parse streaming model generation content strings.";

    // Pipe text back up to Streamlit's chatbot_router.py stdout listener
    process.stdout.write(assistantOutput);
    process.exit(0);

  } catch (err) {
    process.stderr.write(`Node.js Process Pipeline Fault: ${err.message}`);
    process.exit(1);
  }
}

processChatPipeline();
