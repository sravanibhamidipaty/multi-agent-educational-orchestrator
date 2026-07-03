Hand-made gold triples of **(question, correct answer, paragraph)** for evaluating the
retrieval + verification stack.

### 01
- **question:** What is a node in a network?
- **relevant_chapter:** 2
- **correct_answer:** A node (vertex) is a fundamental component of a network representing one element of the system — a person, web page, protein, etc. — while links connect nodes. A maximal set of nodes mutually reachable by paths forms a *component*, and a network is *connected* if every pair of nodes is joined by a path.
- **gold_paragraph:** "A network is connected if all pairs of nodes in the network are connected. A network is disconnected if there is at least one pair with d = ∞ … we call its two subnetworks components or clusters. A component is a subset of nodes … there is a path between any two nodes that belong to the component … Such a link is called a bridge." *(chapter_02.txt · chunk 27)*

### 02
- **question:** How does the scale-free network form?
- **relevant_chapter:** 5
- **correct_answer:** A scale-free network emerges from two jointly necessary mechanisms captured by the Barabási–Albert model: *growth* (new nodes are continually added) and *preferential attachment* (new nodes link preferentially to already well-connected nodes). These two are necessary and sufficient — remove either and the scale-free property or stationarity is lost.
- **gold_paragraph:** "The Barabási-Albert model raises a fundamental question: Is the combination of growth and preferential attachment the real reason why networks are scale-free? … growth and preferential attachment are jointly needed to generate scale-free networks, hence if one of them is absent, either the scale-free property or stationarity is lost. Second … if they are both present, they do lead to scale-free networks." *(chapter_05.txt · chunk 39)*

### 03
- **question:** What is the clustering coefficient?
- **relevant_chapter:** 2
- **correct_answer:** The local clustering coefficient measures how interconnected a node's neighbors are — the fraction of possible links among its neighbors that actually exist. For a node *i* of degree *kᵢ* it is `Cᵢ = 2Lᵢ / (kᵢ(kᵢ−1))`, where *Lᵢ* is the number of links among *i*'s neighbors; it ranges from 0 (no neighbor links) to 1 (neighbors form a complete graph).
- **gold_paragraph:** "The clustering coefficient captures the degree to which the neighbors of a given node link to each other. For a node i with degree k the local clustering coefficient is defined as … 2Lᵢ / (kᵢ(kᵢ−1)) where Lᵢ represents the number of links between the kᵢ neighbors of node i. Note that Cᵢ is between 0 and 1: Cᵢ = 0 if none of the neighbors … link to each other. Cᵢ = 1 if the neighbors … form a complete graph." *(chapter_02.txt · chunk 29)*

### 04
- **question:** What is preferential attachment?
- **relevant_chapter:** 5
- **correct_answer:** Preferential attachment is the tendency of new nodes to connect to higher-degree nodes with probability proportional to their degree ("rich-get-richer"). In the Barabási–Albert model it coexists with growth; the limiting Models A and B show that isolating either ingredient fails to reproduce the scale-free property.
- **gold_paragraph:** "The coexistence of growth and preferential attachment in the Barabási-Albert model raises an important question: Are they both necessary for the emergence of the scale-free property? … we discuss two limiting cases of the model, each containing only one of the two ingredients. Model A … keep the growing character … and eliminate preferential attachment." *(chapter_05.txt · chunk 14)*

### 05
- **question:** What is a random network?
- **relevant_chapter:** 3
- **correct_answer:** A random network (Erdős–Rényi model) connects N nodes by placing links completely at random, each of the N(N−1)/2 possible pairs linked independently with probability p. It is the baseline model that embraces the apparent randomness of real networks.
- **gold_paragraph:** "Network science aims to build models that reproduce the properties of real networks. Most networks … do not have the comforting regularity of a crystal lattice … at first inspection they look as if they were spun randomly. Random network theory embraces this apparent randomness by constructing and characterizing networks that [are wired randomly]." *(chapter_03.txt · chunk 1)*

### 06
- **question:** What is the small world phenomenon?
- **relevant_chapter:** 3
- **correct_answer:** The small world phenomenon (six degrees of separation) is the observation that the distance between any two nodes in a network is unexpectedly small — the average shortest path length grows only logarithmically with the number of nodes.
- **gold_paragraph:** "According to six degrees of separation two individuals, anywhere in the world, can be connected through a chain of six or fewer acquaintances … In the language of network science six degrees, also called the small world property, means that the distance between any two nodes in a network is unexpectedly small … the distance between two randomly chosen nodes in a network is short." *(chapter_03.txt · chunk 23)*

### 07
- **question:** What is a power law degree distribution?
- **relevant_chapter:** 4
- **correct_answer:** A power-law degree distribution has the form `p_k ~ k^(−γ)`, so the probability of a node having degree *k* decays polynomially rather than exponentially. This yields many small-degree nodes and a few very high-degree hubs, and has no characteristic scale — the signature of scale-free networks. *(Retrieved passage covers the statistical procedure for fitting the exponent γ.)*
- **gold_paragraph:** "As the degree distribution is typically provided as a list of positive integers … we aim to estimate γ from a discrete set of data points. We use the citation network to illustrate the procedure. The network consists of N=384,362 nodes, each node representing a research paper published between 1890 and 2009 …" *(chapter_04.txt · chunk 63)*

