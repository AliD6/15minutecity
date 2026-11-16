# Literature Review Summary: 15-Minute City, Spatial Accessibility, and Urban Equity

This document summarizes the papers stored in the `papers/` folder and translates them into a research background for the thesis on spatial justice and the 15-minute city in Tehran.

---

## 1. Research context and main takeaway

The literature shows that the 15-minute city concept is not just about proximity; it is about whether daily needs are reachable on foot or by short active travel within a practical threshold. Most papers agree on three core ideas:

- Everyday urban services should be accessible within about 15 minutes on foot or by bike.
- Accessibility varies significantly by age, income, mobility, and location.
- A city can have nearby services but still be unequal if population pressure, service capacity, and spatial distribution are ignored.

Across the reviewed studies, the strongest patterns are:

1. Network-based accessibility measures are more realistic than Euclidean buffers.
2. Distance decay matters: services far away matter much less than nearby services.
3. Age-sensitive assessments show that elderly and vulnerable groups often face lower access.
4. Most studies still rely on service counts or simple coverage ratios, while fewer integrate supply-demand competition explicitly.
5. There is a clear research gap in combining OSM, network analysis, 2SFCA, MCDA weighting, and spatial equity in a single framework for Tehran.

This is the main methodological contribution of the current thesis.

---

## 2. Paper-by-paper summary

### 1) Inclusive 15-minute cities: An age-sensitive assessment of active accessibility in the metropolitan area of Barcelona
File: `1-s2.0-S0264275125003919-main.pdf`

- Main idea: The 15-minute city should be evaluated not only for the average resident, but for different age groups.
- Method: Active accessibility assessment over a metropolitan area, with age-specific thresholds and service categories.
- Findings: Access is uneven across age groups; seniors and some groups face significantly lower accessibility than younger populations.
- Why it matters: It strongly supports the idea that spatial justice is not only geographic but also demographic and social.
- Relevance to thesis: This paper supports the need to distinguish between average accessibility and equity-sensitive accessibility, which aligns with the thesis objective of combining accessibility and justice.

### 2) 15-minute city and active accessibility / transportation research procedural paper
File: `1-s2.0-S2352146521009455-main.pdf`

- Main idea: Urban accessibility is strongly tied to how quickly essential services can be reached by active modes.
- Method: GIS and network-based analysis of service accessibility.
- Findings: A service network can be spatially close on paper but still weak in practice when network connectivity, travel times, and barriers are considered.
- Why it matters: It reinforces the need to use real pedestrian networks rather than simple geometric distances.
- Relevance to thesis: Very relevant because the thesis is based on walk-network distance and 15-minute thresholds.

### 3) Developing a Geospatial Framework for Calculating a 15-Minute City Index (FMCI): The Case of Quezon City
File: `134261.pdf`

- Main idea: The paper builds an index for 15-minute accessibility using geospatial frameworks.
- Method: Service area analysis and network analysis for urban neighborhood accessibility, with a composite urban index.
- Findings: The 15-minute city can be operationalized through measurable spatial indices, but results depend heavily on the chosen threshold and urban service mix.
- Why it matters: It shows the value of translating the concept into a spatial index.
- Relevance to thesis: This is one of the clearest methodological references for building an operational 15-minute city index.

### 4) Application of the 15-Minute City Criteria to a Metropolitan Area: A Case Study of the Metropolitan City of Cagliari, Italy
File: `Application-of-the-15-Minute-City-Criteria-to-a-Metropolitan-Area_-A-Case-Study-of-the-Metropolitan-City-of-Cagliari-Italy.pdf`

- Main idea: The 15-minute city concept can be applied to metropolitan regions, not only central urban cores.
- Method: GIS-based application of accessibility criteria and service distribution across a metropolitan area.
- Findings: Accessibility is uneven across municipalities and peri-urban areas; metropolitan structures often create unequal access beyond city centers.
- Why it matters: It highlights the spatial mismatch between service distribution and metropolitan expansion.
- Relevance to thesis: Important for the Tehran case, where neighborhood-level inequalities are likely shaped by urban geography and peripheral disadvantage.

### 5) From urban planning techniques to 15-minute neighbourhoods: A theoretical framework and GIS-based analysis of pedestrian accessibility to public services
File: `ET_2021_85_10.pdf`

