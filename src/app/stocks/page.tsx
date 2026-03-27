'use client'

import { useEffect, useState } from 'react'
import {
  AreaChart, Area, XAxis, YAxis, Tooltip,
  ResponsiveContainer, CartesianGrid
} from 'recharts'

interface StockData {
  ticker: string
  name: string
  price: number
  change: string
  changePercent: string
  currency: string
  chartData: { date: string; close: number }[]
}

const RANGES = ['3d', '7d', '1m', '1y', '10y']

const CATEGORIES = [
  { key: 'Commodity', label: 'Commodity', emoji: '🛢️' },
  { key: 'Index',     label: 'Index',     emoji: '📊' },
  { key: 'Stocks',   label: 'Stocks',    emoji: '🏢' },
  { key: 'Forex',    label: 'Forex',     emoji: '💱' },
  { key: 'Crypto',   label: 'Crypto',    emoji: '🃏' },
  { key: 'Bond',     label: 'Bond',      emoji: '📜' },
]

const CATEGORY_TICKERS: Record<string, { ticker: string; label: string }[]> = {
  Commodity: [
    { ticker: 'CL=F',   label: 'Crude Oil' },
    { ticker: 'BZ=F',   label: 'Brent Crude' },
    { ticker: 'NG=F',   label: 'Natural Gas' },
    { ticker: 'GC=F',   label: 'Gold' },
    { ticker: 'SI=F',   label: 'Silver' },
    { ticker: 'HG=F',   label: 'Copper' },
    { ticker: 'ZS=F',   label: 'Soybeans' },
    { ticker: 'ZW=F',   label: 'Wheat' },
    { ticker: 'GLD',    label: 'Gold ETF' },
    { ticker: 'GDX',    label: 'Gold Miners' },
  ],
  Index: [
    { ticker: 'SPY',    label: 'US500 (S&P 500)' },
    { ticker: '^DJI',   label: 'US30 (Dow Jones)' },
    { ticker: '^NDX',   label: 'US100 (Nasdaq)' },
    { ticker: '^N225',  label: 'JP225 (Nikkei)' },
    { ticker: '^FTSE',  label: 'GB100 (FTSE)' },
    { ticker: '^GDAXI', label: 'DE40 (DAX)' },
    { ticker: 'FXI',    label: 'China ETF' },
    { ticker: 'EWJ',    label: 'Japan ETF' },
    { ticker: 'EWT',    label: 'Taiwan ETF' },
    { ticker: 'EWY',    label: 'Korea ETF' },
  ],
  Stocks: [
    { ticker: 'AAPL',   label: 'Apple' },
    { ticker: 'TSLA',   label: 'Tesla' },
    { ticker: 'MSFT',   label: 'Microsoft' },
    { ticker: 'AMZN',   label: 'Amazon' },
    { ticker: 'META',   label: 'Meta' },
    { ticker: 'NVDA',   label: 'Nvidia' },
    { ticker: 'JPM',    label: 'JPMorgan' },
    { ticker: 'XOM',    label: 'ExxonMobil' },
    { ticker: 'LMT',    label: 'Lockheed Martin' },
    { ticker: 'SOXX',   label: 'Semiconductors ETF' },
  ],
  Forex: [
    { ticker: 'EURUSD=X', label: 'EUR/USD' },
    { ticker: 'GBPUSD=X', label: 'GBP/USD' },
    { ticker: 'AUDUSD=X', label: 'AUD/USD' },
    { ticker: 'JPY=X',    label: 'USD/JPY' },
    { ticker: 'DX-Y.NYB', label: 'DXY (USD Index)' },
    { ticker: 'CNY=X',    label: 'USD/CNY' },
    { ticker: 'CHFUSD=X', label: 'CHF/USD' },
    { ticker: 'CADUSD=X', label: 'CAD/USD' },
    { ticker: 'INRUSD=X', label: 'INR/USD' },
    { ticker: 'THBUSD=X', label: 'THB/USD' },
  ],
  Crypto: [
    { ticker: 'BTC-USD', label: 'Bitcoin' },
    { ticker: 'ETH-USD', label: 'Ethereum' },
    { ticker: 'BNB-USD', label: 'Binance' },
    { ticker: 'SOL-USD', label: 'Solana' },
    { ticker: 'XRP-USD', label: 'Ripple' },
    { ticker: 'ADA-USD', label: 'Cardano' },
    { ticker: 'AVAX-USD', label: 'Avalanche' },
    { ticker: 'DOGE-USD', label: 'Dogecoin' },
    { ticker: 'COIN',    label: 'Coinbase' },
    { ticker: 'HACK',    label: 'Cybersecurity ETF' },
  ],
  Bond: [
    { ticker: '^TNX',   label: 'US 10Y Treasury' },
    { ticker: '^TYX',   label: 'US 30Y Treasury' },
    { ticker: '^FVX',   label: 'US 5Y Treasury' },
    { ticker: 'TLT',    label: 'US Bond ETF' },
    { ticker: 'HYG',    label: 'High Yield Bonds' },
    { ticker: 'EMB',    label: 'EM Bonds' },
    { ticker: '^IRX',   label: 'US 13W T-Bill' },
    { ticker: 'SHY',    label: 'Short-Term Bond ETF' },
    { ticker: 'LQD',    label: 'Corp Bond ETF' },
    { ticker: '^VIX',   label: 'VIX Fear Index' },
  ],
}