### 08
- **question:** What is network robustness?
- **relevant_chapter:** 8
- **correct_answer:** Robustness is a network's ability to retain its connectivity (a giant component) when a fraction of nodes or links is removed. Scale-free networks are remarkably robust to random failures but fragile to targeted attacks on hubs; the analysis rests on percolation theory, with the percolation threshold set by the moments of the degree distribution.
- **gold_paragraph:** "The systematic study of network robustness started with a paper published in Nature by Réka Albert, Hawoong Jeong and Albert-László Barabási, reporting the robustness of scale-free networks to random failures and their fragility to attacks. Yet, the analytical understanding of network robustness relies on percolation theory … the percolation threshold of a scale-free network is determined by the moments of the degree distribution." *(chapter_08.txt · chunk 62)*

### 09
- **question:** How did analyzing web-crawler data reveal a power law instead of a Poisson degree distribution?
- **relevant_chapter:** 0
- **correct_answer:** When the group used Hawoong Jeong's web-crawling robot to measure the WWW's degree distribution, they expected the Poisson distribution predicted by random network theory but instead found a power law — an unprecedented, shocking result implying a few pages act as enormous hubs.
- **gold_paragraph:** "To answer it we needed the Web's degree distribution, which was now provided by Hawoong's robot. The data granted us our first real surprise: We did not see the Poisson distribution that random network theory predicted. A power law greeted us instead … There was no trace in the literature of a network with a power law degree distribution." *(chapter_00.txt · chunk 15)*

### 10
- **question:** What computer-science problem did Barabási map onto invasion percolation in his first network paper?
- **relevant_chapter:** 0
- **correct_answer:** He mapped the *minimal spanning tree* problem — specifically Kruskal's algorithm — onto invasion percolation, a well-known model from statistical physics, in his first network paper submitted to Physical Review Letters on Feb 24, 1995.
- **gold_paragraph:** "One chapter, focusing on the minimal spanning tree problem, particularly piqued my interest … I realized that the Kruskal algorithm described in the book mapped into of a well-known model of statistical physics, called invasion percolation. So … on Feb 24, 1995, I submitted my first paper on networks to Physical Review Letters." *(chapter_00.txt · chunk 1)*

### 11
- **question:** What is a complex system and why can't its behavior be derived from its components alone?
- **relevant_chapter:** 1
- **correct_answer:** A complex system is composed of many interacting components — neurons, genes, people, computers — whose collective behavior emerges from their interactions and so cannot be derived from knowledge of the individual parts alone. Understanding, describing, predicting, and controlling such systems is a central scientific challenge.
- **gold_paragraph:** "These systems are collectively called complex systems, capturing the fact that it is difficult to derive their collective behavior from a knowledge of the system's components. Given the important role complex systems play in our daily life, in science and in economy, their understanding, mathematical description, prediction, and eventually control is one of the major intellectual and scientific [challenges]." *(chapter_01.txt · chunk 4)*

### 12
- **question:** What is a cascading failure, as illustrated by the 2003 Northeast blackout?
- **relevant_chapter:** 1
- **correct_answer:** A cascading failure is a domino-like collapse in which one component's failure overloads and triggers the failure of others across an interconnected system. The August 14, 2003 Northeast blackout — where a local fault cascaded to leave an estimated ~55 million people without power — illustrates how interconnectivity creates system-wide vulnerability.
- **gold_paragraph:** "represents a real image of the US Northeast on August 14, 2003, before and after the blackout that left without power an estimated 45 million people in eight US states and another 10 million in Ontario … Toronto, Detroit, Cleveland, Columbus and Long Island, bright and shining in (a), have gone dark in (b)." *(chapter_01.txt · chunk 0, Section 1.1 Vulnerability Due to Interconnectivity)*

### 13
- **question:** What two forces, network maps and universality, enabled the emergence of network science?
- **relevant_chapter:** 1
- **correct_answer:** Network science emerged from (1) the availability of *network maps* — large-scale data charting the wiring of real systems — and (2) *universality*, the discovery that networks across disparate domains are governed by the same organizing principles and can therefore be studied with a common set of mathematical tools.
- **gold_paragraph:** "A key discovery of network science is that the architecture of networks emerging in various domains of science, nature, and technology are similar to each other, a consequence of being governed by the same organizing principles. Consequently we can use a common set of mathematical tools to explore these systems. This universality is one of the guiding principles of this book." *(chapter_01.txt · chunk 11)*

