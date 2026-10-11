import { DirectionalSkill, PT_ALPHA, PT_CRITICAL } from '@/lib/skill'

// The reference rates and the Pesaran-Timmermann statistic shown beside every GPVS
// direction-accuracy figure (S111, R60). Computation: src/lib/skill.ts.
const pct = (x: number) => String(Math.round(x * 100)) + '%'

export default function DirectionalSkillNote({ s3, s7 }: { s3: DirectionalSkill | null; s7: DirectionalSkill | null }) {
  if (!s3 && !s7) return null
  const rows: [string, DirectionalSkill | null][] = [['3-day', s3], ['7-day', s7]]
  return (
    <div className="mt-4 bg-gray-800 rounded-lg p-3 text-xs text-gray-400 leading-relaxed">
      <span className="text-white font-bold">Skill check: </span>
      A direction call shows skill only if it beats calls made with no information about the market.
      The Pesaran-Timmermann test compares the hit rate with the rate expected if the calls and the market moves were unrelated; a value above {PT_CRITICAL} is evidence of skill at the {PT_ALPHA * 100}% level, one-sided.
      Neighbouring reports share the same market move because their windows overlap, so the test overstates the evidence.
      <div className="mt-2 space-y-1">
        {rows.map(([label, s]) => s && (
          <div key={label} className="text-gray-300">
            <span className="text-white font-bold">{label}</span>{' over '}{s.n}{' calls: right '}{pct(s.hitRate)}
            {' · unrelated calls '}{pct(s.noSkillRate)}{' · always Bullish '}{pct(s.alwaysBullishRate)}
            {' · always Bearish '}{pct(s.alwaysBearishRate)}{' · PT '}{s.pt === null ? 'undefined' : s.pt.toFixed(2)}
            {' - '}<span className={s.pt !== null && s.pt > PT_CRITICAL ? 'text-green-400' : 'text-yellow-400'}>{s.pt !== null && s.pt > PT_CRITICAL ? 'skill shown' : 'skill not shown'}</span>
          </div>
        ))}
      </div>
    </div>
  )
}
