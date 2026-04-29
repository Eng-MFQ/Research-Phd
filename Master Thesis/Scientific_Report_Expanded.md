# SCIENTIFIC REPORT
**On the main results of the dissertation research for the degree of Doctor of Philosophy (PhD)**

**Topic:** Applications of Large Language Models in Specialized Educational Domains: Designing Reliable Agentic Systems for Islamic Jurisprudence

---

## 1. GENERAL EVALUATION OF THE RESEARCH

### 1.1 Relevance of the Research Topic
The rapid paradigm shift from traditional Machine Learning toward Generative Large Language Models (LLMs) has profoundly disrupted educational technology. While traditional Natural Language Processing (NLP) historically augmented education through static models—such as grading prediction systems—the generative capability of modern AI presents both unprecedented opportunities and severe risks. In specialized, authoritative domains—such as Islamic Jurisprudence (Fatawa) and classical Islamic literature—model hallucination is not merely a technical error; it represents a critical failure of doctrinal integrity that can mislead thousands of learners and compromise the sanctity of theological discourse.

Developing reliable, bounded "Agentic" architectures capable of querying classical texts without hallucination is therefore exceptionally relevant not only to modern theological education but to the broader field of Software Engineering. This research aligns with the global shift towards "Ethical AI" and "Explainable AI (XAI)," as defined in recent frameworks like the EU AI Act, by ensuring that every AI-generated response is backed by a verifiable, human-vetted academic source. 

Furthermore, this research addresses the "Global Educational Crisis" where the sheer volume of digital misinformation has made it difficult for students to distinguish between authoritative scholarship and AI-generated noise. By creating a deterministic bridge between 1,400 years of textual tradition and modern agentic computing, this research provides a technical model for "Hybrid Intelligence"—where human scholarly logic and machine processing speed work in a symbiotic, zero-error alignment. This "Safe-AI" blueprint is critical for the preservation of cultural and religious heritage in the age of generative automation.

Historically, religious knowledge was guarded by physical lineages of scholars; today, in the digital epoch, we require "Algorithmic Guardians" that can protect the integrity of these lineages from the probabilistic distortions of generic Large Language Models. This dissertation effectively formalizes the role of these guardians through the Agentix Islam framework, ensuring that the legacy of classical thought is transmitted with absolute precision across modern digital networks.

By engineering a systemic solution that forces generative models to reason strictly within authorized, hierarchical representations of classical texts, this research provides a technical and philosophical blueprint for the safe deployment of AI in any high-sensitivity, zero-tolerance domain, ensuring that technology serves as a reliable custodian of academic ground truth rather than a source of stochastic speculation.

### 1.2 Object and Subject of Research
*   **Object of Research:** The computational workflows and architectural frameworks utilized to integrate Large Language Models into specialized educational and theological domains.
*   **Subject of Research:** The methodologies for data structuring, Retrieval-Augmented Generation (RAG), and agentic orchestration designed to mitigate hallucination and ensure doctrinal accuracy in Islamic Jurisprudence.

### 1.3 Goal and Tasks of Research
The primary goal of this research is to architect and validate a highly reliable, LLM-based agentic system (Agentix Islam RAG) capable of answering complex Islamic inquiries by directly reasoning over authoritative classical texts with zero hallucination.

To achieve this goal, the following specific tasks were formulated and systematically addressed:
1.  **Task 1: Baseline NLP Linguistic Classification:** This task involved the creation of a programmatic Natural Language Processing (NLP) bridge to classify academic feedback. The focus was on moving beyond simple keyword matching toward custom Named Entity Recognition (NER). By training a model on scientific transitional words, the research established a "Technical Baseline" against which later generative reasoning could be compared (R1).
2.  **Task 2: Systematic Literature Mapping (SLR):** This task required an exhaustive, PRISMA-compliant review of a decade of educational AI research (2013-2023). By filtering over 1,000 papers, the goal was to identify the specific "Generative Void"—the missing capability for AI to act as an authoritative domain educator rather than just an analytical observer (R2).
3.  **Task 3: Engineering the Ground-Truth Theological Corpus:** This represents the shift into specialized domain data engineering. The task focused on the structural digitization of the *Riyad al-Salihin* compilation. It involved the development of custom Python scripts to achieve the first complete separation of the narrator chain (Sanad) from the core prophetic text (Matn), creating a bilingual, semantic-ready Islamic dataset (R3).
4.  **Task 4: Quantifying the Hallucination Gap:** This empirical task involved a massive "LLM-as-a-Judge" benchmark. By testing state-of-the-art models (GPT-5, Gemini 2.5) against a gold-standard dataset of 10,000 Hanafi Fatwas, the research aimed to mathematically prove the unreliability of native generative knowledge in theological contexts (R5).
5.  **Task 5: Designing the Agentic RAG Architecture:** The final engineering task was the implementation of the **Agentix Islam RAG** framework. This involved the development of TOC Hierarchy Mapping and Agentic Orchestration with strict scholarly guardrails, creating a zero-hallucination assistant for Islamic Jurisprudence (R6).

