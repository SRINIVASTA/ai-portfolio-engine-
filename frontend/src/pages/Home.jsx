import React from 'react';

export default function Home() {
  const handleLogin = () => {
    window.location.href = 'http://localhost:3000/auth/github';
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', height: '100vh', fontFamily: 'sans-serif', backgroundColor: '#0f172a', color: '#fff' }}>
      <h1 style={{ fontSize: '3rem', marginBottom: '1rem' }}>Turn Your GitHub Into An AI Portfolio</h1>
      <p style={{ color: '#94a3b8', marginBottom: '2rem', fontSize: '1.2rem' }}>Deploy a self-updating website with an interactive recruiter chatbot trained entirely on your code repositories.</p>
      <button onClick={handleLogin} style={{ padding: '1rem 2rem', fontSize: '1.1rem', backgroundColor: '#2563eb', color: '#fff', border: 'none', borderRadius: '8px', cursor: 'pointer', fontWeight: 'bold' }}>
        Sign In with GitHub
      </button>
    </div>
  );
}
