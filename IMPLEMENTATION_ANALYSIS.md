# Implementation Analysis: 15-Minute City Accessibility and Spatial Justice Model

This document reviews the implementation in [src/main.py](src/main.py) and explains its theoretical basis, the exact literature behind each algorithm, and whether the implementation is scientifically valid according to the resources used in this project.

---

## 1. Overall assessment

The current implementation is methodologically consistent with the research design described in [AGENTS.md](AGENTS.md), [CLAUDE.md](CLAUDE.md), and [THESIS_REPORT.md](THESIS_REPORT.md). The structure of the code follows the established logic of:

- 15-minute city accessibility concept from Moreno et al. (2021)
- distance decay from Weng et al. (2019)
- 2SFCA from Luo & Wang (2003)
- saturation / capping from Duncan et al. (2011) and Walk Score methodology
- neighborhood-level spatial access logic from contemporary applied studies in the literature review

In short: the implementation is a reasonable and defensible version of the research model, but it is not yet a fully validated final scientific pipeline because some inputs are placeholder values, especially population and weight data.

---

## 2. What the code is trying to implement

The script is designed to compute a neighborhood-level 15-minute city accessibility score and a weighted spatial justice index for Tehran.

The conceptual pipeline is:

1. Load neighborhood polygons.
2. Download the pedestrian network for Tehran.
3. Download POIs (amenities/services) from OSM.
4. Map each POI to a category matching the questionnaire variables.
5. Compute the nearest network node for each POI and each neighborhood centroid.
6. For each neighborhood, compute accessible services within 1200 meters.
7. Apply a distance decay function to weight nearby opportunities more than distant ones.
8. Compute a 2SFCA-style supply-to-demand ratio.
9. Normalize scores with a threshold cap and compute a weighted total index.
10. Save outputs to Shapefile, GeoPackage, and a field dictionary.

This is the correct overall research strategy for a neighborhood-level 15-minute city accessibility and spatial justice model, especially when the research goal is to combine network-based access, service capacity, and weighted social preferences.

---

## 3. Code-to-literature mapping

### 3.1 15-minute city logic

The idea that essential services should be reachable within 15 minutes on foot is directly grounded in the 15-minute city literature, especially:

- Moreno et al. (2021)
- Caselli et al. (2021)
- Mañago et al. (2025)
- Plaza-Herrera & Mercadé-Aloy (2025)

The code implements this via:

- `distance_threshold = 1200`
- `network_type='walk'`
- `nx.single_source_dijkstra_path_length(G, ref_node, cutoff=1200, weight='length')`

This is consistent with a 15-minute walking threshold because:

- 15 minutes × 80 m/min ≈ 1200 meters
- The model explicitly uses network distance rather than straight-line distance
- This matches the project standard in [AGENTS.md](AGENTS.md) and [CLAUDE.md](CLAUDE.md)

Evidence from the literature:

- Moreno et al. (2021): the definition of the 15-minute city appears in the abstract and introductory framing, where the city is described as one in which daily needs are reachable within a short active-travel window. This is the conceptual anchor for the 1200 m threshold used in the code. Quality: high, because this is the core conceptual definition of the concept itself.
- Caselli et al. (2021): in the framework and GIS-analysis sections, the authors operationalize neighborhood accessibility using pedestrian travel time and public-service reachability, which supports the walk-network threshold used here. Quality: high for conceptual and methodological relevance.
- Mañago et al. (2025): in the abstract and methods sections, the authors construct a 15-minute city index with service areas and network analysis; this directly supports the use of a 15-minute service radius. Quality: high.
- Plaza-Herrera & Mercadé-Aloy (2025): the title, abstract, and method emphasize age-sensitive active accessibility in a metropolitan context; the emphasis on active accessibility and travel-time constraints validates the use of an active-mobility threshold and walk-based accessibility analysis. Quality: high.

This is scientifically correct in principle.

### 3.2 Walking network and shortest-path logic

The network-based implementation is: 

- `G = ox.graph_from_place(place_name, network_type='walk')`
- `ref_node = ox.distance.nearest_nodes(G, X=row["lon"], Y=row["lat"])`
- `nx.single_source_dijkstra_path_length(G, ref_node, cutoff=1200, weight='length')`

This logic is standard in urban accessibility research using GIS and OSM. It is the correct method for computing path-based service reachability on a pedestrian network, rather than using Euclidean distance.

This is consistent with the literature cited in [THESIS_REPORT.md](THESIS_REPORT.md), especially:

