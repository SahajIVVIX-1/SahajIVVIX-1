"""Write README.md from the generated assets. Run from the repo root."""
BASE = "https://raw.githubusercontent.com/SahajIVVIX-1/SahajIVVIX-1/main/assets"
GH = "https://github.com/SahajIVVIX-1"


def pic(name, alt, width=None, height=None):
    size = (f' width="{width}"' if width else "") + (f' height="{height}"' if height else "")
    return (f'<picture><source media="(prefers-color-scheme: dark)" srcset="{BASE}/{name}-dark.svg">'
            f'<source media="(prefers-color-scheme: light)" srcset="{BASE}/{name}-light.svg">'
            f'<img alt="{alt}" src="{BASE}/{name}-dark.svg"{size}></picture>')


def link(href, inner):
    return f'<a href="{href}">{inner}</a>'


def themed(dark_url, light_url, alt, extra=""):
    return (f'<picture><source media="(prefers-color-scheme: dark)" srcset="{dark_url}">'
            f'<source media="(prefers-color-scheme: light)" srcset="{light_url}">'
            f'<img alt="{alt}" src="{dark_url}"{extra}></picture>')


BUTTONS = [
    ("portfolio", "Portfolio", "https://info.sahaj.si/"),
    ("linkedin", "LinkedIn", "https://www.linkedin.com/in/sahajs59/"),
    ("x", "X", "https://x.com/SahajS59"),
    ("medium", "Medium", "https://sahajs59.medium.com"),
    ("resume", "Résumé", f"https://raw.githubusercontent.com/SahajIVVIX-1/SahajIVVIX-1/main/Resume_WIcon.pdf"),
    ("leetcode", "LeetCode", "https://leetcode.com/sahajs59"),
]
buttons = "\n".join(link(u, pic(f"btn-{k}", a, height=44)) for k, a, u in BUTTONS)


def section(key, title):
    return f'<br/>\n\n{pic(f"section-{key}", title, width="100%")}\n'


def card(key, repo, alt):
    return link(f"{GH}/{repo}", pic(f"card-{key}", alt, width="49%"))


# palette for third-party stat cards (kept in sync with build.py THEMES)
D = dict(bg="141413", text="F5F4EE", muted="A8A598", accent="D97757", line="35332D")
L = dict(bg="FAF9F5", text="1A1915", muted="5C5A52", accent="BD5A37", line="DCD7CA")


def stats_url(p):
    return (f"https://github-readme-stats.vercel.app/api?username=SahajIVVIX-1&show_icons=true&count_private=true"
            f"&include_all_commits=true&hide_border=true&bg_color={p['bg']}&title_color={p['accent']}"
            f"&text_color={p['text']}&icon_color={p['accent']}&ring_color={p['accent']}")


def langs_url(p):
    return (f"https://github-readme-stats.vercel.app/api/top-langs/?username=SahajIVVIX-1&layout=compact&langs_count=8"
            f"&hide_border=true&bg_color={p['bg']}&title_color={p['accent']}&text_color={p['text']}")


def streak_url(p):
    return (f"https://streak-stats.demolab.com?user=SahajIVVIX-1&hide_border=true&background={p['bg']}&ring={p['accent']}"
            f"&fire={p['accent']}&currStreakNum={p['text']}&sideNums={p['text']}&currStreakLabel={p['accent']}"
            f"&sideLabels={p['muted']}&dates={p['muted']}&stroke={p['line']}")


def graph_url(p):
    return (f"https://github-readme-activity-graph.vercel.app/graph?username=SahajIVVIX-1&hide_border=true&area=true"
            f"&bg_color={p['bg']}&color={p['muted']}&line={p['accent']}&point={p['text']}&area_color={p['accent']}")


