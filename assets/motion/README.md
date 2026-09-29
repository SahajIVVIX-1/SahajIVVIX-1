<<<<<<< HEAD
# Motion system

The profile graphics in this directory are generated from `generate.py` and committed as SVG assets.

The design deliberately uses native SVG animation (`animate`, `animateMotion`, `animateTransform`) rather than JavaScript. This keeps the profile portable while allowing moving data packets, pulsing system cores, animated architecture wires and telemetry rails.

Run:

```bash
python generate.py
```

The GitHub Action regenerates the assets automatically.
=======
# Motion Graphics

The profile's animated visuals are generated locally from code. No JavaScript, GIFs, or animation SaaS is required for these assets.

```powershell
python assets/motion/generate.py
```

Generated files:

- `hero.svg` — animated profile hero with network/data-flow motion.
- `multi-agent-rag.svg` — animated architecture card for the Multi-Agent RAG project.
- `divider.svg` — lightweight animated section divider.

The SVGs use native SVG animation (`<animate>`, `<animateMotion>`, and stroke-dash animation), so the source remains editable and version-controlled.
>>>>>>> ae7521f548dd7215d1602cf0f95a2cca22f442ca
