import os

# ── 1. robots.txt ──────────────────────────────────────────────────────────
robots = """User-agent: *
Allow: /

Sitemap: https://gni-autonomous.vercel.app/sitemap.xml
"""
with open('public/robots.txt', 'w', encoding='utf-8', newline='\n') as f:
    f.write(robots)
print('robots.txt written')

# ── 2. sitemap.ts ──────────────────────────────────────────────────────────
sitemap = """\
import { MetadataRoute } from 'next'

export default function sitemap(): MetadataRoute.Sitemap {
  const base = 'https://gni-autonomous.vercel.app'
  const now = new Date()

  return [
    {
      url: base,
      lastModified: now,
      changeFrequency: 'hourly',
      priority: 1.0,
    },
    {
      url: `${base}/history`,
      lastModified: now,
      changeFrequency: 'hourly',
      priority: 0.9,
    },
    {
      url: `${base}/debate`,
      lastModified: now,
      changeFrequency: 'hourly',
      priority: 0.9,
    },
    {
      url: `${base}/transparency`,
      lastModified: now,
      changeFrequency: 'hourly',
      priority: 0.8,
    },
    {
      url: `${base}/stocks`,
      lastModified: now,
      changeFrequency: 'hourly',
      priority: 0.8,
    },
    {
      url: `${base}/map`,
      lastModified: now,
      changeFrequency: 'hourly',
      priority: 0.8,
    },
    {
      url: `${base}/health`,
      lastModified: now,
      changeFrequency: 'hourly',
      priority: 0.7,
    },
    {
      url: `${base}/security`,
      lastModified: now,
      changeFrequency: 'weekly',
      priority: 0.6,
    },
    {
      url: `${base}/autonomy`,
      lastModified: now,
      changeFrequency: 'weekly',
      priority: 0.6,
    },
    {
      url: `${base}/about`,
      lastModified: now,
      changeFrequency: 'monthly',
      priority: 0.5,
    },
  ]
}
"""
with open('src/app/sitemap.ts', 'w', encoding='utf-8', newline='\n') as f:
    f.write(sitemap)
print('sitemap.ts written')

# ── 3. layout.tsx ──────────────────────────────────────────────────────────
layout = """\
import type { Metadata } from "next";
import { GeistSans } from "geist/font/sans";
import { GeistMono } from "geist/font/mono";
import "./globals.css";
import { cn } from "@/lib/utils";

const siteUrl = 'https://gni-autonomous.vercel.app'

export const metadata: Metadata = {
  title: {
    default: 'GNI \u2014 Global Nexus Insights (Autonomous)',
    template: '%s | GNI \u2014 Global Nexus Insights',
  },
  description: 'Free AI-powered geopolitical intelligence. Real-time analysis of global conflicts, market impact, escalation risk, and financial sentiment. Autonomous pipeline. $0/month.',
  keywords: [
    'free geopolitical intelligence',
    'AI news analysis',
    'autonomous AI pipeline',
    'global conflict analysis',
    'market impact geopolitics',
    'Myanmar news analysis',
    'Strait of Hormuz',
    'Iran conflict market impact',
    'free intelligence tool',
    'explainable AI',
    'SPY geopolitics',
    'multi-agent AI debate',
  ],
  authors: [{ name: 'GNI Autonomous' }],
  creator: 'GNI Autonomous',
  publisher: 'GNI Autonomous',
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      'max-video-preview': -1,
      'max-image-preview': 'large',
      'max-snippet': -1,
    },
  },
  openGraph: {
    type: 'website',
    locale: 'en_US',
    url: siteUrl,
    siteName: 'Global Nexus Insights (Autonomous)',
    title: 'GNI \u2014 Free AI Geopolitical Intelligence',
    description: 'Free AI-powered geopolitical intelligence. Real-time analysis of global conflicts, market impact, and escalation risk. Autonomous pipeline. $0/month.',
    images: [
      {
        url: `${siteUrl}/og-image.png`,
        width: 1200,
        height: 630,
        alt: 'Global Nexus Insights \u2014 Free AI Geopolitical Intelligence',
      },
    ],
  },
  twitter: {
    card: 'summary_large_image',
    title: 'GNI \u2014 Free AI Geopolitical Intelligence',
    description: 'Real-time autonomous AI analysis of global conflicts and market impact. Free forever.',
    images: [`${siteUrl}/og-image.png`],
  },
  alternates: {
    canonical: siteUrl,
  },
  metadataBase: new URL(siteUrl),
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className={cn("font-sans", GeistSans.variable, GeistMono.variable)}>
      <body className="min-h-screen bg-background antialiased">
        {children}
      </body>
    </html>
  );
}
"""
with open('src/app/layout.tsx', 'w', encoding='utf-8', newline='\n') as f:
    f.write(layout)
print('layout.tsx written')

# ── 4. Simple OG image placeholder ─────────────────────────────────────────
# Create a simple SVG as og-image.png placeholder
# Real OG image can be designed later
og_svg = """<svg width="1200" height="630" xmlns="http://www.w3.org/2000/svg">
  <rect width="1200" height="630" fill="#030712"/>
  <rect x="0" y="0" width="1200" height="4" fill="#22c55e"/>
  <text x="600" y="220" font-family="Arial, sans-serif" font-size="80" font-weight="bold" fill="white" text-anchor="middle">
    GNI
  </text>
  <text x="600" y="300" font-family="Arial, sans-serif" font-size="32" fill="#9ca3af" text-anchor="middle">
    Global Nexus Insights (Autonomous)
  </text>
  <text x="600" y="380" font-family="Arial, sans-serif" font-size="24" fill="#6b7280" text-anchor="middle">
    Free AI Geopolitical Intelligence
  </text>
  <text x="600" y="460" font-family="Arial, sans-serif" font-size="48" font-weight="bold" fill="#22c55e" text-anchor="middle">
    $0.00 / month
  </text>
  <text x="600" y="520" font-family="Arial, sans-serif" font-size="20" fill="#6b7280" text-anchor="middle">
    gni-autonomous.vercel.app
  </text>
</svg>"""

with open('public/og-image.svg', 'w', encoding='utf-8', newline='\n') as f:
    f.write(og_svg)
print('og-image.svg written')

# Verify all files
for path in ['public/robots.txt', 'src/app/sitemap.ts', 'src/app/layout.tsx', 'public/og-image.svg']:
    size = os.path.getsize(path)
    print(f'{path}: {size} bytes')