### 14
- **question:** What is the difference between network science from graph theory?
- **relevant_chapter:** 1
- **correct_answer:** Network science shares many roots with graph theory but is distinguished by its *empirical, data-driven nature* — its focus on real data, function, and utility, and on asking how widely observed properties apply across real systems, rather than on abstract mathematical structures alone.
- **gold_paragraph:** "Several key concepts of network science have their roots in graph theory, a fertile field of mathematics. What distinguishes network science from graph theory is its empirical nature, i.e. its focus on data, function and utility." *(chapter_01.txt · chunk 15, "Empirical, Data Driven Nature")*

### 15
- **question:** Why is network science described as an empirical, data-driven discipline?
- **relevant_chapter:** 1
- **correct_answer:** Because it is grounded in the analysis of real network maps — it focuses on data, function, and utility, testing which properties actually hold across many real systems (enabled by modern technologies that map real networks) rather than deriving them from pure theory.
- **gold_paragraph:** "What distinguishes network science from graph theory is its empirical nature, i.e. its focus on data, function and utility. As we will see in the coming chapters, in network science we are [driven by real data] … major efforts by the scientific community to develop technologies that can map out [real networks]." *(chapter_01.txt · chunk 15)*

### 16
- **question:** How is the average degree of an undirected network related to its number of nodes and links?
- **relevant_chapter:** 2
- **correct_answer:** In an undirected network the total number of links is `L = (1/2) Σ kᵢ`, where the ½ corrects for each link being counted at both endpoints. Hence the average degree is `⟨k⟩ = 2L/N`.
- **gold_paragraph:** "In an undirected network the total number of links, L, can be expressed as the sum of the node degrees: L = (1/2) Σ kᵢ. Here the 1/2 factor corrects for the fact that in the sum each link is counted twice. For example, the link connecting the nodes 2 and 4 … will be counted once in the degree of node 2 and once in the degree of node 4." *(chapter_02.txt · chunk 9)*

### 17
- **question:** What does the degree distribution p_k of a network represent?
- **relevant_chapter:** 2
- **correct_answer:** The degree distribution `p_k` is the probability that a randomly chosen node has degree *k* (equivalently, the fraction of degree-*k* nodes). It underpins key quantities such as `⟨k⟩ = Σ k p_k` and its precise form determines many network phenomena, from robustness to virus spreading.
- **gold_paragraph:** "the average degree of a network can be written as ⟨k⟩ = Σ k p_k … the precise functional form of p_k determines many network phenomena, from network robustness to the spread of viruses. The degree distribution … For the network in (a) with N = 4 … p₁ = 1/4 (one of the four nodes has degree 1), p₂ = 1/2 (two nodes have degree 2)." *(chapter_02.txt · chunk 11)*

### 18
- **question:** What is the transitivity (global clustering coefficient) of a network?
- **relevant_chapter:** 2
- **correct_answer:** The global clustering coefficient (transitivity) measures the overall density of triangles in a network: `C = 3 × (number of triangles) / (number of connected triples)`. The factor of 3 accounts for each triangle contributing three connected triplets.
- **gold_paragraph:** "the global clustering coefficient, defined as C = 3 × NumberOfTriangles / NumberOfConnectedTriples where a connected triplet is an ordered set of three nodes ABC such that A connects to B and B connects to C … The factor three in the numerator is due to the fact that each triangle is counted three times in the triplet count." *(chapter_02.txt · chunk 39)*

### 19
- **question:** How are the diameter and characteristic path length of a network defined?
- **relevant_chapter:** 2
- **correct_answer:** The distance `d_ij` is the length of the shortest path between nodes *i* and *j*. The **diameter** is the largest shortest-path distance in the network, while the **characteristic (average) path length** is the mean distance over all node pairs.
- **gold_paragraph:** "The number of shortest paths, N_ij, and the distance d_ij between nodes i and j can be calculated directly from the adjacency matrix A_ij. d_ij = 1: If there is a direct link … d_ij = 2: If there is a path of length two … The number of paths of length d between i and j is N_ij(d) = [Aᵈ]_ij." *(chapter_02.txt · chunk 24)*

### 20
- **question:** Why does a random network have a Poisson degree distribution?
- **relevant_chapter:** 3
- **correct_answer:** In a random network each node connects independently to others with probability *p*, so its degree follows a binomial distribution, which for large *N* is well approximated by a Poisson distribution. Its key feature is that the distribution depends only on the average degree ⟨k⟩ and is independent of network size.
- **gold_paragraph:** "while the Poisson distribution is only an approximation to the degree distribution of a random network, thanks to its analytical simplicity, it is the preferred form for p_k … Its key feature is that its properties are independent of the network size and depend on a single parameter, the average degree ⟨k⟩." *(chapter_03.txt · chunk 9)*

### 21
- **question:** At what average degree does a giant component emerge in a random network?
- **relevant_chapter:** 3
- **correct_answer:** A giant component emerges at the critical point `⟨k⟩ = 1` (start of the supercritical regime). The network becomes *fully connected* only later, in the connected regime at `⟨k⟩ = ln N`.
- **gold_paragraph:** "Connected Regime: ⟨k⟩ > lnN (p > lnN/N). For sufficiently large p the giant component absorbs all nodes and components, hence N_G ≃ N. In the absence of isolated nodes the network becomes connected. The average degree at which this happens depends on N as ⟨k⟩ = lnN." *(chapter_03.txt · chunk 18)*

