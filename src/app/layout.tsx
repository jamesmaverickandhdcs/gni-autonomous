import type { Metadata } from "next";
import { GeistSans } from "geist/font/sans";
import { GeistMono } from "geist/font/mono";
import "./globals.css";
import { cn } from "@/lib/utils";

const siteUrl = 'https://gni-autonomous.vercel.app'

export const metadata: Metadata = {
  title: {
    default: 'GNI — Global Nexus Insights (Autonomous)',
    template: '%s | GNI — Global Nexus Insights',
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
    title: 'GNI — Free AI Geopolitical Intelligence',
    description: 'Free AI-powered geopolitical intelligence. Real-time analysis of global conflicts, market impact, and escalation risk. Autonomous pipeline. $0/month.',
    images: [
      {
        url: `${siteUrl}/og-image.png`,
        width: 1200,
        height: 630,
        alt: 'Global Nexus Insights — Free AI Geopolitical Intelligence',
      },
    ],
  },
  twitter: {
    card: 'summary_large_image',
    title: 'GNI — Free AI Geopolitical Intelligence',
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
