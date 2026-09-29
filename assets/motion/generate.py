from pathlib import Path
<<<<<<< HEAD
ROOT=Path(__file__).resolve().parent

def w(name, s): (ROOT/name).write_text(s, encoding='utf-8')

w('hero.svg', '''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="390" viewBox="0 0 1200 390"><defs><linearGradient id="b" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#030712"/><stop offset=".5" stop-color="#071426"/><stop offset="1" stop-color="#031b19"/></linearGradient><linearGradient id="c"><stop stop-color="#22d3ee"/><stop offset="1" stop-color="#34d399"/></linearGradient><radialGradient id="h"><stop stop-color="#22d3ee" stop-opacity=".25"/><stop offset="1" stop-color="#22d3ee" stop-opacity="0"/></radialGradient><filter id="g"><feGaussianBlur stdDeviation="4" result="x"/><feMerge><feMergeNode in="x"/><feMergeNode in="SourceGraphic"/></feMerge></filter><pattern id="p" width="32" height="32" patternUnits="userSpaceOnUse"><path d="M32 0H0V32" fill="none" stroke="#94a3b8" stroke-opacity=".05"/></pattern></defs><rect width="1200" height="390" rx="28" fill="url(#b)"/><rect width="1200" height="390" rx="28" fill="url(#p)"/><circle cx="980" cy="180" r="240" fill="url(#h)"><animate attributeName="r" values="210;275;210" dur="7s" repeatCount="indefinite"/></circle><g fill="none" stroke="url(#c)" stroke-width="1.5" opacity=".42" stroke-dasharray="4 12"><path d="M700 72 C790 25 830 125 905 78 S1030 38 1160 112"><animate attributeName="stroke-dashoffset" from="0" to="-160" dur="4s" repeatCount="indefinite"/></path><path d="M690 300 C780 250 835 345 915 278 S1060 220 1180 285"><animate attributeName="stroke-dashoffset" from="0" to="-170" dur="5s" repeatCount="indefinite"/></path><path d="M760 205 C830 165 870 230 935 190 S1050 155 1170 205"><animate attributeName="stroke-dashoffset" from="0" to="-120" dur="3.5s" repeatCount="indefinite"/></path></g><g fill="#67e8f9" filter="url(#g)"><circle r="4"><animateMotion dur="3.8s" repeatCount="indefinite" path="M700 72 C790 25 830 125 905 78 S1030 38 1160 112"/></circle><circle r="3"><animateMotion dur="4.6s" begin="-2s" repeatCount="indefinite" path="M690 300 C780 250 835 345 915 278 S1060 220 1180 285"/></circle></g><g transform="translate(915 190)"><circle r="82" fill="#06101e" stroke="#22d3ee" stroke-opacity=".2"><animate attributeName="r" values="76;88;76" dur="4s" repeatCount="indefinite"/></circle><circle r="57" fill="none" stroke="url(#c)" stroke-width="2" stroke-dasharray="5 8"><animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="12s" repeatCount="indefinite"/></circle><circle r="32" fill="#071421" stroke="#67e8f9" stroke-width="2" filter="url(#g)"/><text y="-3" text-anchor="middle" fill="#e2e8f0" font-family="monospace" font-size="11" font-weight="700">AI CORE</text><text y="14" text-anchor="middle" fill="#67e8f9" font-family="monospace" font-size="8">ONLINE</text></g><g font-family="Inter,Segoe UI,Arial,sans-serif"><text x="60" y="68" fill="#67e8f9" font-family="monospace" font-size="12" letter-spacing="3">/SAHAJ.SALIYA :: AI SYSTEMS LAB</text><text x="56" y="143" fill="#f8fafc" font-size="57" font-weight="750">Sahaj Saliya</text><text x="60" y="181" fill="#cbd5e1" font-size="20">Engineering systems that retrieve · reason · validate · act.</text><text x="60" y="218" fill="#94a3b8" font-size="14">Agentic AI  /  RAG  /  Security  /  Computer Vision  /  Research</text><g font-family="monospace" font-size="11"><rect x="60" y="250" width="118" height="32" rx="8" fill="#071827" stroke="#164e63"/><text x="78" y="270" fill="#67e8f9">◉ RAG</text><rect x="188" y="250" width="150" height="32" rx="8" fill="#0b1022" stroke="#312e81"/><text x="206" y="270" fill="#a5b4fc">◉ AGENTIC AI</text><rect x="348" y="250" width="142" height="32" rx="8" fill="#061a17" stroke="#065f46"/><text x="366" y="270" fill="#86efac">◉ SECURE AI</text></g><text x="60" y="330" fill="#64748b" font-family="monospace" font-size="11">SYSTEM STATUS</text><text x="155" y="330" fill="#34d399" font-family="monospace" font-size="11">● BUILDING</text><text x="270" y="330" fill="#64748b" font-family="monospace" font-size="11">MODE:</text><text x="315" y="330" fill="#67e8f9" font-family="monospace" font-size="11">RESEARCH</text><rect x="60" y="346" width="330" height="2" rx="1" fill="url(#c)"><animate attributeName="width" values="35;330;90;330" dur="5s" repeatCount="indefinite"/></rect></g></svg>''')

