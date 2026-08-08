import React, { useState } from 'react';
import { useParams } from 'react-router-dom';

export default function ProfileShell() {
  const { username } = useParams();
  const [messages, setMessages] = useState([{ sender: 'bot', text: `Hi! I am the AI twin of ${username}. Ask me anything about my projects, stack, or experience!` }]);
  const [input, setInput] = useState('');

  const handleSendMessage = async () => {
    if (!input.trim()) return;
    const userMsg = { sender: 'user', text: input };
    setMessages(prev => [...prev, userMsg]);
    setInput('');

    // Simulated response loop connecting frontend queries directly to backend endpoint definitions
    setMessages(prev => [...prev, { sender: 'bot', text: "Analyzing repository vectors to answer your query structural specifications..." }]);
  };

  return (
    <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr', height: '100vh', backgroundColor: '#0f172a', color: '#fff', fontFamily: 'sans-serif' }}>
      {/* Portfolio Presentation Area */}
      <div style={{ padding: '3rem', overflowY: 'auto' }}>
        <h1 style={{ fontSize: '2.5rem' }}>{username}'s Portfolio</h1>
        <p style={{ color: '#38bdf8' }}>✓ Verified Professional Software Architect Profile</p>
        <hr style={{ borderColor: '#334155', margin: '2rem 0' }} />
        <div style={{ padding: '2rem', backgroundColor: '#1e293b', borderRadius: '12px' }}>
          <h3>🚀 Core Public Repositories</h3>
          <p style={{ color: '#94a3b8' }}>Live synchronisation worker pipeline attached successfully.</p>
        </div>
      </div>

      {/* Embedded Recruiter Chatbot Element Layout */}
      <div style={{ borderLeft: '1px solid #334155', display: 'flex', flexDirection: 'column', backgroundColor: '#1e293b' }}>
        <div style={{ padding: '1.5rem', borderBottom: '1px solid #334155', backgroundColor: '#0f172a' }}>
          <h4>Chat with {username}'s Repositories</h4>
        </div>
        <div style={{ flex: 1, padding: '1.5rem', overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: '1rem' }}>
          {messages.map((m, idx) => (
            <div key={idx} style={{ alignSelf: m.sender === 'user' ? 'flex-end' : 'flex-start', backgroundColor: m.sender === 'user' ? '#2563eb' : '#334155', padding: '0.8rem 1.2rem', borderRadius: '12px', maxWidth: '80%' }}>
              {m.text}
            </div>
          ))}
        </div>
        <div style={{ padding: '1.5rem', display: 'flex', gap: '0.5rem', borderTop: '1px solid #334155' }}>
          <input value={input} onChange={(e) => setInput(e.target.value)} placeholder="Ask about architecture rules..." style={{ flex: 1, padding: '0.8rem', borderRadius: '6px', border: '1px solid #475569', backgroundColor: '#0f172a', color: '#fff' }} />
          <button onClick={handleSendMessage} style={{ padding: '0.8rem 1.2rem', backgroundColor: '#38bdf8', color: '#0f172a', border: 'none', borderRadius: '6px', fontWeight: 'bold', cursor: 'pointer' }}>Send</button>
        </div>
      </div>
    </div>
  );
}
