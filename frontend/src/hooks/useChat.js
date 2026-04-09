import { useState, useCallback } from 'react';
import { sendMessage, sendMessageWithImage, resetSession } from '../utils/api';

export function useChat() {
  const [messages, setMessages] = useState([]);
  const [sessionId, setSessionId] = useState(null);
  const [loading, setLoading] = useState(false);
  const [wasteSummary, setWasteSummary] = useState(null);
  const [rewardPoints, setRewardPoints] = useState(0);
  const [stage, setStage] = useState('greeting');
  const [error, setError] = useState(null);

  const addMessage = (role, content) => {
    setMessages(prev => [...prev, { role, content, id: Date.now() + Math.random() }]);
  };

  const send = useCallback(async (text, imageFile = null) => {
    if (!text.trim() && !imageFile) return;
    setError(null);
    addMessage('user', text || '📷 Image uploaded');
    setLoading(true);

    try {
      let data;
      if (imageFile) {
        data = await sendMessageWithImage(text, imageFile, sessionId);
      } else {
        data = await sendMessage(text, sessionId);
      }

      setSessionId(data.session_id);
      setStage(data.stage);
      addMessage('assistant', data.reply);

      if (data.waste_summary) {
        setWasteSummary(data.waste_summary);
        setRewardPoints(prev => prev + (data.waste_summary.reward_points || 0));
      }
    } catch (err) {
      setError('Could not reach the server. Please make sure the backend is running.');
      addMessage('assistant', '⚠️ Sorry, I could not connect to the server. Please try again.');
    } finally {
      setLoading(false);
    }
  }, [sessionId]);

  const reset = useCallback(async () => {
    if (sessionId) await resetSession(sessionId).catch(() => {});
    setMessages([]);
    setSessionId(null);
    setWasteSummary(null);
    setStage('greeting');
    setError(null);
  }, [sessionId]);

  // Kick off greeting on first load
  const startChat = useCallback(async () => {
    setLoading(true);
    try {
      const data = await sendMessage('', null);
      setSessionId(data.session_id);
      setStage(data.stage);
      addMessage('assistant', data.reply);
    } catch {
      addMessage('assistant', '🌿 Namaste! Welcome to the Waste Classification Assistant. Please start the backend server and refresh.');
    } finally {
      setLoading(false);
    }
  }, []);

  return { messages, loading, wasteSummary, rewardPoints, stage, error, send, reset, startChat };
}