w('multi-agent-rag.svg', '''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="470" viewBox="0 0 1200 470"><defs><linearGradient id="b" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#030712"/><stop offset="1" stop-color="#071b1b"/></linearGradient><linearGradient id="w"><stop stop-color="#22d3ee"/><stop offset=".5" stop-color="#818cf8"/><stop offset="1" stop-color="#34d399"/></linearGradient><filter id="g"><feGaussianBlur stdDeviation="3" result="x"/><feMerge><feMergeNode in="x"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs><rect x="2" y="2" width="1196" height="466" rx="26" fill="url(#b)" stroke="#173047"/><text x="38" y="48" fill="#f8fafc" font-family="Inter,Arial" font-size="26" font-weight="700">Multi-Agent RAG</text><text x="38" y="72" fill="#64748b" font-family="monospace" font-size="11">ENTERPRISE AGENTIC RAG ORCHESTRATOR // LIVE EXECUTION MODEL</text><rect x="38" y="90" width="1124" height="1" fill="#173047"/><g fill="none" stroke="url(#w)" stroke-width="2" stroke-dasharray="7 10" opacity=".62"><path d="M135 177 H245"/><path d="M365 177 H490"/><path d="M610 177 H735"/><path d="M855 177 H980"/><path d="M550 230 C550 285 430 300 340 335"/><path d="M650 230 C650 285 770 300 860 335"/><animate attributeName="stroke-dashoffset" from="0" to="-68" dur="2.7s" repeatCount="indefinite"/></g><g fill="#67e8f9" filter="url(#g)"><circle r="4"><animateMotion dur="2.6s" repeatCount="indefinite" path="M135 177 H245"/></circle><circle r="4"><animateMotion dur="3s" begin="-.6s" repeatCount="indefinite" path="M365 177 H490"/></circle><circle r="4"><animateMotion dur="2.8s" begin="-1.2s" repeatCount="indefinite" path="M610 177 H735"/></circle><circle r="4"><animateMotion dur="3.1s" begin="-1.8s" repeatCount="indefinite" path="M855 177 H980"/></circle></g><g font-family="monospace" font-size="10" text-anchor="middle"><g><rect x="38" y="140" width="97" height="74" rx="13" fill="#071827" stroke="#22d3ee"/><text x="86" y="166" fill="#e2e8f0">GATEWAY</text><text x="86" y="185" fill="#67e8f9">FastAPI</text><text x="86" y="201" fill="#64748b">auth + rate</text></g><g><rect x="245" y="140" width="120" height="74" rx="13" fill="#0b1022" stroke="#818cf8"/><text x="305" y="166" fill="#e2e8f0">SUPERVISOR</text><text x="305" y="185" fill="#a5b4fc">route query</text><text x="305" y="201" fill="#64748b">LLM classifier</text></g><g><rect x="490" y="140" width="120" height="74" rx="13" fill="#111024" stroke="#f59e0b"/><text x="550" y="166" fill="#e2e8f0">CRAG</text><text x="550" y="185" fill="#fde68a">grade → rewrite</text><text x="550" y="201" fill="#64748b">max 2 loops</text></g><g><rect x="735" y="140" width="120" height="74" rx="13" fill="#071a17" stroke="#34d399"/><text x="795" y="166" fill="#e2e8f0">RERANK</text><text x="795" y="185" fill="#86efac">hybrid search</text><text x="795" y="201" fill="#64748b">dense + BM25</text></g><g><rect x="980" y="140" width="120" height="74" rx="13" fill="#071827" stroke="#22d3ee"/><text x="1040" y="166" fill="#e2e8f0">VALIDATOR</text><text x="1040" y="185" fill="#67e8f9">re-ground</text><text x="1040" y="201" fill="#64748b">answer + source</text></g></g><g font-family="monospace" font-size="10" text-anchor="middle"><rect x="250" y="315" width="180" height="58" rx="12" fill="#071827" stroke="#164e63"/><text x="340" y="339" fill="#67e8f9">QDRANT ANN CACHE</text><text x="340" y="357" fill="#64748b">cosine ≥ 0.96</text><rect x="510" y="315" width="180" height="58" rx="12" fill="#071827" stroke="#334155"/><text x="600" y="339" fill="#cbd5e1">SPECIALIST AGENTS</text><text x="600" y="357" fill="#64748b">DB · TOOL · CHAT · RAG</text><rect x="770" y="315" width="180" height="58" rx="12" fill="#071827" stroke="#065f46"/><text x="860" y="339" fill="#86efac">REDIS MEMORY</text><text x="860" y="357" fill="#64748b">sessions + queues</text></g><rect x="38" y="400" width="1124" height="42" rx="12" fill="#050b14" stroke="#17283a"/><g font-family="monospace" font-size="10"><text x="58" y="426" fill="#67e8f9">RAGAS</text><text x="106" y="426" fill="#e2e8f0">0.81 faithfulness</text><text x="265" y="426" fill="#67e8f9">PRECISION</text><text x="340" y="426" fill="#e2e8f0">1.00</text><text x="400" y="426" fill="#67e8f9">RECALL</text><text x="458" y="426" fill="#e2e8f0">0.90</text><text x="520" y="426" fill="#67e8f9">RELEVANCY</text><text x="605" y="426" fill="#e2e8f0">0.75</text><text x="680" y="426" fill="#67e8f9">STACK</text><text x="732" y="426" fill="#94a3b8">LangGraph · Qdrant · Redis · FastAPI · Next.js</text></g></svg>''')