- Murgante & Annunziata (2025)
- Mañago et al. (2025)
- Caselli et al. (2021)
- Koljensic (2022)

Why it is correct:

- real pedestrian access is constrained by the street network
- shortest-path routing is the accepted method for evaluating service access
- using `weight='length'` ensures travel cost is measured in meters, not in abstract edge count

Source-specific evidence:

- Murgante & Annunziata (2025): in the abstract and method sections they explicitly use a 1200 m attraction-reach logic and network-based accessibility, which is conceptually the same as the current routing model. Quality: high.
- Mañago et al. (2025): the methods section describes service areas, network analysis, and spatial index construction; this is the strongest direct precedent for using OSM + network analysis with service buffers and walksheds. Quality: high.
- Caselli et al. (2021): the GIS and pedestrian-accessibility sections show that neighborhood analysis depends on real pedestrian routes, not Euclidean distance. Quality: high.
- Koljensic (2022): in the thesis-level methods and comparative discussion, the emphasis is on spatial and sociodemographic attributes, again supporting network-based service analysis. Quality: medium to high, because the paper is more comparative but still methodologically relevant.

This means the routing logic is not arbitrary; it follows the standard operating logic of GIS-based pedestrian accessibility studies.

### 3.3 Distance decay function

The code uses this formula:

- `math.exp(-beta * dist)`
- with `beta = 0.002`

This is a direct implementation of the exponential distance decay used in the literature, especially:

- Weng et al. (2019)
- Murgante & Annunziata (2025)
- the project design in [AGENTS.md](AGENTS.md)

This matches the mathematical structure described in the project documentation:

- `f(d) = e^{-beta * d}`
- for `d <= 1200`
- and zero beyond that cutoff

This is correct and well-supported by the literature. The logic is sound because nearby services contribute much more to access than distant ones, which is exactly the point of distance decay.

Source-specific evidence:

- Weng et al. (2019): in the abstract and method sections, the authors explicitly use an exponential distance-decay function to model accessibility decline with distance. This is the closest direct match to the code’s `exp(-beta * d)` term. Quality: high.
- Murgante & Annunziata (2025): in the method section they use an attraction-reach approach with a distance-decay logic over a 1200 m threshold, which is conceptually similar to the current implementation. Quality: high.
- The project documentation in [AGENTS.md](AGENTS.md) also formalizes the same structure mathematically, which gives a consistent research standard for the implementation. Quality: high as an internal methodological specification.

The key point is that the decay is not just a convenience—it is a well-established method for preventing all destinations within the threshold from being treated as equally valuable.

### 3.4 2SFCA supply-demand logic

The implementation contains the core two-step logic:

1. Step 1: compute service supply per demand weight:

   - `potential_demand += row["population"] * math.exp(-beta * dist)`
   - `poi_supply_ratios[pid] = capacity / potential_demand`

2. Step 2: for each neighborhood, aggregate weighted supply accessible from that neighborhood:

   - `raw_scores[cat] += poi_supply_ratios[pid] * math.exp(-beta * dist)`

This is the essence of the 2SFCA family, which was introduced by Luo & Wang (2003) and later extended with distance decay in enhanced 2SFCA approaches.

This is the strongest part of the implementation and matches the theory in the project documentation.

Why it is correct:

- 2SFCA explicitly models supply and demand together
- it avoids the major weakness of simple service-count approaches
- the use of a distance-decayed demand term is consistent with enhanced 2SFCA formulations

Source-specific evidence:

- Luo & Wang (2003): this paper is the foundational source for the 2SFCA method. In the abstract and method sections, the authors formalize the two-stage supply-demand logic and show that access is a function of both service availability and demand pressure. This is the direct methodological source behind the script’s `poi_supply_ratios` and neighborhood-level aggregation. Quality: very high.
- The project documentation in [THESIS_REPORT.md](THESIS_REPORT.md) and [AGENTS.md](AGENTS.md) explicitly explains the use of 2SFCA with distance decay and saturation, which is a faithful extension of the original method rather than a deviation from it. Quality: high.
- The enhanced version of the method (as discussed in the literature review and project notes) adds continuous decay within the catchment, which is exactly what the code does through the `exp(-beta * dist)` term. Quality: high.

This is the proper conceptual foundation for spatial justice analysis.

### 3.5 Capping and threshold saturation

The implementation uses:

- `capped_ratio = min(raw_ratio / ideal, 1.0)`
- `regions.at[idx, score_col(cat)] = round(capped_ratio * 100, 2)`