- Main idea: The paper moves from classic urban planning concepts to a 15-minute neighborhood framework.
- Method: Theoretical framework plus GIS-based analysis of pedestrian accessibility to public services.
- Findings: The neighborhood scale matters; service access is shaped by both land-use mix and pedestrian network quality.
- Why it matters: It bridges planning theory with operational GIS methods.
- Relevance to thesis: This paper is highly relevant to the thesis methodology because it supports a neighborhood-scale, GIS-based, network-dependent interpretation of 15-minute access.

### 6) Analysis of 15-Minute City Index regarding Spatial and Sociodemographic Attributes: Based on a Case Study of Amsterdam
File: `Koljensic Petar - 2022 - Analysis of 15-Minute City Index regarding Spatial and...pdf`

- Main idea: The 15-minute city should be assessed across social and spatial dimensions, not only as a physical proximity measure.
- Method: Spatial and sociodemographic analysis of the city of Amsterdam.
- Findings: Spatial structure and sociodemographic characteristics strongly affect access; outer areas and vulnerable groups often perform worse.
- Why it matters: It strengthens the argument that 15-minute city outcomes are socially differentiated.
- Relevance to thesis: Useful for framing the equity dimension of the Tehran study and for considering how geography and demographics interact.

### 7) Investigating factors affecting realization of the 15-minute city in urban neighborhoods (Case study: Ahmadabad neighborhood, Mashhad)
File: `URBANPLANING10_113.pdf`

- Main idea: The 15-minute city is not only a policy concept but a neighborhood-level urban form issue.
- Method: Local case study in a neighborhood of Mashhad, with AHP-based weighting of factors under urban planning.
- Findings: Factors such as accessibility to services, walking infrastructure, and proximity to jobs are key to realization.
- Why it matters: It captures the Iranian urban planning context and the role of neighborhood design.
- Relevance to thesis: Very relevant because it provides a local Iranian perspective on the operationalization of the 15-minute city concept.

### 8) Theoretical model of the realization of the 15-minute city in urban planning (systematic review / meta-synthesis)
File: `USD_Volume 4_Issue 11_Pages 89-111.pdf`

- Main idea: The paper develops a theoretical model for the realization of the 15-minute city through a systematic review.
- Method: Meta-synthesis and conceptual model building.
- Findings: Key factors include proximity, mixed land use, public services, social needs, and environmental sustainability.
- Why it matters: It provides the conceptual framework behind many empirical applications.
- Relevance to thesis: Very useful for establishing the theoretical foundation of the thesis and for connecting the concept to urban planning theory.

### 9) Walkability Index for Elderly Health: A Proposal
File: `Walkability_Index_for_Elderly_Health_A_Proposal.pdf`

- Main idea: Walkability is not universal; it must be assessed differently for older adults.
- Method: Proposal of a walkability index oriented toward elderly health and daily accessibility.
- Findings: Elderly mobility is affected by sidewalk quality, pedestrian safety, route continuity, and local service access.
- Why it matters: It shows that access is shaped not only by distance but by route quality and vulnerability.
- Relevance to thesis: It strengthens the case for age-sensitive analysis and supports the inclusion of walkability-related justice considerations.

### 10) The integration of geospatial analyses based on AI in GIS in the context of the “15-minute city” concept
File: `bb81ddf12bf59145929079b5699c7bc398ed.pdf`

- Main idea: AI-supported geospatial analysis can enhance urban accessibility assessment.
- Method: GIS-based analysis integrated with AI-assisted geospatial methods.
- Findings: Spatial analysis can be improved by combining computational intelligence with classic GIS operations, especially in large urban scales.
- Why it matters: It shows how modern urban analysis moves beyond basic mapping toward machine-assisted scenario testing.
- Relevance to thesis: Less central to the core thesis but useful as a methodological direction for future expansion, especially for scaling and automation.

### 11) Designing the 15-minute city at the street scale: a bottom-up analysis of social proximity
File: `csanchezpedreno,+01BROWNRIGG_CyT220+Mtds.pdf`

- Main idea: The 15-minute city should be assessed at the street level, not only at the neighborhood or city scale.
- Method: Bottom-up, neighborhood-level, social proximity analysis.
- Findings: Social proximity and local service access are shaped by small-scale urban design, not only by administrative boundaries.
- Why it matters: It broadens the concept from service coverage to lived urban experience.
- Relevance to thesis: It supports the idea that access should be evaluated at multiple scales and that the human experience of the city matters.

### 12) The role of GIS in promoting the 15-minute city concept for sustainable urban development using network analysis (Case study: El Rehab city)
File: `document.pdf`

