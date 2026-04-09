const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

/**
 * Send a chat message to the backend.
 * @param {string} message
 * @param {string|null} sessionId
 * @returns {Promise<{reply, session_id, waste_summary, stage}>}
 */
export async function sendMessage(message, sessionId = null) {
  const res = await fetch(`${BASE_URL}/api/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message, session_id: sessionId }),
  });
  if (!res.ok) throw new Error(`Server error: ${res.status}`);
  return res.json();
}

/**
 * Send a chat message with an image file.
 */
export async function sendMessageWithImage(message, imageFile, sessionId = null) {
  const form = new FormData();
  form.append('message', message || '');
  form.append('file', imageFile);
  if (sessionId) form.append('session_id', sessionId);

  const res = await fetch(`${BASE_URL}/api/chat/image`, {
    method: 'POST',
    body: form,
  });
  if (!res.ok) throw new Error(`Server error: ${res.status}`);
  return res.json();
}

/**
 * Reset / delete session.
 */
export async function resetSession(sessionId) {
  const res = await fetch(`${BASE_URL}/api/session/${sessionId}`, {
    method: 'DELETE',
  });
  return res.json();
}