### 22
- **question:** What is the connectivity threshold ln(N)/N for a random network to become fully connected?
- **relevant_chapter:** 3
- **correct_answer:** A random network becomes fully connected (no isolated nodes) once `⟨k⟩ ≥ ln N`, i.e. `p ≥ ln N / N`. Because `ln N / N → 0` for large *N*, the network is connected while still sparse — it only becomes a complete graph at ⟨k⟩ = N − 1.
- **gold_paragraph:** "It is useful … to determine how many links we expect for a particular realization of a random network with fixed N and p. The probability that a random network has exactly L links is the product of three terms … [leading to the connectivity threshold analysis at p ~ lnN/N]." *(chapter_03.txt · chunk 5, Section 3.3 Number of Links)*

### 23
- **question:** What does the degree exponent gamma tell us about a scale-free network?
- **relevant_chapter:** 4
- **correct_answer:** The degree exponent γ governs a scale-free network's behavior — especially hub size and whether the second moment ⟨k²⟩ diverges. The most interesting regime is `2 < γ < 3`, where ⟨k²⟩ diverges (the "ultra-small world" with dominant hubs); for γ > 3 hubs are relatively smaller and behavior approaches that of a random network.
- **gold_paragraph:** "we find that the behavior of scale-free networks is sensitive to the value of the degree exponent γ. Theoretically the most interesting regime is 2 < γ < 3, where ⟨k²⟩ [diverges] … For example, if we wish to document the scale-free nature of a network with γ = 5 … the size of the network must exceed N > 10⁸." *(chapter_04.txt · chunk 29)*

### 24
- **question:** Why are hubs present in scale-free networks but effectively forbidden in random networks?
- **relevant_chapter:** 4
- **correct_answer:** In a scale-free network the power-law tail allows a maximum degree that grows as a power of *N*, so hubs can be orders of magnitude larger than the average node. In a random network the exponentially bounded (Poisson) distribution makes such large deviations astronomically unlikely, so comparably large hubs are effectively forbidden.
- **gold_paragraph:** "Overall, hubs in a scale-free network are several orders of magnitude larger than the biggest node in a random network with the same N and ⟨k⟩ … if the degree distribution were to follow an exponential, (4.17) predicts that the maximum [degree would be tiny by comparison]." *(chapter_04.txt · chunk 10)*

### 25
- **question:** Why do scale-free networks with gamma below 3 lack a meaningful internal scale?
- **relevant_chapter:** 4
- **correct_answer:** For `2 < γ < 3` the second moment ⟨k²⟩ diverges as N → ∞, so the fluctuations in degree have no finite characteristic value — there is no typical degree that characterizes the network. This absence of an internal scale is exactly why such networks are called "scale-free."
- **gold_paragraph:** "we find that the behavior of scale-free networks is sensitive to the value of the degree exponent γ. Theoretically the most interesting regime is 2 < γ < 3, where ⟨k²⟩ [diverges, leaving no finite characteristic scale]." *(chapter_04.txt · chunk 29)*

### 26
- **question:** How does the configuration model generate a network with a given degree sequence?
- **relevant_chapter:** 4
- **correct_answer:** The configuration model assigns each node a number of *stubs* (half-links) equal to its prescribed degree, then repeatedly picks two random stubs and connects them until all are paired. It reproduces any target degree sequence exactly, though it may generate cycles, self-loops, or multi-links.
- **gold_paragraph:** "Assign a degree to each node, represented as stubs or half-links. The degree sequence is either generated analytically from a preselected p_k distribution, or … extracted from the adjacency matrix of a real network … Randomly select a stub pair and connect them. Then randomly choose another pair from the remaining 2L - 2 stubs … repeated until all stubs are paired up." *(chapter_04.txt · chunk 32)*

### 27
- **question:** What degree exponent does the Barabási–Albert model predict?
- **relevant_chapter:** 5
- **correct_answer:** The Barabási–Albert model predicts a degree exponent `γ = 3`, independent of the parameter *m*, together with a stationary (time- and size-independent) scale-free degree distribution — both confirmed by numerical simulation.
- **gold_paragraph:** "The degree exponent γ is independent of m, a prediction that agrees with the numerical results … according to (5.11) the degree distribution of the Barabási-Albert model is independent of both t and N. Hence the model predicts the emergence of a stationary scale-free state." *(chapter_05.txt · chunk 13)*