- Main idea: A GIS-based network analysis approach can operationalize the 15-minute city concept in a planned city.
- Method: Network analysis and GIS-based spatial evaluation.
- Findings: Spatial accessibility to essential services can be clearly mapped and compared across areas.
- Why it matters: It shows the practical value of GIS tools for planning and policy.
- Relevance to thesis: Directly relevant because the thesis uses the same principle of GIS + network analysis for Tehran.

### 13) Post-Pandemic Urban Planning: Applying the 15-Minute City Approach in Iranian Cities (Case Study: Mehrshahr, Karaj)
File: `mdrsjrns-v3n2p97-en.pdf`

- Main idea: The 15-minute city model is a useful planning response after the pandemic, especially in Iranian urban systems.
- Method: Iranian urban planning case study with neighborhood-level evaluation.
- Findings: The concept provides a path toward more resilient, local, and walkable urban planning.
- Why it matters: It connects global literature with Iranian urban conditions and policy debates.
- Relevance to thesis: Highly relevant because it grounds the 15-minute city concept in the Iranian urban context and strengthens the local justification for the Tehran study.

### 14) The 15-minute city concept: The case study within a neighbourhood of Thessaloniki
File: `shoina-et-al-2024-the-15-minute-city-concept-the-case-study-within-a-neighbourhood-of-thessaloniki-1.pdf`

- Main idea: The local neighborhood is the real scale at which the 15-minute city should be judged.
- Method: Neighborhood case study with local service access analysis.
- Findings: Local service distribution and walking conditions determine whether the neighborhood truly functions as a 15-minute urban unit.
- Why it matters: It emphasizes that large-city indicators can hide important local inequities.
- Relevance to thesis: Strongly relevant because Tehran is also a large city where neighborhood heterogeneity is central.

### 15) Mapping the Implementation Practices of the 15-Minute City
File: `smartcities-07-00083.pdf`

- Main idea: The 15-minute city is being implemented in different ways around the world, and the practice is diverse.
- Method: Review and mapping of implementation practices.
- Findings: There is no single universal model; practice varies based on institutional context, planning culture, transport systems, and governance.
- Why it matters: It reminds us that access indicators must be adapted to local conditions rather than copied blindly.
- Relevance to thesis: Important for contextualizing the Tehran model and for recognizing that local institutions and data conditions matter.

---

## 3. New papers added from the v2 review stage

### 3.1 Is proximity enough? A critical analysis of a 15-minute city considering individual perceptions
File: `1-s2.0-S0264275124000969-main.pdf`

- Main idea: The paper argues that physical proximity alone is not sufficient; individual perceptions and lived experience shape whether a 15-minute city is truly functional.
- Method: Critical review and empirical analysis combining accessibility and perception-based evaluation.
- Findings: Even when services are nearby, real accessibility depends on how residents perceive distance, safety, comfort, and usability.
- Why it matters: This paper challenges the simplistic assumption that geographic proximity automatically equals justice or usability.
- Relevance to thesis: Very relevant, because the thesis relies on objective network access but also needs to acknowledge that perceived access and real lived access are not identical.

### 3.2 An assessment framework for 15-minute Cities: Progress worldwide and the impact of urban form
File: `1-s2.0-S0965856425002113-main.pdf`

- Main idea: The paper proposes a framework for assessing 15-minute cities worldwide and examines the role of urban form.
- Method: Comparative assessment and review of global progress in 15-minute city implementation.
- Findings: Urban form strongly shapes the feasibility of 15-minute services, and implementation varies from city to city.
- Why it matters: It strengthens the argument that the concept is not universal in practice; local morphology, density, and street structure matter.
- Relevance to thesis: Useful for contextualizing the Tehran case and for justifying a city-specific adaptation rather than a generic global formula.

### 3.3 The 15-minute city revisited: A GIS approach to measuring, visualizing, and analyzing accessibility by proximity and by public transport supply
File: `1-s2.0-S2214367X25001693-main.pdf`

- Main idea: The paper revisits the 15-minute city concept and evaluates accessibility both by proximity and by public transport supply.
- Method: GIS-based spatial analysis of accessibility patterns.
- Findings: Access by proximity and access by transit supply are not equivalent; multimodal supply strongly affects the practical service radius.
- Why it matters: It moves beyond the simple walk-only model and reminds researchers that accessibility is sensitive to available transport modes and connectivity.
- Relevance to thesis: Relevant but not central, because the thesis focuses on walking accessibility and neighborhood-level active access.