This is exactly the logic described in the research design and is consistent with:

- Duncan et al. (2011)
- Walk Score methodology
- AGENTS and CLAUDE documentation

This is scientifically reasonable because:

- a neighborhood should not receive unlimited score merely because it has an oversized service concentration
- the local objective is to measure whether a service meets the neighborhood need, not whether the neighborhood has an excessive number of facilities

Source-specific evidence:

- Duncan et al. (2011) / Walk Score methodology: in the methodological discussion, the value of a given service is treated as meaningful only up to a threshold of adequate access; beyond that, returns diminish. This is the direct conceptual basis for the code’s `min(raw_ratio / ideal, 1.0)` formula. Quality: high.
- Plaza-Herrera & Mercadé-Aloy (2025): the paper’s abstract and methods explicitly discuss age-sensitive accessibility and threshold-based evaluation of service adequacy, which supports the idea that accessibility should be normalized rather than left unbounded. Quality: high.
- The project specification in [AGENTS.md](AGENTS.md) also formalizes the same logic as a research rule: after reaching the ideal threshold, the score saturates. This is consistent with the broader literature and not an ad hoc design decision. Quality: high.

This is one of the most defensible aspects of the model.

### 3.6 Weighting and MCDA logic

The script defines `global_weights` and then computes:

- `total_weighted_index += capped_ratio * global_weights[cat]`
- `Index_15Min = weighted_index * 100`

This is aligned with the project’s MCDA reasoning, where the weights are meant to reflect citizen preferences collected by questionnaire and then combined with accessibility scores.

This is conceptually valid, but the actual weights are still placeholders based on the project specification, not yet final MCDA outputs. That is acceptable as a prototype, but not as a finalized research result.

Source-specific evidence:

- Mañago et al. (2025): in the methods section, the authors explicitly construct a composite index using weighted service components, which supports the concept that a 15-minute city index should combine multiple service categories. The method is robust, but it does not validate a single final weight vector for Tehran. Quality: high for the general principle; medium for transferability to this exact dataset.
- Plaza-Herrera & Mercadé-Aloy (2025): the paper’s age-sensitive assessments and weighting logic show that different population groups can change the effective importance of services. This supports the idea that final weights should come from validated preference data rather than a generic default. Quality: high for the principle, medium for exact implementation.
- The project’s own documentation states clearly that weights are temporary placeholders and should eventually be replaced by the final AHP/Likert results. This is an honest and methodologically correct position. Quality: high.

This is therefore a legitimate prototype structure, but not yet a final weighted index claim.

### 3.7 OSM mapping logic

The function `get_category_from_tags` maps environmental tags such as:

- `amenity`, `shop`, `leisure`, `highway`, `station`, `office`

to the research categories such as `q14_park`, `q18_bus_stop`, `q4_hospital`, etc.

This is aligned with the mapping table in [AGENTS.md](AGENTS.md) and the code design in [CLAUDE.md](CLAUDE.md).

Why it is correct:

- the mapping is needed to connect OSM data to the research variables
- the code is consistent with the variable list in the questionnaire
- the ordering of conditions matters and is documented in the project rules

Source-specific evidence:

- The variable-to-tag mapping is supported by the project’s literature synthesis in [THESIS_REPORT.md](THESIS_REPORT.md), which draws directly from the reviewed studies that use OSM and GIS to operationalize services such as parks, schools, transit, and healthcare. Quality: medium to high, because the literature is methodologically supportive but not all papers share the exact same OSM tag taxonomy.
- In the core 15-minute city papers, the method is consistently built on service categories (education, retail, recreation, health, transit, public facilities), and the code follows the same category structure. Quality: high for conceptual alignment.
- The practical issue is not the logic of the mapping itself, but the quality of tagging in OSM. Some categories are not consistently coded, so edge-case errors are possible. This is a known limitation of the data source, not a flaw in the general method. Quality: high.

In principle this is valid. In practice, the category mapping can still produce edge-case errors because many OSM features are imperfectly tagged.

---

## 4. What is implemented correctly

The following parts of the implementation are well-grounded and methodologically sound:

1. Use of pedestrian network rather than straight-line distance.
2. Use of a cutoff of 1200 meters.
3. Use of exponential decay for distance.
4. Use of 2SFCA-style supply-demand model.
5. Use of capping to avoid infinite or unrealistic scores.
6. Use of separate score columns for each category and a weighted overall index.
7. Use of GeoPackage + Shapefile + field dictionary output design.
8. Strong alignment with the project methodology described in the documentation.

