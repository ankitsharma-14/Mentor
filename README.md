# Mentor OS

Mentor OS is a personal learning dashboard with weekly developer goals, curated learning resources, and a Python research-data pipeline. The dashboard is implemented in `gos/mentor.html` and reads data from `gos/mentor_store.js`.

## Getting started

1. Clone this repository:

   ```bash
   git clone https://github.com/ankitsharma-14/Mentor.git
   cd Mentor
   ```

2. Open `gos/mentor.html` in a modern browser. The dashboard loads the committed `gos/mentor_store.js` snapshot, so you can inspect the sample data without first running the pipeline. Internet access is required for CDN assets such as Chart.js and Google Fonts.

3. To run a local web server instead of opening the HTML file directly:

   ```bash
   python3 -m http.server 8000
   ```

   Then open `http://localhost:8000/gos/mentor.html`.

## Repository layout

```text
Mentor/
├── README.md
└── gos/
    ├── agent_pipeline.py  # Python data-generation pipeline
    ├── mentor.html        # Browser-based dashboard
    ├── mentor_store.js    # Dashboard data available as window.MENTOR_STORE
    ├── mentor_data.json   # Generated or stored research data
    ├── mentor_goals.json  # Goal data
    └── mentor_report.json # Report snapshot
```

## Refreshing research data

The pipeline lives at `gos/agent_pipeline.py`. It fetches research metadata from arXiv and writes dashboard data. Review its output paths and generated data before running it; the supplied JSON and JavaScript files may be overwritten.

Run it from the `gos` directory so relative paths refer to the right files:

```bash
cd gos
python3 agent_pipeline.py
```

The script uses Python standard-library modules. Internet connectivity is required to fetch live research resources, and arXiv requests can fail if the network service is unavailable.

## Contributing

Useful contributions include documentation corrections, dashboard accessibility improvements, small bug fixes, and tests for the data pipeline. Please describe the problem and the verification performed in your pull request.

## Licensing

This repository does not currently include a `LICENSE` file. Please contact the repository owner before assuming permission to redistribute the source code.
