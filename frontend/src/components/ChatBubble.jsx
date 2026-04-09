import { formatMessage } from '../utils/formatMessage';

const WASTE_ICONS = {
  Plastic: '♻️',
  Organic: '🌿',
  'E-Waste': '💻',
  Hazardous: '⚠️',
  Unknown: '❓',
};

export default function ChatBubble({ message }) {
  const isUser = message.role === 'user';

  return (
    <div className={`flex items-end gap-3 animate-slide-up ${isUser ? 'justify-end' : 'justify-start'}`}>
      {/* Bot avatar */}
      {!isUser && (
        <div className="w-8 h-8 rounded-full bg-emerald-500 flex items-center justify-center text-sm flex-shrink-0 mb-1">
          ♻️
        </div>
      )}

      <div
        className={`max-w-[75%] px-4 py-3 rounded-2xl text-sm leading-relaxed shadow-lg ${
          isUser
            ? 'bg-emerald-600 text-white rounded-br-sm'
            : 'bg-slate-800 text-slate-100 rounded-bl-sm border border-slate-700'
        }`}
      >
        <div
          dangerouslySetInnerHTML={{ __html: formatMessage(message.content) }}
        />
      </div>

      {/* User avatar */}
      {isUser && (
        <div className="w-8 h-8 rounded-full bg-slate-600 flex items-center justify-center text-sm flex-shrink-0 mb-1">
          👤
        </div>
      )}
    </div>
  );
}