### 3.4 A robust method for evaluating the potentials of 15-minute cities: Implications for sustainable urban futures
File: `1-s2.0-S2666683924000646-main.pdf`

- Main idea: The paper proposes a robust method to assess the potentials of 15-minute cities at the urban scale.
- Method: Evaluation framework for measuring implementation potential and sustainability consequences.
- Findings: The quality of urban accessibility depends on both service availability and system robustness across the urban fabric.
- Why it matters: It supports the idea that 15-minute city analysis should move beyond static counts toward more integrated assessment frameworks.
- Relevance to thesis: Useful as a methodological guide for building a stronger evaluation framework and for discussing sustainability implications.

### 3.5 Are Italian cities already 15-minute? Presenting the Next Proximity Index: A novel and scalable way to measure it, based on open data
File: `1-s2.0-S2667091723000134-main.pdf`

- Main idea: The paper proposes a new index for proximity-based accessibility using open data.
- Method: Open-data-based GIS measurement of a proximity index.
- Findings: The index can operationalize the 15-minute city in a scalable way across many places.
- Why it matters: It provides evidence that proximity metrics can be standardized and scaled across cities.
- Relevance to thesis: Useful for thinking about how to create a citywide, comparable, and reproducible spatial metric, especially in a Tehran context.

### 3.6 A novel evaluation framework for 15-minute city using satellite imagery
File: `3748636.3764182.pdf`

- Main idea: The paper uses satellite imagery to evaluate the physical and spatial structure of 15-minute cities.
- Method: Remote sensing and spatial feature extraction combined with urban evaluation.
- Findings: Built form and land-use patterns visible from imagery can help proxy service access and neighborhood compactness.
- Why it matters: It expands the data frontier beyond standard GIS and OSM datasets.
- Relevance to thesis: Less direct for the current Tehran model, but useful for future extensions that combine urban form and remote sensing.

### 3.7 Assessing the readiness for 15-minute cities: a literature review on performance metrics and implementation challenges worldwide
File: `Assessing the readiness for 15-minute cities  a literature review on performance metrics and implementation challenges worldwide.pdf`

- Main idea: This paper reviews the readiness of cities to implement 15-minute city planning and identifies key performance metrics and implementation barriers.
- Method: Literature review of implementation standards, barriers, and performance measures.
- Findings: Cities differ widely in readiness, and implementation is shaped by governance, land-use patterns, infrastructure, and inequality.
- Why it matters: It provides a strong policy framing for why the concept must be contextualized rather than copied directly.
- Relevance to thesis: Highly relevant for the conceptual framing of Tehran as a city with specific governance and urban form constraints.

### 3.8 Quantifying and visualizing the 15-Minute walkable city concept across Europe: a multicriteria approach
File: `Quantifying and visualizing the 15-Minute walkable city concept across Europe  a multicriteria approach.pdf`

- Main idea: This paper quantifies and visualizes the 15-minute walkable city concept using a multicriteria approach.
- Method: Multicriteria evaluation across European cities.
- Findings: Walkability and service accessibility are multi-dimensional and cannot be reduced to a single binary threshold.
- Why it matters: It supports the use of multi-criteria evaluation rather than simple one-criterion coverage measures.
- Relevance to thesis: Very relevant, because the project also combines multiple service categories and weighting logic in a multicriteria framework.

### 3.9 Accessibility inequality across Europe: a comparison of 15-minute pedestrian accessibility in cities with 100,000 or more inhabitants
File: `s42949-023-00133-w.pdf`

- Main idea: The paper compares 15-minute pedestrian accessibility across European cities and measures inequality.
- Method: Cross-city comparison of pedestrian accessibility and inequality using service accessibility indicators.
- Findings: Accessibility is unequal even across relatively similar urban systems; some cities have far more balanced access than others.
- Why it matters: It provides a strong empirical basis for the spatial inequality dimension of the research.
- Relevance to thesis: Central to the project’s objective of evaluating not only access but also social and spatial inequity.

### 3.10 Barcelona under the 15-Minute City Lens: Mapping the Accessibility and Proximity Potential Based on Pedestrian Travel Times
File: `smartcities-05-00010-v2.pdf`

- Main idea: The paper maps accessibility and proximity potential in Barcelona based on pedestrian travel times.
- Method: GIS mapping of pedestrian travel-time networks and service proximity.
- Findings: The city is easier to evaluate when spatial access is mapped in travel-time terms rather than administrative boundaries alone.
- Why it matters: It shows the value of pedestrian travel-time analyses for identifying service gaps and local deprivation.
- Relevance to thesis: Strongly relevant because the Tehran approach similarly relies on pedestrian travel times and spatially explicit neighborhood analysis.

