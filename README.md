
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

## 📐 Triangle-Based Subdivision Tiling  

This version generates Penrose tilings using **iterative subdivision** of thin (acute) and thick (obtuse) **golden triangles**, based on Robinson’s decomposition.  

### Key Characteristics  

* **Fixed Initial Pattern:** Uses a 10-triangle star configuration (no user-selectable seed).  
* **Triangle-Based Only:** Generates tilings exclusively from acute/obtuse triangles.  
* **Iterative Subdivision:** Uses stack-based iteration (avoiding recursion limits) while preserving Penrose’s rules.  
* **Implicit Matching Rules:** No decorative arcs needed; aperiodicity is inherent in the subdivision logic.  

### Features  

* **Color Modes:**  
  * **Mono (Grayscale):** Renders all triangles uniformly.  
  * **By Type:** Colors acute/obtuse triangles differently.  
  * **By Orientation:** Colors by rotational alignment (reveals 5-fold symmetry).  
* **Recursion Depth Control:** Adjust detail level (3–6 recommended for balance).  
* **Export Options:** Save as PNG/SVG.  

### Usage  

Upon running, you’ll be prompted to:  

1. Enter recursion depth (e.g., 4).  
2. Select a color mode (`mono`/`type`/`color`).  
3. Optionally save the output (e.g., `tiling.png`).  

📝 This version offers a cleaner geometric representation and is particularly useful for studying the underlying substitution logic of Penrose tilings without the visual clutter of explicit matching rule enforcement.
