Automatic Research Assistant for Academics – Project Plan and Research
Project Vision and Objectives

The goal is to create an “Automatic Researcher” assistant – essentially a GitHub Copilot for scientists that can autonomously assist in academic research tasks. This system is intended for academic researchers (and R&D teams) across domains, focusing initially on STEM and computer science. It should be capable of taking a research topic or a draft paper as input and then following the scientific method steps (literature review, hypothesis generation, experimentation, analysis, and paper writing) to help “finish the paper.” In other words, given a question or partial draft, the assistant will gather up-to-date knowledge, propose experiments (including running simulations/code), and compile results into a well-structured academic report.

Key objectives include:

Literature Review: Retrieve and summarize the latest relevant papers (e.g. from arXiv or other open sources) to ensure the research is grounded in current knowledge.

Idea Generation: Formulate hypotheses or research directions based on gaps or questions identified in the literature.

Simulation/Experimentation: If applicable, design and execute simple simulations or code experiments (e.g. mathematical modeling, data analysis) to test hypotheses.

Autonomous Research Workflow: Allow an agentic mode where the AI cycles through tasks with minimal user intervention, essentially acting as a junior researcher. Also allow a copilot mode where the human can guide or provide input at each step.

Paper Drafting: Automatically produce a draft research paper or report – with sections like Introduction (background & literature review), Methodology, Results, Discussion/Conclusion – incorporating the findings and properly citing sources. This is akin to having the AI “work on its own and find its own hypothesis,” then document the outcomes.

Ultimately, the system aims to accelerate research by handling tedious tasks (literature search, coding, documentation) so that humans can focus on creative and critical thinking
agentlaboratory.github.io
agentlaboratory.github.io
. It should not replace the researcher’s creativity or judgment, but rather complement it by automating repetitive, time-intensive tasks like searching, coding, and writing documentation
agentlaboratory.github.io
.

Key Functionalities and Workflow

To meet these objectives, the workflow of the Automatic Research Assistant can be broken down into modular steps or phases. Each phase corresponds to a component of the scientific research process:

Input Intake: The user either provides a research question/idea (text prompt describing what they want to investigate) or uploads a partial draft or reference paper that they want to build upon. This sets the initial context.

Literature Retrieval: The system searches academic databases (starting with arXiv preprints) for relevant papers based on the input topic or the contents of the provided paper. It will leverage an API (e.g., arXiv API) to fetch titles, abstracts, and links for top relevant papers
info.arxiv.org
.

Literature Review & Summarization: Using the search results, the assistant reads the abstracts (and potentially full texts) of those papers. It summarizes key findings, methods, and gaps from the literature. This forms a knowledge base for the agent. (This could involve an LLM summarizing each paper’s abstract or introduction.)

Knowledge Integration (RAG): The relevant information from papers is integrated via a Retrieval-Augmented Generation approach – i.e., the assistant stores or embeds the key points so that it can cite or use them when reasoning. This ensures up-to-date factual content is available to the language model, mitigating hallucinations.

Hypothesis Generation: Based on the literature review (and the user’s initial question), the system brainstorms research questions or hypotheses to explore. For example, it might identify a gap or an unexplored aspect in the literature and propose to investigate that. This step uses the LLM’s reasoning capabilities to suggest logical next steps or potential solutions.

Experiment Planning: The assistant devises a plan to test the chosen hypothesis. This could be designing a small simulation, choosing a dataset to analyze, or formulating a theoretical derivation. The plan will specify what needs to be done (e.g., “simulate the proposed algorithm under various conditions” or “solve these equations to see if the hypothesis holds”).

Simulation/Code Execution: Using an integrated code execution module, the assistant carries out the experiment. It might generate Python code (e.g., using libraries like NumPy/SciPy, or domain-specific tools) to run calculations or simulations. The code is then executed in a sandbox or REPL environment, and results are obtained.

Analysis of Results: The outcomes from the simulation are analyzed by the system. The LLM can be prompted to interpret the numeric results or plots – identifying whether they support or refute the hypothesis. If the results are inconclusive or suggest another question, the agent could loop back to step 5 (adjusting the hypothesis or running a new experiment).

Report Drafting: Finally, the system compiles a draft academic paper. It uses the information from the literature (with citations), the methodology of the experiment, the results, and the analysis to generate a structured report. The output includes an Introduction (context and related work), Methodology (what was done, e.g. simulation details), Results, Discussion, and Conclusion. The writing should be in formal academic language. Ideally, citations to the literature are embedded (and could be numbered or by author as needed). If possible, the draft could be formatted in LaTeX or Markdown for easy editing.

User Review & Iteration: The human user can then review the draft, make edits, or ask the assistant to clarify or expand certain parts. In copilot mode, the user might iteratively interact with the system at several points – for instance, selecting which papers from the literature search to focus on, or refining the hypothesis – while in autonomous mode the agent would make those choices itself.

This workflow ensures the AI assistant touches all parts of the research process. Notably, it aligns with how a human researcher works: survey current knowledge, identify a gap, formulate a hypothesis, test it, and write the findings. Recent AI research projects like Agent Laboratory have demonstrated the feasibility of this pipeline by splitting the workflow into specialized phases (Literature Review, Experimentation, Report Writing) with different agents handling each part
agentlaboratory.github.io
.

Below we dive deeper into the architecture and each component of the system:

System Architecture and Components