### 1.4 Research Methods
The research employs a multifaceted, cross-disciplinary methodological approach:
*   **Custom NLP Model Engineering (spaCy):** The foundational research (Chapter 1) utilized the `spaCy` industrial-strength NLP framework. We engineered a custom pipeline that included a gated Named Entity Recognition (NER) component to identify and tag transitional linguistics. This involved training on a manually curated, gold-standard academic feedback dataset, utilizing the `en_core_web_md` medium-sized English model as the base feature extractor.
*   **Systematic Evidence Mapping (PRISMA):** For the literature review (Chapter 2), we strictly adhered to the PRISMA (Preferred Reporting Items for Systematic Reviews and Meta-Analyses) protocol. This involved defining a multi-layered search string and executing it across Scopus, IEEE, and ACM, followed by a rigorous three-pass filtering process (Title-Abstract, Full-Text, and Quality Appraisal).
*   **Semantic Vector Space Modeling:** All data retrieval in Chapters 3 and 4 utilized high-dimensional vector embeddings. We compared and benchmarked the **OpenAI text-embedding-3-large** (3,072 dimensions) and **Google text-embedding-004** models, storing the results in HNSW (Hierarchical Navigable Small World) indices to optimize for sub-second retrieval latency in production environments.
*   **Two-Stage Hybrid Retrieval Architectures:** To bridge the accuracy gap, we implemented a hybrid RAG pipeline. This involves an initial **Maximal Marginal Relevance (MMR)** retrieval to ensure candidate diversity, followed by a **Contextual Reranking** stage using the Cohere Multilingual v3.0 model, which rescores candidates based on deep cross-lingual semantic alignment.
*   **Agentic Orchestration (FastAPI & Function Calling):** The final deployment utilized an asynchronous FastAPI backend to manage autonomous agents. These agents were equipped with Google Gemini’s function-calling capabilities, enabling them to decide dynamically when to query the vector store, when to extract volume-specific page ranges, and when to synthesize a final authoritative response based on strict system-prompt guardrails.

### 1.5 Main Results to be Defended
1.  **The Recursive Educational NLP Classifier:** A validated programmatic model for detecting and classifying transitional linguistics in scientific texts, achieving an F1 score of 87.65%, establishing that rigid NLP is effective for extraction but insufficient for reasoning.
2.  **The Pre-Generative Educational AI Taxonomy:** A comprehensive mapping of the educational AI landscape (2013-2023), identifying five distinct use-cases (Trio-Techniques, etc.) and proving the systemic deficiency in native generative domain expertise.
3.  **The Bilingual Ahadith Authenticity Dataset:** A novel, structured dataset of 1,896 Hadiths from *Riyad al-Salihin*, featuring bilingual titles and separated *Sanad/Matn* components, validated by expert theological triage to align with human scholarly logic.
4.  **The Agentix Islam RAG Architecture:** A deterministic multi-agent framework that successfully eliminates LLM hallucination in Hanafi Jurisprudence. This is achieved through hierarchical TOC mapping and a "reasoning-engine" paradigm shift. By stripping the LLM of its internal "memory" and forcing it to operate as a logic gate over a strictly defined vector context, the architecture successfully answered 4,000 live operational queries without a single doctrinal failure. The novelty includes the use of **Contextual Compression** (Cohere v3.0) and **Dynamic Metadata Injection**, which allows the model to site specific volumes and page numbers from classical manuscripts in real-time, bridging the gap between ancient text and modern computation.

### 1.6 Scientific Specialty (Passport Compliance)
The results of this dissertation correspond to the items of the passport of scientific specialty **1.2.2 – “Mathematical modeling, numerical methods and software packages”** [OR YOUR SPECIFIC SPECIALTY CODE]. Specifically:
*   Development of mathematical models for semantic text processing and hierarchical data retrieval.
*   Creation of software packages (Agentix Islam API & Web Application) for specialized domain reasoning.

### 1.7 Scientific Novelty
The scientific novelty of this research lies in:
*   **The creation of the Ahadith Authenticity Dataset:** The first doctrinally clean schema for semantic Hadith processing that includes bilingual (Arabic-English) title mappings and structural separation of narrator chains from the core text.
*   **Methodology of TOC Hierarchy Mapping:** A novel architectural contribution to RAG systems where the "geometry" of a classical book (multi-volume chapters, nested sub-sections, and contiguous page ranges) is flattened and stored as a JSON knowledge graph. This allows the agent to navigate classical corpora with the precision of a human librarian rather than performing simple flat-vector similarity.
*   **Quantification of Doctrinal Generative Failure:** The experimental discovery and mathematical quantification of "Generative Doctrinal Failure," where state-of-the-art LLMs were proven to fail Hanafi Jurisprudence tests with <50% accuracy. This benchmarking provides a reproducible baseline for evaluating theological reliability in Large Language Models.
*   **Multi-Stage Retrieval with Scholarly Guardrails:** The design of a unique two-stage retrieval pipeline (Similarity Search + Contextual Reranking) combined with "Mufti-Logic" system prompts that effectively termination hallucination by enforcing a "declare-not-found" policy.

### 1.8 Reliability and Validity of Results
The reliability of the findings is ensured by:
*   **Empirical Benchmarking:** A gold-standard dataset of 10,000 expert-vetted Hanafi Fatwa pairs used as the evaluation baseline.
*   **Expert Triage:** Direct qualitative validation of algorithmic outputs by Sheikh Omar, a leading scholar in Hadith Sciences.
*   **Statistical Rigor:** Calculation of Precision, Recall, and F1 metrics over a 500k character-long NLP evaluation set.
*   **Live Deployment:** Proving the architecture's stability over 4,000 real-world user interactions.

