import { useEffect, useRef } from 'react';
import ChatBubble from '../components/ChatBubble';
import ChatInput from '../components/ChatInput';
import WasteSummaryCard from '../components/WasteSummaryCard';
import EcoRewardBadge from '../components/EcoRewardBadge';
import TypingIndicator from '../components/TypingIndicator';
import { useChat } from '../hooks/useChat';

export default function ChatPage() {
  const { messages, loading, wasteSummary, rewardPoints, send, reset, startChat } = useChat();
  const bottomRef = useRef(null);

  useEffect(() => {
    startChat();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, loading]);

  return (
    <div className="flex flex-col h-screen bg-slate-900">
      {/* ── Header ── */}
      <header className="flex items-center justify-between px-5 py-4 bg-slate-900 border-b border-slate-800 flex-shrink-0">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-emerald-600 flex items-center justify-center text-xl shadow-lg">
            ♻️
          </div>
          <div>
            <h1 className="text-white font-bold text-base leading-tight">Waste Wise</h1>
            <p className="text-emerald-400 text-xs">Smart Disposal Assistant · SDG 12</p>
          </div>
        </div>

        <div className="flex items-center gap-3">
          <EcoRewardBadge points={rewardPoints} />
          <button
            onClick={reset}
            className="p-2 rounded-xl text-slate-400 hover:text-white hover:bg-slate-700 transition-colors"
            title="Start new conversation"
          >
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
                d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
          </button>
        </div>
      </header>

      {/* ── Body: chat + sidebar ── */}
      <div className="flex flex-1 overflow-hidden">
        {/* Chat area */}
        <main className="flex-1 flex flex-col overflow-hidden">
          <div className="flex-1 overflow-y-auto px-4 py-5 space-y-4">
            {messages.length === 0 && !loading && (
              <div className="flex flex-col items-center justify-center h-full text-center space-y-4 py-16">
                <div className="text-6xl animate-bounce">♻️</div>
                <h2 className="text-2xl font-bold text-white">Waste Wise Assistant</h2>
                <p className="text-slate-400 max-w-sm text-sm">
                  Your AI-powered guide to responsible waste disposal — tailored for Indian households. 🇮🇳
                </p>
                <div className="flex flex-wrap justify-center gap-2 mt-4">
                  {['🌿 Organic', '♻️ Plastic', '💻 E-Waste', '⚠️ Hazardous'].map(tag => (
                    <span key={tag} className="px-3 py-1.5 bg-slate-800 border border-slate-700 rounded-full text-sm text-slate-300">
                      {tag}
                    </span>
                  ))}
                </div>
              </div>
            )}

            {messages.map(msg => (
              <ChatBubble key={msg.id} message={msg} />
            ))}

            {loading && <TypingIndicator />}

            <div ref={bottomRef} />
          </div>

          {/* Input */}
          <div className="px-4 pb-4 pt-2 border-t border-slate-800 flex-shrink-0">
            <ChatInput onSend={send} loading={loading} />
          </div>
        </main>

        {/* Sidebar: waste summary */}
        {wasteSummary && (
          <aside className="w-80 flex-shrink-0 overflow-y-auto border-l border-slate-800 p-4 bg-slate-900 space-y-4 hidden lg:block">
            <h2 className="text-sm font-semibold text-slate-400 uppercase tracking-widest">
              Last Classification
            </h2>
            <WasteSummaryCard summary={wasteSummary} />

            {/* SDG Info */}
            <div className="rounded-xl bg-slate-800 border border-slate-700 p-4 space-y-2">
              <p className="text-xs font-bold text-emerald-400 uppercase tracking-widest">SDG 12</p>
              <p className="text-slate-300 text-xs leading-relaxed">
                Responsible Consumption and Production — By segregating waste correctly, you contribute to a circular economy and reduce landfill pollution across India.
              </p>
              <div className="flex flex-wrap gap-2 pt-1">
                <span className="text-[11px] px-2 py-0.5 bg-emerald-900/50 text-emerald-400 rounded-full border border-emerald-800">♻️ Zero Waste</span>
                <span className="text-[11px] px-2 py-0.5 bg-blue-900/50 text-blue-400 rounded-full border border-blue-800">🌊 Clean India</span>
              </div>
            </div>
          </aside>
        )}
      </div>

      {/* Mobile: waste summary below chat */}
      {wasteSummary && (
        <div className="lg:hidden px-4 pb-4 border-t border-slate-800 pt-4">
          <WasteSummaryCard summary={wasteSummary} />
        </div>
      )}
    </div>
  );
}
