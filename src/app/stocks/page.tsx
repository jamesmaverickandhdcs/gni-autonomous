'use client'
const GNI_KEY = process.env.NEXT_PUBLIC_GNI_API_KEY || ''

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
  rangeChange: string
  rangeChangePercent: string
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

const CATEGORY_TICKERS: Record<string, { ticker: string; label: string; note: string }[]> = {
  Commodity: [
    { ticker: 'CL=F',   label: 'Crude Oil',    note: `Crude oil is the world's most important commodity — it powers cars, planes, factories, and ships across every country. Its price rises sharply when conflicts break out in the Middle East or when major oil producers cut supply. Watching this chart tells you whether the global economy is running smoothly or facing an energy shock.` },
    { ticker: 'BZ=F',   label: 'Brent Crude',  note: `Brent crude is the global standard for oil pricing, used to set prices for roughly two-thirds of the world's traded oil. It reflects geopolitical tension in oil-producing regions like the Middle East, Russia, and West Africa more directly than any other benchmark. When Brent rises, energy costs rise everywhere — from fuel at the pump to airline tickets.` },
    { ticker: 'NG=F',   label: 'Natural Gas',  note: `Natural gas heats homes, generates electricity, and powers industries across Europe and Asia. Its price spikes during cold winters, supply disruptions, or when pipeline routes are cut — as happened dramatically when Russia restricted gas exports to Europe in 2022. This chart is one of the clearest early signals of an energy crisis developing anywhere in the world.` },
    { ticker: 'GC=F',   label: 'Gold',         note: `Gold has been humanity's most trusted store of value for thousands of years, and it still performs that role today. When wars break out, economies wobble, or investors lose confidence in paper currencies, money flows into gold and its price rises. A sharp move upward in this chart is almost always a signal that something serious is worrying the world's investors.` },
    { ticker: 'SI=F',   label: 'Silver',       note: `Silver plays a dual role — it is both a safe haven like gold and an industrial metal used in electronics, solar panels, and medical equipment. It tends to follow gold during crises but moves more dramatically in both directions, making it a more volatile signal. Rising silver alongside gold usually confirms that investors are genuinely worried, not just cautious.` },
    { ticker: 'HG=F',   label: 'Copper',       note: `Copper is used in virtually every form of construction, wiring, and manufacturing — which is why economists call it Dr. Copper and treat it as one of the best indicators of global economic health. When copper prices rise, it usually means factories are busy, construction is booming, and the world economy is expanding. A falling copper price often arrives months before a slowdown becomes obvious in other data.` },
    { ticker: 'ZS=F',   label: 'Soybeans',     note: `Soybeans are one of the world's most important food and animal feed crops, consumed heavily across Asia, Europe, and the Americas. Their price is highly sensitive to weather in Brazil and the US, China's import demand, and trade war tariffs that redirect supply chains. Watching this chart matters because soybean price movements signal stress in global food supply and trade relationships.` },
    { ticker: 'ZW=F',   label: 'Wheat',        note: `Wheat feeds billions of people through bread, pasta, and flour, making it one of the most politically sensitive commodities in the world. The 2022 Russia-Ukraine war sent wheat prices to all-time highs almost overnight because both countries supply roughly 30% of global wheat exports. A spike on this chart can translate directly into food inflation, political instability, and hunger in import-dependent countries.` },
    { ticker: 'GLD',    label: 'Gold ETF',     note: `GLD is an exchange-traded fund that tracks the physical price of gold, making it easy for everyday investors to buy gold without storing bars or coins. It moves almost identically to the gold futures price but trades on the stock exchange like a regular share. This is the instrument most professional investors use when they want gold exposure in a crisis — watching its price is effectively the same as watching gold itself.` },
    { ticker: 'GDX',    label: 'Gold Miners',  note: `GDX holds shares in companies that mine gold, meaning it gives amplified exposure to the gold price — when gold rises 5%, gold miners often rise 10-15% because their profit margins expand dramatically. This makes GDX a powerful indicator of just how seriously investors are treating a safe-haven signal. If gold is rising but GDX is rising even faster, it confirms that institutional money is genuinely fleeing into hard assets.` },
  ],
  Index: [
    { ticker: 'SPY',    label: 'US500 (S&P 500)',   note: `The S&P 500 tracks the 500 largest companies in the United States — Apple, Microsoft, Amazon, Google, and 496 others — and is the single most watched financial chart in the world. When this chart falls sharply, it means that professional investors are selling their holdings because they believe something bad is coming for the economy. Almost every other financial market takes its cue from how the S&P 500 is performing.` },
    { ticker: '^DJI',   label: 'US30 (Dow Jones)',  note: `The Dow Jones Industrial Average tracks 30 of America's most iconic companies — including Boeing, Goldman Sachs, Walmart, and Nike — and has been the world's best-known stock index for over a century. It is less representative than the S&P 500 but more psychologically powerful, because policymakers and the media treat round numbers like Dow 40,000 as major milestones. A big Dow drop makes front-page news around the world and affects consumer confidence everywhere.` },
    { ticker: '^NDX',   label: 'US100 (Nasdaq)',    note: `The Nasdaq 100 tracks the 100 largest technology and growth companies — including Nvidia, Apple, Meta, and Tesla — making it the index most sensitive to the AI revolution, semiconductor policy, and US-China tech competition. When the US government restricts chip exports to China, or when a major AI company reports results, this index moves first and fastest. It represents the part of the economy that is most directly reshaping the world.` },
    { ticker: '^N225',  label: 'JP225 (Nikkei)',    note: `The Nikkei 225 is Japan's main stock index, tracking 225 major companies including Toyota, Sony, and SoftBank, and it is Asia's most closely watched equity benchmark. Japan is deeply integrated into global supply chains, especially in cars and electronics, making the Nikkei sensitive to both regional geopolitical tensions and global trade flows. The yen's exchange rate also plays a huge role — a weaker yen tends to lift the Nikkei because it makes Japanese exports cheaper and more competitive.` },
    { ticker: '^FTSE',  label: 'GB100 (FTSE)',      note: `The FTSE 100 tracks the 100 largest companies listed on the London Stock Exchange, including major banks, oil companies, and pharmaceutical giants with revenues earned worldwide. Unlike many other indices, the FTSE is heavily weighted toward energy and mining companies, meaning it often holds up well during commodity price spikes even when other markets fall. It is the primary gauge of confidence in the UK economy and the global financial system centred on London.` },
    { ticker: '^GDAXI', label: 'DE40 (DAX)',        note: `The DAX tracks Germany's 40 largest companies — including Volkswagen, BMW, Siemens, and BASF — making it the clearest window into the health of Europe's largest economy. Germany's industrial powerhouse status means the DAX is highly sensitive to energy prices, global trade volumes, and relations with Russia and China, all of which have been severely tested in recent years. A falling DAX often signals trouble spreading across all of continental Europe.` },
    { ticker: 'FXI',    label: 'China ETF',         note: `FXI tracks the 50 largest Chinese companies listed in Hong Kong, including Alibaba, Tencent, and major state banks, providing the clearest real-time signal of investor confidence in China's economy. China is Myanmar's largest trading partner and the biggest driver of economic growth across Southeast Asia, so a sharp drop in FXI often ripples outward across the entire region. Regulatory crackdowns, property market stress, and US-China tensions all show up immediately in this chart.` },
    { ticker: 'EWJ',    label: 'Japan ETF',         note: `EWJ holds shares in Japan's major publicly listed companies and trades on US exchanges, making it easy for global investors to gain or reduce their Japan exposure quickly. It tracks the same companies as the Nikkei but is traded in US dollars, meaning it also reflects currency movements between the yen and the dollar. Watching EWJ alongside the Nikkei shows whether investors are moving because of Japan's economy or because of the yen's exchange rate.` },
    { ticker: 'EWT',    label: 'Taiwan ETF',        note: `EWT tracks Taiwan's stock market, which is dominated by TSMC — the company that manufactures the most advanced chips in the world and whose factories are irreplaceable to the entire global technology industry. Any increase in tension between China and Taiwan sends this chart immediately lower, because a conflict would disrupt the semiconductor supply chain that everything from iPhones to fighter jets depends upon. This is one of the most geopolitically sensitive charts in the world right now.` },
    { ticker: 'EWY',    label: 'Korea ETF',         note: `EWY tracks South Korea's stock market, led by Samsung, SK Hynix, and Hyundai — companies that are central to the global semiconductor, battery, and electric vehicle industries. South Korea sits directly between China, Japan, and North Korea, making it one of Asia's most geopolitically exposed economies. Any escalation involving North Korea or a deterioration in US-China relations tends to hit South Korean markets and this ETF quickly.` },
  ],
  Stocks: [
    { ticker: 'AAPL',   label: 'Apple',              note: `Apple is the world's most valuable company, selling iPhones, Macs, and services to over a billion active users globally, with its entire supply chain running through China and Southeast Asia. Its share price is sensitive to US-China trade tensions, tariffs on electronics, and the pace of consumer spending in major markets. Because Apple is so large, it moves the entire S&P 500 — when Apple falls, the broad market usually follows.` },
    { ticker: 'TSLA',   label: 'Tesla',              note: `Tesla is the world's leading electric vehicle company, selling cars in the US, Europe, and China while also building energy storage systems and solar products. Its share price is unusually sensitive to Elon Musk's public statements, China sales data, and competition from cheaper Chinese EV brands like BYD. Tesla's trajectory matters because it shapes the pace of the entire global transition from petrol to electric vehicles.` },
    { ticker: 'MSFT',   label: 'Microsoft',          note: `Microsoft is the world's leading provider of business software and cloud computing, with its Azure platform powering everything from government systems to hospital records to AI applications worldwide. It has become one of the primary beneficiaries of the artificial intelligence revolution through its partnership with OpenAI and integration of AI into all its products. As one of the largest companies in the world, Microsoft's performance is a direct reflection of how the global corporate and technology sector is doing.` },
    { ticker: 'AMZN',   label: 'Amazon',             note: `Amazon dominates both global e-commerce and cloud computing through AWS, which powers roughly a third of the internet's infrastructure including Netflix, Airbnb, and countless government systems. Its performance reflects the health of consumer spending, the pace of digital transformation, and the competitive dynamics of the cloud computing industry. Amazon's logistics network has also made it one of the world's largest employers, making it a meaningful indicator of labour market conditions.` },
    { ticker: 'META',   label: 'Meta',               note: `Meta owns Facebook, Instagram, and WhatsApp — the social media platforms used by nearly four billion people every month — and generates almost all its revenue by selling targeted advertising to businesses worldwide. Its share price is highly sensitive to digital advertising spending, which tends to fall sharply in recessions, as well as to regulatory actions by the EU, US Congress, and competition authorities. Meta's virtual reality ambitions through its Quest headsets represent its bet on what computing will look like in the next decade.` },
    { ticker: 'NVDA',   label: 'Nvidia',             note: `Nvidia designs the specialised chips — called GPUs — that power virtually all artificial intelligence training and inference, making it arguably the most important company in the current technology revolution. Its share price has become a direct proxy for investor confidence in the AI industry, rising dramatically when AI enthusiasm is high and falling when doubts emerge. US export controls restricting Nvidia chip sales to China are the single biggest regulatory risk to its business and a key flashpoint in the US-China technology war.` },
    { ticker: 'JPM',    label: 'JPMorgan',           note: `JPMorgan Chase is the largest bank in the United States and one of the most systemically important financial institutions in the world, touching everything from consumer mortgages to government bond markets to global corporate financing. Its share price tends to fall sharply at the first sign of financial system stress — making it one of the earliest warning signals when a banking crisis or recession may be approaching. Watching JPMorgan alongside bond yields gives a clear picture of whether the financial system is functioning normally or beginning to strain.` },
    { ticker: 'XOM',    label: 'ExxonMobil',         note: `ExxonMobil is one of the world's largest oil and gas companies, producing energy across every major region and selling fuel, chemicals, and lubricants globally. Its share price rises when oil prices rise — which typically happens during geopolitical conflicts, supply cuts, or energy shortages — making it a direct proxy for energy sector health. Investors often buy ExxonMobil as a hedge when they expect geopolitical instability to push energy prices higher.` },
    { ticker: 'LMT',    label: 'Lockheed Martin',    note: `Lockheed Martin is the world's largest defence contractor, building the F-35 fighter jet, missile defence systems, and military satellites primarily for the US government and its allies. Its share price tends to rise when military conflicts escalate or when governments increase their defence budgets in response to geopolitical threats — making it one of the most direct indicators of global conflict risk. When LMT rises sharply, it is almost always because investors believe military spending is about to increase somewhere in the world.` },
    { ticker: 'SOXX',   label: 'Semiconductors ETF', note: `SOXX holds shares across the entire semiconductor industry — including chip designers like Nvidia and AMD, manufacturers like TSMC and Intel, and equipment makers like ASML — giving exposure to the full supply chain of the technology that powers modern life. Semiconductors are at the centre of the US-China technology war, with export controls, factory subsidies, and supply chain reshoring all directly affecting companies in this index. This is the single most concentrated bet on the future of technology, artificial intelligence, and great power competition.` },
  ],
  Forex: [
    { ticker: 'EURUSD=X', label: 'EUR/USD',       note: `The EUR/USD exchange rate shows how many US dollars one Euro can buy, and it is the most heavily traded currency pair in the world with over a trillion dollars changing hands every day. It reflects the relative economic strength of the United States versus the Eurozone — when the US economy outperforms Europe, the dollar strengthens and this number falls. Major moves in EUR/USD often signal a shift in the global economic balance of power or a significant policy change by the US Federal Reserve or European Central Bank.` },
    { ticker: 'GBPUSD=X', label: 'GBP/USD',       note: `The GBP/USD pair shows how many US dollars one British pound buys, and it is one of the oldest and most watched currency pairs in the world due to London's historic role as the global financial centre. The pound is particularly sensitive to UK political events, Bank of England interest rate decisions, and the ongoing economic consequences of Brexit which reshaped the UK's trading relationships with Europe. A sharp drop in the pound signals that investors have lost confidence in UK economic management.` },
    { ticker: 'AUDUSD=X', label: 'AUD/USD',        note: `The Australian dollar is known as a commodity currency because Australia's economy is built on exporting iron ore, coal, and agricultural products, primarily to China. When China's economy is growing and buying Australian resources, the AUD strengthens — making this pair one of the clearest real-time signals of Chinese economic health available to investors. Traders watch AUD/USD as a risk indicator: when it falls sharply, it usually means investors are worried about the global economy or Chinese demand specifically.` },
    { ticker: 'JPY=X',    label: 'USD/JPY',        note: `The USD/JPY pair shows how many Japanese yen one US dollar buys, and the yen is one of the world's most important safe haven currencies — meaning investors buy it when they are frightened. When global crises strike, money floods into yen and this number falls as the yen strengthens against the dollar. The Bank of Japan's unusual policy of keeping interest rates near zero for decades has made this pair particularly volatile when US interest rates rise, creating dramatic moves that affect borrowers and investors across Asia.` },
    { ticker: 'DX-Y.NYB', label: 'DXY (USD Index)',note: `The US Dollar Index measures the strength of the dollar against a basket of six major currencies — the euro, yen, pound, Canadian dollar, Swedish krona, and Swiss franc — giving the clearest single picture of global dollar strength. When the dollar strengthens, it puts pressure on all other currencies, raises the cost of dollar-denominated debt for developing countries, and generally tightens financial conditions globally. This is one of the most important charts in the world because almost everything in global finance — commodities, debt, trade — is priced in US dollars.` },
    { ticker: 'CNY=X',    label: 'USD/CNY',        note: `The USD/CNY rate shows how many Chinese yuan one US dollar buys, and unlike most currencies this rate is tightly controlled by the Chinese government within a narrow band around a daily reference rate. A deliberate devaluation of the yuan by Beijing — allowing this number to rise — is often used as a tool in trade disputes to make Chinese exports cheaper and more competitive. Watching this chart closely reveals whether China is using its currency as a weapon in trade or geopolitical negotiations.` },
    { ticker: 'CHFUSD=X', label: 'CHF/USD',        note: `The Swiss franc is one of the world's most reliable safe haven currencies — when political or financial crises erupt in Europe, wealthy individuals and institutions move money to Switzerland because of its political neutrality, strong rule of law, and stable banking system. A rising franc against the dollar signals that European risk is increasing and that investors are seeking safety. Switzerland's central bank sometimes intervenes to weaken the franc when it rises too sharply, because an overvalued currency hurts Swiss exporters.` },
    { ticker: 'CADUSD=X', label: 'CAD/USD',        note: `The Canadian dollar is deeply tied to oil prices because Canada is one of the world's largest oil exporters, making it one of the most direct currency expressions of energy market sentiment. When crude oil prices rise, the Canadian dollar typically strengthens against the US dollar — making this pair a useful cross-check on oil market moves. Canada's close economic integration with the United States also means that US tariff policy and trade negotiations directly affect the loonie's value.` },
    { ticker: 'INRUSD=X', label: 'INR/USD',        note: `The Indian rupee's exchange rate against the dollar matters enormously for South Asian trade and investment flows, as India has become one of the world's fastest-growing major economies and an increasingly important manufacturing hub. India imports large quantities of oil, meaning a weaker rupee raises energy costs across the country and puts pressure on inflation and the current account deficit. Watching the rupee gives a useful signal of South Asian economic health and India's competitiveness as an alternative to Chinese manufacturing.` },
    { ticker: 'THBUSD=X', label: 'THB/USD',        note: `The Thai baht is the closest major currency to Myanmar and one of the most important in mainland Southeast Asia, making it a useful proxy for regional economic conditions and investor sentiment toward the ASEAN bloc. Thailand's economy is heavily dependent on tourism, exports, and foreign investment — all of which are sensitive to global growth and regional political stability. Movements in the baht often reflect broader confidence in Southeast Asian economic prospects and can signal currency pressure spreading across the region.` },
  ],
  Crypto: [
    { ticker: 'BTC-USD',  label: 'Bitcoin',         note: `Bitcoin is the world's first and largest cryptocurrency, a digital asset with a fixed maximum supply of 21 million coins that operates without any central bank or government controlling it. It has become both a speculative investment and a tool for capital flight — people in countries with currency crises or heavy financial restrictions increasingly use Bitcoin to move wealth across borders. Its price is driven by a combination of institutional investor sentiment, regulatory news, and its use as a hedge against currency debasement.` },
    { ticker: 'ETH-USD',  label: 'Ethereum',        note: `Ethereum is the second largest cryptocurrency and the platform that most decentralised applications, smart contracts, and digital tokens are built upon — making it the infrastructure layer of the broader crypto ecosystem. Unlike Bitcoin which primarily stores value, Ethereum is a programmable blockchain where developers build financial applications, digital ownership systems, and automated contracts that run without intermediaries. Its price reflects both general crypto sentiment and the pace of adoption of decentralised finance and Web3 applications specifically.` },
    { ticker: 'BNB-USD',  label: 'Binance',         note: `BNB is the native token of Binance, the world's largest cryptocurrency exchange by trading volume, and it is used to pay fees, access special features, and participate in token sales on the Binance platform. Its price is closely tied to the health and regulatory standing of Binance itself — when regulators in the US, Europe, or Asia take action against the exchange, BNB typically falls sharply. Watching BNB gives a signal of how much regulatory pressure the centralised cryptocurrency exchange industry is facing globally.` },
    { ticker: 'SOL-USD',  label: 'Solana',          note: `Solana is a high-speed blockchain designed to process thousands of transactions per second at very low cost, positioning it as a competitor to Ethereum for applications requiring speed — including digital payments, gaming, and decentralised trading. Its price rose dramatically during the 2021 crypto boom and fell sharply in 2022 partly due to its association with the FTX exchange collapse, giving it a reputation for high volatility. Solana's recovery since then is watched as a signal of whether alternative blockchain ecosystems can challenge Ethereum's dominance.` },
    { ticker: 'XRP-USD',  label: 'Ripple',          note: `XRP is the digital token used by Ripple's payment network, which is designed to enable fast and cheap cross-border money transfers between banks and financial institutions worldwide. Its price has been dominated for years by a lawsuit from the US Securities and Exchange Commission which argued XRP is an unregistered security — a case whose partial resolution in 2023 caused a dramatic price spike. XRP's trajectory matters because its outcome set important legal precedents for how cryptocurrencies are regulated in the United States.` },
    { ticker: 'ADA-USD',  label: 'Cardano',         note: `Cardano is a blockchain platform built with an unusually rigorous academic approach — every feature is peer-reviewed by researchers before being implemented — making it one of the most methodically developed projects in the cryptocurrency space. It aims to provide smart contract and decentralised application capabilities with lower energy consumption than older blockchains. Its price reflects general appetite for alternative smart contract platforms and whether its deliberate development pace is gaining traction with developers and users.` },
    { ticker: 'AVAX-USD', label: 'Avalanche',       note: `Avalanche is a blockchain platform designed for speed and customisability, allowing developers to create their own specialised blockchain networks that can be tailored for specific applications like gaming, finance, or enterprise use. It has attracted significant institutional interest as a platform for tokenising real-world assets like bonds, real estate, and funds. Its price reflects developer activity, the growth of its DeFi ecosystem, and broader sentiment toward alternative smart contract platforms competing with Ethereum.` },
    { ticker: 'DOGE-USD', label: 'Dogecoin',        note: `Dogecoin began as an internet joke in 2013 but became one of the world's most recognised cryptocurrencies largely due to Elon Musk repeatedly promoting it on social media, causing dramatic price spikes whenever he posts about it. Unlike most cryptocurrencies it has no supply cap, meaning new coins are created continuously, which limits its appeal as a store of value. It is best understood as a sentiment and social media indicator — when Dogecoin is rising, retail investor enthusiasm for speculative assets is typically at a peak.` },
    { ticker: 'COIN',     label: 'Coinbase',        note: `Coinbase is the largest regulated cryptocurrency exchange in the United States, where millions of Americans buy and sell Bitcoin, Ethereum, and hundreds of other digital assets. As a publicly listed company, its share price moves with cryptocurrency market volumes — rising when crypto trading is active and falling when markets are quiet or regulatory pressure increases. Coinbase's performance is a useful proxy for the overall health of the regulated crypto industry and the pace of mainstream adoption in the West.` },
    { ticker: 'HACK',     label: 'Cybersecurity ETF',note: `HACK holds shares in companies that protect computer systems, networks, and data from attacks — including CrowdStrike, Palo Alto Networks, and other cybersecurity specialists whose services are in increasing demand as state-sponsored hacking and ransomware attacks proliferate globally. Cybersecurity spending is one of the few technology categories that grows during geopolitical crises because governments and corporations rush to protect critical infrastructure when tensions rise. Rising HACK prices often signal that the threat environment — state-sponsored attacks, data breaches, critical infrastructure targeting — is intensifying.` },
  ],
  Bond: [
    { ticker: '^TNX',   label: 'US 10Y Treasury',    note: `The US 10-year Treasury yield is arguably the single most important number in global finance — it sets the baseline interest rate against which mortgages, corporate loans, and government borrowing costs around the world are measured. When this yield rises, it means borrowing becomes more expensive everywhere, stock valuations fall, and pressure builds on emerging market currencies and debt. Every major asset class in the world — stocks, bonds, real estate, currencies — adjusts when the 10-year yield moves significantly.` },
    { ticker: '^TYX',   label: 'US 30Y Treasury',    note: `The US 30-year Treasury yield reflects what investors expect interest rates and inflation to look like over the next three decades, making it a long-term barometer of confidence in the US economy and the dollar's purchasing power. It is used to set the interest rate on 30-year home mortgages across the United States, meaning millions of homeowners are directly affected by its movements. When the 30-year yield rises sharply, it signals that investors expect prolonged inflation or fiscal stress — both of which have global consequences.` },
    { ticker: '^FVX',   label: 'US 5Y Treasury',     note: `The US 5-year Treasury yield is closely tied to expectations for Federal Reserve interest rate policy over the next few years, making it one of the most sensitive indicators of how markets interpret central bank signals. It sits in the middle of the yield curve and is watched for signs of inversion — when short-term rates exceed long-term rates — which has historically preceded every US recession. Traders analyse the 5-year yield alongside other maturities to understand whether the market believes inflation will be controlled or persist.` },
    { ticker: 'TLT',    label: 'US Bond ETF',        note: `TLT is an exchange-traded fund that holds long-term US government bonds, and it moves in the opposite direction to interest rates — rising when yields fall and falling when yields rise. During stock market crashes and financial crises, investors typically rush into TLT as a safe haven because US government bonds are considered the safest assets in the world. Watching TLT alongside the S&P 500 shows whether a market selloff is being accompanied by a flight to safety or whether both stocks and bonds are falling simultaneously — a much more alarming scenario.` },
    { ticker: 'HYG',    label: 'High Yield Bonds',   note: `HYG holds high-yield corporate bonds — debt issued by companies with lower credit ratings that pay higher interest rates to compensate investors for the greater risk of default. It is one of the earliest warning indicators in financial markets because credit stress appears in high-yield bonds before it shows up in stock prices, as lenders become nervous about weaker companies first. When HYG falls sharply while stocks are still holding steady, experienced investors pay close attention because it often signals that a broader market selloff is approaching.` },
    { ticker: 'EMB',    label: 'EM Bonds',           note: `EMB holds sovereign bonds issued by emerging market governments in US dollars — including debt from countries across Asia, Latin America, Africa, and the Middle East — giving a broad picture of how the developing world is managing its finances. When the US dollar strengthens or US interest rates rise, emerging market bonds typically fall because countries struggle to repay dollar-denominated debt. This chart is particularly relevant for Southeast Asian economies including Myanmar's neighbours, as it captures the financial stress that can precede currency crises and debt defaults in developing countries.` },
    { ticker: '^IRX',   label: 'US 13W T-Bill',      note: `The 13-week Treasury bill yield reflects the interest rate on the US government's safest and most liquid short-term debt, and it spikes dramatically when investors fear the financial system itself may be under stress. During the 2008 financial crisis and the 2020 COVID crash, the T-bill yield collapsed as trillions of dollars flooded into the safest possible asset. Watching this rate gives a real-time signal of acute fear in the financial system — when it moves sharply, something serious is happening.` },
    { ticker: 'SHY',    label: 'Short-Term Bond ETF',note: `SHY holds US government bonds with maturities of 1 to 3 years, making it one of the most conservative and stable investments available to market participants seeking to reduce risk without going entirely to cash. Investors rotate into SHY from stocks and longer-term bonds when they want to reduce exposure to market volatility while still earning some return. A large inflow into SHY signals that institutional investors are de-risking their portfolios — often a precursor to broader market caution.` },
    { ticker: 'LQD',    label: 'Corp Bond ETF',      note: `LQD holds investment-grade corporate bonds — debt issued by financially strong companies like Apple, Microsoft, and JPMorgan — and it reflects the cost for major corporations to borrow money in the bond market. When LQD falls, it means corporate borrowing costs are rising, which squeezes profit margins, reduces investment, and signals that the credit environment is tightening. The spread between LQD yields and US Treasury yields is watched closely as a measure of how much additional risk investors think the corporate sector carries versus the government.` },
    { ticker: '^VIX',   label: 'VIX Fear Index',     note: `The VIX measures how much volatility options traders expect in the S&P 500 over the next 30 days, and it has earned the nickname the fear gauge because it spikes dramatically during market panics and crises. A VIX below 15 signals calm and complacency, a reading above 20 signals elevated concern, and a reading above 30 signals genuine fear — the VIX hit 80 during the 2008 financial crisis and 85 at the peak of the 2020 COVID crash. This is one of the most important single numbers to watch because it tells you not just what is happening in markets but how frightened professional investors actually are.` },
  ],
}


