export default function EcoRewardBadge({ points }) {
  const level =
    points >= 100 ? { label: 'Eco Champion', color: 'text-yellow-400', icon: '🏆' }
    : points >= 50  ? { label: 'Green Hero',    color: 'text-emerald-400', icon: '🌿' }
    : points >= 20  ? { label: 'Eco Starter',   color: 'text-blue-400',   icon: '♻️' }
    :                 { label: 'Beginner',       color: 'text-slate-400',  icon: '🌱' };

  return (
    <div className="flex items-center gap-2 bg-slate-800 border border-slate-700 rounded-xl px-4 py-2">
      <span className="text-xl">{level.icon}</span>
      <div>
        <p className="text-[10px] uppercase tracking-widest text-slate-500">Eco Score</p>
        <p className={`text-base font-bold ${level.color}`}>{points} pts</p>
      </div>
      <div className="ml-2 border-l border-slate-700 pl-2">
        <p className={`text-xs font-semibold ${level.color}`}>{level.label}</p>
      </div>
    </div>
  );
}
