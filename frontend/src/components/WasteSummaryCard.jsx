const CATEGORY_CONFIG = {
  Plastic:   { emoji: '♻️', bg: 'bg-blue-900/40',   border: 'border-blue-500',   badge: 'bg-blue-500',   text: 'text-blue-300' },
  Organic:   { emoji: '🌿', bg: 'bg-green-900/40',  border: 'border-green-500',  badge: 'bg-green-500',  text: 'text-green-300' },
  'E-Waste': { emoji: '💻', bg: 'bg-amber-900/40',  border: 'border-amber-500',  badge: 'bg-amber-500',  text: 'text-amber-300' },
  Hazardous: { emoji: '⚠️', bg: 'bg-red-900/40',    border: 'border-red-500',    badge: 'bg-red-500',    text: 'text-red-300' },
  Unknown:   { emoji: '❓', bg: 'bg-slate-800/60',  border: 'border-slate-500',  badge: 'bg-slate-500',  text: 'text-slate-300' },
};

export default function WasteSummaryCard({ summary }) {
  if (!summary) return null;

  const cfg = CATEGORY_CONFIG[summary.waste_type] || CATEGORY_CONFIG.Unknown;

  return (
    <div className={`animate-fade-in rounded-2xl border ${cfg.border} ${cfg.bg} p-5 space-y-4`}>
      {/* Header */}
      <div className="flex items-center justify-between flex-wrap gap-2">
        <div className="flex items-center gap-3">
          <span className="text-3xl">{cfg.emoji}</span>
          <div>
            <p className="text-xs uppercase tracking-widest text-slate-400 font-medium">Waste Item</p>
            <h3 className="text-white font-semibold text-lg capitalize">{summary.waste_item}</h3>
          </div>
        </div>
        {/* Category badge */}
        <span className={`px-3 py-1 rounded-full text-white text-sm font-semibold ${cfg.badge}`}>
          {summary.waste_type}
        </span>
      </div>

      {/* Disposal instructions */}
      <div>
        <p className={`text-xs uppercase tracking-widest font-medium mb-2 ${cfg.text}`}>
          Disposal Instructions
        </p>
        <ol className="space-y-1.5">
          {summary.disposal_instructions.map((step, i) => (
            <li key={i} className="flex gap-2 text-sm text-slate-300">
              <span className={`font-bold ${cfg.text} flex-shrink-0`}>{i + 1}.</span>
              <span>{step}</span>
            </li>
          ))}
        </ol>
      </div>

      {/* Reward points */}
      <div className="flex items-center gap-2 pt-2 border-t border-slate-700">
        <span className="text-xl">🌟</span>
        <span className="text-sm text-slate-300">
          You earned <span className="text-emerald-400 font-bold">+{summary.reward_points} Eco Points</span> for responsible disposal!
        </span>
      </div>
    </div>
  );
}
