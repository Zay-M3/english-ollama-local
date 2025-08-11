
interface Card {
    title? : string,
    text? : string,
    color? : string,
    two_color? :string,
}

export function Card ({title, text, color, two_color} : Card) {
  return (
    <div className={`border rounded-xl p-4 bg-gradient-to-br  from${color}-500/10 to-${two_color}-500/10`}>
        <p className="text-xs font-semibold mb-1 text-slate-700">{title}</p>
        <p className="text-[11px] leading-relaxed">{text}</p>
    </div>
  )
}

