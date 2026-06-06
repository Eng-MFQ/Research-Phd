# State Exam — Study Notes

Short, beginner-friendly answers. Each answer is enough to talk about the topic confidently for a few minutes.

---

## PART A — Scientific Specialty

### 1. Stanford Prison Experiment — why a warning?

> **Q: What was the Stanford prison experiment and why is it a warning to future researchers?**

**What it was:** A 1971 study by psychologist Philip Zimbardo at Stanford University. Students were randomly split into "guards" and "prisoners" in a mock prison in the basement. The experiment was planned for 2 weeks but stopped after only 6 days because guards became cruel and prisoners showed serious psychological distress.

**Why it's a warning for researchers:**
- **Ethical failure:** Participants were psychologically harmed; there was no proper informed consent about what could happen.
- **Researcher bias:** Zimbardo himself acted as "prison superintendent" — he lost objectivity and let the abuse continue.
- **Bad methodology:** No control group, small sample, leading instructions to guards.
- **Lesson:** Researchers must protect subjects, stay neutral, and follow strict ethical review. This experiment helped trigger the creation of modern ethics boards (IRBs).

---

### 2. Three exponential technologies in informatics

> **Q: Name at least 3 informatics-related areas, which can be considered exponential technologies (i.e. can provide exponential boost to some industrial areas). Explain your choice.**