### 28
- **question:** Why do older nodes become hubs in the Barabási–Albert model (first-mover advantage)?
- **relevant_chapter:** 5
- **correct_answer:** In the BA model each node's degree grows as a power law in time (`kᵢ(t) ~ (t/tᵢ)^β` with β = 1/2), so nodes added earlier have more time to accumulate links. This "first-mover advantage" means the oldest nodes systematically acquire the highest degrees and become the hubs.
- **gold_paragraph:** "The growth of the degrees of nodes added at time t = 1, 10, 10², 10³, 10⁴, 10⁵ … Each node increases its degree following (5.7). Consequently at any moment the older nodes have higher degrees. The dotted line corresponds to the analytical prediction with β = 1/2." *(chapter_05.txt · chunk 10)*

### 29
- **question:** Why are both growth and preferential attachment necessary for a scale-free network?
- **relevant_chapter:** 5
- **correct_answer:** Both are required: without preferential attachment (Model A) the network grows but has an exponential degree distribution; without growth (Model B) it loses stationarity and converges toward a complete graph. Only the coexistence of growth and preferential attachment yields the scale-free property.
- **gold_paragraph:** "the absence of preferential attachment leads to a growing network with a stationary but exponential degree distribution. In contrast the absence of growth leads to the loss of stationarity … This failure of Models A and B to reproduce the empirically observed scale-free distribution indicates that growth and preferential attachment are simultaneously needed for the emergence of the scale-free property." *(chapter_05.txt · chunk 17)*

### 30
- **question:** What is node fitness in the Bianconi–Barabási model?
- **relevant_chapter:** 6
- **correct_answer:** Fitness η is an intrinsic property of each node capturing its ability to attract links; new links attach preferentially to nodes with both high degree and high fitness. When all fitnesses are equal (ρ(η) = δ(η−1)), the Bianconi–Barabási model reduces to the Barabási–Albert model.
- **gold_paragraph:** "Equation (6.6) is a weighted sum of multiple power-laws, indicating that p_k depends on the precise form of the fitness distribution, ρ(η) … Equal Fitnesses: When all fitnesses are equal, the Bianconi-Barabási model reduces to the Barabási-Albert model. Indeed … ρ(η) = δ(η − 1), capturing the fact that each node has the same fitness η = 1." *(chapter_06.txt · chunk 6)*

### 31
- **question:** How does fitness produce a fit-gets-rich dynamic in evolving networks?
- **relevant_chapter:** 6
- **correct_answer:** A node's degree grows with an exponent β(η) that increases with its fitness, so a fitter node accumulates links faster and can overtake older but less fit nodes — a "fit-gets-rich" dynamic. Measurements on Web documents show the fitness distribution is time-independent and roughly exponential.
- **gold_paragraph:** "each node's degree has a power law time dependence … The slope of each curve is β(η), which corresponds to the node's fitness η … demonstrating that the fitness distribution is time independent. The dashed line suggests that the fitness distribution is well approximated by an exponential." *(chapter_06.txt · chunk 10)*

### 32
- **question:** What does an exponentially bounded fitness distribution imply about how hubs form?
- **relevant_chapter:** 6
- **correct_answer:** With an exponentially bounded fitness distribution the fittest node's advantage is limited, so hubs still emerge through the fit-gets-rich mechanism but no single node captures a finite fraction of all links. The network stays scale-free rather than undergoing winner-takes-all condensation.
- **gold_paragraph:** "The fitness distribution ρ(η) … illustrates the difference in the shape of the two ρ(η) functions … The Barabási-Albert model is a minimal model … it has several well-known limitations: The model predicts γ = 3, while the experimentally observed degree exponents vary between 2 and 5 … [motivating fitness-based extensions]." *(chapter_06.txt · chunk 24)*

### 33
- **question:** What is Bose–Einstein condensation, or the winner-takes-all phenomenon, in a network?
- **relevant_chapter:** 6
- **correct_answer:** By mapping fitness to energy levels, the Bianconi–Barabási model can undergo Bose–Einstein condensation for certain fitness distributions: a single fittest node grabs a finite fraction of all links ("winner-takes-all"), analogous to particles collapsing into the lowest energy state of a Bose gas at low temperature.
- **gold_paragraph:** "In a Fermi gas only one particle is allowed on each energy level, while in a Bose gas there is no such restriction … the precise shape of the fitness distribution determines the topology of a growing network. While fitness distributions like the uniform distribution lead to a scale-free topology, some ρ(η) allow for Bose-Einstein condensation. If a network undergoes a Bose-Einstein condensation, then one or a few nodes grab most of the [links]." *(chapter_06.txt · chunk 22)*

### 34
- **question:** How do initial attractiveness and node deletion change the degree exponent of an evolving network?
- **relevant_chapter:** 6
- **correct_answer:** Both processes shift the degree exponent γ. As long as the network keeps growing, node removal can preserve the scale-free property but changes γ depending on the removal rule; the joint presence of initial attractiveness and node deletion can even drive phase transitions between scale-free and exponential networks.
- **gold_paragraph:** "the joint presence of initial attractiveness and node deletion induces phase transitions between scale-free and exponential networks … in most networks nodes can disappear. Yet as long as the network continues to grow, its scale-free nature can persist. The degree exponent depends, however, on the details governing the node removal process." *(chapter_06.txt · chunk 33)*