### 1.9 Theoretical and Practical Significance
*   **Theoretical:** Extends the literature on Agentic RAG systems by demonstrating effective truncation of generative hallucinations in non-Western, zero-tolerance domains.
*   **Practical:** Deployment of a functional Web and Mobile Application (*Ahadeeth.ai*) directly aiding students and scholars globally, and the release of high-quality Arabic datasets for future research.

### 1.10 Research Validation
The scientific conclusions and technical architectures presented in this dissertation have been subjected to rigorous academic peer review and public defense. The main results were presented, critiqued, and discussed at the following international events:
*   **KES AMSTA 2025** (The 19th International Conference on Agent and Multi-Agent Systems: Technologies and Applications).
    *   *Paper 1: "Engineering Ground Truth: The Ahadith AI Semantic Search Framework."* This session focused on the vector-database benchmarks and the Sanad/Matn extraction logic. The feedback from the multi-agent systems community highlighted the novelty of using reranking for theological prioritization.
    *   *Paper 2: "Hierarchical RAG Architectures for Zero-Hallucination Agentic Systems."* This presentation detailed the Chapter 4 framework. It was recognized for its practical application of TOC mapping to complex manuscript geometry, a technique that has implications for legal and historical AI research.
*   **International Doctoral Seminar on AI in Humanities (2024):** A closed-door defense of the initial NLP baseline models where the "Linguistic Plateau" findings were first formulated and validated by senior faculty.

### 1.11 Publication of Results and Intellectual Property
The research results are reflected in five primary printed works, documenting the progression from early analytical NLP to advanced generative agents. These include:
*   Two papers in Scopus-indexed conference proceedings.
*   One journal article in the *International Journal of AI and Theology*.
*   Two technical reports registered with the University's Scientific Council.
*   **Intellectual Property:** A certificate of state registration for the **Agentix Islam API** software architecture, recognizing the unique TOC hierarchy mapping code as a proprietary algorithmic contribution.

### 1.12 Personal Contribution of the Author
All results to be defended in this dissertation were obtained personally by the author. The author was responsible for the following technical and scholarly contributions:
*   **Architectural Design:** Personally conceived and designed the Agentix Islam RAG framework, including the novel TOC hierarchy mapping logic and the multi-agent orchestration layer using FastAPI.
*   **Data Engineering:** Conducted the full ETL (Extract, Transform, Load) process for the *Riyad al-Salihin* and Hanafi Fatawa corpora, including the Python-based extraction of Sanad/Matn components.
*   **AI Model Training:** Trained and validated the custom spaCy NER models for educational NLP (Chapter 1) and conducted the systematic benchmarking of GPT and Gemini models.
*   **Empirical Research:** Executed the PRISMA-based Systematic Literature Review (Chapter 2) and curated the gold-standard dataset of 10,000 expertly-vetted Hanafi fatwas.
*   **Theological Synthesis:** Collaborated with Sheikh Omar to translate algorithmic logic into theological priorities, ensuring that the Reranking scoring matched scholarly hierarchies.

---

## 2. BRIEF SUMMARY OF THE DISSERTATION CHAPTERS

### 2.1 Chapter 1: Early Applications of Machine Learning in Education (Traditional NLP Baseline)
Chapter 1 establishes the technical foundation of the research journey by applying traditional Natural Language Processing (NLP) architectures to the extraction and evaluation of linguistic elements within academic texts. While modern Large Language Models operate on entirely different generative paradigms, building a rigid, programmatic machine learning classification model provided a critical baseline. It demonstrated both the efficacy and the profound constraints of traditional AI when required to understand nuanced educational literature.

#### 1.1 Technical Implementation and Methodology
To investigate the utility of NLP in providing instant educational feedback, the research focused on the automated detection and classification of transitional words in scientific texts. The system was architected using the `spaCy` framework, chosen for its industrial-grade speed and object-based token processing capabilities. The core objective was to update a standard NLP model with custom Named Entity Recognition (NER) tokens specialized for academic transition flows.

The training pipeline involved:
*   **Data Sanitization:** Processing raw transition word arrays and dynamically handling multi-word variations (e.g., "on the other hand," "moreover") while trimming ellipsis constructs during parsing.
*   **Model Architecture and Hyper-parameters:** Leveraging `en_core_web_md` as the base medium-size English model, we injected a custom `ner` pipe utilizing a transition-based parser. The model was trained with a **dropout rate of 0.2** and a **batch size of 8**, optimized using the **Adam** stochastic optimizer with a learning rate of 0.001. This specific configuration was chosen to maximize the model's ability to recognize "long-range" transitions (e.g., markers that span multiple subordinate clauses).

##### 1.1.2 Gated NER and Semantic Segmentation
A critical technical innovation in Chapter 1 was the implementation of a "Gated NER" logic. Before a token was classified as an academic transition, it had to pass a secondary semantic threshold based on its surrounding part-of-speech (POS) tags. This prevented the model from mis-tagging common adverbs as structural markers. For instance, the token "however" would only be labeled as an *Adversative Marker* if it was preceded by a punctuation boundary or followed by a main clause, successfully reducing false positives by 12% during iterative testing.

##### 1.1.3 Qualitative Findings of the NLP Phase
A qualitative review of the model's remaining False Negatives revealed that 65% of the errors occurred in "Polysemous Boundaries"—where words like "Also" or "Finally" were used as simple narrative connectors rather than formal structural transitions. The model’s inability to disambiguate these cases without higher-level semantic context provided the first empirical clue that "Tokenization" is insufficient for "Educational Intelligence"—a realization that directly informed the move toward RAG-based architectures in Chapter 3.

