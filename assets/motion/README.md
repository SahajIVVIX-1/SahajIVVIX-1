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