Exponential technology = doubles in power/capability every short period (like Moore's Law).

1. **Artificial Intelligence / Machine Learning** — model capability and adoption have grown exponentially (e.g., GPT-2 → GPT-4 in a few years). Boosts healthcare diagnostics, finance, content creation.
2. **Cloud computing & distributed systems** — compute power available on demand grows exponentially with cheaper hardware. Enables startups to scale globally overnight (Netflix, Uber).
3. **Quantum computing** — qubits double processing power for certain problems with each added qubit. Will revolutionize cryptography, drug discovery, optimization.

(Other valid choices: blockchain, IoT, robotics, biotech/bioinformatics, 3D printing.)

---

### 3. Markov Chain — brief description

> **Q: Provide a brief description of a Markov Chain.**

A **Markov Chain** is a mathematical model that describes a sequence of events where the **next state depends only on the current state**, not on the history (this is called the **Markov property** / "memoryless").

- Has a set of **states** (e.g., Sunny, Rainy).
- Has **transition probabilities** between states (e.g., P(Sunny → Rainy) = 0.3).
- Used in: weather prediction, Google PageRank, speech recognition, board games, finance.

Example: If today is Sunny, tomorrow has 70% chance Sunny, 30% Rainy — yesterday doesn't matter.

---

### 4. Can a study approved by an ethics board still be unethical?

> **Q: Can a study which is approved by an institutional ethics board still be unethical? Explain.**

**Yes.** Approval is not a guarantee.

Reasons:
- **New information emerges** during the study (unexpected harm) but researchers don't stop.
- **Researchers deviate** from the approved protocol.
- **The board itself can be wrong** — has limited time/expertise (Stanford and Tuskegee studies had institutional support).
- **Cultural/social context changes** — what was acceptable 20 years ago may be unethical now.
- **Hidden conflicts of interest** not disclosed during review.

**Conclusion:** Ethics is the ongoing responsibility of the researcher, not a one-time checkbox.

---

### 5. Legal evaluation: university publishing your name + phone

> **Q: Give a legal evaluation of the following situation. University published your full name and phone number in the list of Hackathon winners. Can you ask to remove the data? Why?**

**Yes, you can ask them to remove it.** This is **personal data** under data-protection law (GDPR in the EU, similar laws elsewhere).

Reasoning:
- **Phone number + full name = personal data** that identifies you.
- You have the **right to erasure** ("right to be forgotten") if the data is no longer necessary or was published without proper consent.
- The university needs a **legal basis** (consent or legitimate interest) to publish personal data. Announcing winners might justify the **name**, but **phone number is unnecessary** (excessive — violates the *data minimization* principle).
- You also have the **right to object** to further processing.

**Action:** File a request with the university's Data Protection Officer (DPO).

---

### 6. Chomsky Hierarchy

> **Q: What is the Chomsky Hierarchy?**

A classification of **formal grammars / languages** by Noam Chomsky (1956), from most powerful to most restricted. It's used in compiler theory and computer science.

| Type | Name | Recognized by | Example |
|------|------|---------------|---------|
| **Type 0** | Recursively enumerable | Turing machine | Any computable language |
| **Type 1** | Context-sensitive | Linear-bounded automaton | Natural language fragments |
| **Type 2** | Context-free | Pushdown automaton | Programming language syntax |
| **Type 3** | Regular | Finite automaton | Regex, simple patterns |

Each level is **strictly contained** in the level above. Important because it tells us what kind of machine is needed to parse a language.

---

### 7. Informed consent

> **Q: What is informed consent?**

A core ethical principle: a person voluntarily agrees to participate in research/medical procedure **after fully understanding** what it involves.

Three elements:
1. **Information** — explained in plain language: purpose, what you'll do, risks, benefits, duration.
2. **Comprehension** — the person actually understands (not just signed a paper).
3. **Voluntariness** — no pressure, coercion, or hidden incentives. They can withdraw at any time.

Origin: **Nuremberg Code (1947)** after Nazi medical experiments, then expanded in the **Declaration of Helsinki**.

---

### 8. Protecting your novel technology — what belongs to the university?

> **Q: Imagine you created a novel approach (technology). How can you protect your rights? Which of them will belong to University?**

**Ways to protect your rights:**
- **Patent** — for inventions (technical solutions). Gives 20-year monopoly.
- **Copyright** — automatic for source code, papers, designs.
- **Trademark** — protects the name/logo.
- **Trade secret / NDA** — keep it confidential.
- **Publishing** — establishes priority of the idea (defensive publication).

**What belongs to the university:**
- If you created it **during your work/studies using university resources** (lab, funding, equipment), it usually counts as a **"work for hire"** or **employee invention**.
- The university typically owns the **patent rights** and **commercial rights**.
- You usually keep **moral rights** (right to be named as inventor/author) and often receive a **share of royalties**.
- Exact rules depend on your **employment contract** and the university's IP policy.

---

### 9. Why organize networks in layers (ISO/OSI)?

> **Q: Explain the reasons to organize the description of computer networks in layers, like the ISO/OSI.**

The **OSI model** has 7 layers: Physical, Data Link, Network, Transport, Session, Presentation, Application.

**Reasons for layering:**
- **Separation of concerns** — each layer solves one problem (e.g., signaling, routing, sessions).
- **Modularity** — you can change one layer without breaking others (e.g., switch Wi-Fi to Ethernet — same TCP/IP works).
- **Interoperability** — vendors can build different products that work together as long as they respect the interface.
- **Easier teaching & debugging** — you can isolate a problem to one layer.
- **Standardization** — encourages open protocols.

Analogy: like sending a letter — you don't need to know how the truck works to write the message.

---

### 10. h-index

> **Q: What is the h-index and how is it calculated? What problems can occur in using this index to rank researchers?**

**Definition:** A researcher has h-index = **h** if they have **h papers that each have at least h citations**.

**Example:** If you have 5 papers cited at least 5 times each (and the 6th is cited <6 times), your h-index = 5.

**Problems / criticism:**
- **Favors senior researchers** — needs time to accumulate citations.
- **Doesn't capture impact** — one Nobel-level paper can be ignored if you have few others.
- **Field bias** — biology/medicine cite a lot; pure mathematics cites little. Comparing across fields is misleading.
- **Self-citations & citation cartels** can inflate it.
- **Doesn't measure quality** — a heavily cited paper might be cited for being *wrong*.
- **Discourages risky/innovative research** — encourages "safe" incremental work.

---

### 11. Logic gates — NAND with transistors, then NOT and OR from NAND

> **Q: Basis of logical operations. Logic gates. Implement a NAND gate with transistors. Then implement NOT and OR gates with NAND.**

**Basic logic operations:** AND, OR, NOT, NAND, NOR, XOR.

**NAND with transistors (CMOS):**
NAND outputs 0 only when both inputs are 1. Uses 2 PMOS (top, in parallel) + 2 NMOS (bottom, in series).

```
          Vcc
           |
       P1--+--P2     (PMOS in parallel)
           |
           Y (output)
           |
       N1--+
           |
       N2--+
           |
          GND        (NMOS in series)
```

- If both A=1, B=1 → both NMOS conduct → Y pulled to GND → Y=0.
- Otherwise at least one PMOS conducts → Y=Vcc → Y=1.

**NOT from NAND:** connect both inputs together.
`NOT(A) = NAND(A, A)`

**OR from NAND:** use De Morgan's law: `A OR B = NOT(NOT A AND NOT B) = NAND(NOT A, NOT B)`
So: `OR(A,B) = NAND( NAND(A,A), NAND(B,B) )` — uses 3 NAND gates.

**Why this matters:** NAND is a **universal gate** — any logic circuit can be built using only NAND gates.

---

### 12. Role of SQL in DBMS

> **Q: What is the role of SQL in DB Management Systems?**

**SQL = Structured Query Language.** It is the **standard language to interact with relational databases** (MySQL, PostgreSQL, Oracle, SQL Server).

Roles:
- **DDL (Data Definition Language)** — define structure: `CREATE TABLE`, `ALTER`, `DROP`.
- **DML (Data Manipulation Language)** — work with data: `SELECT`, `INSERT`, `UPDATE`, `DELETE`.
- **DCL (Data Control Language)** — permissions: `GRANT`, `REVOKE`.
- **TCL (Transaction Control)** — `COMMIT`, `ROLLBACK`.

**Why important:**
- **Declarative** — you say *what* you want, not *how* to get it. The DBMS optimizes.
- **Standard** — works across vendors (mostly).
- Built-in support for **transactions (ACID)**, joins, aggregation.

---

### 13. Vancouver protocol (citation style)

> **Q: What is the Vancouver protocol?**

A **citation style** used mostly in **medicine and biomedical sciences**, created by the International Committee of Medical Journal Editors in Vancouver, 1978.

Features:
- Citations in the text are **numbered** in the order they appear: `... as shown in [1].`
- References listed at the end in **numeric order** (not alphabetical).
- Author names: surname + initials, no full first names.
- Up to 6 authors listed; more → use "et al."

Example:
`1. Smith J, Brown K. Title of paper. Journal Name. 2023;12(4):100–110.`

Compare: APA uses (Author, Year); Vancouver uses [1].

---

### 14. NDA (Non-Disclosure Agreement)

> **Q: What is an NDA (non-disclosure agreement)? Did you sign one with University? What does it say?**

A **legal contract** where one or more parties agree **not to share confidential information** with outsiders.

Typical contents:
- **What information is confidential** (research data, source code, business plans).
- **Duration** of confidentiality (e.g., 5 years, or indefinite).
- **Permitted use** — what you may do with the information.
- **Exceptions** — info already public, info you already knew, info you developed independently.
- **Penalties** for breach.

**Did you sign one with the university?** Most universities have students/researchers sign NDAs when working with:
- Industry-funded projects
- Patentable inventions before disclosure
- Government/military research

Common clauses for PhDs: must keep research data/IP confidential until publication or until the university decides to publish.

---

### 15. Definite integral

> **Q: What is a definite integral?**

A **definite integral** computes the **signed area under a curve** between two points `a` and `b`.

Notation: $\int_{a}^{b} f(x)\,dx$

**Geometric meaning:** Area between the function f(x) and the x-axis, between x=a and x=b. Areas below the axis count as negative.

**Fundamental theorem of calculus:**
$\int_{a}^{b} f(x)\,dx = F(b) - F(a)$
where F is an antiderivative of f.

**Example:** $\int_{0}^{2} x\,dx = \frac{x^2}{2}\Big|_0^2 = \frac{4}{2} - 0 = 2$ (area of a triangle).

**Applications:** area, volume, total distance, probability, signal energy, work in physics.

---

### 16. How DNS (Domain Name System) works

> **Q: Explain how domain name services work.**

**DNS = phone book of the Internet.** It translates human-readable names (`google.com`) into IP addresses (`142.250.190.46`).

**Steps when you type `www.example.com`:**
1. **Browser cache** — does the browser already know the IP? If yes, use it.
2. **OS cache / hosts file** — check locally.
3. **Recursive resolver** (usually your ISP or 8.8.8.8) — your computer asks it.
4. The resolver asks the **root DNS server** → "I don't know, but ask the `.com` server."
5. Asks **TLD server** (`.com`) → "Ask example.com's authoritative server."
6. **Authoritative server** for example.com → returns the IP.
7. Resolver returns the IP to your browser; result is **cached** with a TTL.

**Key records:** A (IPv4), AAAA (IPv6), MX (mail), CNAME (alias), NS (name server).

**Why it matters:** Without DNS, you'd have to memorize IPs. Also enables load balancing, CDNs, failover.

---

### 17. Maximizing CPU utilization for huge matrix multiplication on a full-mesh multi-core cluster

> **Q: How would you maximize CPU utilization of very big matrix multiplication using high-speed full mesh network connection among multicore CPU-based machines?**

**Goal:** keep every CPU core busy, minimize network waiting time.

**Strategy:**

1. **Partition matrices into blocks** (tiles) — e.g., split A and B into NxN blocks that fit in CPU cache.
2. **Use a known parallel algorithm**:
   - **Cannon's algorithm** or **SUMMA** — designed for grids of processors, balance communication and compute.
3. **Distribute blocks across machines** — each node gets a block, doing local multiplications.
4. **Overlap computation and communication** — while the CPU multiplies one block, the network is already fetching the next block (async / non-blocking MPI).
5. **Exploit cache hierarchy** — choose block size to fit in L1/L2 cache (cache blocking / loop tiling).
6. **Multi-threading per node** — use OpenMP / threads to use all cores of each multi-core CPU.
7. **SIMD vectorization** — use AVX/SSE instructions; or use BLAS libraries (Intel MKL, OpenBLAS).
8. **Load balancing** — make sure no node is idle waiting for slower ones.

**Key idea:** Full-mesh means every node can talk to every other node directly with low latency — exploit this with **collective communication** (broadcast, reduce) and async data exchange.

---

## PART B — History and Philosophy of Science

### 1. Theories of information society

> **Q: Theories of information society.**

The **information society** is one where the creation, distribution, and use of **information** is the primary economic and cultural activity (replacing industry as the driver, just as industry replaced agriculture).

**Key thinkers:**
- **Daniel Bell (1973)** — *Post-Industrial Society*: shift from goods to services; knowledge becomes the central resource.
- **Manuel Castells (1996)** — *The Network Society*: information flows through global networks (internet, finance), reshaping space and time.
- **Yoneji Masuda** — Japanese theorist: information society as a peaceful, collaborative civilization.
- **Alvin Toffler** — *Third Wave*: agriculture → industry → information.
- **Marshall McLuhan** — *Global Village*: media transform society.

**Common features:**
- Information as the main commodity.
- ICT (Information & Communication Tech) is the infrastructure.
- New social divides: "digital divide" between those with/without access.
- Knowledge workers replace factory workers.

**Critiques:** the term overestimates the novelty; capitalism still drives social structure (Frank Webster).

---

### 2. Computer science as an interdisciplinary science

> **Q: Computer science as an interdisciplinary science.**

Computer science (CS) is not a single discipline — it sits at the intersection of many fields and uses tools from each.

**Foundations:**
- **Mathematics** — logic, discrete math, probability, linear algebra.
- **Engineering** — hardware design, circuits, systems.
- **Physics** — semiconductors, quantum computing.
- **Linguistics** — formal languages, NLP, compilers.

**Applications and bridges:**
- **Biology** → bioinformatics (genome analysis).
- **Medicine** → AI diagnostics, medical imaging.
- **Economics** → algorithmic trading, game theory.
- **Psychology / Neuroscience** → cognitive science, neural networks.
- **Social sciences** → computational sociology, data mining.
- **Humanities** → digital humanities, text analysis.

**Why interdisciplinary?** Computers are **tools for processing information**, and *every* field deals with information. CS provides both the tools (algorithms, software) and the abstract models (computation, complexity) that other sciences use.

---

### 3. The problem of artificial intelligence and its evolution

> **Q: The problem of artificial intelligence and its evolution.**

**Central question:** Can machines think? Can they have intelligence comparable to or exceeding human intelligence?

**Brief history:**
- **1950** — Alan Turing proposes the **Turing Test**.
- **1956** — Dartmouth Conference: term "AI" coined by John McCarthy. Optimistic period.
- **1970s–80s** — **AI winters**: funding dried up after symbolic AI (expert systems, rule-based) failed to scale.
- **1990s** — Deep Blue beats Kasparov at chess (1997).
- **2010s** — **Deep learning revolution**: ImageNet (2012), AlphaGo (2016), GPT (2018+).
- **2020s** — Large Language Models (ChatGPT, Claude), generative AI for images/video.

**Philosophical problems:**
- **Strong AI vs Weak AI** (John Searle) — does AI truly *understand* (Chinese Room argument), or just simulate?
- **Consciousness** — can a machine be conscious?
- **Ethics** — bias, jobs, autonomous weapons, alignment problem.
- **Singularity** — Kurzweil's idea that AI will surpass humans by ~2045.

**Current debate:** are LLMs a real step toward general intelligence (AGI), or just statistical pattern matchers?

---

### 4. Computer and information ethics

> **Q: Computer and information ethics.**

A branch of applied ethics that studies the **moral issues created or transformed by information technology**.

**Founders:** Norbert Wiener (1940s — cybernetics), Walter Maner (1970s — coined "computer ethics"), James Moor, Deborah Johnson.

**Main topics:**
- **Privacy** — data collection, surveillance, GDPR.
- **Intellectual property** — software piracy, open source, AI-generated content.
- **Accuracy & reliability** — who is responsible if software causes harm? (Therac-25, Boeing MCAS.)
- **Access** — digital divide, accessibility.
- **Security & cybercrime** — hacking, ransomware.
- **AI ethics** — bias in algorithms, fairness, explainability, autonomous weapons.
- **Professional ethics** — codes of conduct (ACM, IEEE).

**Key principles:** transparency, accountability, fairness, privacy, beneficence (do good), non-maleficence (do no harm).

**Why now?** Technology amplifies the scale and speed of decisions, making ethical judgment more urgent.

---

### 5. Mathematical modeling in various fields

> **Q: The use of mathematical modeling in various fields of knowledge.**

A **mathematical model** is a representation of a real system using mathematical concepts (equations, graphs, probabilities) to study, predict, or optimize its behavior.

**Steps:** problem → assumptions → equations → solve → validate against reality → refine.

**Examples across fields:**
- **Physics** — Newton's laws, Maxwell's equations, Schrödinger equation.
- **Biology** — population dynamics (Lotka-Volterra predator-prey), epidemic spread (SIR model used during COVID-19).
- **Economics** — supply/demand, game theory, Black-Scholes for options.
- **Engineering** — finite element analysis, control systems.
- **Medicine** — pharmacokinetics, tumor growth models, medical imaging.
- **Climate science** — global warming forecasts, weather prediction.
- **Computer science** — algorithm complexity, queuing theory, neural networks.
- **Social sciences** — voting models, traffic flow, opinion dynamics.

**Advantages:** cheap, fast, lets us explore "what if" scenarios.
**Limits:** model is a simplification; "all models are wrong, but some are useful" (George Box).

---

## PART C — Pedagogical Activities

### 1. Online education — specifics, limitations, opportunities, pedagogical design

> **Q: The specifics and limitations of online education. Opportunities and pedagogical design in the implementation of online education in higher education. Give a detailed answer.**

**Specifics of online education:**
- Delivered via the internet (LMS like Moodle, Coursera, Zoom).
- **Synchronous** (live lectures, webinars) vs **asynchronous** (recorded videos, forums).
- Self-paced, place-independent.

**Opportunities:**
- **Accessibility** — students anywhere, including disabled, working, or remote learners.
- **Scalability** — one course → thousands of students (MOOCs).
- **Personalization** — adaptive learning paths based on AI/analytics.
- **Multimedia** — videos, simulations, interactive quizzes.
- **Cost-effective** in the long run for institutions.
- **Lifelong learning** — fits adult learners.

**Limitations:**
- **Lack of social interaction** — isolation, loss of peer learning.
- **Requires self-discipline** — high dropout rates (MOOCs ~90%).
- **Digital divide** — internet/device inequality.
- **Hard to assess practical skills** (labs, clinical work).
- **Cheating** in unsupervised exams.
- **Teacher workload** — designing online materials is time-intensive.
- **Reduced non-verbal cues** for teachers.

**Pedagogical design — key principles:**
- **Constructive alignment** — learning outcomes ↔ activities ↔ assessment.
- **Use the ADDIE model**: Analyze, Design, Develop, Implement, Evaluate.
- **Blended learning** — combine online and face-to-face.
- **Active learning** — quizzes, discussions, projects, not just passive video watching.
- **Microlearning** — short, focused modules (5–10 min videos).
- **Community of Inquiry** (Garrison): combine cognitive, social, and teaching presence.
- **Continuous feedback** — peer reviews, automated quizzes, instructor check-ins.
- **Inclusive design** — captions, transcripts, mobile-friendly.

**Conclusion:** Online education is powerful when designed thoughtfully but cannot fully replace face-to-face for skills requiring physical practice or deep mentoring.

---

### 2. Psychological and professional characteristics of IT specialists; their development in higher education

> **Q: Psychological and professional characteristics of IT specialists and their development in the pedagogical process in higher education. Give a detailed answer.**

**Typical psychological characteristics:**
- **Analytical thinking** — decomposing problems logically.
- **Abstract / systems thinking** — reasoning about invisible structures (code, data flow).
- **High concentration** for long periods ("flow state").
- **Tolerance for frustration** — debugging, dealing with errors.
- **Curiosity** and continuous learning (tech changes fast).
- **Preference for working with systems over people** (often, not always).
- Risk of **burnout**, sedentary lifestyle, social isolation.

**Professional characteristics:**
- **Technical skills (hard skills):** programming, algorithms, math, software architecture, security, databases.
- **Soft skills:** teamwork (Agile, Scrum), communication with non-technical stakeholders, project management, writing documentation, ethical judgment.
- **Lifelong learning mindset** — frameworks, languages, paradigms evolve every few years.
- **Adaptability** to change.

**Development in higher education:**

*Curriculum:*
- Foundation in mathematics, theory of computation, algorithms.
- Programming projects of increasing complexity.
- **Team projects** to develop collaboration.
- Internships / industry placements.
- Ethics and social impact of IT.

*Pedagogical methods:*
- **Problem-based learning (PBL)** — students learn by solving real problems.
- **Project-based learning** — building real software end-to-end.
- **Hackathons & coding competitions** — develop creativity under pressure.
- **Pair programming** — develops communication and code review skills.
- **Flipped classroom** — theory at home, practice in class.
- **Capstone projects** — integrate everything in final year.

*Developing soft skills:*
- Presentations of own projects.
- Writing reports and documentation.
- Working in diverse, multidisciplinary teams.
- Cross-faculty courses (business, design, ethics).

*Supporting psychological health:*
- Awareness of burnout / mental health.
- Mentorship programs.
- Balanced workload, ergonomic awareness.

**Conclusion:** The role of higher education is not only to transfer technical knowledge, but to shape a **well-rounded professional** who can think critically, work in teams, communicate, and adapt to lifelong change.

---

## Quick last-minute tips

- For ethics questions (1, 4, 7, 14, B4): mention **Nuremberg Code → Declaration of Helsinki → modern IRBs**, plus **GDPR** for privacy.
- For technical questions: always give one concrete **example** — examiners like seeing you can connect theory to practice.
- For "explain" questions: structure = **definition → how it works → example → why it matters**.
- Stay calm, speak slowly, and if you don't know an exact detail, say what you *do* know in the area.

Good luck! 🍀