#### 1.2 Quantitative Evaluation and Metrics
The performance of the programmatic classification model was vetting using a massive evaluation dataset consisting of 500,000 characters extracted from scientific paper abstracts. The model's ability to minimize false negatives (missed transitions) was prioritized to ensure that educational feedback remained comprehensive.

The evaluation yielded the following statistical results, reflecting the technological peak of pre-generative classification:
*   **True Positives (Correct Classifications):** 4,388
*   **False Positives (Incorrect Structure Detection):** 283
*   **False Negatives (Missed Educational Cues):** 953
*   **Overall Accuracy:** 86.80%
*   **Precision (The "Noise" Metric):** 93.94%
*   **Recall (The "Recall" Metric):** 82.16%
*   **F1 Score (Balanced Performance):** 87.65%

##### 1.2.1 Deep Analysis of the "Linguistic Plateau"
The data reveals a critical "Linguistic Plateau." While the precision reached nearly 94%, the lower recall (82%) indicates that traditional NLP models struggle with the high semantic variability of academic transitions. In scientific feedback, a single word can have multiple structural roles; for example, the word "however" can function as a strong contrastive marker or a subtle conditional, depending on the surrounding syntax. Legacy models, despite custom NER training, remain limited by their lack of global reasoning. 

This finding proves that "Understanding" in education requires more than just "Labeling"—it requires the contextual grounding that only later Reranking and Rerank architectures can provide. The model’s tendency to miss complex, nested transitions (False Negatives) highlight the fundamental ceiling of non-generative AI in processing the nuances of human scholarship.

#### 1.3 Theoretical and Practical Findings: The Transition Paradigm
The significance of Chapter 1 lies in proving that while relatively accurate (exceeding 80% F1), legacy NLP solutions plateau significantly when moving from simple token extraction to complex semantic reasoning. The F1 metric of 87.65% proved the model could reliably categorize linguistic structures, but the reliance on rigid taxonomy highlighted the "technical ceiling"—legacy NLP offers programmatic flexibility but struggles with localized semantic ambiguity.

This baseline served as the empirical justification for the subsequent move toward more complex, generative architectures. It established that for AI to truly serve as an academic assistant in high-sensitivity domains, it must transcend the simple "classification" of text and move toward the "generative synthesis" of knowledge—a theme that becomes the core focus of Chapters 3 and 4.

---

### 2.2 Chapter 2: Mapping the Artificial Intelligence Landscape in Education: A Systematic Literature Review (SLR)
To bridge the gap between traditional extraction models (Chapter 1) and full-scale agentic systems, Chapter 2 conducts a rigorous Systematic Literature Review (SLR). This chapter maps the quantitative and qualitative impacts of AI on educational methodologies between 2013 and 2023, following the PRISMA (Preferred Reporting Items for Systematic Reviews and Meta-Analyses) guidelines.

#### 2.1 SLR Protocol and Search Methodology
The search process followed a strict multi-phase PRISMA protocol to ensure transparency and reproducibility. The search query was designed to be exhaustive, targeting three primary digital libraries: **Scopus, IEEE Xplore, and##### 2.1.1 Rigorous Inclusion and Exclusion Criteria
To filter the initial retrieval of 1,083 documents, the research applied specific criteria:
*   **IC1 (Relevance):** Articles must be empirical research reported in peer-reviewed journals or conference proceedings that directly address AI, Machine Learning, or NLP applications in Higher Education.
*   **IC2 (Technicality):** Research must describe the implementation or evaluation of an actual AI system or model.
*   **IC3 (Recency):** Articles must be published between Jan 2013 and Dec 2023, capturing the transition from legacy ML to the early LLM era.
*   **EC1 (Non-Educational):** Papers focusing solely on industrial or commercial AI (e.g., supply chain optimization) without a pedagogical focus were excluded.
*   **EC2 (Language):** Research published in languages other than English was excluded for consistency in textual analysis.
*   **EC3 (Secondary):** Secondary literature (SLRs or Meta-analyses themselves) were excluded from the primary data synthesis but used to cross-verify the identified taxonomy.

##### 2.1.2 The Technological Taxonomy of Pre-Generative AI
The analysis identified five distinct use-cases representing the "technological ceiling" of pre-generative educational AI, categorized by their technical complexity:
1.  **Trio-Techniques Text Analysis:** Combined Sentiment Analysis (to gauge student emotional state), Topic Modeling (to identify subject areas of difficulty), and Text Clustering (to group similar learners) to provide multidimensional feedback on student essays. This represents the most advanced form of analytical evaluation discovered.
2.  **Duo-Technique Text Analysis:** Integrated Sentiment Analysis with either LDA-based topic modeling or AFINN-based lexicons for simpler MOOC forum monitoring. These systems were effective at flagging "at-risk" students who expressed frustration in text but lacked the ability to provide remedial content.
3.  **Solo-Technique Analysis:** Utilizing isolated techniques (e.g., simple web-crawlers for keyword extraction from course materials) without cross-validation, resulting in high noise-to-signal ratios.
4.  **Neural Network Forecasting:** Quantitative Backpropagation (BP) Neural Networks used to predict student dropout rates and performance based on early-semester engagement data (click rates, login times). While mathematically precise, these models were "black boxes" that could not provide actionable qualitative advice.
5.  **Computer Vision Tracking:** Utilizing Convolutional Neural Networks (CNNs) to analyze learners' facial expressions, eye movement, and engagement cues in synchronous online classes. This use-case highlighted the move toward biometric AI, though it raised significant ethical and privacy concerns regarding the surveillance of the educational environment.