ISSUER = {
    "IBM": "https://img.shields.io/badge/IBM-052FAD?style=flat-square&logo=ibm&logoColor=white",
    "AWS": "https://img.shields.io/badge/AWS-232F3E?style=flat-square&logo=amazonwebservices&logoColor=white",
    "Anthropic": "https://img.shields.io/badge/Anthropic-191919?style=flat-square&logo=anthropic&logoColor=white",
    "Dataiku": "https://img.shields.io/badge/Dataiku-2AB1AC?style=flat-square",
    "IIT Ropar · NPTEL": "https://img.shields.io/badge/IIT_Ropar_·_NPTEL-C2410C?style=flat-square",
    "Oracle": "https://img.shields.io/badge/Oracle-F80000?style=flat-square&logo=oracle&logoColor=white",
    "Udemy": "https://img.shields.io/badge/Udemy-A435F0?style=flat-square&logo=udemy&logoColor=white",
    "Guinness World Records": "https://img.shields.io/badge/Guinness_World_Records-000000?style=flat-square",
}
CERTS = [
    ("AI / GenAI & agents", [("Agentic AI with LangChain and LangGraph", "IBM"), ("Fundamentals of Building AI Agents", "IBM"),
                             ("AWS Generative AI and AI Agents with Amazon Bedrock", "AWS"), ("Building with the Claude API", "Anthropic"),
                             ("Claude Code 101", "Anthropic"), ("Dataiku Generative AI Practitioner", "Dataiku")]),
    ("ML / DL", [("Deep Learning", "IIT Ropar · NPTEL")]),
    ("Cloud", [("Oracle Cloud and AI", "Oracle")]),
    ("Other", [("Data Structure & Algorithm With Python", "Udemy"), ("2,121-Word Book", "Guinness World Records")]),
]
cert_rows = []
for group, items in CERTS:
    cert_rows.append(f'<tr><td colspan="2"><sub><b>{group.upper().replace("&", "&amp;")}</b></sub></td></tr>')
    for name, iss in items:
        cert_rows.append(f'<tr><td>{name.replace("&", "&amp;")}</td><td><img src="{ISSUER[iss]}" alt="{iss}"/></td></tr>')
cert_table = "\n".join(cert_rows)

