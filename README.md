<!-- ═══════════════════════════════  HEADER  ═══════════════════════════════ -->
<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=6,11,20&height=230&section=header&text=Sahaj%20Saliya&fontSize=48&fontColor=fff&animation=twinkling&fontAlignY=32&desc=AI%20Engineer%20%E2%80%A2%20LLMs%20%E2%80%A2%20Agentic%20AI%20%E2%80%A2%20RAG%20%E2%80%A2%20Reinforcement%20Learning&descAlignY=52&descSize=17" width="100%"/>

<a href="https://www.linkedin.com/in/sahajs59/">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=21&pause=1000&color=39FF14&center=true&vCenter=true&width=680&lines=Building+production-grade+Agentic+AI+systems;Multi-Agent+RAG+%E2%80%A2+LangGraph+%E2%80%A2+Qdrant+%E2%80%A2+FastAPI;Ex-Research+Intern+%40+HNNOIX+%E2%80%94+AI+Agents+for+6G;IEEE+AIMV+2025+%E2%80%94+2+papers+presented;B.Tech+ICT+%40+PDEU+%E2%80%A2+CGPA+8.5+%E2%80%A2+Class+of+2027" alt="Typing SVG"/>
</a>

<br/>

<a href="https://sahajivvix-1.github.io/Portfolio2026/"><img src="https://img.shields.io/badge/Portfolio-000000?style=for-the-badge&logo=vercel&logoColor=white"/></a>
<a href="https://www.linkedin.com/in/sahajs59/"><img src="https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white"/></a>
<a href="https://x.com/SahajS59"><img src="https://img.shields.io/badge/X-000000?style=for-the-badge&logo=x&logoColor=white"/></a>
<a href="https://sahajs59.medium.com"><img src="https://img.shields.io/badge/Medium-12100E?style=for-the-badge&logo=medium&logoColor=white"/></a>
<a href="mailto:sahajs7959@gmail.com"><img src="https://img.shields.io/badge/Email-EA4335?style=for-the-badge&logo=gmail&logoColor=white"/></a>
<a href="https://raw.githubusercontent.com/SahajIVVIX-1/SahajIVVIX-1/main/Resume_WIcon.pdf"><img src="https://img.shields.io/badge/Résumé-2EA44F?style=for-the-badge&logo=readthedocs&logoColor=white"/></a>

<img src="https://komarev.com/ghpvc/?username=SahajIVVIX-1&style=flat-square&color=39FF14&label=profile+views" alt="profile views"/>

</div>

---

## 🧠 About Me

<div align="center">
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/SahajIVVIX-1/SahajIVVIX-1/main/dark_mode.svg">
  <img alt="Sahaj Saliya — terminal profile" src="https://raw.githubusercontent.com/SahajIVVIX-1/SahajIVVIX-1/main/light_mode.svg" width="100%">
</picture>
</div>

```python
class SahajSaliya:
    role       = "AI Engineer & Researcher"
    education  = "B.Tech ICT @ PDEU, Gandhinagar  (CGPA 8.5 · graduating May 2027)"
    building   = ["Multi-agent LLM systems", "Self-correcting RAG", "RL-driven agents"]
    interests  = ["LLMs", "AI Agents", "RAG", "AI Infrastructure", "Cybersecurity", "Advanced ML"]
    philosophy = "Ship it, benchmark it, then make it smarter."

    def now(self):
        return "Turning research ideas into open-source tools engineers actually use."
```

---

## 💼 Experience

<table>
<tr>
<td width="50%" valign="top">

### 🛰️ Research & Innovation Intern
**HNNOIX Private Limited** · *May – Jul 2026*

- Built reusable AI infrastructure for **6G R&D** — **LLM Gateway**, **RAG Runtime**, **AI Memory Layer** & **Knowledge Base**
- Enabled scalable agent execution, context management and workflow orchestration
- Applied GenAI, RAG and agent-based decision-making to network architectures & communication systems

</td>
<td width="50%" valign="top">

### 📈 Freelance Financial AI Engineer
**Quantitative Investment Analysis** · *Dec 2024 – Jun 2025*

- Shipped **2 autonomous trading-signal systems** using Agentic AI + RAG over live market news
- **↓ 37% false-positive signals** via confidence scoring & filtering rules
- **CrewAI** research pipeline over GPT-4, Bloomberg, FMP & Alpha Vantage for automated earnings analysis

</td>
</tr>
</table>

---

## 🚀 Featured Projects