### 3.11 A framework on 15-minute city and sustainable urban futures
File: `1-s2.0-S2352146525007069-main.pdf`

- Main idea: The paper frames the 15-minute city as part of broader sustainable urban future planning.
- Method: Conceptual and applied framing of the city as a sustainable, proximate, and service-oriented urban system.
- Findings: The concept should be understood not just as a planning ideal but as a sustainability and quality-of-life strategy.
- Why it matters: It expands the literature beyond access metrics to include urban sustainability and social livability.
- Relevance to thesis: Useful for situating the project within the broader sustainability discourse of urban planning.

### 3.12 A broader literature and method review on 15-minute cities and public service accessibility
File: `100-Article Text-103-1-10-20261010.pdf`

- Main idea: This paper broadens the literature base on 15-minute cities by connecting them to public service accessibility and urban function.
- Method: Review and synthesis of urban accessibility literature and planning practice.
- Findings: A city’s service structure and accessibility performance determine whether the 15-minute objective is operationally achievable.
- Why it matters: It strengthens the need for context-sensitive and evidence-based evaluation.
- Relevance to thesis: It complements the earlier review by emphasizing that accessibility is a function of service structure, not just distance.

---

## 4. Cross-paper insights

The reviewed papers collectively suggest the following research direction for the thesis:

### A. The 15-minute city is a spatial accessibility concept, not just a slogan
Most studies define it in terms of walking distance or time thresholds, but only a subset measure service access in a precise and comparable manner.

### B. Accessibility is not equal to justice
A place may have services nearby but still suffer from unequal distribution, over-concentration, or unfair service competition. This is especially important in dense urban systems like Tehran.

### C. Distance decay and capacity matter
Studies increasingly show that proximity alone is too simplistic. The value of a service decreases with distance, and service capacity matters. This supports the use of a decay function + 2SFCA structure in the thesis.

### D. Vulnerable groups require different metrics
Elderly residents, children, and lower-mobility groups often face greater barriers. This supports the argument that equity should be evaluated not just by the average point, but by spatially differentiated disadvantage.

### E. GIS and OSM are central tools
Most of the empirical work uses GIS, network analysis, service areas, or data from open spatial platforms. This aligns directly with the thesis design using OSM, NetworkX, and GeoPandas.

---

## 4. Research gap revealed by the papers

The literature review clearly indicates a gap in the current state of the art:

- Many studies use binary access thresholds or simple service counts.
- Fewer studies apply continuous distance decay functions.
- Very few integrate both supply-demand competition and weighted citizen preferences into the same model.
- Local Iranian urban studies are often conceptual or small-scale, not citywide and network-based.
- There is limited work linking 15-minute city metrics with spatial justice in Tehran at the neighborhood level.

This is exactly where the current thesis contributes: it combines walk-network analysis, supply-demand competition, capacity thresholds, population context, and person-centered MCDA weights into a single spatial equity framework.

---

## 5. How these papers inform the thesis design

The papers collectively support the following decisions for the thesis:

- Use walk-network distance rather than straight-line distance.
- Use a 15-minute threshold equivalent to roughly 1200 meters.
- Apply distance decay to reflect diminishing access with increasing distance.
- Use 2SFCA to account for competition between demand points and service supply.
- Use threshold capping to avoid unlimited scores from over-supply.
- Use citizen-based weights rather than only expert-driven weights.
- Evaluate both neighborhood-level access and spatial inequality.

---

## 6. Bottom-line conclusion

The reviewed literature confirms that the 15-minute city is an important and widely discussed planning concept, but the real challenge is not only whether a service exists nearby. The real challenge is whether the service is actually accessible, sufficiently capacitated, equitably distributed, and valued by residents.

This thesis responds to that challenge by combining:

- OSM-based urban service data,
- network analysis,
- distance decay,
- 2SFCA supply-demand logic,
- threshold saturation,
- and citizen-prioritized weighting.

This makes the research methodologically stronger than the standard binary coverage approaches that dominate much of the literature.

---

## 7. Suggested next step for the thesis

Use this summary as the literature review foundation and then translate the findings into a formal literature review chapter with:

- conceptual definitions,
- an overview of the 15-minute city concept,
- a review of accessibility and justice models,
- the gap in Tehran-specific research,
- and the thesis contribution.

