# Netflix Catalog Exploratory Data Analysis — Executive Insights Summary

**Author:** Ahmed Mahmoud Khalifa  
**Track:** Data Science  
**Task:** Task 3 — Exploratory Data Analysis (EDA)  
**Organization:** Synent Technologies  

---

## Executive Overview
This report synthesizes the core empirical findings from the Exploratory Data Analysis (EDA) conducted on the Netflix catalog snapshot (`8,790` records). All reported metrics, distributions, and associations are strictly calculated from the dataset without data simulation or manual fabrication.

---

## 1. Content Composition & Catalog Profile
- **Type Distribution:** The catalog consists of **6,126 Movies (69.69%)** and **2,664 TV Shows (30.31%)**, representing a ratio of approximately 2.30 Movies per TV Show.
- **Titles & Entities:** The dataset encompasses 8,787 distinct title names, 4,528 directors (with 2,588 records lacking director data), and representations from 86 distinct countries.
- **Multi-genre Classification:** Titles carry an average of **2.40 categories/genres**, totaling 42 unique genre classifications when exploded.

---

## 2. Temporal Dynamics (Release Year vs. Date Added)
- **Catalog Additions Surge:** Additions to Netflix remained modest prior to 2016 (only 426 titles before 2016), accelerating rapidly to peak in **2019 with 2,016 titles added (22.94%)**, followed by 1,879 titles in 2020.
- **Concentration in Contemporary Content:** Over **84.8%** of catalog titles were originally released in **2010 or later**. The median release year across all content is **2017** (Movies: 2016, TV Shows: 2018).
- **Time-to-Platform Lag:** The median lag between a title's original release and its date added to Netflix is **1 year**, showing that catalog expansion heavily leverages recently produced media.
- **Evolution of Content Mix:** While Movies represent the overall majority, the proportion of TV Shows added annually expanded from early sparse levels to reach **33.7% in 2021**.

---

## 3. Geographic & Rating Dominance
- **Top Production Countries:** 
  1. **United States:** 3,240 titles (36.86% of total catalog)
  2. **India:** 1,057 titles (12.03%)
  3. **United Kingdom:** 638 titles (7.26%)
  4. **Pakistan:** 421 titles (4.79%)
  5. **Canada:** 271 titles (3.08%)
  *(The top 10 countries account for over 74% of all catalog titles).*
- **Rating Profile:**
  - **TV-MA** is the single most prevalent maturity rating with **3,205 titles (36.46%)**, followed by **TV-14 (2,157 titles, 24.54%)**, and **TV-PG (861 titles, 9.80%)**.
  - Mature-rated content (TV-MA, R, NC-17) comprises **45.59%** of the catalog, demonstrating a heavy catalog orientation toward adult and teen audiences.

---

## 4. Genre Prevalence & Shift Across Decades
*Note: Genre frequency serves as a proxy for catalog prevalence and availability, not viewer engagement or ratings.*
- **Overall Leading Genres (Exploded):**
  1. *International Movies:* 2,752 titles (31.31%)
  2. *Dramas:* 2,426 titles (27.60%)
  3. *Comedies:* 1,674 titles (19.04%)
  4. *International TV Shows:* 1,349 titles (15.35%)
  5. *Documentaries:* 869 titles (9.89%)
- **Generational Shift across Release Eras:**
  - **Pre-1980s / Early Era:** Dominated by *Classic Movies* (40.4% of pre-1980 titles) and curated *Documentaries*.
  - **1990s – 2000s:** Shifted toward mainstream *Dramas* and *Comedies*.
  - **2010s – 2020s:** Tremendous expansion in *International Movies* (32.5% of 2010s titles) and *International TV Shows* (growing to over 23.5% of 2020s titles).
- **Movies vs. TV Shows Genre Distinction:**
  - Movies are dominated by *Drama* (39.6%) and *Comedy* (27.3%).
  - TV Shows show significantly higher prevalence of *Crime TV Shows* (17.7%) and *Kids' TV* (17.0%).

---

## 5. Duration & Season Structure
- **Movie Runtimes:**
  - Evaluated exclusively on Movies ($N = 6,126$).
  - **Median:** 98.0 minutes (Mean: 99.58 min, Standard Deviation: 28.28 min).
  - **Interquartile Range (IQR):** 87.0 to 114.0 minutes, with 63.8% of movies falling within the standard 80–120 minute feature window.
- **TV Show Seasons:**
  - Evaluated exclusively on TV Shows ($N = 2,664$).
  - **Single-season dominance:** **67.23% (1,791 shows)** consist of exactly 1 season; **83.03%** have $\le 2$ seasons.
  - Mean season count is 1.75 seasons (Max: 17 seasons).

---

## 6. Correlation Analysis & Empirical Relationships
- **Methodology:** Calculated only on meaningful continuous/discrete numeric variables without arbitrary integer encoding of nominal categories.
- **Key Coefficients:**
  - `release_year` vs. `movie_duration_minutes`: Pearson $r = -0.206$ (Spearman $\rho = -0.191$). Indicates a **weak negative correlation**; contemporary films in the catalog are slightly shorter on average than vintage films, but release year accounts for only $\approx 4.2\%$ of runtime variance ($r^2 = 0.042$).
  - `release_year` vs. `tv_seasons`: Pearson $r = -0.082$ (Spearman $\rho = 0.030$). Demonstrates a **negligible correlation**; number of seasons is largely independent of original release year in this catalog snapshot.
  - `release_year` vs. `added_year`: Pearson $r = 0.039$ for Movies, $r = 0.388$ for TV Shows.

---

## 7. Analytical Limitations
1. **Catalog Snapshot:** The dataset represents titles available at a single snapshot point in time. It does not track licensing expirations, title removals, or subscriber viewing history.
2. **Absence of Engagement Metrics:** Views, streaming hours, completion rates, and user ratings are absent; thus, catalog prevalence cannot be interpreted as viewer popularity.
3. **Correlation is Not Causation:** Observed associations reflect catalog acquisition and production strategies rather than direct causal mechanisms.