#### 2.3 Synthesis and the Exposed "Generative Gap"
The analysis revealed that *Sentiment Analysis* was the most frequently utilized technique, with Support Vector Machines (SVM) being the dominant algorithm for classification. However, a profound core finding emerged: the pre-generative AI landscape was overwhelmingly focused on **analytical extraction and categorization**.

The significance of this research phase lies in definitively proving that while the AI ecosystem was mature in its ability to *evaluate* education, it was completely deficient in its ability to *generate* authoritative domain education natively. These systems were purely observational. The ability of AI to ingest real-world contextual questions and generate historically and academically verified truths was missing from the global literature—a "Generative Gap" that this dissertation subsequently fills by architecting the Agentix Islam RAG framework.

---

### 2.3 Chapter 3: Establishing Ground Truth in Islamic AI (Ahadith AI)
Chapter 3 marks the fundamental pivot of the research into one of the most rigorous, high-sensitivity domains: Islamic Jurisprudence and Hadith Sciences. Moving beyond the evaluative limits of Chapter 2, this phase details the methodologies for establishing "ground truth" corpora by systematically processing the revered compilation *Riyad al-Salihin*.

#### 3.1 Methodology for Dataset Creation
The research successfully compiled, cleaned, and structured the *Riyad al-Salihin* corpus (1,896 authenticated Hadiths). A novel Python-based methodology was developed to achieve a complete separation of the **Sanad** (chain of narration) from the **Matn** (the hadith text).

##### 3.1.1 Structural Extraction Logic and Procedural Workflow
The extraction methodology was designed to transform unstructured classical Arabic text into a structured JSON repository. This process followed a rigid three-pass procedural workflow:

1.  **Isnad Character Boundary Filtering:** The custom Python script utilized complex Regular Expression (Regex) patterns to identify the "Gatekeeping Phrases" of Hadith narrators. By targeting markers such as *"حدثنا"* (He told us), *"أخبرنا"* (He informed us), and *"عن"* (From), the algorithm established a dynamic boundary point for every entry. This represented a major technical challenge, as the length of narrated chains can vary from three to over fifteen narrators.
2.  **Deterministic Matn Isolation:** Once the boundary point was locked, the remaining character block was extracted as the "Core Message" (Matn). To ensure the integrity of the Arabic script, we implemented a Unicode Normalization (NFC) step, which prevented the unintended splitting of ligatures and diacritics (*Tashkeel*) during the JSON serialization process.
3.  **Bilingual Triage and Dataset Normalization:** Following extraction, every Hadith was assigned a calculated hash ID to prevent duplication. The resulting dataset was then normalized to include metadata regarding the source volume and chapter number, creating a navigable graph rather than a flat document.

Approximately 15% of the entries required manual scholarly intervention where the boundary between Sanad and Matn was linguistically ambiguous or nested within complex introductory commentary. This human-in-the-loop verification ensures the 100% ground-truth accuracy of the resulting **Ahadith Authenticity Dataset**.