w('constellation.svg', '''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="280" viewBox="0 0 1200 280"><defs><linearGradient id="g"><stop stop-color="#22d3ee"/><stop offset=".5" stop-color="#818cf8"/><stop offset="1" stop-color="#34d399"/></linearGradient><filter id="b"><feGaussianBlur stdDeviation="3" result="x"/><feMerge><feMergeNode in="x"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs><rect width="1200" height="280" rx="24" fill="#030712" stroke="#17283a"/><g fill="none" stroke="#1e293b"><path d="M130 140 L340 65 L575 145 L805 72 L1050 140 L875 220 L610 175 L340 215 Z"/></g><g fill="none" stroke="url(#g)" stroke-width="1.5" stroke-dasharray="4 10" opacity=".65"><path d="M130 140 L340 65 L575 145 L805 72 L1050 140"><animate attributeName="stroke-dashoffset" from="0" to="-140" dur="4s" repeatCount="indefinite"/></path><path d="M340 215 L575 145 L875 220 L1050 140"><animate attributeName="stroke-dashoffset" from="0" to="-140" dur="5s" repeatCount="indefinite"/></path></g><g fill="#67e8f9" filter="url(#b)"><circle cx="130" cy="140" r="5"/><circle cx="340" cy="65" r="5"/><circle cx="575" cy="145" r="7"><animate attributeName="r" values="6;10;6" dur="2.5s" repeatCount="indefinite"/></circle><circle cx="805" cy="72" r="5"/><circle cx="1050" cy="140" r="5"/><circle cx="875" cy="220" r="5"/><circle cx="340" cy="215" r="5"/></g><g font-family="monospace" font-size="11"><text x="86" y="175" fill="#94a3b8">VISION</text><text x="300" y="42" fill="#94a3b8">GEN AI</text><text x="520" y="125" fill="#67e8f9">AI SYSTEMS</text><text x="770" y="50" fill="#94a3b8">SECURITY</text><text x="1000" y="175" fill="#94a3b8">CLOUD</text><text x="820" y="252" fill="#94a3b8">INFRA</text><text x="285" y="247" fill="#94a3b8">RESEARCH</text></g><text x="600" y="55" text-anchor="middle" fill="#f8fafc" font-family="Inter,Arial" font-size="18" font-weight="700">ONE LAB · MANY SYSTEMS</text></svg>''')

