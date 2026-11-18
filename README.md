# Engineering Material Selector (MSE)

#### Video Demo: https://youtu.be/_B56likNDaA

#### Description:
**Engineering Material Selector (MSE)** is a command-line Python application developed as a CS50P Final Project to assist Materials Science and Engineering (MSE) decision-making. Inspired by the classic Ashby material selection methodology—hard-constraint screening followed by multi-criteria weighted ranking—the program reads engineering material properties from an SQLite database and recommends optimal candidates for **Automotive**, **Aerospace**, and **Rail** applications.

Users interactively select a target sector and specify design constraints—minimum tensile strength (MPa), minimum elastic modulus (GPa), minimum operating temperature (°C), maximum cost (USD/kg), and minimum corrosion resistance (`1–10` scale)—with the option to press `Enter` to skip any limit. The application outputs two formatted ASCII tables:
1. **Recommended Materials (Ranked):** Surviving materials normalized and scored on a `0–100` scale using sector-specific weights, sorted from highest to lowest, including computed specific strength (`tensile_strength / density`).
2. **Eliminated Materials (Summary):** Filtered-out candidates paired with the exact engineering constraints they failed to satisfy (e.g., `Low tensile strength`, `Over budget`).

#### Project Files:
- `project.py`: Main CLI entry point (`main`) and top-level selection/formatting functions:
  - `load_materials`: Connects to `materials.db` via `sqlite3`, verifies database existence (`FileNotFoundError` if missing), and converts rows into structured dictionaries.
  - `filter_materials`: Applies active user limits and separates passing candidates from eliminated ones while recording every failed constraint per material.
  - `rank_materials`: Validates the target sector, performs min-max normalization across all six engineering properties (inverting `density` and `cost` so lower values score higher, and safely handling zero-range sets), calculates `specific_strength`, applies sector weights, and sorts results in descending score order.
  - `format_tables`: Uses `tabulate` (`grid` format) to produce clean terminal tables or informative empty-state messages.
  - `get_sector` and `get_float_input`: Interactive input validators supporting numeric/name sector selection, non-negative float enforcement, and optional limit skipping via `Enter`.
- `test_project.py`: Automated `pytest` suite (`test_load_materials`, `test_filter_materials`, `test_rank_materials`, `test_format_tables`) covering database loading, error handling (`FileNotFoundError`, `ValueError`), constraint filtering, sector-specific ranking differences, single-item/empty edge cases, and table formatting.
- `init_db.py`: Standalone database initialization script that recreates and seeds `materials.db` with 16 engineering metals, composites, and polymers (`name`, `category`, `density`, `tensile_strength`, `elastic_modulus`, `max_temp`, `corrosion_resistance`, `cost`).
- `materials.db`: Local SQLite database storing the 16-material catalog.
- `requirements.txt`: External dependencies (`tabulate`, `pytest`).

#### Engineering Methodology & Sector Weights:
Surviving materials are normalized relative to the filtered pool (`[0, 1]`) and combined via a weighted sum model:
- **Automotive:** Cost (`0.25`), density (`0.20`), tensile strength (`0.20`), elastic modulus (`0.15`), max temperature (`0.10`), corrosion resistance (`0.10`).
- **Aerospace:** Density (`0.30`), tensile strength (`0.25`), elastic modulus (`0.15`), max temperature (`0.15`), corrosion resistance (`0.10`), cost (`0.05`).
- **Rail:** Tensile strength (`0.25`), elastic modulus (`0.25`), cost (`0.25`), corrosion resistance (`0.15`), density (`0.05`), max temperature (`0.05`).

#### Design Choices:
- **SQLite with a Dedicated Seed Script (`init_db.py`):** Rather than hardcoding material dictionaries inside `project.py`, storing properties in `materials.db` cleanly decouples engineering data from selection logic, avoids external database servers, and allows reproducible database resets.
- **Min-Max Normalization over Raw Metrics:** Because engineering properties span different units and scales (e.g., MPa vs. g/cm³), normalizing across surviving candidates prevents high-magnitude numbers from dominating sector weights. When all surviving materials share an identical metric value (or only one candidate remains), the ratio safely defaults to `1.0` to prevent division by zero.
- **Skipping Constraints & Explaining Eliminations:** Early design iterations often lack firm limits for every parameter. Supporting empty `Enter` inputs and reporting exact elimination reasons lets engineers identify bottleneck requirements quickly.

#### Installation, Usage & Testing:
```bash
pip install -r requirements.txt
python3 init_db.py
python3 project.py
```

Run the automated test suite with:
```bash
pytest -v
```