### 35
- **question:** What are degree correlations in a network?
- **relevant_chapter:** 7
- **correct_answer:** Degree correlations describe whether nodes tend to link to others of similar or dissimilar degree, captured formally by the degree correlation matrix `e_ij` (the probability a randomly chosen link connects a degree-*i* and a degree-*j* node). Because the matrix is hard to read directly, summary functions such as `k_nn(k)` are used instead.
- **gold_paragraph:** "high-degree nodes tend to connect to low-degree nodes (disassortative) … information about degree correlations is carried by the degree correlation matrix e_ij. Yet, the study of degree correlations through the inspection of e_ij has numerous disadvantages: It is difficult to extract information from the visual inspection of a matrix." *(chapter_07.txt · chunk 7)*

### 36
- **question:** What is the difference between assortative, neutral, and disassortative networks?
- **relevant_chapter:** 7
- **correct_answer:** In an **assortative** network high-degree nodes tend to connect to other high-degree nodes (hubs link to hubs); in a **neutral** network there are no degree correlations; in a **disassortative** network high-degree nodes tend to connect to low-degree nodes (hubs avoid hubs). Scientific collaboration networks are assortative, power grids neutral, and metabolic networks disassortative.
- **gold_paragraph:** "Scientific Collaboration Network … indicating that the network's assortativity is not structural … Power Grid: The horizontal k_nn(k) … support the lack of degree correlations (neutral network). Metabolic Network: As both k_nn(k) and k_nn^R-S(k) decrease, we conclude that the network's disassortativity is induced by its scale-free property." *(chapter_07.txt · chunk 19)*

### 37
- **question:** What is the friendship paradox and why does it depend on the ratio of the second moment to the first moment of the degree distribution?
- **relevant_chapter:** 7
- **correct_answer:** The friendship paradox is that, on average, your friends have more friends than you do. A randomly chosen neighbor is reached with probability proportional to its degree, so the expected neighbor degree is `⟨k²⟩/⟨k⟩`, which exceeds the average degree ⟨k⟩ — dramatically so in scale-free networks where ⟨k²⟩ is enormous.
- **gold_paragraph:** "The gap between ⟨k⟩ and our friends' degree can be particularly large in scale-free networks, for which ⟨k²⟩/⟨k⟩ significantly exceeds ⟨k⟩. Consider … the actor network, for which ⟨k²⟩/⟨k⟩ = 565 … The friendship paradox has a simple origin: We are more likely to be friends with hubs than with small-degree nodes, simply because hubs have more friends than the small nodes." *(chapter_07.txt · chunk 10)*

### 38
- **question:** How does the degree correlation function k_nn(k) and its exponent classify a network's correlations?
- **relevant_chapter:** 7
- **correct_answer:** `k_nn(k)` is the average degree of the neighbors of degree-*k* nodes. Fitting it to a power law `k_nn(k) ~ k^μ`, the sign of the correlation exponent μ classifies the network — matching the sign of the assortativity coefficient *r*: μ < 0 → disassortative, μ = 0 → neutral, μ > 0 → assortative.
- **gold_paragraph:** "if the degree correlation function follows (7.10), then the sign of the degree correlation exponent μ will determine the sign of the coefficient r: μ < 0 → r < 0; μ = 0 → r = 0; μ > 0 → r > 0." *(chapter_07.txt · chunk 46)*

### 39
- **question:** What is structural disassortativity in simple scale-free networks?
- **relevant_chapter:** 7
- **correct_answer:** In simple scale-free networks with γ < 3, the natural degree cutoff would require more hub–hub links than the simple-graph constraint (at most one link per node pair) permits. This forces fewer links between hubs than a neutral network would have, producing disassortativity purely from structural constraints — even when no correlations were imposed during construction.
- **gold_paragraph:** "For scale-free networks with γ < 3 … nodes whose degree is between k_s and k_max can violate [the simple-graph bound]. In other words the network has fewer links between its hubs than (7.14) would predict. These networks will therefore become disassortative, a phenomenon we call structural disassortativity … despite the fact that we did not impose degree correlations during its construction." *(chapter_07.txt · chunk 15)*

### 40
- **question:** How does percolation theory describe a network breaking apart under random node removal?
- **relevant_chapter:** 8
- **correct_answer:** Percolation theory tracks the size of the largest (giant) component as a fraction *f* of nodes is randomly removed, measured by `P∞`, the probability a random node belongs to the giant component. Random node removal is the inverse of percolation: below a critical threshold `f_c` a giant component survives; above it the network shatters into small clusters.
- **gold_paragraph:** "We randomly select and remove an f fraction of nodes and measure the size of the largest component … captured by P∞, the probability that a randomly selected node belongs to the largest component … for random networks the answer continues to be provided by percolation theory." *(chapter_08.txt · chunk 9)*