w('divider.svg', '''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="54" viewBox="0 0 1200 54"><defs><linearGradient id="g"><stop stop-color="#22d3ee" stop-opacity="0"/><stop offset=".48" stop-color="#22d3ee"/><stop offset=".52" stop-color="#34d399"/><stop offset="1" stop-color="#34d399" stop-opacity="0"/></linearGradient></defs><path d="M0 27H1200" stroke="url(#g)" stroke-width="1.5" stroke-dasharray="6 18"><animate attributeName="stroke-dashoffset" from="0" to="-144" dur="3s" repeatCount="indefinite"/></path><circle cx="600" cy="27" r="4" fill="#67e8f9"><animate attributeName="r" values="3;7;3" dur="2s" repeatCount="indefinite"/></circle><circle cx="600" cy="27" r="12" fill="none" stroke="#67e8f9" stroke-opacity=".2"><animate attributeName="r" values="6;20;6" dur="2.5s" repeatCount="indefinite"/></circle></svg>''')
print('generated')
=======

ROOT = Path(__file__).resolve().parent

HERO = r'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="330" viewBox="0 0 1200 330" role="img" aria-labelledby="title desc">
<title id="title">Sahaj Saliya — AI Systems and Research</title>
<desc id="desc">Animated technical profile banner with an agentic AI network, data flow and research focus.</desc>
<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#05070d"/><stop offset="0.55" stop-color="#0a1020"/><stop offset="1" stop-color="#071b1a"/></linearGradient>
  <linearGradient id="line" x1="0" y1="0" x2="1" y2="0"><stop stop-color="#67e8f9"/><stop offset="0.5" stop-color="#818cf8"/><stop offset="1" stop-color="#34d399"/></linearGradient>
  <radialGradient id="orb"><stop stop-color="#67e8f9" stop-opacity=".9"/><stop offset="1" stop-color="#67e8f9" stop-opacity="0"/></radialGradient>
  <filter id="glow"><feGaussianBlur stdDeviation="5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
  <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M40 0H0V40" fill="none" stroke="#94a3b8" stroke-opacity=".07"/></pattern>
</defs>
<rect width="1200" height="330" rx="22" fill="url(#bg)"/>
<rect width="1200" height="330" rx="22" fill="url(#grid)"/>
<ellipse cx="930" cy="85" rx="260" ry="150" fill="url(#orb)" opacity=".12">
  <animate attributeName="opacity" values=".06;.18;.06" dur="5s" repeatCount="indefinite"/>
</ellipse>

<!-- flowing network -->
<g fill="none" stroke="url(#line)" stroke-width="2" opacity=".45" stroke-linecap="round">
  <path d="M760 55 C850 10 900 115 990 62 S1110 35 1170 90" stroke-dasharray="8 12">
    <animate attributeName="stroke-dashoffset" from="0" to="-80" dur="4s" repeatCount="indefinite"/>
  </path>
  <path d="M735 245 C835 205 875 285 955 225 S1080 175 1175 225" stroke-dasharray="6 14">
    <animate attributeName="stroke-dashoffset" from="0" to="-80" dur="5s" repeatCount="indefinite"/>
  </path>
</g>

