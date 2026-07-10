# mystery_scribe 

🚧 Work in progress — core pipeline functional, ROI calibration ongoing

Extract structured stats from Overwatch 2 Mystery Heroes post-match scoreboards
using classical computer vision (OpenCV/PIL) + OCR, so you stop hand-recording
scores. Screenshots in, tidy table out.

## Approach

OpenCV handles **localization** (fixed-coordinate ROI grid per template); OCR
handles **reading** (Tesseract + digit whitelist for numbers, EasyOCR for
stylized names). A validation pass flags dubious cells rather than silently
saving bad data.

## Workflow

Prototype in notebooks, then promote stable functions into classes.

| Notebook | Does | Refactors into |
|----------|------|----------------|
| `01_explore_and_calibrate` | draw & save ROI boxes for a template | `template.TemplateConfig` |
| `02_preprocess_and_ocr` | get one cell reading right | `ocr.OCRReader`, `ocr.preprocess` |
| `03_extract_full_board` | loop all cells → DataFrame → validate | `extract.Extractor`, `extract.Validator` |

The `mystery_scribe/` package holds the refactor targets; `pipeline.Pipeline`
is the orchestration layer you assemble last.

## Quick start

```bash
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
```

Tesseract is a system binary (not a pip package) — install it separately:
`brew install tesseract` (macOS) / `sudo apt-get install tesseract-ocr`
(Debian/Ubuntu) / `choco install tesseract` (Windows). Verify with
`tesseract --version`.

**Enable nbstripout** (once per clone) so notebook outputs are stripped from
commits, keeping diffs clean and the repo small:

```bash
nbstripout --install --attributes .gitattributes
```

This registers a git filter using the committed `.gitattributes`. Without it,
the tool is installed but won't run.

Then start prototyping:

```bash
# drop a screenshot at data/raw/sample.png
jupyter notebook notebooks/01_explore_and_calibrate.ipynb
```

Then, once calibrated:

```python
from mystery_scribe.template import TemplateConfig
from mystery_scribe.pipeline import Pipeline

cfg = TemplateConfig.load("configs/template_a.json")
pipe = Pipeline([cfg])
df = pipe.process_folder("data/raw")
df.to_csv("output/all_matches.csv", index=False)
```

## Structure

```
mystery_scribe/
├── notebooks/        # staged prototyping (start here)
├── mystery_scribe/   # refactored classes
│   ├── template.py   # ROI config loader
│   ├── ocr.py        # number + name readers
│   ├── extract.py    # Extractor + Validator
│   └── pipeline.py   # batch orchestration
├── configs/          # per-template ROI JSON (from notebook 01)
├── data/raw/         # input screenshots
└── output/           # extracted tables
```

## Roadmap

- [ ] EasyOCR/PaddleOCR for names (better on gamertags)
- [ ] Template classifier for multiple layouts (`Pipeline.classify`)
- [ ] ORB+homography alignment for varying resolutions (`align.py`)
- [ ] Correction UI for flagged rows

## License

This project's **code** is released under the [MIT License](LICENSE). You're
free to use, modify, and redistribute it.

The license covers the source code only — not the data it produces (see below).

## Data handling & responsible use

`mystery_scribe` extracts statistics from Overwatch 2 post-match scoreboards.
That output contains real player handles (Battletag names) alongside
performance numbers. A few notes on using and sharing that data responsibly:

### Player names are personal data
Scoreboard handles identify real people. Extracting them for your own
analysis is fine. Publishing a public, searchable dataset that links named
players to their stats is a different thing — at scale it's the kind of
profiling people don't expect or consent to.

**If you publish any extracted data, anonymize the name column first** (hash
or replace with stable pseudonyms) and keep the raw name→ID mapping private.

### Example data only in this repo
The sample screenshots and `sample_extracted.csv` included here exist solely to
let you run and test the pipeline. They are **not** a dataset for downstream
research and should not be redistributed as one. Treat them as fixtures.

### Game terms of service
This data is extracted from screenshots of the Overwatch 2 client. Blizzard's
EULA / Terms of Service govern use of the game and its content. Personal,
non-commercial use of your own match screenshots is unremarkable; bulk
collection or public redistribution of extracted match data sits in a grayer
area. Review the current terms before publishing anything beyond examples.

### What's safe to share
- The code in this repo ✅
- A handful of sample screenshots + their extracted output, as test fixtures ✅
- An **anonymized** aggregate dataset, if you have a reason to publish one ✅
- A large dataset of named players' stats ❌ (anonymize first)

---

*This is general guidance, not legal advice. If you plan to publish a dataset
at any meaningful scale, confirm the relevant terms yourself.*