### 41
- **question:** What is the Molloy–Reed criterion for the existence of a giant component?
- **relevant_chapter:** 8
- **correct_answer:** The Molloy–Reed criterion states that a network has a giant component as long as `κ = ⟨k²⟩/⟨k⟩ > 2`. It ties the existence of the giant component directly to the first two moments of the degree distribution, and explains the anomalously high breakdown threshold of scale-free networks (where ⟨k²⟩ is large).
- **gold_paragraph:** "Molloy-Reed Criterion: To understand the origin of the anomalously high f_c characterizing the Internet and scale-free networks, we calculate f_c for a network with an arbitrary degree distribution. To do so we rely on a simple observation: For a [node to belong to the giant component it must connect to at least two others]." *(chapter_08.txt · chunk 14)*

### 42
- **question:** How does the critical breakdown threshold depend on the first and second moments of the degree distribution?
- **relevant_chapter:** 8
- **correct_answer:** The critical threshold is `f_c = 1 − 1/(⟨k²⟩/⟨k⟩ − 1)`, so it is governed by the ratio of the second to first moment. For scale-free networks with 2 < γ < 3, ⟨k²⟩ diverges, driving f_c → 1 — meaning essentially all nodes must be removed to destroy the giant component (enhanced robustness to random failure).
- **gold_paragraph:** "The exponent characterizing the average component size near p_c follows … for γ < 3 we always have a giant component. Hence, the divergence cannot be observed in this regime. For a randomly connected network with arbitrary degree distribution the size distribution of the finite clusters follows n_s ~ s^(−τ) e^(−s/s*)." *(chapter_08.txt · chunk 69)*

### 43
- **question:** What distribution do the sizes of cascading failures follow?
- **relevant_chapter:** 8
- **correct_answer:** Cascade sizes follow a power-law (fat-tailed) distribution: most cascades are tiny but a few are enormous. This holds across very different systems — blackout energy losses, Twitter retweet cascades, and earthquake amplitudes.
- **gold_paragraph:** "The distribution of energy loss for all North American blackouts between 1984 and 1998 … is typically fitted to (8.14) … The distribution of cascade sizes on Twitter. While most tweets go unnoticed, a tiny fraction of tweets are shared thousands of times … well approximated with (8.14) with α ≃ 1.75 … The cumulative distribution of earthquake amplitudes … the power law fit." *(chapter_08.txt · chunk 35)*

### 44
- **question:** What is a community, defined by the connectedness and density hypotheses?
- **relevant_chapter:** 9
- **correct_answer:** A community is a locally dense connected subgraph, defined by two hypotheses: the **connectedness hypothesis** (a community is a connected subgraph, confined to a single component) and the **density hypothesis** (nodes within a community link to each other more densely than to the rest of the network).
- **gold_paragraph:** "Communities are locally dense connected subgraphs in a network. This expectation relies on two distinct hypotheses: Connectedness Hypothesis: Each community corresponds to a connected subgraph … if a network consists of two isolated components, each community is limited to only one component … Density Hypothesis." *(chapter_09.txt · chunk 7)*

### 45
- **question:** What is the difference between a strong community and a weak community?
- **relevant_chapter:** 9
- **correct_answer:** In a **strong community** every node individually has more links inside the community than to the rest of the network (`k_int > k_ext` for each node). A **weak community** relaxes this to the community as a whole — the total internal degree exceeds the total external degree — so some individual nodes may violate the strong condition. Every clique is a strong community, and every strong community is a weak community, but not vice versa.
- **gold_paragraph:** "a subgraph C forms a weak community if Σ k_int(C) > Σ k_ext(C) … A weak community relaxes the strong community requirement by allowing some nodes to violate [the per-node condition]. In other words, the inequality applies to the community as a whole rather than to each node individually. Note that each clique is a strong community, and each strong community is a weak community." *(chapter_09.txt · chunk 10)*

### 46
- **question:** How does the Girvan–Newman algorithm use link betweenness to detect communities?
- **relevant_chapter:** 9
- **correct_answer:** The Girvan–Newman algorithm is a divisive method that scores each link by its **link betweenness** — the number of shortest paths passing through it. Inter-community links carry high betweenness, so the algorithm repeatedly removes the highest-betweenness link and recomputes, progressively fragmenting the network into communities.
- **gold_paragraph:** "Divisive algorithms require a centrality measure that is high for nodes that belong to different communities … Link Betweenness captures the role of each link in information transfer. Hence x_ij is proportional to the number of shortest paths between all node pairs that run along the link (i,j). Consequently, inter-community links … have large betweenness. The calculation of link betweenness scales as O(LN)." *(chapter_09.txt · chunk 24)*

### 47
- **question:** What does the modularity metric measure for a community partition, and when does merging two communities increase it?
- **relevant_chapter:** 9
- **correct_answer:** Modularity *M* measures how much more densely connected a partition's communities are than expected under a degree-preserving random null model; higher *M* indicates stronger community structure. Merging two communities increases *M* when the fraction of links actually running between them exceeds what the null model would predict by chance.
- **gold_paragraph:** "Partitions with comparable modularity tend to have rather distinct community structure … The modularity of this random partition is still high, M=0.80, not too far from the optimal M=0.87 … a high-modularity plateau that consists of numerous low-modularity partitions." *(chapter_09.txt · chunk 46)*

