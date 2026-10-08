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