These elements are not arbitrary—they are built directly from the literature and the project rationale.

---

## 5. What is still weak or not yet fully valid

These are the main limitations of the current implementation.

### 5.1 Population is placeholder data

This is the biggest issue.

The code contains:

- `if "population" not in regions.columns: regions["population"] = 5000`

This is explicitly identified in [AGENTS.md](AGENTS.md) as a temporary fallback and is not acceptable as a final scientific result.

Why this matters:

- 2SFCA is fundamentally about supply relative to demand
- if every neighborhood has the same artificial population, the residential competition part becomes meaningless
- the results cannot be interpreted as real spatial justice without actual population data

This is the single most important limitation.

### 5.2 The model uses a single centroid per neighborhood

The script uses:

- `regions["lon"] = regions.geometry.centroid.x`
- `regions["lat"] = regions.geometry.centroid.y`

This is a common simplification, but it creates a Modifiable Areal Unit Problem (MAUP) and ignores internal variation within large neighborhoods.

This is discussed explicitly in [AGENTS.md](AGENTS.md) as a known limitation.

Valid in a prototype, but not ideal for final scientific claims.

### 5.3 Some service types are conceptually simplified

Examples include:

- `q22_main_street` based on `highway in ['primary', 'secondary']`
- `q17_public_space` using `amenity='cafe'` or `highway='pedestrian'`

These are not equivalent to full service accessibility measures and may be overly broad or conceptually weak.

The literature supports the treatment of transport and public space as service categories, but the exact operationalization must be justified carefully.

### 5.4 Point feature capacity assumptions are rough

The code uses `area_sqm` for polygon-based features and a nominal capacity of `1.0` for most count-based features.

For some POIs, especially point-based public facilities, this can be too simplistic. This is acknowledged in the project documentation as a known limitation.

### 5.5 Final weights are not yet research-final

The script clearly states that weights are placeholders and should be replaced by the final MCDA results.

This means the current weighted overall index is a valid prototype, but it should not yet be presented as a final published result.

---

## 6. Is the implementation valid overall?

### Verdict: Methodologically valid as a research prototype, but not yet fully valid as a final empirical result.

This is the most accurate conclusion.

Why yes:

- the logic is consistent with established methods in the literature
- the formula choices are correct in concept
- the network and distance-decay elements are standard and defensible
- the 2SFCA and capping structure is appropriate for the research question

Why not final yet:

- population data are not real
- weight data are not final
- neighborhood representation is simplified
- some service definitions are rough
- no sensitivity or validation analysis has been done yet

So the answer is:

- as a methodological implementation: yes, it is credible and consistent with the literature
- as a final thesis finding: not yet, because the inputs and validation are incomplete

---

## 7. Final scientific judgment

The implementation in [src/main.py](src/main.py) is a good and defensible prototype of the chosen research design. It is aligned with the main streams of literature used in the project:

- 15-minute city concept: Moreno et al. (2021)
- pedestrian network accessibility: Caselli et al. (2021), Mañago et al. (2025)
- distance decay: Weng et al. (2019)
- supply-demand logic: Luo & Wang (2003)
- threshold capping: Duncan et al. (2011), Walk Score methodology

The method is therefore correct in principle and structurally consistent with the literature.

However, its final empirical validity depends on replacing the temporary assumptions with real:

- population data,
- final MCDA weights,
- validated POI selection,
- and some sensitivity analysis.

Without that, it should be treated as a strong prototype rather than a final published scientific model.

---

## 8. Recommended next step

The next phase should not be a code rewrite; it should be a validation phase:

1. Replace the mock population with actual neighborhood or block-level population data.
2. Replace the temporary weights with final MCDA values from the questionnaire.
3. Run the pipeline on a small subset first and compare to known accessibility patterns.
4. Check sensitivity for beta and threshold values.
5. Then treat the model as a final empirical analysis.

At that point, the implementation will be scientifically much stronger and much closer to a final thesis-ready method.

---

## 9. Practical conclusion

If your question is: “Is my implementation correct based on the resources?”

The answer is:

- Yes, in terms of method and logic: strongly aligned with the literature.
- No, in terms of final scientific validity: not yet fully, because the current input data are not final.

This is a good research implementation for an MSc thesis pipeline, but it should be framed as a robust prototype that still needs real population data and validated weights before final conclusions are drawn.
