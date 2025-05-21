# UWB Citations vs References Map Visualization

## Overview

This interactive web-based visualization displays a **global map** showing the relationship between **citations** and **references** for scientific articles from the **University of West Bohemia (UWB)**. It allows users to explore how often institutions around the world cite UWB articles versus how often UWB references them.

Data was collected in **April 2025** and filtered to **exclude articles cited by fewer than 15 institutions**.

## Files
- **data.zip** – a reduced version of the dataset; must be extracted and placed in the same directory as `map.html` before visualization.
- **map.html** – the web-based visualization; recommended launch instructions are below or in the file `run.txt`.
- **preprocess.ipynb** – method for transforming data collected from the SCOPUS API, stored in the `data_by_year` directory.

---

## Key Features

### 🌍 Interactive World Map
- The map uses a **Natural Earth projection** to show countries and bubbles for cities.
- Cities are represented as **bubbles**, whose:
  - **Size** reflects the total number of citations and references combined.
  - **Color** shows the **ratio of citations to references**.

### 🎨 Color Encoding (Ratio of Citations to References)
- A **diverging color scale** (`RdBu`) indicates the citation/reference balance:
  - **Red**: UWB cites the city more than it's cited in return.
  - **Blue**: The city cites UWB more.
  - **Grayish**: Balanced.

### 🟢 Bubble Size (Total Activity)
- Larger bubbles indicate more activity (citations + references).
- A size legend is provided with examples (e.g., 1,000 – 100,000 total interactions).

---

## Filters and Controls

### 📆 Year Range Filter
- Users can filter the data by publication year using an **interactive slider**.
- The map dynamically updates to reflect changes.

### 👨‍🔬 Author Filter
- Users can filter data by specific **UWB authors**:
  - Search for author names.
  - Select multiple authors via checkboxes.
  - Clear all selections with a single button.

---

## User Interaction

### 🔍 Tooltip on Hover
- Hovering over a city bubble reveals:
  - **City and State**
  - Number of times the city **cited UWB**
  - Number of times the city was **referenced by UWB**

### 🔎 Zoom and Pan
- Users can zoom and pan across the map using mouse interactions.
- Bubble sizes and opacity scale dynamically with zoom level for readability.

---

## Technical Stack

| Feature       | Library / Tool              |
|--------------|-----------------------------|
| Visualization | [D3.js v7](https://d3js.org) |
| Map Geometry  | [TopoJSON](https://github.com/topojson/topojson) |
| Slider Control | [noUiSlider](https://refreshless.com/nouislider/) |
| Layout & Styling | Vanilla CSS |
| Data Format | `data.json` (geo + citation data) |
| Map Source | `world-atlas` TopoJSON data |

---

## Notes

- Projection is recalculated responsively on window resize.
- All controls are mobile-friendly and adapt to smaller screens.
- Data processing includes log and normalization steps to ensure effective visualization even with high variance in values.

---

## How to Run the Visualization

1. Save the HTML file locally as `index.html`.
2. Serve it using a local web server (to allow JS file loading):
   - **Using Python**:
     ```bash
     python -m http.server
     ```
     Open browser to: `http://localhost:8000`
   - **Using Node.js**:
     ```bash
     npx serve
     ```

---

## Example Use Cases

- Analyzing global citation networks of UWB researchers.
- Identifying collaborative hotspots.
- Highlighting under-acknowledged regions in academic exchange.
- Filtering to assess individual researcher outreach.

---

## Screenshot

_Add a screenshot here to provide a quick visual preview._

---

© University of West Bohemia — 2025