### 🏆 [Enterprise Agentic RAG Orchestrator](https://github.com/SahajIVVIX-1/Multi-Agent-RAG)
> *Production-grade multi-agent RAG with a self-correcting retrieval loop*

<p>
<img src="https://img.shields.io/badge/LangGraph-1C3C3C?style=flat-square&logo=langchain&logoColor=white"/>
<img src="https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white"/>
<img src="https://img.shields.io/badge/Qdrant-DC244C?style=flat-square&logo=qdrant&logoColor=white"/>
<img src="https://img.shields.io/badge/Redis-DC382D?style=flat-square&logo=redis&logoColor=white"/>
<img src="https://img.shields.io/badge/RAGAS-Faithfulness_0.81-8A2BE2?style=flat-square"/>
<img src="https://img.shields.io/badge/Context_Precision-1.00-2EA44F?style=flat-square"/>
</p>

```mermaid
flowchart LR
    Q([User query]) --> G{{Prompt-injection guard}}
    G --> C{Semantic cache<br/>Qdrant ANN}
    C -- hit --> A([Answer])
    C -- miss --> S[Supervisor agent]
    S --> R[Corrective RAG worker]
    S --> SQL[NL → SQL worker]
    S --> H[Human-in-the-loop<br/>email tool]
    R --> HY[Hybrid retrieval<br/>dense + BM25]
    HY --> RR[CrossEncoder rerank<br/>parent-child 200→800 tok]
    RR --> GR{LLM doc grader}
    GR -- irrelevant --> QW[Query rewrite] --> HY
    GR -- relevant --> V[Validator agent]
    SQL --> V
    H --> V
    V --> A
```

- **Supervisor → Worker → Validator** pipeline routing across Corrective RAG, NL-to-SQL and human-in-the-loop tools
- **CRAG loop** with LLM document grading + query rewriting; hybrid Qdrant dense + BM25 retrieval, CrossEncoder reranking
- Sub-millisecond **semantic caching**, Redis session memory, prompt-injection guards and Fernet encryption

<br/>

<table>
<tr>
<td width="50%" valign="top">

### 🤖 [OpenEnv — RL Data-Cleaning Agent](https://github.com/SahajIVVIX-1/open-env-nuclei)
*An agent that doesn't just clean data — it **learns** how to.*

- Custom **Q-Learning environment** where a **Llama 3** agent picks cleaning actions from structured observations
- Reward shaping, anti-loop penalties & step constraints against destructive ops
- Pydantic-typed JSON outputs, **FastAPI** server, **Docker** on HF Spaces

<img src="https://img.shields.io/badge/RL-FF6B35?style=flat-square"/> <img src="https://img.shields.io/badge/Llama_3-0467DF?style=flat-square&logo=meta&logoColor=white"/> <img src="https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white"/>
<a href="https://chetangadhiya017-data-cleaning-env.hf.space"><img src="https://img.shields.io/badge/🤗_Live_Demo-FFD21E?style=flat-square"/></a>

</td>
<td width="50%" valign="top">

### 🧬 [Modern DCGAN Reproducibility Study](https://github.com/SahajIVVIX-1/Modern-DCGAN-Reproducibility)
*Re-implementing Radford et al. (2015) — then upgrading it.*

- Paper-faithful all-conv architecture modernised with **LSGAN** + **Spectral Normalization**
- Custom `GANAnalyzer` hooks internal layers to visualise learned filters & feature maps
- Formal **paper-vs-modern** comparison and 4-panel convergence dashboard

<img src="https://img.shields.io/badge/PyTorch-EE4C2C?style=flat-square&logo=pytorch&logoColor=white"/> <img src="https://img.shields.io/badge/GenAI-8A2BE2?style=flat-square"/> <img src="https://img.shields.io/badge/Research-555?style=flat-square"/>

</td>
</tr>
<tr>
<td width="50%" valign="top">

### 📊 [Explainable Student-Performance Platform](https://github.com/SahajIVVIX-1/student-performance-platform)
*End-to-end MLOps with trustworthy explanations.*

- Benchmarks **9 ML/DL models** (XGBoost, CatBoost, LightGBM, PyTorch, FLAML) with Pandera validation
- **SHAP + LIME** attributions, Spearman rank correlation to measure explanation agreement
- MLflow tracking, FastAPI + Streamlit, Docker Compose, GitHub Actions CI

<img src="https://img.shields.io/badge/MLflow-0194E2?style=flat-square&logo=mlflow&logoColor=white"/> <img src="https://img.shields.io/badge/SHAP_%2B_LIME-XAI-2EA44F?style=flat-square"/> <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=flat-square&logo=streamlit&logoColor=white"/>

