<div align="center">

# High-Functioning Prompting

### A practical framework for AI-assisted knowledge work

**Research · Analysis · Writing · Software Work · Knowledge Management**

<br>

[![Format](https://img.shields.io/badge/format-GitHub%20Markdown-24292f?style=flat-square)](#)
[![Templates](https://img.shields.io/badge/prompt%20templates-12-1f6b62?style=flat-square)](#reusable-prompt-patterns)
[![Focus](https://img.shields.io/badge/focus-workflow%20design-bf6d42?style=flat-square)](#prompting-as-workflow-design)
[![Use](https://img.shields.io/badge/use-adapt%20%26%20reuse-59636e?style=flat-square)](#building-a-prompt-library)

<br>

> **Core pattern**
>
> **Context → operation → standards → constraints → deliverable → verification → repackaging**

</div>

---

## Contents

- [Prompting as workflow design](#prompting-as-workflow-design)
- [The recurring method](#the-recurring-method)
- [What makes these prompts effective](#what-makes-these-prompts-effective)
- [Reusable prompt patterns](#reusable-prompt-patterns)
- [Building a prompt library](#building-a-prompt-library)
- [Responsible use](#responsible-use)

---

## Prompting as workflow design

High-functioning prompts do more than request an answer. They establish the working corpus, name the intellectual operation, define the evidentiary standard, specify the form of the deliverable, and create an explicit path for verification and revision.

The most productive use of conversational AI is therefore iterative. A first response is often a **diagnostic object**: it reveals hidden assumptions, missing constraints, weak categories, and opportunities for refinement. The prompt evolves as the task becomes better understood.

> [!NOTE]
> The aim is not to produce more text. It is to make each stage of intellectual work visible, testable, and reusable.

---

## The recurring method

| Step | Practice | What it accomplishes |
|---:|---|---|
| **1** | **Create a bounded world** | Supply the relevant files, links, examples, prior decisions, definitions, and constraints. Ask the model to map the material before narrowing the task. |
| **2** | **Name the operation** | Use precise verbs: *audit, distill, classify, compare, verify, revise, map, extract, merge,* or *repackage*. Different verbs imply different standards of work. |
| **3** | **Provide house rules** | State the criteria that govern judgment. Explicit rules about evidence, tone, naming, uncertainty, and inclusion are more useful than generic requests for quality. |
| **4** | **Explain the downstream use** | Describe what will happen after the response. A result intended for a spreadsheet, public website, meeting, or text-to-speech system should be shaped differently. |
| **5** | **Compress in stages** | Move material through useful representations: source corpus, analysis, decision, table, link list, and final artifact. Compression should serve the next action. |
| **6** | **Use iteration diagnostically** | Treat follow-up prompts as specification work. Identify the habit causing a weak result and revise the underlying instruction, not only one sentence. |
| **7** | **Separate generation from review** | Ask for a dedicated second pass that looks for unsupported claims, duplicated records, inconsistency, stale sources, and fluent but weak reasoning. |
| **8** | **Repackage for action** | Once the analysis is accepted, request only the operational form needed: HTML, Markdown, TSV, a checklist, a clean table, or a list of links. |

---

## What makes these prompts effective

> [!TIP]
> **Editorial authority replaces theatrical role-play.**  
> Instead of asking the model to impersonate an expert, supply the real conditions of expertise: a source corpus, decision rules, institutional context, evidentiary standards, and consequences of error.

### Two complementary movements

| Movement | Purpose | Typical requests |
|---|---|---|
| **Down-leveling** | Break a difficult task into inspectable parts. | Extract fields, create records, separate stages, list tests, identify cases. |
| **Up-leveling** | Determine the larger pattern or architecture. | Find themes, define categories, map an ontology, identify an intervention, redesign a workflow. |

Strong knowledge work moves repeatedly between these levels. Decomposition makes the task manageable; abstraction makes the result meaningful.

---

# Reusable prompt patterns

These templates are designed to be adapted. Replace bracketed text with project-specific information, examples, criteria, and constraints.

> [!IMPORTANT]
> GitHub collapses each template below using standard `<details>` elements. Open only the prompt you need, then copy the text from its code block.

---

<details>
<summary><strong>1. Corpus Distillation</strong></summary>

<br>

**Best used when:** several documents, links, or records need to be understood as one system.

```text
Distill everything you can determine from the materials below. Begin by identifying the overall structure, purpose, principal components, and implicit assumptions. Then explain the most important details, tensions, gaps, and opportunities. Do not merely summarize each item in sequence; reconstruct the larger system they collectively form.

Materials:
[Insert links, files, or pasted text.]
```

</details>

---

<details>
<summary><strong>2. Evidence-Constrained Evaluation</strong></summary>

<br>

**Best used when:** a decision must distinguish evidence from inference and uncertainty.

```text
Evaluate this material according to the following decision criteria:

[Insert criteria or house rules.]

Distinguish clearly among:
- what the evidence establishes;
- what is probable but uncertain;
- what would be an unsupported inference;
- what additional evidence would change the judgment.

Give the preferred determination, explain the decisive reason, and provide the exact fields or language needed for implementation.
```

</details>

---

<details>
<summary><strong>3. Comprehensive Audit</strong></summary>

<br>

**Best used when:** a product needs a systematic second pass for errors, omissions, and drift.

```text
Run a systematic audit of the material below. Assume that earlier reviews may have missed something.

Check for:
- factual or evidentiary errors;
- internal inconsistencies;
- duplicate or overlapping entries;
- naming and terminology drift;
- broken, stale, or inappropriate links;
- formatting problems;
- unsupported or overstated claims;
- omissions that materially weaken the product.

Verify questionable points against authoritative or primary sources where possible. Report what you found, explain why it matters, and provide the corrected version. Do not invent problems merely to make the audit appear productive.
```

</details>

---

<details>
<summary><strong>4. Public-Facing Product Review</strong></summary>

<br>

**Best used when:** an internal draft must become intelligible and trustworthy to an outside reader.

```text
Review this as though it were a public-facing product rather than an internal draft. Evaluate its usefulness, navigability, intellectual coherence, transparency, tone, accessibility, and likely points of misunderstanding. Preserve methodological candor without exposing internal working history that would not benefit the public.

Recommend concrete revisions and then implement them in the requested format.
```

</details>

---

<details>
<summary><strong>5. Classification and Triage</strong></summary>

<br>

**Best used when:** a collection of cases must be categorized consistently and conservatively.

```text
Process each item according to these categories:

[Insert categories.]

Apply the categories conservatively and consistently. For each item, provide:
- the preferred classification;
- the evidence supporting it;
- any duplication or relationship to existing records;
- the action to take;
- a concise rationale.

Keep uncertainty visible. Do not force an item into a category when the evidence is insufficient.
```

</details>

---

<details>
<summary><strong>6. Architecture and Ontology Review</strong></summary>

<br>

**Best used when:** categories have accumulated and the underlying conceptual structure needs revision.

```text
Step back from the individual entries and determine what conceptual structure is emerging. Identify the recurring classes, boundary problems, inconsistent levels of abstraction, and categories that are doing too much work.

Propose an ontology that is broad enough to be reusable but precise enough to guide actual classification. Explain where existing terms should be merged, divided, renamed, or subordinated.
```

</details>

---

<details>
<summary><strong>7. Source Verification</strong></summary>

<br>

**Best used when:** factual claims and citations must be checked against reliable sources.

```text
Verify every important factual claim, date, title, institutional name, and citation in this draft. Prefer primary or authoritative sources. Confirm that each source actually supports the claim attached to it and distinguish the date of an event from the date of publication.

Flag anything you cannot verify. Do not silently fill gaps with plausible language.
```

</details>

---

<details>
<summary><strong>8. Exact Operational Output</strong></summary>

<br>

**Best used when:** the analysis is settled and only the final usable format remains.

```text
The underlying analysis has been accepted. Repackage it for the following use:

Purpose:
[Explain what will be done with it.]

Output format:
[HTML, PDF, raw Markdown, TSV rows, bare URLs, table, and so forth.]

Include:
[Required fields.]

Exclude:
[Anything that would obstruct the workflow.]

Preserve:
[Accepted wording, quotations, hierarchy, citations, or metadata.]

Do not add explanatory material outside the requested format.
```

</details>

---

<details>
<summary><strong>9. Iterative Style Correction</strong></summary>

<br>

**Best used when:** a draft repeatedly exhibits the same stylistic habit.

```text
Revise the draft while preserving its substantive argument. The current version repeatedly falls into this stylistic habit:

[Describe or quote the unwanted pattern.]

Correct the generative tendency throughout the piece rather than repairing only the examples identified. Use the following prose principles:

[Insert preferred principles.]

After revising, reread the whole piece for places where the old habit remains.
```

</details>

---

<details>
<summary><strong>10. Continuation by Established Pattern</strong></summary>

<br>

**Best used when:** new material should follow a workflow already established in prior examples.

```text
Continue using the method, fields, house style, and output structure established in the preceding examples. Treat those examples as the template, but adapt the substance to the new material rather than copying language mechanically.

New material:
[Insert material.]

Changes for this batch:
[Insert any changed dates, limits, fields, or exceptions.]
```

</details>

---

<details>
<summary><strong>11. Adversarial Second Pass</strong></summary>

<br>

**Best used when:** a polished answer may be concealing weak reasoning or unsupported confidence.

```text
Review the previous answer as a skeptical editor. Look especially for anything that sounds convincing because it is smoothly written rather than because it is well supported.

Check:
- whether the conclusion follows from the evidence;
- whether alternative interpretations were considered;
- whether any source was misread;
- whether categories were applied consistently;
- whether inconvenient evidence was omitted;
- whether uncertainty was flattened.

Revise the answer wherever the second pass changes the judgment.
```

</details>

---

<details>
<summary><strong>12. Research-to-Artifact Workflow</strong></summary>

<br>

**Best used when:** a task should move from source inspection through research and verification to a finished deliverable.

```text
Carry this task through all necessary stages:

1. inspect and organize the source material;
2. research missing or unstable information;
3. formulate the analysis;
4. verify factual and bibliographic details;
5. convert the result into the requested artifact;
6. inspect the finished artifact for usability and presentation problems.

The final product should be self-contained and ready for direct use. Include a concise account of any limitations or unresolved uncertainties.
```

</details>

---

## Building a prompt library

A durable prompt library should document **working methods**, not collect decontextualized incantations. Each record should explain when the prompt is useful, what information it requires, how its output should be checked, and how the prompt changed after real use.

| Field | Purpose |
|---|---|
| **Prompt name** | A stable, descriptive title. |
| **Intended operation** | Audit, distillation, classification, revision, research, or another cognitive task. |
| **Best used when** | The conditions under which the prompt performs well. |
| **Required context** | Files, examples, prior rules, definitions, or source corpus. |
| **Prompt template** | The reusable instruction language. |
| **Variables** | Dates, limits, categories, formats, and project-specific substitutions. |
| **Expected output** | The shape and level of detail of the deliverable. |
| **Verification step** | How the result should be tested or reviewed. |
| **Failure modes** | Typical ways a model misinterprets or weakens the task. |
| **Revision history** | Changes made after actual use. |
| **Example application** | A real, anonymized, or synthetic case. |
| **Tool notes** | Whether browsing, code execution, files, databases, or other tools are required. |

### Suggested record structure

```yaml
prompt_name: ""
intended_operation: ""
best_used_when: ""
required_context: []
prompt_template: |
  ...
variables: []
expected_output: ""
verification_step: ""
failure_modes: []
revision_history: []
example_application: ""
tool_notes: []
```

---

## Responsible use

<table>
<tr>
<td width="50%" valign="top">

### Keep uncertainty visible

Require the model to distinguish evidence, inference, assumptions, and unresolved questions. Fluent prose should never substitute for support.

</td>
<td width="50%" valign="top">

### Use the right tool

Conversational AI is not always the appropriate instrument. Search, databases, calculators, code environments, editors, and domain tools may be better suited to part of the task.

</td>
</tr>
<tr>
<td width="50%" valign="top">

### Protect sensitive information

Apply data minimization, anonymization, access controls, disclosure policies, and secrets management before sharing material with any AI system.

</td>
<td width="50%" valign="top">

### Retain human approval

Separate diagnosis from execution when changes are consequential. Ask the model to identify proposed actions before authorizing edits, submissions, or publication.

</td>
</tr>
</table>

> [!WARNING]
> A high-functioning prompt is not judged by how impressive it sounds. It is judged by whether it makes the work more transparent, reproducible, verifiable, and useful.

---

<div align="center">

### Adapt, test, revise

This guide is designed for adaptation, teaching, and internal workflow development. AI systems and tool capabilities change over time; verify important outputs and revise templates to match the risks of the task.

<br>

**High-Functioning Prompting for AI-Assisted Knowledge Work**

</div>