<!-- moving data packets -->
<g fill="#67e8f9" filter="url(#glow)">
  <circle r="4"><animateMotion dur="3.8s" repeatCount="indefinite" path="M760 55 C850 10 900 115 990 62 S1110 35 1170 90"/></circle>
  <circle r="3"><animateMotion dur="4.6s" begin="-2s" repeatCount="indefinite" path="M735 245 C835 205 875 285 955 225 S1080 175 1175 225"/></circle>
</g>

<!-- agent nodes -->
<g font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="11" text-anchor="middle">
  <g transform="translate(820 92)"><circle r="34" fill="#0b1220" stroke="#67e8f9" stroke-width="2"><animate attributeName="r" values="31;36;31" dur="3s" repeatCount="indefinite"/></circle><text y="4" fill="#c4f1f9">SUPERVISOR</text></g>
  <g transform="translate(970 65)"><circle r="28" fill="#0b1220" stroke="#818cf8" stroke-width="2"/><text y="4" fill="#c7d2fe">RAG</text></g>
  <g transform="translate(1030 220)"><circle r="28" fill="#0b1220" stroke="#34d399" stroke-width="2"/><text y="4" fill="#bbf7d0">VALIDATE</text></g>
  <g transform="translate(870 240)"><circle r="28" fill="#0b1220" stroke="#f59e0b" stroke-width="2"/><text y="4" fill="#fde68a">TOOLS</text></g>
</g>

<g font-family="Inter,Segoe UI,Arial,sans-serif">
  <text x="62" y="105" fill="#94a3b8" font-size="15" letter-spacing="4">AI SYSTEMS • AGENTIC AI • SECURITY • RESEARCH</text>
  <text x="58" y="164" fill="#f8fafc" font-size="54" font-weight="700" letter-spacing="-2">Sahaj Saliya</text>
  <text x="62" y="205" fill="#cbd5e1" font-size="20">Building intelligent systems that retrieve, reason, validate and act.</text>
  <g fill="#67e8f9" font-size="13" font-family="ui-monospace, SFMono-Regular, Menlo, monospace">
    <text x="62" y="250">[ RAG ]</text><text x="145" y="250">[ MULTI-AGENT ]</text><text x="300" y="250">[ COMPUTER VISION ]</text>
    <text x="62" y="278" fill="#94a3b8">Research • Infrastructure • Secure AI</text>
  </g>
  <rect x="62" y="292" width="330" height="2" rx="1" fill="url(#line)">
    <animate attributeName="width" values="90;330;90" dur="4s" repeatCount="indefinite"/>
  </rect>
</g>
</svg>'''

RAG = r'''<svg xmlns="http://www.w3.org/2000/svg" width="1100" height="300" viewBox="0 0 1100 300" role="img" aria-labelledby="title desc">
<title id="title">Multi-Agent RAG — Enterprise Agentic RAG Orchestrator</title>
<desc id="desc">Animated architecture card showing supervisor, retrieval, database, tools and validation agents.</desc>
<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#07111f"/><stop offset="1" stop-color="#071b18"/></linearGradient>
  <linearGradient id="wire"><stop stop-color="#67e8f9"/><stop offset="1" stop-color="#34d399"/></linearGradient>
  <filter id="glow"><feGaussianBlur stdDeviation="3" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
</defs>
<rect x="2" y="2" width="1096" height="296" rx="20" fill="url(#bg)" stroke="#1e3a4a"/>
<g font-family="Inter,Segoe UI,Arial,sans-serif">
<text x="30" y="42" fill="#f8fafc" font-size="25" font-weight="700">Multi-Agent RAG</text>
<text x="30" y="66" fill="#94a3b8" font-size="13">Supervisor → Worker → Validator • CRAG • Hybrid Retrieval • Secure Tooling</text>

<g fill="none" stroke="url(#wire)" stroke-width="2" stroke-dasharray="7 10" opacity=".65">
 <path d="M170 145 H310"/><path d="M420 145 H540"/><path d="M650 145 H790"/><path d="M900 145 H1010"/>
 <animate attributeName="stroke-dashoffset" from="0" to="-68" dur="2.8s" repeatCount="indefinite"/>