function formatPrice(price: number) {
  if (!price) return '--'
  return price >= 1000
    ? '$' + price.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
    : '$' + price.toFixed(4).replace(/\.?0+$/, '') || price.toFixed(2)
}

function formatDate(dateStr: string, range: string) {
  const date = new Date(dateStr)
  if (range === '3d' || range === '7d') return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })
  if (range === '1m') return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })
  return date.toLocaleDateString('en-US', { month: 'short', year: '2-digit' })
}

export default function StocksPage() {
  const [selectedCategory, setSelectedCategory] = useState('Commodity')
  const [selectedTicker, setSelectedTicker] = useState('GC=F')
  const [selectedRange, setSelectedRange] = useState('1y')
  const [stockData, setStockData] = useState<StockData | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [priceCache, setPriceCache] = useState<Record<string, { price: number; changePercent: string; change: string }>>({})
  const [loadingCategory, setLoadingCategory] = useState(false)
  const [aiContext, setAiContext] = useState('')
  const [aiLoading, setAiLoading] = useState(false)

  // Load prices for current category
  /* eslint-disable react-hooks/exhaustive-deps */
  useEffect(() => {
    setLoadingCategory(true)
    const tickers = CATEGORY_TICKERS[selectedCategory] || []
    let completed = 0
    tickers.forEach(({ ticker }) => {
      if (priceCache[ticker]) {
        completed++
        if (completed === tickers.length) setLoadingCategory(false)
        return
      }
      fetch(`/api/stocks?ticker=${encodeURIComponent(ticker)}&range=7d`)
        .then(r => r.json())
        .then(data => {
          if (!data.error) {
            setPriceCache(prev => ({
              ...prev,
              [ticker]: { price: data.price, changePercent: data.changePercent, change: data.change }
            }))
          }
        })
        .catch(() => {})
        .finally(() => {
          completed++
          if (completed === tickers.length) setLoadingCategory(false)
        })
    })
    if (tickers.length === 0) setLoadingCategory(false)
  }, [selectedCategory])

  // Load chart data
  useEffect(() => {
    setLoading(true)
    setError('')
    fetch(`/api/stocks?ticker=${encodeURIComponent(selectedTicker)}&range=${selectedRange}`)
      .then(r => r.json())
      .then(data => {
        if (data.error) setError(data.error)
        else {
          setStockData(data)
          setPriceCache(prev => ({
            ...prev,
            [data.ticker]: { price: data.price, changePercent: data.changePercent, change: data.change }
          }))
        }
      })
      .catch(() => setError('Failed to load stock data'))
      .finally(() => setLoading(false))
  }, [selectedTicker, selectedRange])

  /* eslint-enable react-hooks/exhaustive-deps */
  // Load AI context
  /* eslint-disable react-hooks/exhaustive-deps */
  useEffect(() => {
    setAiContext('')
    setAiLoading(true)
    const cached = priceCache[selectedTicker]
    const change = cached?.changePercent || '0'
    fetch(`/api/stock-context?ticker=${encodeURIComponent(selectedTicker)}&change=${change}`)
      .then(r => r.json())
      .then(data => setAiContext(data.context || ''))
      .catch(() => setAiContext('AI context temporarily unavailable.'))
      .finally(() => setAiLoading(false))
  }, [selectedTicker])
  /* eslint-enable react-hooks/exhaustive-deps */

  const isPositive = stockData ? parseFloat(stockData.changePercent) >= 0 : true
  const chartColor = isPositive ? '#22c55e' : '#ef4444'
  const chartData = stockData?.chartData?.map(d => ({ ...d, date: formatDate(d.date, selectedRange) })) || []
  const tickCount = selectedRange === '3d' ? 3 : selectedRange === '7d' ? 7 : 8

  return (
    <div className="min-h-screen bg-gray-950 text-gray-100">

      {/* Header */}
      <header className="border-b border-gray-800 bg-gray-900">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between mb-3">
            <div>
              <h1 className="text-xl font-bold text-white">📈 Market Intelligence</h1>
              <p className="text-xs text-gray-400">6-Category Market View -- Trading Economics Style -- Yahoo Finance Data</p>
            </div>
            <a href="/" className="text-xs text-blue-400 hover:text-blue-300 border border-blue-800 rounded px-3 py-1">
              ← Quantum Strategist
            </a>
          </div>
          {/* Cross-nav */}
          <div className="flex flex-wrap gap-2">
            <a href="/researcher" className="flex items-center gap-1.5 bg-green-900 hover:bg-green-700 border border-green-700 rounded-lg px-3 py-1.5 text-xs font-bold text-green-200 transition-colors">
              📊 Researcher
            </a>
            <a href="/developer-hub" className="flex items-center gap-1.5 bg-purple-900 hover:bg-purple-700 border border-purple-700 rounded-lg px-3 py-1.5 text-xs font-bold text-purple-200 transition-colors">
              🧠 Developer
            </a>
            <a href="/reports" className="flex items-center gap-1.5 bg-amber-900 hover:bg-amber-700 border border-amber-700 rounded-lg px-3 py-1.5 text-xs font-bold text-amber-200 transition-colors">
              🎯 Reports
            </a>
            <a href="/about" className="flex items-center gap-1.5 bg-gray-800 hover:bg-gray-700 border border-gray-600 rounded-lg px-3 py-1.5 text-xs font-bold text-gray-200 transition-colors">
              🌟 About
            </a>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-6 py-6">

        {/* 6 Category Tabs */}
        <div className="flex gap-2 mb-4 flex-wrap">
          {CATEGORIES.map(({ key, label, emoji }) => (
            <button
              key={key}
              onClick={() => {
                setSelectedCategory(key)
                const first = CATEGORY_TICKERS[key]?.[0]
                if (first) setSelectedTicker(first.ticker)
              }}
              className={`flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-bold transition-colors border ${
                selectedCategory === key
                  ? 'bg-blue-700 border-blue-500 text-white'
                  : 'bg-gray-900 border-gray-700 text-gray-400 hover:border-gray-500 hover:text-white'
              }`}
            >
              <span>{emoji}</span><span>{label}</span>
            </button>
          ))}
        </div>

        {/* Trading Economics Style Listing Table */}
        <div className="bg-gray-900 border border-gray-700 rounded-xl mb-6 overflow-hidden">
          <div className="grid grid-cols-4 px-4 py-2 border-b border-gray-800 text-xs text-gray-500 uppercase tracking-wider">
            <div>Instrument</div>
            <div className="text-right">Price</div>
            <div className="text-right">Day Change</div>
            <div className="text-right">% Change</div>
          </div>
          {loadingCategory && (
            <div className="px-4 py-8 text-center text-xs text-gray-500">Loading {selectedCategory} prices...</div>
          )}
          {!loadingCategory && (CATEGORY_TICKERS[selectedCategory] || []).map(({ ticker, label }) => {
            const cached = priceCache[ticker]
            const pct = cached ? parseFloat(cached.changePercent) : null
            const isUp = pct !== null ? pct >= 0 : null
            return (
              <button
                key={ticker}
                onClick={() => setSelectedTicker(ticker)}
                className={`w-full grid grid-cols-4 px-4 py-3 border-b border-gray-800 hover:bg-gray-800 transition-colors text-left ${
                  selectedTicker === ticker ? 'bg-gray-800 border-l-2 border-l-blue-500' : ''
                }`}
              >
                <div>
                  <div className="text-sm font-bold text-white">{label}</div>
                  <div className="text-xs text-gray-500 font-mono">{ticker}</div>
                </div>
                <div className="text-right text-sm font-bold text-white self-center">
                  {cached ? formatPrice(cached.price) : '--'}
                </div>
                <div className={`text-right text-sm font-bold self-center ${isUp === null ? 'text-gray-500' : isUp ? 'text-green-400' : 'text-red-400'}`}>
                  {cached?.change ? (isUp ? '+' : '') + cached.change : '--'}
                </div>
                <div className="text-right self-center">
                  {pct !== null ? (
                    <span className={`text-xs font-bold px-2 py-1 rounded ${isUp ? 'bg-green-900 text-green-300' : 'bg-red-900 text-red-300'}`}>
                      {isUp ? '+' : ''}{pct.toFixed(2)}%
                    </span>
                  ) : (
                    <span className="text-xs text-gray-600">--</span>
                  )}
                </div>
              </button>
            )
          })}
        </div>

        {/* Chart Section */}
        <div className="bg-gray-900 border border-gray-700 rounded-xl p-6">
          <div className="flex items-start justify-between mb-4">
            <div>
              <div className="text-white font-bold text-xl">{stockData?.ticker || selectedTicker}</div>
              <div className="text-gray-400 text-sm">{stockData?.name || 'Loading...'}</div>
            </div>
            {stockData && !loading && (
              <div className="text-right">
                <div className="text-white font-bold text-2xl">{formatPrice(stockData.price)}</div>
                <div className={`text-sm font-bold ${isPositive ? 'text-green-400' : 'text-red-400'}`}>
                  {isPositive ? '▲' : '▼'} {stockData.change} ({stockData.changePercent}%)
                </div>
              </div>
            )}
          </div>

          {/* Range selector */}
          <div className="flex gap-2 mb-4">
            {RANGES.map(range => (
              <button
                key={range}
                onClick={() => setSelectedRange(range)}
                className={`px-3 py-1.5 rounded-lg text-xs font-bold transition-colors ${
                  selectedRange === range
                    ? 'bg-blue-600 text-white'
                    : 'bg-gray-800 text-gray-400 hover:bg-gray-700 hover:text-white'
                }`}
              >
                {range.toUpperCase()}
              </button>
            ))}
          </div>

          {loading && (
            <div className="flex items-center justify-center h-48 text-gray-400 text-sm">
              Loading chart...
            </div>
          )}
          {error && (
            <div className="flex items-center justify-center h-48 text-red-400 text-sm">
              ⚠️ {error}
            </div>
          )}
          {!loading && !error && stockData && (
            <ResponsiveContainer width="100%" height={260}>
              <AreaChart data={chartData} margin={{ top: 5, right: 10, left: 10, bottom: 5 }}>
                <defs>
                  <linearGradient id="colorClose" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor={chartColor} stopOpacity={0.3} />
                    <stop offset="95%" stopColor={chartColor} stopOpacity={0} />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#1f2937" />
                <XAxis dataKey="date" tick={{ fill: '#6b7280', fontSize: 10 }} tickLine={false} axisLine={false} interval={Math.floor(chartData.length / tickCount)} />
                <YAxis tick={{ fill: '#6b7280', fontSize: 10 }} tickLine={false} axisLine={false} tickFormatter={v => '$' + v.toLocaleString()} width={65} domain={['auto', 'auto']} />
                <Tooltip
                  contentStyle={{ backgroundColor: '#111827', border: '1px solid #374151', borderRadius: '8px', color: '#f9fafb', fontSize: '11px' }}
                  formatter={(value) => ['$' + Number(value).toLocaleString(), 'Price']}
                />
                <Area type="monotone" dataKey="close" stroke={chartColor} strokeWidth={2} fill="url(#colorClose)" dot={false} activeDot={{ r: 4, fill: chartColor }} />
              </AreaChart>
            </ResponsiveContainer>
          )}
          <div className="mt-2 text-center text-xs text-gray-600">
            Data: Yahoo Finance -- Updates hourly -- Not financial advice
          </div>

          {/* AI Context */}
          <div className="mt-4 bg-blue-950 border border-blue-800 rounded-lg p-3">
            <div className="text-xs text-blue-400 uppercase tracking-wider mb-1 flex items-center gap-2">
              <span>🧠</span>
              <span>GNI AI Context -- Why did {selectedTicker} move recently?</span>
            </div>
            {aiLoading && <p className="text-gray-400 text-xs">Analyzing geopolitical events...</p>}
            {!aiLoading && aiContext && (
              <div>
                <p className="text-blue-200 text-xs leading-relaxed mb-2">{aiContext}</p>
                <p className="text-yellow-400 text-xs">⚠️ For informational purposes only. Not financial advice.</p>
              </div>
            )}
          </div>
        </div>

      </div>

      <footer className="border-t border-gray-800 mt-8">
        <div className="max-w-7xl mx-auto px-4 py-4 text-center text-xs text-gray-600">
          Global Nexus Insights (Autonomous) | Market Intelligence | Yahoo Finance Data | Higher Diploma in Computer Science | SUM
        </div>
      </footer>
    </div>
  )
}
