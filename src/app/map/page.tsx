'use client'
const GNI_KEY = process.env.NEXT_PUBLIC_GNI_API_KEY || ''

import { useEffect, useState } from 'react'
import dynamic from 'next/dynamic'

const MapView = dynamic(() => import('@/components/MapView'), { ssr: false })

interface ArticleEvent {
  id: string
  source: string
  bias: string
  title: string
  url: string
  summary: string
  stage3_score: number
  stage4_rank: number
  location_name: string
  lat: number
  lng: number
  created_at: string
}

export default function MapPage() {
  const [events, setEvents] = useState<ArticleEvent[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [daysFilter, setDaysFilter] = useState(7)

  useEffect(() => {
    fetch(`/api/article-events?days=${daysFilter}`, { headers: { 'X-GNI-Key': GNI_KEY } })
      .then(r => r.json())
      .then(data => setEvents(data.events || []))
      .catch(() => setError('Failed to load map data.'))
      .finally(() => setLoading(false))
  }, [daysFilter])

  return (
    <div className="min-h-screen bg-gray-950 text-gray-100">
      <header className="border-b border-gray-800 bg-gray-900">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <a href="/" className="inline-flex items-center gap-1.5 bg-blue-900 hover:bg-blue-700 border border-blue-700 text-blue-200 rounded-lg px-3 py-1.5 text-xs font-bold transition-colors shrink-0">← Quantum Strategist</a>
          <div className="flex items-center justify-between mt-2">
          <div>
            <h1 className="text-2xl font-bold text-white">🌍 Geopolitical Event Map</h1>
            <p className="text-sm text-gray-400">The Geopolitical Event Map plots every news article GNI has collected onto a world map, with each pin colored by sentiment — red for bearish, yellow for neutral, green for bullish. Click any pin to read the article summary and source link directly. Use the time filter to see how geopolitical hotspots have shifted over the last 1, 3, 7, or 14 days.</p>
          </div>
          <div className="flex items-center gap-4">
            {/* Days filter */}
            <div className="flex gap-2">
              {[1, 3, 7, 14].map(d => (
                <button
                  key={d}
                  onClick={() => setDaysFilter(d)}
                  className={`text-xs px-3 py-1.5 rounded-lg transition-colors ${
                    daysFilter === d
                      ? 'bg-blue-600 text-white'
                      : 'bg-gray-800 text-gray-400 hover:bg-gray-700'
                  }`}
                >
                  {d}d
                </button>
              ))}
            </div>
            
          </div>
</div>
          </div>
      </header>

      {/* Legend */}
      <div className="bg-gray-900 border-b border-gray-800 px-6 py-2 flex gap-6 text-xs text-gray-400">
        <span className="flex items-center gap-1.5">
          <span className="w-3 h-3 rounded-full bg-red-600 inline-block"></span>
          Bearish / High Risk
        </span>
        <span className="flex items-center gap-1.5">
          <span className="w-3 h-3 rounded-full bg-yellow-500 inline-block"></span>
          Neutral / Medium Risk
        </span>
        <span className="flex items-center gap-1.5">
          <span className="w-3 h-3 rounded-full bg-green-500 inline-block"></span>
          Bullish / Low Risk
        </span>
        <span className="text-gray-600">📰 = news article | Click pin for details + source link</span>
      </div>

      {loading && (
        <div className="flex items-center justify-center h-96 text-gray-400">
          <p>Loading events...</p>
        </div>
      )}


        {error && (
          <div className="text-center py-20 text-red-400">
            <div className="text-4xl mb-4">&#9888;&#65039;</div>
            <p>{error}</p>
          </div>
        )}
      {!loading && (
        <MapView events={events} height="calc(100vh - 200px)" />
      )}

      
      {/* DISCLAIMER */}
      <div className="max-w-6xl mx-auto px-6 pb-4">
        <div className="bg-yellow-950 border border-yellow-800 rounded-xl p-3">
          <p className="text-xs text-yellow-300">
            ⚠️ Warning: GNI reports are for informational purposes only and do not constitute financial advice. Always conduct your own research before making investment decisions.
          </p>
        </div>
      </div>
      <footer className="border-t border-gray-800">
        <div className="max-w-7xl mx-auto px-6 py-3 text-center text-xs text-gray-600">
          GNI Autonomous | Geopolitical Event Map | Higher Diploma in Computer Science | Spring University Myanmar (SUM)
        </div>
      </footer>
    </div>
  )
}