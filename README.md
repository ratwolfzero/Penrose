
# Penrose Tiling Generator

![Penrose tiling](penrose_tiling.png)

-----

## 📚 Historical Background

**Penrose tilings** are non-periodic tilings discovered by mathematician and physicist **Sir Roger Penrose** in the 1970s. Unlike regular tilings (like square or hexagonal grids), Penrose tilings **never repeat** in a translational sense but exhibit **local fivefold rotational symmetry** and **quasiperiodic order**.

Penrose developed different types of tilings, with **kite and dart** tiling being one of the earliest and most visually iconic forms.

These tilings became important in **mathematics**, **physics**, and **crystallography** (e.g., explaining structures of quasicrystals), and were also a major influence in **art** (e.g., M.C. Escher's later work).

> 📖 Reference:
> R. Penrose, "Pentaplexity: A class of non-periodic tilings of the plane", *The Mathematical Intelligencer*, 1979.
> DOI: [10.1007/BF03026814](https://doi.org/10.1007/BF03024384)

-----

## 📐 Alternative: Recursive Triangle Tiling

This optional version of the program generates Penrose tilings using **recursive subdivision** of thin and thick **golden triangles**, based on Robinson’s decomposition. It produces equivalent aperiodic tilings without relying on traditional matching rules or arcs. Instead, each triangle recursively subdivides into new triangles according to Penrose's substitution rules.

### Key Characteristics

* **Single Initial Pattern:** No seed selection; a consistent starting pattern is used.
* **Triangle-Based Only:** Generates tilings exclusively from thin and thick triangles, omitting kites or darts.
* **Simplified Recursive Logic:** Ideal for exploring self-similarity due to its straightforward subdivision process.
* **Implicit Matching Rules:** No decorative arcs are rendered, as matching rules are inherent in the recursive logic.

### Features

* **Color Modes:**
  * **By Type:** Distinguishes between the two fundamental triangle shapes – the **acute** and **obtuse** golden triangles – with different colors.
  * **By Orientation:** Colors triangles based on their rotational alignment, revealing hidden symmetries and patterns within the tiling.
* **Recursion Depth Control:** Adjust the level of detail for the tiling.
* **Export Options:** Save generated tilings as PNG or SVG files.

### Usage

Upon running this version, you'll be prompted to:

* Choose the desired recursion depth.
* Select a color mode.
* Optionally save the output.

📝 This version offers a cleaner geometric representation and is particularly useful for studying the underlying substitution logic of Penrose tilings without the visual clutter of explicit matching rule enforcement.

-----