function formatPrice(price: number) {
  if (!price) return '--'
  return price >= 1000
    ? '$' + price.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
    : '$' + price.toFixed(2)
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
  const [selectedRange, setSelectedRange] = useState('3d')
  const [stockData, setStockData] = useState<StockData | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [priceCache, setPriceCache] = useState<Record<string, { price: number; changePercent: string; change: string }>>({})
  const [loadingCategory, setLoadingCategory] = useState(false)
  

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
      fetch(`/api/stocks?ticker=${encodeURIComponent(ticker)}&range=7d`, { headers: { 'X-GNI-Key': GNI_KEY } })
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

  useEffect(() => {
    setLoading(true)
    setError('')
    fetch(`/api/stocks?ticker=${encodeURIComponent(selectedTicker)}&range=${selectedRange}`, { headers: { 'X-GNI-Key': GNI_KEY } })
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

  // Auto-refresh 3d every 5 min for selected ticker only (GNI stand-by architecture)
  useEffect(() => {
    if (selectedRange !== '3d') return
    const interval = setInterval(() => {
      fetch(`/api/stocks?ticker=${encodeURIComponent(selectedTicker)}&range=3d`, { headers: { 'X-GNI-Key': GNI_KEY } })
        .then(r => r.json())
        .then(data => {
          if (!data.error) {
            setStockData(data)
            setPriceCache(prev => ({
              ...prev,
              [data.ticker]: { price: data.price, changePercent: data.changePercent, change: data.change }
            }))
          }
        })
        .catch(() => {})
    }, 5 * 60 * 1000) // 5 minutes
    return () => clearInterval(interval)
  }, [selectedTicker, selectedRange])

  /* eslint-enable react-hooks/exhaustive-deps */
  const isRangePositive = stockData ? parseFloat(stockData.rangeChangePercent || stockData.changePercent) >= 0 : true
  const chartColor = isRangePositive ? '#22c55e' : '#ef4444'
  const chartData = stockData?.chartData?.map(d => ({ ...d, date: formatDate(d.date, selectedRange) })) || []
  const tickCount = selectedRange === '3d' ? 3 : selectedRange === '7d' ? 7 : 8

  const currentNote = CATEGORY_TICKERS[selectedCategory]?.find(t => t.ticker === selectedTicker)?.note || ''
  const currentLabel = CATEGORY_TICKERS[selectedCategory]?.find(t => t.ticker === selectedTicker)?.label || selectedTicker

  return (
    <div className="min-h-screen bg-gray-950 text-gray-100">

      <header className="border-b border-gray-800 bg-gray-900">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <a href="/" className="inline-flex items-center gap-1.5 bg-blue-900 hover:bg-blue-700 border border-blue-700 text-blue-200 rounded-lg px-3 py-1.5 text-xs font-bold transition-colors mb-3">← Quantum Strategist</a>
          <div className="flex items-center justify-between mb-3">
            <div>
              <h1 className="text-xl font-bold text-white">📈 Market Intelligence</h1>
              <p className="text-xs text-gray-400">6-Category Market View -- Trading Economics Style -- Yahoo Finance Data</p>
            </div>
            
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

        {/* SIDE BY SIDE: Listing LEFT + Chart RIGHT */}
        <div className="flex gap-4" style={{ minHeight: '520px' }}>

          {/* LEFT -- Instrument Listing Table */}
          <div className="w-1/3 bg-gray-900 border border-gray-700 rounded-xl overflow-hidden flex flex-col">
            <div className="grid grid-cols-4 px-3 py-2 border-b border-gray-800 text-xs text-gray-500 uppercase tracking-wider shrink-0">
              <div className="col-span-2">Instrument</div>
              <div className="text-right">Change</div>
              <div className="text-right">%</div>
            </div>
            <div className="overflow-y-auto flex-1">
              {loadingCategory && (
                <div className="px-4 py-8 text-center text-xs text-gray-500">Loading {selectedCategory}...</div>
              )}
              {!loadingCategory && (CATEGORY_TICKERS[selectedCategory] || []).map(({ ticker, label }) => {
                const cached = priceCache[ticker]
                const pct = cached ? parseFloat(cached.changePercent) : null
                const isUp = pct !== null ? pct >= 0 : null
                return (
                  <button
                    key={ticker}
                    onClick={() => setSelectedTicker(ticker)}
                    className={`w-full grid grid-cols-4 px-3 py-2.5 border-b border-gray-800 hover:bg-gray-800 transition-colors text-left ${
                      selectedTicker === ticker ? 'bg-gray-800 border-l-2 border-l-blue-500' : ''
                    }`}
                  >
                    <div className="col-span-2">
                      <div className="text-xs font-bold text-white truncate">{label}</div>
                      <div className="text-xs text-gray-600 font-mono">{ticker}</div>
                    </div>
                    <div className={`text-right text-xs font-bold self-center ${isUp === null ? 'text-gray-500' : isUp ? 'text-green-400' : 'text-red-400'}`}>
                      {cached?.change ? (isUp ? '+' : '') + cached.change : '--'}
                    </div>
                    <div className="text-right self-center">
                      {pct !== null ? (
                        <span className={`text-xs font-bold px-1.5 py-0.5 rounded ${isUp ? 'bg-green-900 text-green-300' : 'bg-red-900 text-red-300'}`}>
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
          </div>

          {/* RIGHT -- Chart Card */}
          <div className="w-2/3 bg-gray-900 border border-gray-700 rounded-xl p-4 flex flex-col">

            {/* Range selector + range change label */}
            <div className="flex items-center justify-between mb-3 shrink-0">
              <div className="flex gap-2">
                {RANGES.map(range => (
                  <button
                    key={range}
                    onClick={() => setSelectedRange(range)}
                    className={`px-3 py-1 rounded-lg text-xs font-bold transition-colors ${
                      selectedRange === range
                        ? 'bg-blue-600 text-white'
                        : 'bg-gray-800 text-gray-400 hover:bg-gray-700 hover:text-white'
                    }`}
                  >
                    {range.toUpperCase()}
                  </button>
                ))}
              </div>
              {stockData && (
                <div className={`text-xs font-bold px-2 py-1 rounded ${isRangePositive ? 'text-green-400 bg-green-950' : 'text-red-400 bg-red-950'}`}>
                  {selectedRange.toUpperCase()}: {isRangePositive ? '+' : ''}{stockData.rangeChangePercent || stockData.changePercent}%
                </div>
              )}
            </div>

            {/* Chart */}
            <div className="flex-1 min-h-0">
              {loading && (
                <div className="flex items-center justify-center h-full text-gray-400 text-sm">Loading chart...</div>
              )}
              {error && (
                <div className="flex items-center justify-center h-full text-red-400 text-sm">⚠️ {error}</div>
              )}
              {!loading && !error && stockData && (
                <ResponsiveContainer width="100%" height="100%">
                  <AreaChart data={chartData} margin={{ top: 5, right: 10, left: 10, bottom: 5 }}>
                    <defs>
                      <linearGradient id="colorClose" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="5%" stopColor={chartColor} stopOpacity={0.3} />
                        <stop offset="95%" stopColor={chartColor} stopOpacity={0} />
                      </linearGradient>
                    </defs>
                    <CartesianGrid strokeDasharray="3 3" stroke="#1f2937" />
                    <XAxis dataKey="date" tick={{ fill: '#6b7280', fontSize: 9 }} tickLine={false} axisLine={false} interval={Math.floor(chartData.length / tickCount)} />
                    <YAxis tick={{ fill: '#6b7280', fontSize: 9 }} tickLine={false} axisLine={false} tickFormatter={v => '$' + v.toLocaleString()} width={60} domain={['auto', 'auto']} />
                    <Tooltip
                      contentStyle={{ backgroundColor: '#111827', border: '1px solid #374151', borderRadius: '8px', color: '#f9fafb', fontSize: '11px' }}
                      formatter={(value) => ['$' + Number(value).toLocaleString(), 'Price']}
                    />
                    <Area type="monotone" dataKey="close" stroke={chartColor} strokeWidth={2} fill="url(#colorClose)" dot={false} activeDot={{ r: 4, fill: chartColor }} />
                  </AreaChart>
                </ResponsiveContainer>
              )}
            </div>

            {/* Parameters under chart */}
            {stockData && !loading && (
              <div className="mt-3 shrink-0 border-t border-gray-800 pt-3">
                <div className="flex items-center justify-between mb-2">
                  <div>
                    <div className="text-white font-bold text-base">{currentLabel}</div>
                    <div className="text-xs text-gray-500 font-mono">{stockData.ticker} -- {stockData.name}</div>
                  </div>
                  <div className="text-right">
                    <div className="text-white font-bold text-lg">{formatPrice(stockData.price)}</div>
                    {priceCache[selectedTicker] && (
                      <div className={`text-xs font-bold ${parseFloat(priceCache[selectedTicker].changePercent) >= 0 ? 'text-green-400' : 'text-red-400'}`}>
                        {parseFloat(priceCache[selectedTicker].changePercent) >= 0 ? '▲' : '▼'} {priceCache[selectedTicker].change} ({priceCache[selectedTicker].changePercent}%) today
                      </div>
                    )}
                  </div>
                </div>
                {/* Instrument description note */}
                {currentNote && (
                  <div className="bg-gray-800 rounded-lg px-3 py-2 text-xs text-gray-400 leading-relaxed">
                    <span className="text-gray-300 font-bold">Note: </span>{currentNote}
                  </div>
                )}
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