</td>
<td width="50%" valign="top">

### 🛡️ [SentinelProxy Suite](https://github.com/SahajIVVIX-1/SentinelProxy-Suite)
*Local HTTPS proxy + DNS server with a live threat dashboard.*

- HTTPS proxy and DNS resolver dropping malicious domains before a connection is negotiated
- Millions of blocklist domains in an indexed **SQLite3** store for near-zero-latency lookups
- Real-time **Socket.IO** dashboard, auto OS proxy/DNS hooks & firewall rules

<img src="https://img.shields.io/badge/Node.js-339933?style=flat-square&logo=nodedotjs&logoColor=white"/> <img src="https://img.shields.io/badge/Socket.IO-010101?style=flat-square&logo=socketdotio&logoColor=white"/> <img src="https://img.shields.io/badge/Security-B22222?style=flat-square"/>

</td>
</tr>
<tr>
<td colspan="2" valign="top">

### 🔬 [Microplastic Detection — SIH](https://github.com/SahajIVVIX-1/SIH-AI-Gyani)
**YOLOv11** (n/s/m/l) fine-tuned with custom hyperparameters for microplastic particle detection and size estimation under varying imaging conditions, built for Smart India Hackathon.
&nbsp; <img src="https://img.shields.io/badge/YOLOv11-00FFFF?style=flat-square"/> <img src="https://img.shields.io/badge/OpenCV-5C3EE8?style=flat-square&logo=opencv&logoColor=white"/> <img src="https://img.shields.io/badge/CUDA-76B900?style=flat-square&logo=nvidia&logoColor=white"/>

</td>
</tr>
</table>

<details>
<summary><b>🧰 Desktop & automation tools (Python · PyQt6)</b></summary>
<br/>