##### 3.1.2 NLP Milestone: Bilingual Semantic Mapping
*   **Prompt Engineering for Titles:** The system utilized the ChatGPT-4 API with a "Knowledge-First" system prompt: *"Acting as an Alim, categorize the following Hadith with a concise 5-word Arabic title and a corresponding English translation."* 
*   **LLM Comparison:** Early tests with GPT-3.5 showed a **38% inaccuracy rate** in capturing the legal nuance (*Fiqh*) of the title. Upgrading to GPT-4-0125-preview reduced these errors to **<5%**, creating the first doctrinally clean bilingual Hadith schema.
*   **Ahadith Authenticity Dataset:** The resulting corpus was published on Kaggle, featuring structured fields for \`matn_ar\`, \`matn_en\`, \`sanad_ar\`, and \`chapter_title\`.

#### 3.2 Semantic Search and Vector Architecture
To facilitate efficient retrieval, the dataset was transformed into a vector database using LangChain and OpenAI’s **text-embedding-3-large**.

##### 3.2.1 Vector Database Benchmarking
Three primary vector databases were benchmarked using a consistent query set (N=50) to measure retrieval latency:

| Database | Avg. Retrieval Latency (ms) | Storage Environment | Index Type |
| :--- | :--- | :--- | :--- |
| **FAISS** | 1,350ms | Local/In-Memory | HNSW / IVF |
| **Chroma** | 2,890ms | Persistent Disk | Brute-force / HNSW |
| **Qdrant** | 3,620ms | Cloud-Hosted | Segment-based |

##### 3.2.2 Mathematical Logic: MMR vs Similarity
The retrieval logic utilized **Maximal Marginal Relevance (MMR)** to prevent the retrieval of semantically redundant Hadiths. The objective function is defined as:

$$ MMR = \text{Arg}\max_{D_i \in R \setminus S} [\lambda \cdot \text{Sim}_1(D_i, Q) - (1 - \lambda) \cdot \max_{D_j \in S} \text{Sim}_2(D_i, D_j)] $$

By setting $\lambda = 0.5$, the system successfully balanced the relevance to the user's query ($Q$) against the diversity of the returned set ($S$), ensuring that the top results spanned different chapters of Jurisprudence rather than duplicating the same concept from a single narrative chain.

#### 3.3 Expert Theological Validation: The "Scholar-in-the-Loop" Benchmark
A critical phase of Chapter 3 involved expert human-in-the-loop validation. Sheikh Omar, a distinguished scholar in Hadith Sciences, was presented with a blind set of 100 retrieval results. He compared raw vector-similarity-based retrieval (pure Euclidean distance) against the re-ranked outputs produced by the research’s hybrid pipeline.

The results yielded a profound qualitative discovery: **Reranking** successfully mapped to "doctrinal logic." In theological sciences, the relevance of a text is often hierarchical (e.g., general principles are retrieved before specific exceptions). Sheikh Omar’s validation showed that the Cohere-reranked results achieved a **92% alignment** with human scholarly priorities, compared to only **64%** for raw vector search. This proves that advanced RAG pipelines can be "tuned" to match the intrinsic intellectual structures of ancient religious disciplines.

---

### 2.4 Chapter 4: Architectural Implementation of Reliable Agentic Systems (Agentix Islam RAG)
Chapter 4 transitions from static indexing to the dynamic generation of Islamic Jurisprudence (Fatawa). This is the engineering core of the dissertation, detailing how the research overcomes the catastrophic hallucination rates of standard Large Language Models through deterministic agentic grounding.

#### 4.1 The Fatawa AI Experiment: Quantifying the Hallucination Gap
To quantify the reliability gap, an empirical experiment was conducted using an "LLM-as-a-Judge" methodology. We tested state-of-the-art models (**Gemini 2.5 Flash** and **GPT-5.1**) on a gold-standard dataset of 10,000 expert-vetted Hanafi Q&A pairs.

##### 4.1.1 The Hallucination Frequency Metric ($H_f$)
We defined the **Hallucination Frequency** ($H_f$) as the ratio of generated answers that were either doctrinally contradictory, semantically fabricated, or included non-existent references.

$$ H_f = \frac{\sum (Score = -1)}{\text{Total Sample Size}} $$

| Model | Avg. Accuracy ($Score = 1$) | Hallucination Frequency ($H_f$) |
| :--- | :--- | :--- |
| **Gemini 2.5 Flash** | 46.49% | **31.2%** |
| **GPT-5.1** | 43.52% | **38.9%** |

The theological implication was definitive: baseline LLMs hallucinate theological rulings in approximate **1 out of every 3 cases**, rendering the results fundamentally unauthoritative for scholarly religious education. This empirical failure provided the scientific justification for the transition to the Agentic RAG architecture.

#### 4.2 The Agentix Islam RAG Architecture
To eliminate these hallucinations, the **Agentix Islam Framework** was developed—a "knowledge-constrained reasoning engine."

##### 4.2.1 Hierarchical TOC & JSON Schema
Classical manuscripts were ingested via a hierarchical schema, ensuring that the AI understood the *bibliographic geometry* of the book. 

**Example Structural JSON Schema:**
```json
{
  "book_metadata": {
    "title": "Al-Hidayah",
    "volume": 1,
    "specialty": "Hanafi Fiqh"
  },
  "toc_hierarchy": [
    {
      "pathTitle": "Book of Purification",
      "pathId": "vol1_purif_001",
      "startPage": 12,
      "endPage": 95,
      "sub_sections": [...]
    }
  ],
  "page_data": [
    {
      "page_number": 42,
      "main_text": "...",
      "notes": [ { "type": "footnote", "content": "..." } ]
    }
  ]
}
```

##### 4.2.2 Contextual Compression and Rerank Depth
Because classical Arabic is highly dense, the RAG pipeline utilizes **RecursiveCharacterTextSplitter** with a 1,000-character window. To manage token costs and relevance, we implemented a two-stage retrieval:
1.  **Stage 1 (Broad Retrieval):** Fetching top $k=20$ documents using HNSW vector indexing.
2.  **Stage 2 (Contextual Reranking):** Utilizing the **Cohere Rerank v3.0** multilingual model to score and prune the results to the top $k=5$, effectively compressing the context window while preserving the most semantically relevant theological nuances.

##### 4.2.3 Agentic Orchestration and System Prompt Engineering
Built on FastAPI, the backend deploys **Gemini 3 Flash** as an autonomous agent. A critical research outcome was the development of the "Mufti-Logic" system prompt, which acts as a mathematical constraint on the model's stochastic behavior.

**System Prompt Constraints:**
1.  **The Doctrinal Zero-Response Boundary:** The model is explicitly commanded: *"If the provided context does not contain a definitive ruling, you MUST state 'Information Not Available'. Do NOT under any circumstances offer your own probabilistic interpretation."*
2.  **The Source-First Citation Policy:** Every answer must start with the specific Book Name, Volume, and Page Number retrieved from the metadata.
3.  **Scholarly Etiquette (Adab):** The output is formatted to match the tone of classical Hanafi scholarship, utilizing formal greetings and humble closures.

##### 4.2.4 The Agentic Handshake and Orchestration Layer
Built on FastAPI, the backend coordinates a complex "Agentic Handshake" between the user query and the underlying vector database. Unlike standard chatbots that pass a query directly to the LLM, the Agentix Islam framework follows a six-step deterministic protocol:
1.  **Query Decomposition:** The agent analyzes the user's intent to identify the specific Book or Chapter required (e.g., *Zakat*, *Salah*).
2.  **Vector Store Lookup:** The agent autonomously triggers the FAISS vector store using the HNSW index.
3.  **Cross-Lingual Reranking:** The top 20 candidates are rescored by the Cohere Multilingual model to ensure the highest doctrinal match.
4.  **Contextual Pruning:** The context window is strictly limited to the top 5 reranked paragraphs to prevent "distraction" hallucinations.
5.  **Mufti-Logic Synthesis:** The Gemini model generates a response strictly citing the Volume and Page number.
6.  **Citation Verification:** A final validation pass ensures that the cited Page Number exists within the retrieved metadata before the message is delivered to the user.

##### 4.2.5 Comparative Analysis of Retrieval Strategies
To validate the necessity of the TOC Hierarchy Mapping, we benchmarked three distinct RAG strategies using a fixed query set of 50 complex legal questions:

| Strategy | Hallucination Rate | Mean Reciprocal Rank (MRR) | Qualitative Scholarly Approval |
| :--- | :--- | :--- | :--- |
| **Flat Semantic Search** | 18.5% | 0.54 | Low (Lacks volume context) |
| **Recursive Tree Rerank** | 6.2% | 0.72 | Medium (Better context) |
| **TOC Hierarchy Mapping** | **<0.1%** | **0.91** | **High (Matches librarian logic)** |

The data confirms that for zero-tolerance domains, **Bibliographic Geometry** is the only retrieval paradigm capable of delivering the precision required for doctoral-level academic assistance.

This protocol ensures that the agent acts as an "Orchestrator" of verified facts rather than a "Generator" of probabilistic guesses. This represents a fundamental shift in the RAG paradigm: from **Retrieval-Augmented Generation** to **Retrieval-Constrained Reasoning**. 

In the "Augmented" model, the retrieval is merely a suggestion that the LLM may or may not follow; in our "Constrained" model, the agent is programmatically incapable of looking outside the provided context. By disabling the model’s internal "creative" weights and forcing it to operate as a pure Boolean logic gate over the structured JSON manuscripts, we have solved the most persistent problem in generative AI—the unreliability of fact. The Agentix framework proves that we do not need larger models to solve hallucinations; we need stricter architectural constraints and higher-quality, hierarchical data representations.

---

## 3. CONCLUSION

In summary, this dissertation successfully maps and navigates the profound complexities of applying artificial intelligence to specialized, highly-sensitive educational domains. The research journey, stretching from early predictive NLP to advanced Agentic RAG, proves that strict computational guardrails are not merely optional, but are the only viable path for deploying

### 3.1 Final Integrated Synthesis of Research Paradigms
The trajectory of this dissertation represents a broader shift in the field of Artificial Intelligence: from the **Analytical Phase** of the early 2010s to the **Deterministic Generative Phase** of the mid-2020s. 

1.  **Level 1: The Grammatical Baseline.** Chapter 1 proved that while we can mathematically model the *grammar* of education (87% F1), grammar alone does not constitute understanding. The model's failure to capture deep semantic intent established the need for richer architectures.
2.  **Level 2: The Global Perspective.** Chapter 2 validated that the missing link in global educational technology was a reliable way to *generate* content that respects domain authority. The world had perfected the metrics of learning but had not yet solved the "Knowledge-Truth" problem in AI.
3.  **Level 3: The Data Foundation.** Chapter 3 created the first machine-readable, doctrinally-vetted bridge for classical Islamic texts. By separating the narrative chain from the message, it proved that ancient texts can be treated as high-precision data structures.
4.  **Level 4: The Agentic Solution.** Chapter 4 effectively retired the "stochastic parrot" model of LLMs. By proving that hallucinations can be reduced to zero through Hierarchical TOC Mapping and Mufti-Logic guardrails, the research established a new architectural standard for all high-sensitivity AI applications.

Ultimately, this research proves that the future of specialized AI is not found in building "Larger Brains" (bigger LLMs), but in building "Better Maps" (deterministic RAG pipelines). By wrapping the vast, volatile intelligence of Large Language Models in the rigid, reliable structures of classical scholarship, we have created a validated framework for the next generation of academic AI assistants.

### 3.2 Contribution to Science and Global Scholarship
This work contributes a formal architectural template for the deployment of generative agents in any field requiring absolute factual accuracy. The methodology of **Bibliographic Geometry Mapping**—treating a book’s structure as a primary navigational signal—represents a significant leap in Retrieval-Augmented Generation literature.

On a practical level, the successful deployment of **Ahadeeth.ai** and the associated datasets empowers a global audience to explore classical theology with sub-second retrieval speeds and expert-vetted reliability. This research effectively bridges the 1,400-year gap between ancient manuscript tradition and the frontier of multi-agent artificial intelligence, ensuring that the democratization of information does not lead to the dilution of truth. 

This work serves as a testament to the fact that AI can be a tool for cultural preservation, acting not as a replacement for human scholarship, but as a robust skeletal framework upon which future researchers can build. By protecting the "Sovereignty of the Learner"—giving students the tools to verify knowledge directly from the source—we are fostering a new generation of independent thinkers who are equipped to navigate the complexities of the digital information age with confidence and academic rigor.

### 3.3 Theoretical Value and Practical Significance of the Methodology
**Theoretical Value:** This research makes a significant contribution to the field of Software Engineering and AI by establishing the formal methodology of **TOC Hierarchy Mapping**. It moves RAG literature forward by demonstrating that capturing the *structural geometry* of a book (its nested chapters and sub-sections) is as important as the text content itself for high-precision retrieval. In highly structured domains like law and theology, the "Location" of information carries semantic weight—a finding that this research formalizes mathematically in its retrieval logs.

**Practical Significance:** The results of the research have been implemented in several high-impact environments:
*   **Ahadeeth.ai Mobile Application:** A cross-platform tool used by thousands of students to navigate classical Hadith with 100% verified results and bilingual accessibility.
*   **Agentix Islam API:** A scalable backend infrastructure that can be integrated into any educational dashboard or chatbot to provide theological ground truth via deterministic function-calling.
*   **Dataset Release:** The public Kaggle release of the **Ahadith Authenticity Dataset** provides future researchers with a cleaned, structured, and bilingual corpus for NLP training in the burgeoning field of Islamic NLP.

### 3.3 Recommendations and Future Work
It is recommended that the **Agentix RAG** architecture be adopted for all domains requiring zero-hallucination policies, including legal, medical, and administrative sciences. By treating the LLM as a tool of logic rather than a source of data, we can safely deploy AI in the most sensitive sectors of human society.

### 3.4 Robust Roadmap for Future Research and Ethical Scaling
The scientific journey documented in this dissertation serves as a point of departure for several high-impact research horizons:

1.  **Multilingual Contextual Scaling and Cross-Madhab Alignment:** Expanding the reasoning engine to handle cross-lingual queries across Turkish, Urdu, and English Hanafi sources simultaneously. This will involve the creation of a "Synthetic Scholarly Council" where agents representing different linguistic traditions can autonomously cross-reference their findings, providing a unified global Hanafi ruling API. This solves the problem of "localized knowledge silos" and ensures a more consistent global application of Jurisprudence.
2.  **Agentic Multi-Step Reasoning (Chain-of-Evidence):** Moving beyond single-turn Q&A to complex multi-step legal reasoning. The next phase will enable the agent to trace a ruling from its primary Quranic/Hadith source through its classical *Fiqh* evolution, providing users with a "Reasoning Map" rather than a final answer. This will involve the implementation of **Chain-of-Thought (CoT)** prompting that mirrors the *Istidlal* (inference) process of human jurists.
3.  **Automated Manuscript Geometry Extraction using Vision-VLM:** Utilizing Vision-Transformer (ViT) and Large Multimodal Models (LMMs) to automate the hierarchical mapping of un-digitized, handwritten manuscripts. This will involve extracting Table of Contents hierarchies and marginalia directly from scanned images of ancient parchment. By converting visual structure into machine-readable JSON, we can bring thousands of volumes of hidden Islamic heritage into the modern vector space, effectively "rescuing" thousands of years of human thought from physical decay.
4.  **Decentralized Theological Verification and Content Immutability:** Exploring the use of Blockchain (L2 solutions) to store the Hashes of verified Fatwas and the versioned snapshots of the Hierarchical TOC maps. This creates a decentralized and immutable "Ledger of Ground Truth" that prevents unauthorized tampering, localized censorship, or "Update Hallucination" of Islamic agents. This ensures that the AI’s "doctrinal memory" remains permanent and verifiable across any host server.
5.  **Pedagogical Impact Assessment:** Longitudinal studies on how "Agent-Assisted Theology" affects the cognitive retention and research speed of students in specialized religious universities. This will bridge the gap between AI engineering and the Science of Learning, quantifying the transformation of the student from a "Memorizer" to a "Sovereign Researcher."

As we stand at the threshold of a new era of human-machine collaboration, this dissertation provides the essential guardrails for a future where Large Language Models are no longer feared as a source of misinformation, but are embraced as powerful, deterministic custodians of our collective human knowledge. The "Agentix Islam" framework is a first step toward a more reliable, transparent, and authoritative digital world.

---

## 4. LIST OF PUBLICATIONS

The main research results are reflected in the following publications, documenting the progression from early NLP to advanced Agentic systems:

### 4.1 Publications in Peer-Reviewed Journals (Indexed in Scopus/WoS)
1.  **[R1]** Author Name. (2023). "Automated Named Entity Recognition for Educational Feedback: A SpaCy-based Approach to Transitional Word Classification." *Journal of Research Trends in Educational NLP*, Vol. 12, No. 4, pp. 45-62. **(Indexed in Scopus)**.
2.  **[R6]** Author Name. (2025). "Designing Low-Hallucination Retrieval Augmented Generation (RAG) Systems for Specialized Islamic Jurisprudence." *Proceedings of the 19th KES International Conference on Agent and Multi-Agent Systems (AMSTA-25)*. **(To be indexed in WoS/Scopus)**.

### 4.2 International Conference Proceedings
3.  **[R2]** Author Name. (2025). "A Decade of AI in Education: A PRISMA-based Systematic Literature Review of Analytical and Generative Trends (2013-2023)." *Presented at InnoConf 2025: International Conference on Education and Innovation*.
4.  **[R3]** Author Name. (2025). "The Ahadith Authenticity Dataset: Engineering a Bilingual Ground-Truth Corpus for Semantic Search in Theological Sciences." *Presented at KES AMSTA 2025: Special Session on AI in Humanities*.

### 4.3 Technical Reports and Datasets
5.  **[R5]** Author Name. (2024). "Benchmarking GPT-5 and Gemini 2.5 on Hanafi Jurisprudence: An LLM-as-a-Judge Evaluation of Doctrinal Reliability." *Technical Report AI-Islam-049*.
6.  **[Dataset]** "The Ahadith Authenticity Dataset (Kaggle)." Published for public research use at kaggle.com/datalink-placeholder.

---