High-Level Architecture: The system will be structured as a modular pipeline of components orchestrated by a central AI agent (powered by a large language model). We can think of the assistant as an AI orchestrator that coordinates various tools and modules to accomplish the complex task of research. This design is inspired by approaches like HuggingGPT, where a central LLM (e.g., ChatGPT) delegates tasks to specialized tools or models
medium.com
. In our case, the orchestrator will use tools such as a literature search API, a document parser, a code execution environment, etc., to carry out the steps described above.

Key components/modules include:

User Interface (UI): A front-end (likely a local web app built with Django and React or similar) where the user enters their query or uploads a paper, and later views results. This UI will guide the user through the process or display the autonomous agent’s progress. It should present intermediate outputs (like a list of found papers or simulation results) in a human-friendly way.

LLM Orchestrator (Core Engine): At the heart is a language model (such as GPT-4 or a fine-tuned open-source LLM) that drives the reasoning. This orchestrator agent is what parses the user’s request, plans the research steps, and generates or refines content. It uses prompts and possibly a chain-of-thought prompting approach to decide on actions (e.g., whether to search for papers, whether to run code, when to start writing, etc.).

Tool/Agent Integration Layer: The orchestrator is connected to various tools (sub-agents) that perform specific tasks. For example:

A Literature Search Tool that queries external APIs (like arXiv’s) for papers.

A Document Reader/Summarizer tool to extract and summarize content from PDFs or text.

A Python Execution Environment (REPL tool) where the model can write and run code.

Possibly other specialized tools (e.g., a math solver, a data visualization module, or a LaTeX formatter).
This can be implemented using frameworks like LangChain, which supports tool integration and even provides ready-made wrappers – for instance, LangChain’s ArxivAPIWrapper can fetch top-k results’ summaries from arXiv if provided with a query
python.langchain.com
. The LLM can operate in an agent mode where it decides which tool to invoke at each step (using a prompt format like: Thought → “I should search for papers about X” → Action[ArxivSearch] → Observation[results] → etc.). This dynamic decision-making loop is similar to how autonomous agents (e.g., AutoGPT) function.

Knowledge Base / Memory: As the research progresses, the system will accumulate information (papers found, facts learned, intermediate results). Storing this either in memory or a vector database is important so that the LLM can recall relevant details later when writing the paper. For example, after retrieving and summarizing 5 papers, their key points could be stored as embeddings in a vector store (like FAISS or Chroma). Then, when the LLM needs to discuss related work or background, it can query this store to remind itself of specific details to cite (a typical RAG approach). In an MVP, a simpler approach might store all summaries in a text cache and feed them into the prompt when drafting the introduction.

Controller/Workflow Logic: In addition to the LLM’s own planning, we might implement a high-level controller that ensures the process flows logically from start to finish. For instance, after the literature review step is done, the system should explicitly trigger the hypothesis generation step. This controller can be a simple Python logic that calls the LLM with different system prompts for each phase, or it can rely on the LLM to self-navigate. Designing this requires balancing autonomy with reliability: a fully autonomous agent might loop indefinitely or go off-track, so guiding it through a predefined sequence (with the option to iterate) could be more predictable for a hackathon MVP.

The architecture thus combines pipeline elements and agentic control. A user’s query flows through these components and results are passed back to the LLM for reasoning and finally to the UI for display. Crucially, this design is extensible – new tools or data sources can be plugged in. For example, we start with arXiv for papers, but later could add the OpenAlex API for a broader literature search (OpenAlex indexes 250M+ scholarly works and offers a free, no-auth API
docs.openalex.org
). Similarly, the Python execution could be extended to use specific simulation engines or cloud computing if needed.

Below, we discuss each major module in detail:

Literature Retrieval Module (ArXiv API Integration)

For up-to-date academic content, integrating the arXiv API is a priority (since arXiv hosts millions of open-access papers across physics, CS, math, etc.). ArXiv provides a free API endpoint for querying its papers database
info.arxiv.org
. Key points about using the arXiv API:

The API is a RESTful interface at http://export.arxiv.org/api/query. We can pass parameters like search_query to specify keywords, authors, or categories. For example, search_query=all:quantum+AND+all:cryptography would retrieve papers whose title/abstract contain both “quantum” and “cryptography”
info.arxiv.org
. The results are returned in Atom XML format containing entries for each paper.

