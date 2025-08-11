
const colorVariants = {
  blue: 'from-blue-500/10 to-indigo-500/10',
  green: 'from-green-500/10 to-indigo-500/10',
  yellow: 'from-yellow-400/10 to-orange-400/10',
  pink: 'from-pink-400/10 to-purple-400/10',
  gray: 'from-slate-200/60 to-slate-300/40',
};

interface CardProps {
  title?: string;
  text?: string;
  color?: keyof typeof colorVariants;
}

export function Card({ title, text, color = 'blue' }: CardProps) {
  const gradient = colorVariants[color] || colorVariants.blue;
  return (
    <div className={`border rounded-xl p-4 bg-gradient-to-br ${gradient}`}>
      <p className="text-xs font-semibold mb-1 text-slate-700">{title}</p>
      <p className="text-[11px] leading-relaxed">{text}</p>
    </div>
  );
}

