# Motion system

The profile graphics in this directory are generated from `generate.py` and committed as SVG assets.

The design deliberately uses native SVG animation (`animate`, `animateMotion`, `animateTransform`) rather than JavaScript. This keeps the profile portable while allowing moving data packets, pulsing system cores, animated architecture wires and telemetry rails.

Run:

```bash
python generate.py
```

The GitHub Action regenerates the assets automatically.