Each result entry includes metadata like title, abstract (summary), authors, publication date, and links
info.arxiv.org
. Notably, one of the <link> elements in the entry provides the URL to the PDF of the paper (e.g., http://arxiv.org/pdf/<id>). This means our system can fetch the PDF or at least the abstract for further processing.

The API supports pagination via start and max_results parameters, which is useful if a query has hundreds of results
info.arxiv.org
. For our purposes, we might limit to the top N results (say 5 or 10) for manageability. The max_results parameter can be set accordingly.

Rate limiting: arXiv’s API is generally generous but for very frequent calls we should be mindful of not hitting any limits or getting backoff responses. For a hackathon demo, this is unlikely an issue, but caching queries or limiting frequency is wise in design.

Tools/Libraries: Instead of manually handling HTTP requests and XML parsing, we can use existing libraries or wrappers. For instance, lukasschwab/arxiv.py is a Python library that wraps the arXiv API and returns results as Python objects (with fields for title, summary, etc.). This library is conveniently used in LangChain’s ArxivAPIWrapper as well
python.langchain.com
. Using such a wrapper can speed up development.

Another approach is to use a semantic scholar or crossref API for literature, but these may require API keys or have usage limits. Semantic Scholar’s API can return paper abstracts and citations given a paper ID, and CrossRef’s API can search by query to get DOIs. However, sticking to arXiv (and perhaps OpenAlex for broader coverage) is simpler for an MVP. OpenAlex in particular could complement arXiv by providing metadata for papers outside arXiv (e.g., journal articles) in the future, since it covers hundreds of millions of works and is also open
docs.openalex.org
.

Workflow in practice: Given a user’s topic or a draft paper, the system will formulate a search query. If the user provided a paper, we might extract keywords from that paper’s abstract/title to search for related works. If the user gave just a topic, we use that directly. The query is sent to the arXiv API, and we get back, say, the top 5 relevant papers. We then extract each paper’s title and abstract (the API <summary> which is the abstract text
info.arxiv.org
). These abstracts are short (usually a few paragraphs) and can be fed to the LLM for summarization or analysis. We also store the paper’s ID/link so we can cite it or possibly fetch the full PDF if needed.

Example: Suppose the user asks about “quantum key distribution improvements”. The system queries arXiv with that term, gets a list of recent preprints in that area. For each result, it obtains:

Title (e.g., “A Novel Quantum Key Distribution Protocol Using XYZ”),

Abstract (which describes what was done and perhaps results),

PDF link.
The assistant might summarize each abstract or at least identify which ones seem most relevant (perhaps by looking for overlapping themes). This ensures our literature review covers latest knowledge – something crucial since the system’s internal knowledge (the LLM’s training data) might be outdated. By pulling fresh data from arXiv, we tether the AI’s answers to current research
agentlaboratory.github.io
.

Finally, these retrieved summaries will be used in the Literature Review section of the output and to guide the hypothesis. The assistant can explicitly cite these sources to lend credibility. This approach is similar to what tools like Elicit do – Elicit is an AI research assistant that uses AI to search and summarize over 100 million papers
elicit.com
. Likewise, our system will effectively create an automated literature review on the specified topic.

Paper Ingestion and Analysis Module

If the user provides an existing paper (e.g., a PDF or text of a draft), the system should ingest and analyze it. This is useful if the researcher has a partially written manuscript or a key reference paper to start from. Features of this module:

PDF/Text Ingestion: We can use a PDF parsing library (such as PyMuPDF (fitz), PDFPlumber, or pdfminer) to extract the text from the PDF. Another option is using a service like Grobid (which can convert PDFs to structured TEI XML, extracting sections, citations, etc.), but running Grobid may be overkill for an MVP and not easily done within a short hackathon timeframe. A simpler approach: extract raw text and perhaps split it by sections (if we can detect headings like “Introduction”, “Methodology”, etc. via regex).

Understanding Context: Once we have the text, we likely don’t need the entire content for the AI; instead, we can summarize or pick out key elements:

Core Problem or Question: Identify from the introduction or abstract what problem the paper is tackling.

Methods/Approach: If the user’s paper is a draft, see what they have done or plan to do.

Gaps or TODOs: If the paper is incomplete, perhaps there are explicit sections that are blank or marked as future work – the assistant should note these as targets to work on.

Citations/References list: We could extract the bibliography to see what sources the user already considered. If those are relevant, the assistant might look them up (maybe even fetch those via APIs if open access). However, that might be complex; at minimum, knowing the key references could help steer the search for additional literature (to avoid duplicating known info).

Summarization: We can employ the LLM to summarize the user-provided paper’s content, especially if it’s a long document. For example, get a summary of each section or the overall gist. This summary can then be used just like the literature review info – it’s part of the knowledge base the system uses to decide on next steps. If the user’s paper includes a hypothesis or question, the assistant will extract that and perhaps directly start from Experimentation on that hypothesis (skipping hypothesis generation). Alternatively, if the paper is just background, the assistant will incorporate it into the literature review.

Integration with Search: The content of the provided paper can also be used to formulate better search queries. For instance, if the paper mentions a specific technique or prior work, the system can search for that specifically on arXiv to find related studies.

In summary, the ingestion module ensures that the agent fully understands any user-provided materials before proceeding. This way, the assistant’s contributions will be consistent with what the user has already written and will truly “work from there,” building on the user’s initial paper rather than starting from scratch.

Reasoning and Planning Module (LLM Brain for Hypotheses)

This is the cognitive core of the assistant, largely powered by a Large Language Model. After gathering information (from the literature and any user paper), the system needs to plan the research path. Key aspects:

LLM Prompting for Planning: We will craft prompts to encourage the model to follow the scientific method. For example, once the literature summaries are ready, we might prompt the LLM with something like: “Given the above context, what is a promising hypothesis or research question that could be investigated next? List one or more potential hypotheses or problems worth exploring, based on gaps or open issues in the literature.” The model’s response to this will be the starting hypothesis. We can also instruct it to provide reasoning for why that hypothesis is important or how it connects to the references (this could later be part of the Introduction).

Chaining and Memory: We should maintain the state – the hypothesis the model picks should be stored. We then prompt another step for experiment design: “Design an experiment or simulation to test the hypothesis: [hypothesis]. What steps will the experiment involve, and what outcomes will confirm or disconfirm the hypothesis?” This gets the model to outline a plan. If the plan seems too vague or not feasible to implement in code, the system might refine it or ask the LLM to break it down further. This iterative prompting is effectively a chain-of-thought technique, making the LLM think step-by-step rather than going directly from question to final answer.

Agentic Tool Use: Instead of a static chain, we could let the LLM act as an agent that decides on the fly what to do. For example, using an agent loop (like in LangChain or similar frameworks), the model could have a prompt format that includes a “Thought” and “Action” section. It might think: “To validate this hypothesis, I need data on X. Perhaps I should search for a dataset or run a quick simulation.” Then it outputs an Action like Action: Python.run_code along with some code. The system executes the code and returns the output, which the LLM sees, and then it continues the loop by observing results and deciding the next step. This kind of autonomy is powerful but can be tricky to get right in a short time, so we may implement a simplified version: have predetermined points where code is executed rather than completely free-form decisions.

Ensuring Scientific Rigor: The LLM needs to “behave” like a researcher. That means grounding claims in evidence (hence the retrieval step) and logically evaluating results. We will incorporate instructions in the prompts to: use a neutral, analytical tone; cite sources for any factual statements from literature; use math or logic when needed (the presence of the Python tool will help, as the model knows it can calculate rather than guess numeric answers). Additionally, if the model makes a claim (e.g., “Method A is better than Method B”), we might have a secondary check: ask it to list which source supports that claim, or even have a verification agent check consistency. Again, for MVP, a simpler approach is fine – e.g., manually verify a bit, or trust but plan to refine later.

Essentially, this module is where the “brain” of the automatic researcher sits. Modern LLMs are quite capable at such meta-reasoning tasks, especially GPT-4 which has demonstrated abilities to plan and solve complex tasks by calling tools. In fact, our approach resonates with the concept of an AI research agent that “reads hundreds of papers to deliver precisely relevant insights – faster than ever”
undermind.ai
 and then proceeds to solve problems. By dividing the work into clear phases and instructing the LLM accordingly, we aim to keep it focused and factual. The cited Agent Laboratory project found it effective to break the workflow into these distinct phases with specialized prompts/agents
agentlaboratory.github.io
, which we will emulate.

Simulation and Experimentation Module

A standout feature of this project is the ability to run simulations or code-based experiments as part of the research process. This module gives the assistant a kind of “hands-on lab” where it can test ideas rather than only relying on text. Here’s how we envision it:

Python Execution Environment: We will incorporate a Python interpreter that the system can use. In a Django web app context, this could be a backend endpoint that safely executes code (perhaps using a restricted environment or library like execjs or a simple Celery job running the code). For hackathon simplicity, one might allow the code to run directly on the server with precautions. The environment should have common scientific libraries installed – e.g., NumPy, SciPy, pandas, SymPy (for symbolic math), possibly Matplotlib if plotting is needed (though generating actual charts might be beyond MVP scope, but numeric results or data analysis is feasible).

Integration with LLM Agent: If using LangChain or an agent approach, this can be set up as a tool (often called something like PythonREPLTool). This means the LLM knows it has the ability to output some code as an action, which the system will execute, and then return the stdout/result back to it. For example, the LLM might output: `Action: Python_REPL\nCode:\n```\nimport numpy as np; ... print(result)\n````, and the orchestrator will run that and feed the output (and any error messages) back into the LLM’s context. This closes the loop, allowing iterative debugging or multiple runs if needed (similar to how a researcher might tweak their code). In fact, the Agent Laboratory setup has a component called mle-solver that iteratively improves code based on errors/scores
agentlaboratory.github.io
. While we may not implement a full evolutionary code solver, we can at least allow one cycle of code generation and result retrieval, which already shows the concept.

Use Cases for Simulation: Depending on the research question, simulations could vary widely. For MVP, we consider relatively self-contained computational experiments. For example:

Mathematical proof or derivation: The agent could use SymPy to solve an equation or find a counterexample.

Algorithm test: If the hypothesis is “Algorithm A is faster than Algorithm B for X”, the agent could implement small versions of both and time them on random data.

Data analysis: If a dataset is readily available (perhaps a small CSV or a known dataset from online), the agent could perform a statistical test. (During a hackathon, an example dataset could be bundled for demonstration.)

Simulation: e.g., simulating a physics phenomenon or running a Monte Carlo experiment to estimate some probability relevant to the question.

The key is to keep these experiments simple but illustrative. The agent doesn’t have a lab for physical experiments, but many research questions can be at least partially explored with code or math. By demonstrating even a toy experiment, we validate the idea that the AI can not only read papers but also do something active. This sets our project apart from purely text-based assistants.

Capturing Results: Once the code runs, the output (numbers, tables, or any findings) will be captured. If it’s a lot of data, we might have the code summarize it (e.g., print mean values or simple conclusions). If it’s a figure, we could save an image (but integrating that into the final report might be complex for MVP). The results will be analyzed by the LLM: we’ll feed the output back with a prompt like “Here are the results of the experiment: [result]. What do these results indicate? Do they support the hypothesis?” The LLM then provides an analysis in plain text. This analysis will be used in the Results/Discussion section of the paper.

Iterative Loop: In some cases, the analysis might say “the results are inconclusive” or suggest a follow-up. If time permits, the agent could loop: refine the experiment or try a different parameter. But since this is a hackathon project, a single loop from hypothesis → one experiment → result is likely sufficient to showcase the capability. More complex autonomous iteration (like trying multiple approaches until something works) is an advanced feature that can be explored later. For now, demonstrating one full cycle (planning -> execution -> analysis) is a big win.

Technical consideration: Running arbitrary code has risks (security and runtime errors). For the hackathon, since this is all local, security is not the top concern (we trust the user and our code). However, from a design perspective, one could sandbox the execution. Some approaches: using Docker containers to run the code, or restricting builtins and imports in Python. But in the interest of time, we might simply run trusted libraries and hope the LLM doesn’t try anything malicious. We will instruct the LLM (via system prompt) that the Python tool is only for numerical computation or data processing tasks relevant to the research – not for file system access or network calls (which we can explicitly disable in the environment). This will mitigate accidental misuse.

In summary, the Simulation module empowers the AI to act like a researcher running an experiment. It moves beyond just text generation to actually generate results. This is a crucial differentiation from other literature assistants. We’re effectively giving the AI the ability to answer empirical questions by doing the work, not just looking it up. As AI agents (like those in SciSpace’s AI agent or AgentLab) have shown, combining knowledge with action (here via code) is key to a full-stack research assistant
scispace.com
agentlaboratory.github.io
.

Output Generation and Paper Drafting Module

The final step is to compile everything into a coherent research paper draft. The drafting module will use the LLM to generate well-structured text, complete with references and formal academic language. Key points in this module:

Structure of the Paper: We plan to organize the output into standard sections:

Introduction/Background: Explains the research problem and why it’s important, summarizes key related work (from the literature review) to establish the context, and possibly ends with the specific hypothesis or objective of this work. This section will heavily use the information gathered from the Literature Retrieval module, ensuring to cite the sources of important claims or prior approaches. For example, “Prior studies such as Smith et al. (2023) have explored X
scispace.com
, but Y remains unsolved.” We will include citations in a consistent format (maybe numeric [1], [2] or author-year depending on style – numeric might be easier). Since this is a draft, the citations could be placeholders that map to a reference list at the end.

Methodology/Approach: Describes how the hypothesis was tested or how the research was conducted. Here the assistant will detail the experiment design and any simulation or analysis performed. It might read like: “To evaluate the hypothesis, we implemented a simulation of … using Python. The simulation steps were …” It can include enough detail so that the approach is reproducible in principle (code could even be included or summarized). If the experiment is simple (as it will be for MVP), this section will be brief. If code was run, perhaps mention the library or approach (e.g., “a numerical solver was used for the equations”).

Results: Present the outcome of the experiment. This can be a mix of text and possibly tables or figures. For MVP, likely text summarizing results and maybe a small table of numbers if applicable. E.g., “We found that under conditions A and B, the output metric was X. In contrast, varying C led to a drop in performance to Y.” The results should directly address the hypothesis. If the hypothesis was confirmed, say that; if not, explain what happened.

Discussion: Interpret the results in a broader context. This is where the assistant might say “This finding aligns with the theory of Z” or “This contradicts what was reported by Jones (2022)
scispace.com
, possibly because …”. The discussion can also acknowledge limitations (since an MVP experiment will be limited) and suggest future work – which sets up nicely how a human researcher could take over next.

Conclusion: A brief wrap-up of what was learned and the significance.

References: A list of the literature cited in the introduction/discussion. Since we have those from the search, we can output them in a simple format (maybe numbered). Each reference should include enough info to identify it – probably the title and arXiv ID or URL, since with arXiv ID one can find the paper easily. For example: [1] Author Names, “Title”, arXiv:1234.5678 (Year). If we have DOIs via arXiv metadata, we could include those or actual publication info if available (arXiv sometimes has a journal reference field if published).

Using LLM for Drafting: We will use a final prompt that feeds the LLM the outline and the gathered content. By this stage, we have:

Summaries of each relevant paper (with citation placeholders).

The chosen hypothesis and context for it.

Description of what was done (perhaps in bullet form or raw text from the plan).

The results of the experiment (either as raw output or a summary).

The analysis of results (the LLM’s own interpretation).
We can concatenate these or provide them in a structured way, then ask the LLM to “Write a draft research paper using the above information. Include an Introduction, Methodology, Results, and Conclusion. Incorporate the references [list of refs] where relevant.” We’ll emphasize that it should use formal academic tone. The model should ideally incorporate the references by referring to them in the text (like “As per [1]…”). Since we have control over how we feed references, we might number them in the order we gave them to the LLM (which could be sorted by relevance or chronology).

Quality and Coherence: One challenge is ensuring the paper is coherent and not just a disjointed set of AI-generated paragraphs. To mitigate this, we might generate section by section:

Prompt for Introduction separately with relevant info (lit review and hypothesis).

Then prompt for Methodology separately (with experiment plan details).

Etc.
This can produce more focused content for each part, which we then assemble. However, a well-engineered single prompt can also work. We will likely try the simpler route first and see if the output is acceptable.

Citations Accuracy: We will need to double-check that any factual statements are backed by the sources we have. The safest way is to explicitly insert those facts from the summaries rather than rely on the model’s memory. For instance, if one paper (Ref [1]) reported a certain finding, ensure that text is somewhere in the model’s context when writing the intro. This reduces the chance of a hallucinated citation (where the model says [1] did X when it didn’t). If needed, we can have the model output where each piece of info came from (some prompt frameworks have you cite sources as the model writes), but given time, we might manually verify a bit.

Format: Since the user mentioned possibly a web app interface, the output could be displayed in-browser as formatted text (HTML or Markdown). If aiming for a LaTeX output (because academia loves LaTeX), we could have the model produce LaTeX syntax for equations, etc., but that might complicate things. Markdown is a good middle ground – it can handle headings, lists, bold/italic and even LaTeX math in $$ if needed. We’ll likely have the model produce something that can be easily copied into an Overleaf later by the user. The UI could also allow downloading the draft as a .tex or .docx if we post-process it.

By completing this module, the system will have produced the final deliverable: a comprehensive research report that the user can then refine and eventually submit or use. Impressively, much of this draft is generated automatically, but it should clearly be based on real prior work and real experimental evidence (from the simulation), giving it a credibility that pure text generation lacks. This approach is essentially what Agent Laboratory’s “paper-solver” does – it “summarizes outputs and findings from previous experimental phases into a human-readable academic paper”, taking in the research plan, results, insights, and literature review to produce a conference-style paper draft
agentlaboratory.github.io
. Our system mirrors that concept on a smaller scale.

User Interface and UX Considerations

Designing a smooth user experience (UX) is important so that researchers find this tool helpful rather than cumbersome. Here are the UX plans and considerations:

Web Application (Local): We aim for a web-based interface (for accessibility and ease of use), likely served by a Django backend. This keeps everything local to the user’s machine (important if proprietary data is used, and also practical for leveraging local compute for simulations). The UI can be a single-page application that dynamically updates as the agent progresses.

Input Stage: The home screen will have two main options for input:

“New Research” – where the user types a research question, topic, or a brief description of a problem they want to explore. Possibly a text area with guidance like “What would you like to research? (e.g., ‘explore new methods for quantum key distribution’).”

“Upload Paper” – where the user can upload a PDF or paste text of a draft paper. This can be used to either continue a partially written paper or to analyze a reference paper and build new ideas from it.

We might also allow specifying a field or keywords to focus the literature search (or automatically detect from the question).

Progress Visualization: Once the process starts, the user should see that the system is working through phases (to build trust and understanding). A possible UI approach is a step-by-step timeline or checklist on the page, e.g.:

✅ Literature Search – “5 papers found on arXiv for query X.”

✅ Literature Review – “Summarized key findings from papers [1]-[5].”

✅ Hypothesis Generated – “Hypothesis: <i>Quantum channel noise can be reduced by XYZ.</i>”

🔄 Experiment Running – “Simulating 1000 runs of the protocol…” (this might show a loading spinner or progress bar if it takes time).

✅ Results Analyzed – “Preliminary results support the hypothesis.”

🔄 Drafting Report – “Compiling the report…”

Each of these could expand to show details. For example, clicking on “5 papers found” could display the titles of those papers (and maybe the abstracts or a snippet). This not only provides transparency but also lets the user intervene: if they see an irrelevant paper was picked, maybe a future feature is to deselect it. In MVP, we might not implement manual intervention mid-way, but at least showing it is good.

Output Display: After drafting, the paper will be shown in a nice readable format. Perhaps using a rich text viewer or Markdown viewer. If citations are numeric, maybe they’re clickable links that scroll to the reference list at bottom. We can also allow the user to copy the text or download it. In a polished version, we’d allow editing inline, but that’s beyond MVP (the user can copy to their editor of choice).

Interaction Mode (Autonomous vs Guided): Two modes could be offered:

Autonomous (Run All): The user simply hits “Go” and the agent goes through all steps, producing the final output without further input.

Guided (Step-by-step): After each major phase, the system might pause and ask for confirmation or input. For example, after literature search, it could show the list of papers and ask “Would you like to include all of these in the review? You can uncheck any that seem irrelevant.” Or after hypothesis generation, show the proposed hypothesis and allow the user to edit or approve it before proceeding. This mode is akin to a co-pilot where the human is in the loop. It can increase trust (the researcher can steer it if it was going off-course) and also helps the user learn from the process. Given hackathon time constraints, we might implement only the autonomous flow fully, but design the UI with the possibility of adding pauses for input later (perhaps a “Next” button to move from one phase to the next).

Error Handling and Feedback: If something goes wrong (e.g., no papers found, or the code execution fails due to an error), the UI should handle this gracefully. For literature, if nothing is found, maybe suggest a broader query or a different data source. If code fails, we might capture the error message and show it (perhaps with an apology and an option to let the agent try a minor fix). This is important because research is inherently uncertain – the assistant might not always succeed on the first try. Even Agent Laboratory found variability in quality and needed multiple attempts for experiments
agentlaboratory.github.io
. In UX, conveying this and possibly allowing a re-run can be helpful. We might include a “Retry experiment” button if something fails.

Visual Aids: If the simulation produces something visual (like a plot), the UI can show that image in the Results section. This could make the presentation more compelling. We can generate a matplotlib graph in code and save it, then display. But careful that we have time; if not, we focus on textual output.

Performance considerations: Each phase might take time (LLM calls, API calls, code running). We should inform the user of progress (as above) and perhaps use async calls or background tasks for long steps so the UI remains responsive. For example, if the simulation might run for 30 seconds, using a background task and periodically updating status is ideal. However, for MVP, simplifying assumptions (like all runs under a few seconds, or just blocking with a spinner) might be acceptable.

In summary, the UX is aimed at making a complex multi-step process feel understandable and controllable to the user. By breaking down the workflow into clear steps in the interface, we ensure the user always knows what the AI is doing and why. This transparency is crucial for academic users who will want to trust the results. It’s also educational – researchers can see which papers were key, what hypothesis was tested, etc. Our design echoes the notion of “co-pilot vs autonomous” modes discussed in Agent Laboratory’s evaluation, where a co-pilot (human-guided) approach yielded better satisfaction and slightly improved output quality
agentlaboratory.github.io
agentlaboratory.github.io
. We anticipate similar benefits by involving the user to the extent they desire.

Technical Feasibility and APIs Research Summary

To ensure we have a clear path to implementation, here is a summary of the APIs, frameworks, and resources identified and how they fit into the architecture:

ArXiv API for Literature – We will use arXiv’s open API for paper search and metadata. This requires constructing queries and parsing Atom XML results. The API returns all necessary info (title, abstract, authors, etc.)
info.arxiv.org
. We can use the arxiv.py Python package (by Lukas Schwab) for convenience
python.langchain.com
, which is also integrated into LangChain. This avoids dealing with XML manually and gives us Python objects or JSON. No API key is required for arXiv; it’s public. We just must respect reasonable call rates. Example usage in code might be:

import arxiv  
results = arxiv.Search(query="quantum key distribution", max_results=5).results()  
for paper in results:  
    print(paper.title, paper.summary)  


This would give us the top 5 papers’ titles and summaries (abstracts) 
info.arxiv.org
.

OpenAlex API (Future extension) – OpenAlex is a broader academic index covering 250M works
openalex.org
. It offers a REST API with no auth and high rate limits
docs.openalex.org
. We might not use it in the MVP due to time, but it’s worth noting as a way to get papers outside arXiv (including those behind paywalls, by providing links to open access versions if available). It can also provide citation networks, which could enable features like finding which references are most important. For now, it remains a backup plan if arXiv search doesn’t yield enough.

CrossRef API – Another fallback to get DOI metadata or search by keywords. CrossRef is free and widely used for DOI lookup. For example, if our user input is a reference with a DOI, CrossRef API can fetch its metadata (title, author, etc.). This is tangential unless we deal with user-supplied references.

Semantic Scholar API – Could be used to get summaries or related papers, but it requires an API key (limited free tier). One interesting feature: given a paper’s title or DOI, it can return a summary and a list of cited or citing papers. This could be useful for automating a more comprehensive literature review (like citation chasing). However, for MVP we probably skip it.

LLM API/Model – We need a powerful language model for reasoning and writing. Options:

OpenAI’s GPT-4 via API (if we have access and it’s allowed for hackathon usage). GPT-4 would likely perform best at understanding complex text and generating high-quality academic writing. We’d have to manage the prompts and context length (the literature summaries + results must fit in input; GPT-4’s 8K or 32K context could handle multiple abstracts and some data easily). The downside is cost and dependency on internet.

Open-source LLM (e.g., Llama 2 70B or similar) running locally. This could be tricky to run in a limited environment and might not be as capable with reasoning as GPT-4, but avoids external API. Perhaps a smaller model fine-tuned for academic tasks could be used. Due to time, likely we lean on OpenAI if possible, or use a smaller model just for the hack demo.

Another approach: Cohere or Anthropic’s Claude (which has a 100k context window version – very handy for reading long papers). If we have access, Claude could ingest an entire paper PDF content if needed. But assume GPT-4 for concreteness.

LangChain Framework – This can greatly speed up development by providing abstractions for using LLMs with tools. LangChain would let us define the tools (ArxivAPIWrapper, PythonREPL, etc.) and then create an Agent (like an initialize_agent call with those tools and the LLM). It handles the loop of LLM deciding actions and parsing its own outputs to call tools. This is attractive to use in a hackathon to avoid writing our own parsing. That said, LangChain agents can sometimes be unpredictable, so we might use it for specific sub-tasks (like just for the Python execution part) and do simpler sequential prompting for others. It’s a design choice whether to go full LangChain vs custom orchestration. Given familiarity and time, we may mix and match (e.g., use LangChain for retrieval + summary, and custom code for the experiment plan execution).

Python Libraries for Simulation – as noted, NumPy, pandas, SymPy, etc., which we will install in the project environment. No external API needed for these since they run locally.

Matplotlib/Plotly – for generating any plots if needed. These could output images that our web UI can display (with <img> tags referencing a static file or base64 data). Not essential but nice for future.

Django (Backend) – will serve the pages and possibly provide endpoints: one for starting the process, and others for polling status or streaming results. We may use Django Channels or simply AJAX polling for updates. If time is short, even a log panel that updates is fine. The architecture could also be simplified to a single-thread process (the UI sends request, waits for response) but that might make the browser timeout if it’s too slow. So probably better to have asynchronous tasks. Python’s asyncio or threading can be used, or a task queue (Celery) if we want to be robust. For a 36-hour project, simpler async with callbacks might do.

Front-End – Could be simple HTML/JS with some dynamic behavior. Even just periodically fetching an API endpoint for the latest status in JSON. If comfortable, one could use React or similar to manage state. But templating and minimal JS might suffice given the complexity is mostly backend. We should ensure it’s clean and readable (maybe a bootstrap CSS for quick styling).

Citation Management – We have to store the references (likely in a list) when we pull them from arXiv. We’ll number them in the order we add them. If the user adds a paper or has references, those might be included too. We should ensure each reference has enough info:

If from arXiv: we have title, authors, year (from published date), and arXiv ID/URL. We can format like “[1] Author et al. (2023). Title. arXiv:ID.”

If from user’s own paper: maybe they had a bibliography; we might simply carry those over or not use them if they overlap with what we found.
The referencing doesn’t need an external API; it’s just how we assemble the final text. It’s more a formatting task.

With these resources, implementing the system is feasible. Many building blocks are readily available (APIs, libraries), and similar systems have been built which we can draw inspiration from. For example, the commercial tool SciSpace advertises an AI agent that can “search 280M papers, run systematic reviews, draft manuscripts, and even suggest journals”, effectively a full-stack research assistant
scispace.com
. This validates the demand and possibility of such a tool. Our project is essentially building an open-source or custom version tailored for a hackathon demo, focusing on core research workflow with arXiv + Python.

Future Extensions and Considerations

While the MVP focuses on core functionality, it’s worth noting potential future enhancements (some of which have been hinted above):

Broader Data Sources: Integrate more literature databases (IEEE, ACM, PubMed, etc.) through their APIs or via aggregators like CrossRef/OpenAlex. This would make the tool domain-agnostic truly – e.g., biomedical researchers could get PubMed papers. We’d have to handle API keys or rate limits for some.

Full-Text Comprehension: Currently, we rely on abstracts primarily. In future, we could fetch the full PDF from arXiv and use a PDF-to-text to allow the LLM to answer deeper questions (like details of methodology from other papers). With larger-context models (like Claude 100k), we could even feed entire papers for it to digest. Alternatively, implement a smarter chunking strategy to extract specific parts (introduction and conclusion are often most relevant for our needs).

Improved Experimentation: Include the ability to use external compute or specialized tools. For instance, if a research question requires training a machine learning model, integration with cloud ML platforms or using libraries like PyTorch could be considered. Or if it’s a chemistry question, integrate with a chemistry simulator (there are Python libraries for quantum chemistry, etc.). The architecture’s modular nature means we can add such tools as new capabilities down the line.

Collaboration and Feedback: Enable the system to take feedback from the user mid-way (as discussed) or even from other agents. For example, one could imagine a second LLM agent that reviews the draft for coherence or errors (similar to how human co-authors would). This is analogous to having a built-in reviewer that catches weaknesses and prompts the first agent to fix them. Agent Laboratory did something along these lines with “reviewer agents” to refine the output
agentlaboratory.github.io
.

UI enhancements: A richer interface with an embedded editor for the paper, the ability to chat with the agent (ask follow-up questions or clarifications at any time), and possibly a graph view of the literature (like showing how the found papers relate, akin to tools like Connected Papers or Litmaps). Also, supporting multiple projects, saving progress, etc., if this were to become a longer-term tool.

Evaluation and Accuracy: Implementing evaluation metrics for the experiments (already done in a simple way by looking at hypothesis result, but could formalize). Also, ensuring the final paper’s claims are correct – maybe cross-verify with sources or ensure no contradiction. This might involve symbolic reasoning or double-checking computations.

Scalability: If many users or large tasks, use better infrastructure. But for one researcher’s assistant, local should be fine. We might eventually allow plugging in an API key so the heavy LLM calls can be done on a paid service, or let advanced users connect it to their own compute cluster for big simulations.

Finally, a consideration: ethical and quality implications. Autonomously generating research comes with the risk of errors. The tool should ideally warn that the outputs are drafts and need human verification. It accelerates work but doesn’t guarantee correctness or novelty – the human researcher is responsible for verifying and refining the results. In the academic context, transparency of AI assistance is also important (perhaps any AI-written content should be disclosed if going into a paper). Our system as an “automatic researcher” must be positioned as a helpful assistant, not an oracle. Keeping the user in the loop via the UX and providing traceability (citations, logs of what was done) helps ensure it’s used responsibly.

References (and Inspiration Sources)

ArXiv API Documentation – Describes how to query arXiv’s database for papers. Example: Using the query interface: http://export.arxiv.org/api/query?search_query=all:electron returns an Atom feed of results
info.arxiv.org
. The API returns metadata like title, summary (abstract), authors, and links (including PDF links) for each paper
info.arxiv.org
. This allows programmatic literature search.

LangChain Arxiv Tool – LangChain provides an ArxivAPIWrapper which uses the Python arxiv package to fetch top results’ summaries from arXiv. This is a convenient way to integrate literature search in an LLM workflow
python.langchain.com
.

Agent Laboratory (2023) – An academic project demonstrating an LLM-driven research assistant. It divides the research process into three phases: Literature Review, Experimentation, and Report Writing, with specialized agents for each
agentlaboratory.github.io
. It integrates external tools like arXiv (for papers), Python (for running experiments), and LaTeX (for report formatting) into the workflow
agentlaboratory.github.io
. This project inspired parts of our design (e.g., using distinct phases and multi-agent collaboration). It showed that an autonomous agent can indeed generate research papers based on a human’s initial idea, though with some quality gaps
agentlaboratory.github.io
.

SciSpace AI Research Assistant (2023) – A commercial platform advertising an AI “co-scientist”. It claims to link 150+ tools and 30+ databases to handle everything from literature review to data analysis and manuscript drafting
scispace.com
. For example, it can “search 280M papers, run systematic reviews, draft manuscripts & match journals” in one system
scispace.com
. This indicates the viability and demand of an integrated research assistant. Our project targets similar capabilities on a smaller scale (open tools for a personal research companion).

Elicit by Ought – An AI research assistant focused on literature. It can search a vast paper database, provide summaries, and even answer questions by finding relevant excerpts. It demonstrates the power of using AI for literature review: “Use AI to search, summarize, extract data from, and chat with over 125 million papers.”
elicit.com
. We leverage the same idea of augmenting the LLM with a database of papers to ground its answers.

HuggingGPT (Shen et al. 2023) – A framework where an LLM orchestrates various expert models to solve complex tasks. The core idea: the LLM acts as an orchestrator, delegating tasks to the best-suited tool/model
medium.com
. In our context, the LLM directs tools like search and code execution. This concept underpins our agentic architecture design.

OpenAlex – OpenAlex is an open index of academic papers (replacement for Microsoft Academic). It provides a REST API with no auth (up to 100k calls/day) to access metadata of 250M works
docs.openalex.org
. We note this as a future expansion to cover more fields and ensure the assistant can find non-arXiv literature (e.g., social science or humanities research). OpenAlex’s data can also help in finding connections between works (citations, authors, etc.), enriching the assistant’s understanding of the research landscape.

৮ (Additional) The numbering of references in this list is for clarity in this report; in the actual generated paper, sources from the literature search would be cited and listed according to the chosen citation style.