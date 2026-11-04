"""Layout shared by the artwork (build.py) and the mascot route (journey.py)."""

TOOLKIT = [
    ("GenAI & Agents", ["LangChain", "LangGraph", "CrewAI", "AWS Bedrock", "HF Transformers", "Pydantic", "RAGAS"]),
    ("ML · DL · RL", ["PyTorch", "TensorFlow", "scikit-learn", "XGBoost", "CatBoost", "LightGBM", "Q-Learning", "SHAP", "LIME"]),
    ("Retrieval & Data", ["Qdrant", "ChromaDB", "PostgreSQL", "MongoDB", "Redis", "Hadoop", "SQL"]),
    ("Vision & OCR", ["OpenCV", "YOLOv11", "Kraken OCR", "ComfyUI"]),
    ("MLOps & Infra", ["MLflow", "Docker", "Kubernetes", "FastAPI", "Flask", "Streamlit", "HF Spaces", "GitHub Actions", "AWS", "GCP", "Linux"]),
    ("Languages", ["Python", "C++", "SQL", "MATLAB"]),
]
TK_W, TK_LABW, TK_CHIP_H, TK_GAPY = 1200, 290, 36, 10


def toolkit_layout(measure):
    """rows: [(label, items, chips[(x, y, w, name)], top, bottom)], total height.
    measure(text) -> advance width of a chip label in sans 400 at 15.5."""
    rows, y = [], 28
    for label, items in TOOLKIT:
        x, line = TK_LABW, []
        for it in items:
            w = measure(it) + 32
            if x + w > TK_W - 8:
                y += TK_CHIP_H + TK_GAPY; x = TK_LABW
            line.append((x, y, w, it)); x += w + 10
        rows.append((label, items, line, line[0][1], y + TK_CHIP_H))
        y += TK_CHIP_H + 56
    return rows, y - 46


# ── Recognition ─────────────────────────────────────────────────────────────
ACHIEVEMENTS = [
    ("IEEE AIMV 2025", "Presented 2 papers, on Deepfake Detection and Crime Prediction"),
    ("Code4Cause 2.0", "National-level finalist, NSUT Delhi"),
    ("ISRO-IIRS", "AI/ML for Geodata Analysis"),
    ("IEEE Operations Lead", "Coordinated research-paper presentations"),
    ("GDG Gandhinagar", "AI and Firebase workshops"),
]
CERTS = [
    ("AI / GenAI & agents", [("Agentic AI with LangChain and LangGraph", "IBM"), ("Fundamentals of Building AI Agents", "IBM"),
                             ("AWS Generative AI and AI Agents with Amazon Bedrock", "AWS"), ("Building with the Claude API", "Anthropic"),
                             ("Claude Code 101", "Anthropic"), ("Dataiku Generative AI Practitioner", "Dataiku")]),
    ("ML / DL", [("Deep Learning", "IIT Ropar · NPTEL")]),
    ("Cloud", [("Oracle Cloud and AI", "Oracle")]),
    ("Other", [("Data Structure & Algorithm With Python", "Udemy"), ("2,121-Word Book", "Guinness World Records")]),
]
# Harvard ManageMentor badges (Harvard Business Publishing): (title, badge file in build/badges/)
HARVARD = [
    ("Leading with Generative AI", "leading-with-generative-ai"),
    ("Strategic Thinking", "strategic-thinking"),
    ("Strategy Planning and Execution", "strategy-planning-and-execution"),
    ("Project Management", "project-management"),
    ("Team Management", "team-management"),
]
HV_BADGE_W, HV_BADGE_H = 75, 96
RC_W, RC_GAP, RC_PAD = 1200, 16, 22
RC_COL = (RC_W - 4 * RC_GAP) / 5


def wrap_words(text, maxw, width):
    """greedy word wrap; width(s) -> advance of s"""
    lines, cur = [], ""
    for w in text.split():
        nxt = (cur + " " + w) if cur else w
        if cur and width(nxt) > maxw:
            lines.append(cur); cur = w
        else:
            cur = nxt
    return lines + ([cur] if cur else [])


def recognition_layout(measure):
    """measure(text, role, weight, size) -> advance. Everything the artwork and the bots need."""
    inner = RC_COL - 2 * RC_PAD
    L = dict(head1=58, cards=[], tiles=[])
    L["rule1"] = (measure("Achievements", "serif", 400, 30) + 52, L["head1"] - 10)
    top = 84
    bottoms = []
    for i, (title, desc) in enumerate(ACHIEVEMENTS):
        x = i * (RC_COL + RC_GAP)
        tl = wrap_words(title, inner, lambda s: measure(s, "sans", 600, 17))
        dl = wrap_words(desc, inner, lambda s: measure(s, "sans", 400, 14.5))
        y_title = top + 70
        y_desc = y_title + 22 * (len(tl) - 1) + 28
        bottoms.append(y_desc + 21 * (len(dl) - 1))
        L["cards"].append(dict(x=x, title=tl, desc=dl, y_title=y_title, y_desc=y_desc))
    L["card_top"], L["card_bot"] = top, max(bottoms) + 28
    L["head2"] = L["card_bot"] + 76
    L["rule2"] = (measure("Certifications", "serif", 400, 30) + 52, L["head2"] - 10)
    flat = [(name, iss, grp) for grp, items in CERTS for name, iss in items]
    rows_top = L["head2"] + 36
    names = [wrap_words(n, inner, lambda s: measure(s, "sans", 600, 15.5)) for n, _, _ in flat]
    th = 70 + 21 * (max(len(n) for n in names) - 1) + 54
    for i, ((name, iss, grp), nl) in enumerate(zip(flat, names)):
        r, c = divmod(i, 5)
        L["tiles"].append(dict(x=c * (RC_COL + RC_GAP), y=rows_top + r * (th + 30), name=nl, issuer=iss, group=grp))
    L["tile_h"] = th
    certs_bot = rows_top + 2 * th + 30
    # Harvard ManageMentor: badge on the left, course title wrapped beside it
    L["head3"] = certs_bot + 76
    L["rule3"] = (measure("Harvard ManageMentor", "serif", 400, 30) + 52, L["head3"] - 10)
    hv_top = L["head3"] + 36
    text_w = RC_COL - 28 - HV_BADGE_W - 12  # 14px insets, 12px gap after the badge
    L["badges"] = []
    for i, (title, key) in enumerate(HARVARD):
        L["badges"].append(dict(x=i * (RC_COL + RC_GAP), y=hv_top, key=key,
                                name=wrap_words(title, text_w, lambda s: measure(s, "sans", 600, 15))))
    L["badge_h"] = HV_BADGE_H + 36
    L["H"] = hv_top + L["badge_h"] + 1
    return L
