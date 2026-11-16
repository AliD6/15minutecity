# Open Items and Remaining Work

This document groups unfinished work by research component. Implementing and validating the 15-minute city accessibility score is one component of the broader thesis, alongside literature synthesis, spatial-equity analysis, and thesis writing.

---

## 1. Literature review and theoretical foundation

### Completed
- Papers in `papers/` reviewed and summarized in `LITERATURE_REVIEW_SUMMARY.md`.
- Implementation analysis documented in `IMPLEMENTATION_ANALYSIS.md`.
- Theoretical and methodological foundations for the 15-minute city, accessibility, distance decay, and 2SFCA documented.

### Remaining
- Finalize the core papers to cite in the thesis and distinguish primary sources from background sources.
- Develop the consolidated summary into a polished academic literature review chapter.
- Add and verify APA-style in-text citations and full references.
- Distinguish literature supporting the conceptual framework from literature supporting the methods.

---

## 2. Implement and validate the 15-minute city score

This work package covers the full score calculation, from demand and service data through the category scores and the weighted `Index_15Min`. It is a component of the research, not the whole thesis.

### Completed
- Core calculation pipeline implemented in `src/main.py`: walk-network distance, distance decay, 2SFCA-style supply-demand calculation, score capping, weighted aggregation, and output generation.
- OSM category mapping and network-node assignment implemented.
- Capacity and geometry processing logic established.

### Remaining
- Obtain neighborhood or statistical-block population data and incorporate population-based demand into the calculation.
- Implement the questionnaire-based MCDA weight-derivation workflow: determine and document the response-to-weight procedure, calculate and validate the weights (including AHP consistency checks if AHP is used), and make the process reproducible.
- Connect the resulting MCDA weights to the index calculation. The currently configured weights are provisional inputs for the existing pipeline; deriving the research weights is planned work in this work package, not a defect in `main.py`.
- Validate that the implemented OSM-tag-to-questionnaire-category mapping matches the study's predefined categories.
- Check consistent treatment of point and polygon features, capacity values, and missing or poorly tagged facilities.
- Correct and validate spatial calculations that require a projected CRS, including neighborhood demand-point/centroid generation.
- Run a pilot on a subset of neighborhoods, inspect intermediate values and output ranges, then execute the full Tehran calculation.
- Run sensitivity analysis for the distance-decay parameter and access threshold; assess weight sensitivity after the MCDA weight workflow is implemented.
- Check whether `score_q*` columns and `Index_15Min` are within expected ranges and scientifically plausible.
- Finalize a reproducible end-to-end workflow and ensure outputs can be regenerated from documented inputs and parameters.

---

## 3. Spatial justice analysis and interpretation

### Completed
- Conceptual framework for spatial justice and access equity established.
- The 2SFCA supply-demand perspective and the weighted index concept defined.

### Remaining
- Explain the spatial-equity results using a scientifically defensible interpretation.
- Identify underserved neighborhoods and investigate the reasons for their scores.
- Relate the results to documented urban inequality patterns in Tehran.
- Determine and, where appropriate, calculate spatial inequality diagnostics such as a Lorenz curve, Gini coefficient, and Moran's I.
- Interpret the results in relation to residents' daily service access and urban deprivation.

---

## 4. Thesis writing and reporting

### Completed
- Literature review summary and implementation analysis drafted.
- Project methods documented in the internal project documents.

### Remaining
- Write the literature review and methodology chapters in polished academic prose.
- Explain the methodological rationale for combining 2SFCA, distance decay, capping, and questionnaire-derived weights.
- Document assumptions, limitations, data sources, and known data weaknesses.
- Write the results, discussion, and conclusion based only on reproducible analyses.
- Develop evidence-based planning and policy recommendations from the findings.

---

## 5. Final deliverables

### Required outputs
- Literature review, methodology, results and analysis, and discussion/conclusion chapters.
- Verified references list.
- Final code and reproducible workflow.

### Remaining
- Produce the final thesis chapters and supporting outputs.
- Ensure claims and reported results are supported by actual data and reproducible analysis.
- Finalize and verify the code, documentation, and research outputs together.

---

## 6. Priority sequence

1. Implement population-based demand and the questionnaire-based MCDA weight-derivation workflow within the score-calculation work package.
2. Validate the implemented category mapping and spatial processing, then pilot and validate score calculations.
3. Run the full calculation and sensitivity analyses.
4. Conduct spatial-equity analysis and interpret the results.
5. Finalize the literature review, thesis chapters, references, and reproducible deliverables.
