from pathlib import Path

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