README = f"""<!--
  Profile README for SahajIVVIX-1.
  Every visual in assets/ is a self-hosted SVG with its fonts embedded, generated by assets/build/build.py.
  Edit content there (or this file via assets/build/make_readme.py), re-run, commit.
-->

<div align="center">

{pic("hero", "Sahaj Saliya. AI Engineer and Researcher building agents that retrieve, reason and learn. Focus: LLMs, Agentic AI, RAG, Reinforcement Learning.", width="100%")}

{buttons}

{pic("impact", "RAGAS faithfulness 0.81 and context precision 1.00 on the Multi-Agent RAG orchestrator; 37% fewer false-positive trading signals; 2 papers presented at IEEE AIMV 2025", width="100%")}

</div>

{section("about", "01 About")}

I'm an AI engineer and researcher in my final year of **B.Tech in Information & Communication Technology at PDEU, Gandhinagar** (CGPA 8.5, graduating May 2027). I build **LLM agents that retrieve, reason and learn**: multi-agent RAG with self-correcting retrieval, RL environments where an LLM learns a task, and the infrastructure that keeps them measurable in production.

My rule is simple: ship it, benchmark it, then make it smarter. I want the projects here to work as open-source tools, publications or products, and I build them on limited compute, so efficiency is part of the design.

<details>
<summary><b>Open the live terminal card</b> <sub>(regenerated daily by a GitHub Action)</sub></summary>
<br/>
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/SahajIVVIX-1/SahajIVVIX-1/main/dark_mode.svg">
  <img alt="Sahaj Saliya terminal profile card" src="https://raw.githubusercontent.com/SahajIVVIX-1/SahajIVVIX-1/main/light_mode.svg" width="100%">
</picture>
</details>

{section("experience", "02 Experience")}

{pic("experience", "Research & Innovation Intern, HNNOIX Private Limited, May to Jul 2026: built an LLM Gateway, RAG Runtime, AI Memory Layer and Knowledge Base for 6G R&D. Freelance Financial AI Engineer, Dec 2024 to Jun 2025: shipped 2 autonomous trading-signal systems, cut false-positive signals by 37%, built a CrewAI earnings-analysis pipeline.", width="100%")}

{section("work", "03 Selected work")}

### 01 &nbsp;[Enterprise Agentic RAG Orchestrator]({GH}/Multi-Agent-RAG)
*Production-grade multi-agent RAG with a self-correcting retrieval loop.* A **Supervisor** routes each query to Corrective RAG, NL-to-SQL or a human-in-the-loop email tool, and a **Validator** checks the answer before it leaves. Built with LangGraph, FastAPI, Qdrant, Redis and RAGAS.

{link(f"{GH}/Multi-Agent-RAG", pic("rag-pipeline", "Architecture: query, prompt-injection guard, Qdrant semantic cache, supervisor, three workers (Corrective RAG, NL-to-SQL, human-in-the-loop), validator, answer. Inside the CRAG worker: hybrid dense + BM25 retrieval, CrossEncoder rerank, LLM grader with query rewrite.", width="100%"))}

<p>
{card("openenv", "open-env-nuclei", "OpenEnv RL data-cleaning agent: a Llama 3 agent in a custom Q-Learning environment")}
{card("xai", "student-performance-platform", "Explainable Student-Performance Platform: 9 ML/DL models, SHAP + LIME agreement, MLflow")}
</p>
<p>
{card("dcgan", "Modern-DCGAN-Reproducibility", "Modern DCGAN reproducibility study: LSGAN + Spectral Normalization")}
{card("sentinel", "SentinelProxy-Suite", "SentinelProxy Suite: local HTTPS proxy and DNS server that block malicious domains")}
</p>

{link(f"{GH}/SIH-AI-Gyani", pic("card-microplastic", "Microplastic Detection for Smart India Hackathon: YOLOv11 fine-tuned for particle detection and size estimation", width="100%"))}

<sub>OpenEnv is live on Hugging Face Spaces: <a href="https://chetangadhiya017-data-cleaning-env.hf.space">try the demo</a>.</sub>

<details>
<summary><b>Desktop and automation tools</b> <sub>Python · PyQt6</sub></summary>
<br/>

| Tool | What it does | Stack |
|---|---|---|
| [vMix Manager]({GH}/vMix-Manager) | Offline XML engine for batch-editing `.vmix` productions with GUID-safe cloning | Python, PyQt6 |
| [PyEnv Launcher]({GH}/PyEnv-Launcher-Project) | Desktop control center for Python projects, environments and packages | PyQt6 |
| [Smaran Reminder]({GH}/Smaran-Reminder-App) | Non-intrusive tray reminders with deep scheduling and burst mode | PyQt6 |
| [Video Analyzer & Scroller]({GH}/Video-Analyzer-Scroller) | FFmpeg folder auditing to Excel + PDF, and a 1080p scrolling-video generator | OpenCV, FFmpeg |

</details>

{section("toolkit", "04 Toolkit")}

{pic("toolkit", "Toolkit. GenAI and agents: LangChain, LangGraph, CrewAI, AWS Bedrock, Hugging Face Transformers, Pydantic, RAGAS. ML, DL, RL: PyTorch, TensorFlow, scikit-learn, XGBoost, CatBoost, LightGBM, Q-Learning, SHAP, LIME. Retrieval and data: Qdrant, ChromaDB, PostgreSQL, MongoDB, Redis, Hadoop, SQL. Vision and OCR: OpenCV, YOLOv11, Kraken OCR, ComfyUI. MLOps and infra: MLflow, Docker, Kubernetes, FastAPI, Flask, Streamlit, HF Spaces, GitHub Actions, AWS, GCP, Linux. Languages: Python, C++, SQL, MATLAB.", width="100%")}

{section("recognition", "05 Recognition")}

<table>
<tr>
<td width="46%" valign="top">

**Achievements**

- **IEEE AIMV 2025:** presented 2 papers, on Deepfake Detection and Crime Prediction
- **Code4Cause 2.0:** national-level finalist, NSUT Delhi
- **ISRO-IIRS:** AI/ML for Geodata Analysis
- **IEEE Operations Lead:** coordinated research-paper presentations
- **GDG Gandhinagar:** AI and Firebase workshops

</td>
<td width="54%" valign="top">

**Certifications**

<table>
<tr><th align="left">Certificate</th><th align="left">Issuer</th></tr>
{cert_table}
</table>

</td>
</tr>
</table>

{section("signals", "06 Signals")}

<div align="center">

{themed(stats_url(D), stats_url(L), "GitHub stats", ' height="165"')}
{themed(langs_url(D), langs_url(L), "Top languages", ' height="165"')}

{themed(streak_url(D), streak_url(L), "GitHub streak")}

{themed(graph_url(D), graph_url(L), "Contribution activity graph", ' width="100%"')}

<a href="https://leetcode.com/sahajs59">{themed("https://leetcard.jacoblin.cool/sahajs59?theme=dark&font=Fira%20Code&ext=heatmap", "https://leetcard.jacoblin.cool/sahajs59?theme=light&font=Fira%20Code&ext=heatmap", "LeetCode stats")}</a>

</div>

<br/>

<div align="center">

{pic("footer", "Open to AI Engineering and Research roles. Building open-source tools, publications and products around LLM agents.", width="100%")}

{buttons}

<br/><br/>
<img src="https://komarev.com/ghpvc/?username=SahajIVVIX-1&style=flat-square&color=D97757&label=profile+views" alt="profile views"/>

</div>
"""

if __name__ == "__main__":
    with open("README.md", "w", encoding="utf-8") as fh:
        fh.write(README)
    print(f"README.md: {len(README.splitlines())} lines")