### 48
- **question:** How does a dendrogram from hierarchical clustering represent a network's community structure?
- **relevant_chapter:** 9
- **correct_answer:** Hierarchical clustering produces a **dendrogram** — a tree whose leaves are nodes and whose merges/splits reveal nested communities at different scales. Cutting the dendrogram at different heights yields different numbers of communities; the method itself does not indicate where to cut.
- **gold_paragraph:** "inspecting C(k) helps decide if the underlying network has hierarchical modularity … Hierarchical clustering does not tell us where to cut a dendrogram. Indeed, depending on where we make the cut in the dendrogram … we obtain (b) two, (c) three or (d) four communities." *(chapter_09.txt · chunk 32)*

### 49
- **question:** How do the SI, SIS, and SIR compartmental models describe epidemic spreading?
- **relevant_chapter:** 10
- **correct_answer:** Compartmental models divide a population into states: **SI** (susceptible → infected, no recovery), **SIS** (susceptible → infected → susceptible, recovery without immunity), and **SIR** (susceptible → infected → recovered/immune). The appropriate model depends on the pathogen; all three agree in the early phase but differ in long-term dynamics.
- **gold_paragraph:** "we must use the SIR model to describe their spread. The differential equations governing the time evolution of the fraction of individuals in the susceptible s, infected i and the removed r state … all individuals transition from a susceptible (healthy) state to the infected (sick) state and then to the recovered (immune) state … the predictions of the SI, SIS, and SIR models agree with each other in the early [phase]." *(chapter_10.txt · chunk 14)*

### 50
- **question:** What is the basic reproductive number R0 and how does it predict an epidemic's fate?
- **relevant_chapter:** 10
- **correct_answer:** The basic reproductive number `R₀ = β⟨k⟩/μ` is the average number of secondary infections caused by one infected individual. If `R₀ > 1` the epidemic spreads; if `R₀ < 1` the infection dies out exponentially, since cures outpace new infections.
- **gold_paragraph:** "in this state the number of individuals cured per unit time exceeds the number of newly infected individuals. Therefore with time the pathogen disappears … we write the characteristic time of a pathogen as τ = 1/[μ(R₀ − 1)] where R₀ = β⟨k⟩/μ is the basic reproductive [number]." *(chapter_10.txt · chunk 11)*

### 51
- **question:** Why does the epidemic threshold vanish on a scale-free network?
- **relevant_chapter:** 10
- **correct_answer:** On a scale-free network (for γ ≤ 3) the epidemic threshold `λ_c → 0` because ⟨k²⟩ diverges. The hubs act as super-spreaders that keep any pathogen alive and propagate it network-wide, so even vanishingly small spreading rates sustain an epidemic — unlike random networks, which have a finite threshold.
- **gold_paragraph:** "The vanishing epidemic threshold is a direct consequence of the hubs. Indeed, a pathogen that fails to infect other nodes before the infected individual recovers, will slowly disappear … In a random network all nodes have comparable degree … hence if the spreading rate is under the epidemic threshold, the pathogen has no avenues to spread. In a scale-free network, however, even if [the rate is tiny, hubs sustain it]." *(chapter_10.txt · chunk 25)*

### 52
- **question:** Why are super-spreaders equivalent to hubs in a contact network?
- **relevant_chapter:** 10
- **correct_answer:** Super-spreaders are individuals who infect disproportionately many others; in a contact network these are precisely the **hubs** — nodes with very high degree. Because hubs have so many contacts, they both acquire and transmit pathogens far more than average nodes, dominating the spreading dynamics — which is why immunizing hubs is so effective.
- **gold_paragraph:** "Targeted immunization … By making the hubs immune to the disease, the network on which the pathogen spreads becomes the fragmented network … As the immunized network is broken into small islands, the pathogen will be stuck in one of the small clusters, unable to infect the nodes in the other clusters. Hub immunization represents a perspective change in immunization protocols." *(chapter_10.txt · chunk 56)*

### 53
- **question:** Why does random immunization fail on scale-free networks while targeting hubs works?
- **relevant_chapter:** 10
- **correct_answer:** Random immunization fails because the near-zero epidemic threshold would require immunizing almost the entire population, and randomly chosen nodes are mostly low-degree, leaving the hubs intact. Targeting hubs works because immunizing them fragments the contact network into small islands, raising the effective threshold and trapping the pathogen in isolated clusters.
- **gold_paragraph:** "Targeted immunization … By making the hubs immune to the disease, the network on which the pathogen spreads becomes the fragmented network … instead of trying to decrease the spreading rate using random immunization, we must alter the topology of the contact network, which in turn increases λ_c above the biologically determined λ = β/μ." *(chapter_10.txt · chunk 56)*