</g>
<g filter="url(#glow)" fill="#67e8f9">
 <circle r="4"><animateMotion dur="2.8s" repeatCount="indefinite" path="M170 145 H310"/></circle>
 <circle r="4"><animateMotion dur="3.2s" begin="-.8s" repeatCount="indefinite" path="M420 145 H540"/></circle>
 <circle r="4"><animateMotion dur="3s" begin="-1.4s" repeatCount="indefinite" path="M650 145 H790"/></circle>
</g>

<g font-size="11" text-anchor="middle">
 <g><rect x="55" y="112" width="115" height="66" rx="12" fill="#0b1726" stroke="#67e8f9"/><text x="112" y="140" fill="#e2e8f0">SUPERVISOR</text><text x="112" y="158" fill="#67e8f9">route query</text></g>
 <g><rect x="310" y="112" width="110" height="66" rx="12" fill="#0b1726" stroke="#818cf8"/><text x="365" y="140" fill="#e2e8f0">CRAG</text><text x="365" y="158" fill="#a5b4fc">retrieve + grade</text></g>
 <g><rect x="540" y="112" width="110" height="66" rx="12" fill="#0b1726" stroke="#f59e0b"/><text x="595" y="140" fill="#e2e8f0">RERANK</text><text x="595" y="158" fill="#fde68a">CrossEncoder</text></g>
 <g><rect x="790" y="112" width="110" height="66" rx="12" fill="#0b1726" stroke="#34d399"/><text x="845" y="140" fill="#e2e8f0">AGENTS</text><text x="845" y="158" fill="#86efac">DB / Tool / Chat</text></g>
 <g><rect x="1010" y="112" width="65" height="66" rx="12" fill="#0b1726" stroke="#67e8f9"/><text x="1042" y="140" fill="#e2e8f0">VAL</text><text x="1042" y="158" fill="#67e8f9">ground</text></g>
</g>

<g font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="12">
 <text x="30" y="225" fill="#67e8f9">RAGAS</text><text x="90" y="225" fill="#cbd5e1">0.81 faithfulness</text>
 <text x="275" y="225" fill="#67e8f9">CTX</text><text x="320" y="225" fill="#cbd5e1">1.00 precision</text>
 <text x="490" y="225" fill="#67e8f9">CACHE</text><text x="550" y="225" fill="#cbd5e1">Qdrant ANN ≥ 0.96</text>
 <text x="760" y="225" fill="#67e8f9">SECURITY</text><text x="845" y="225" fill="#cbd5e1">API auth • rate limit • injection guard</text>
 <text x="30" y="258" fill="#64748b">FastAPI</text><text x="105" y="258" fill="#64748b">LangGraph</text><text x="205" y="258" fill="#64748b">Qdrant</text><text x="280" y="258" fill="#64748b">BM25</text><text x="350" y="258" fill="#64748b">Redis</text><text x="420" y="258" fill="#64748b">RAGAS</text><text x="505" y="258" fill="#64748b">Next.js</text>
</g>
</g>
</svg>'''

DIVIDER = r'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="44" viewBox="0 0 1200 44"><defs><linearGradient id="g"><stop stop-color="#67e8f9" stop-opacity="0"/><stop offset=".5" stop-color="#67e8f9"/><stop offset="1" stop-color="#34d399" stop-opacity="0"/></linearGradient></defs><path d="M0 22H1200" stroke="url(#g)" stroke-width="2" stroke-dasharray="12 18"><animate attributeName="stroke-dashoffset" from="0" to="-120" dur="3s" repeatCount="indefinite"/></path><circle cx="600" cy="22" r="4" fill="#67e8f9"><animate attributeName="r" values="3;6;3" dur="2s" repeatCount="indefinite"/></circle></svg>'''

(ROOT / 'hero.svg').write_text(HERO, encoding='utf-8')
(ROOT / 'multi-agent-rag.svg').write_text(RAG, encoding='utf-8')
(ROOT / 'divider.svg').write_text(DIVIDER, encoding='utf-8')
print('Generated hero.svg, multi-agent-rag.svg, divider.svg')
>>>>>>> ae7521f548dd7215d1602cf0f95a2cca22f442ca