| Tool | What it does | Stack |
|---|---|---|
| 📺 [**vMix Manager**](https://github.com/SahajIVVIX-1/vMix-Manager) | Offline XML engine for batch-editing `.vmix` productions with GUID-safe cloning | `PyQt6` `XML` |
| 🚀 [**PyEnv Launcher**](https://github.com/SahajIVVIX-1/PyEnv-Launcher-Project) | Desktop control center for Python projects, environments and packages | `PyQt6` `venv` |
| 🔔 [**Smaran Reminder**](https://github.com/SahajIVVIX-1/Smaran-Reminder-App) | Non-intrusive tray reminders with deep scheduling and burst mode | `PyQt6` |
| 🎬 [**Video & PDF Suite**](https://github.com/SahajIVVIX-1/Video-Analyzer-Scroller) | FFmpeg folder auditing to Excel + PDF → 1080p scrolling-video generator | `OpenCV` `FFmpeg` |

</details>

---

## 🛠️ Tech Stack

<div align="center">
<img src="https://skillicons.dev/icons?i=python,cpp,pytorch,tensorflow,sklearn,fastapi,flask,docker,kubernetes,redis,postgres,mongodb,mysql,aws,gcp,linux,git,githubactions&perline=9" />
</div>
<br/>

| Domain | Tools |
|---|---|
| **🤖 GenAI & Agents** | ![LangChain](https://img.shields.io/badge/LangChain-1C3C3C?style=flat-square&logo=langchain&logoColor=white) ![LangGraph](https://img.shields.io/badge/LangGraph-1C3C3C?style=flat-square&logo=langchain&logoColor=white) ![CrewAI](https://img.shields.io/badge/CrewAI-FF5A50?style=flat-square) ![AWS Bedrock](https://img.shields.io/badge/AWS_Bedrock-232F3E?style=flat-square&logo=amazonwebservices&logoColor=white) ![Transformers](https://img.shields.io/badge/🤗_Transformers-FFD21E?style=flat-square) ![Pydantic](https://img.shields.io/badge/Pydantic-E92063?style=flat-square&logo=pydantic&logoColor=white) ![RAGAS](https://img.shields.io/badge/RAGAS-8A2BE2?style=flat-square) |
| **🧠 ML / DL / RL** | ![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C?style=flat-square&logo=pytorch&logoColor=white) ![TensorFlow](https://img.shields.io/badge/TensorFlow-FF6F00?style=flat-square&logo=tensorflow&logoColor=white) ![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?style=flat-square&logo=scikitlearn&logoColor=white) ![XGBoost](https://img.shields.io/badge/XGBoost-337AB7?style=flat-square) ![Q-Learning](https://img.shields.io/badge/Q--Learning-FF6B35?style=flat-square) ![SHAP](https://img.shields.io/badge/SHAP_·_LIME-2EA44F?style=flat-square) |
| **🔎 Retrieval & Data** | ![Qdrant](https://img.shields.io/badge/Qdrant-DC244C?style=flat-square&logo=qdrant&logoColor=white) ![ChromaDB](https://img.shields.io/badge/ChromaDB-FF6446?style=flat-square) ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=flat-square&logo=postgresql&logoColor=white) ![MongoDB](https://img.shields.io/badge/MongoDB-47A248?style=flat-square&logo=mongodb&logoColor=white) ![Redis](https://img.shields.io/badge/Redis-DC382D?style=flat-square&logo=redis&logoColor=white) ![Hadoop](https://img.shields.io/badge/Hadoop-66CCFF?style=flat-square&logo=apachehadoop&logoColor=black) |
| **👁️ Vision & OCR** | ![OpenCV](https://img.shields.io/badge/OpenCV-5C3EE8?style=flat-square&logo=opencv&logoColor=white) ![YOLO](https://img.shields.io/badge/YOLOv11-00FFFF?style=flat-square) ![Kraken](https://img.shields.io/badge/Kraken_OCR-444?style=flat-square) ![ComfyUI](https://img.shields.io/badge/ComfyUI-222?style=flat-square) |
| **⚙️ MLOps & Infra** | ![MLflow](https://img.shields.io/badge/MLflow-0194E2?style=flat-square&logo=mlflow&logoColor=white) ![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white) ![Kubernetes](https://img.shields.io/badge/Kubernetes-326CE5?style=flat-square&logo=kubernetes&logoColor=white) ![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat-square&logo=streamlit&logoColor=white) ![HF Spaces](https://img.shields.io/badge/HF_Spaces-FFD21E?style=flat-square&logo=huggingface&logoColor=black) ![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=flat-square&logo=githubactions&logoColor=white) |

---

## 🏆 Achievements & Certifications

<table>
<tr>
<td width="50%" valign="top">

**🎖️ Achievements**
- 📜 **IEEE AIMV 2025** — presented 2 papers (Deepfake Detection, Crime Prediction)
- 🧪 **Code4Cause 2.0** — national-level finalist, NSUT Delhi
- 🌍 **ISRO-IIRS** — AI/ML for Geodata Analysis
- 📊 **IEEE Operations Lead** — coordinated paper presentations
- 💡 **GDG Gandhinagar** — AI & Firebase workshops

</td>
<td width="50%" valign="top">

**📜 Certifications**
- Agentic AI with LangChain & LangGraph — **IBM**
- Fundamentals of Building AI Agents — **IBM**
- Generative AI & AI Agents with Amazon Bedrock — **AWS**
- Deep Learning — **IIT Ropar (NPTEL)**
- Data Structures & Algorithms with Python — **Udemy**

</td>
</tr>
</table>

---

## 📊 GitHub Analytics

<div align="center">
<img height="165" src="https://github-readme-stats.vercel.app/api?username=SahajIVVIX-1&show_icons=true&theme=tokyonight&hide_border=true&count_private=true&include_all_commits=true&rank_icon=github"/>
<img height="165" src="https://github-readme-stats.vercel.app/api/top-langs/?username=SahajIVVIX-1&layout=compact&theme=tokyonight&hide_border=true&langs_count=8"/>
<br/>
<img src="https://streak-stats.demolab.com?user=SahajIVVIX-1&theme=tokyonight&hide_border=true"/>
<br/><br/>
<img width="100%" src="https://github-readme-activity-graph.vercel.app/graph?username=SahajIVVIX-1&theme=tokyo-night&hide_border=true&area=true"/>
<br/>
<a href="https://leetcode.com/sahajs59"><img src="https://leetcard.jacoblin.cool/sahajs59?theme=dark&font=Fira%20Code&ext=heatmap"/></a>
</div>

---

<div align="center">

### 💬 Open to AI Engineering & Research roles — let's build something intelligent together.

<a href="mailto:sahajs7959@gmail.com"><img src="https://img.shields.io/badge/Say_Hello-EA4335?style=for-the-badge&logo=gmail&logoColor=white"/></a>
<a href="https://www.linkedin.com/in/sahajs59/"><img src="https://img.shields.io/badge/Connect-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white"/></a>
<a href="https://sahajivvix-1.github.io/Portfolio2026/"><img src="https://img.shields.io/badge/Portfolio-000000?style=for-the-badge&logo=vercel&logoColor=white"/></a>

<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=6,11,20&height=110&section=footer" width="100%"/>

</div>
