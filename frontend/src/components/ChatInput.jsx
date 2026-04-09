import { useState, useRef, useEffect } from 'react';
import ImageUpload from './ImageUpload';

export default function ChatInput({ onSend, loading, disabled }) {
  const [text, setText] = useState('');
  const [imageFile, setImageFile] = useState(null);
  const textareaRef = useRef(null);

  // Auto-grow textarea
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = `${Math.min(textareaRef.current.scrollHeight, 140)}px`;
    }
  }, [text]);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (loading || disabled) return;
    if (!text.trim() && !imageFile) return;
    onSend(text.trim(), imageFile);
    setText('');
    setImageFile(null);
  };

  const handleKey = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  const SUGGESTIONS = ['plastic bottle', 'banana peel', 'old phone', 'dead battery', 'newspaper'];

  return (
    <div className="space-y-2">
      {/* Quick suggestion chips */}
      <div className="flex flex-wrap gap-2 px-1">
        {SUGGESTIONS.map(s => (
          <button
            key={s}
            type="button"
            disabled={loading}
            onClick={() => onSend(s, null)}
            className="text-xs px-3 py-1 rounded-full bg-slate-800 border border-slate-700 text-slate-400 hover:border-emerald-500 hover:text-emerald-400 transition-colors disabled:opacity-40"
          >
            {s}
          </button>
        ))}
      </div>

      {/* Input bar */}
      <form
        onSubmit={handleSubmit}
        className="flex items-end gap-2 bg-slate-800 border border-slate-700 rounded-2xl px-3 py-2 focus-within:border-emerald-500 transition-colors"
      >
        <ImageUpload onFileSelect={setImageFile} disabled={loading} />

        <textarea
          ref={textareaRef}
          rows={1}
          value={text}
          onChange={e => setText(e.target.value)}
          onKeyDown={handleKey}
          disabled={loading || disabled}
          placeholder="Type waste item (e.g. plastic bottle)…"
          className="flex-1 bg-transparent text-slate-100 placeholder-slate-500 text-sm resize-none outline-none py-1 max-h-36 disabled:opacity-50"
        />

        <button
          type="submit"
          disabled={loading || (!text.trim() && !imageFile)}
          className="p-2 rounded-xl bg-emerald-600 hover:bg-emerald-500 disabled:opacity-40 disabled:cursor-not-allowed text-white transition-colors flex-shrink-0"
        >
          {loading ? (
            <svg className="animate-spin h-4 w-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z" />
            </svg>
          ) : (
            <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
            </svg>
          )}
        </button>
      </form>
      <p className="text-[11px] text-slate-600 text-center">
        Press Enter to send · Shift+Enter for new line · Or upload a waste image
      </p>
    </div>
  );
}
