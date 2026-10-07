Copyright © HallResearch.ai. Some rights reserved.

Licensed under CC BY 4.0. You may share and adapt this material with attribution to HallResearch.ai.

## Example AI System Card

`*` = required for all system cards

(if applicable) = include when the system has that feature, artifact, or evidence

### I. System Identity, Purpose, and Governance

#### Title / system name *
State the official name of the system.

#### System summary and organizational purpose *
Summarize what the system does and why it exists.

#### Authors, owners, stakeholders, and contact information *
List the people or teams responsible for building, owning, reviewing, or supporting the system with contact information.

#### Version, date, and revision history *
Record the current version, document date, and major changes over time. For important, high-risk, or systems with planned maintenance, include a revision table. 

#### Approval / review status and governance functions *
State the current review status and identify relevant governance, legal, risk, or compliance functions.

#### Human-in-the-loop (HITL) roles and interventions
Explain where people review, approve, correct, escalate, or override system behavior.

#### Privacy impact assessment
Summarize any privacy review, key findings, and resulting controls.

#### Vendor documentation and attestations
List relevant vendor-provided documentation, assurances, or attestations relied on by the system.

#### Summary of content moderation
Briefly discuss any automated or manual content moderation that is in place for the system. 

#### Nutrition or consumer label
Attach any data nutrition labels or other consumer-facing labeling. 

### II. Intended Use, Users, and Operational Scope

#### Intended users / stakeholders *
Identify the users, affected parties, and other relevant stakeholders.

#### Benefits and business justification *
Explain the expected value, benefit, or business need the system addresses.

#### Out-of-scope or prohibited uses *
List uses that are not intended, allowed, or safe.

#### Additional or secondary uses
Describe any other planned or observed uses beyond the primary one.

#### Deployment timeline and lifecycle plans
Summarize key lifecycle stages, milestones, or planned changes.

#### Operating environment *
Describe where, how, and under what conditions the system is used.

#### Assumptions and limitations *
All AI systems have assumptions and limitations. State the main assumptions, constraints, and known limits on system use or performance. 

### III. System Design and Operation

#### High-level system overview *
Describe the system’s main functions, stages, and outputs at a glance.

#### Architecture and component diagram *
Provide a diagram showing the main components and how they interact.

#### Component inventory *
List all material system components and their roles.

- **Data preprocessing** (if applicable)

  Provide a short description of any ETL, data cleaning, annotation, labeling, or other preprocessing.
- **Data resources**:
  - **Training, validation, or testing data** (if applicable)
    
    Describe any data used for training and testing; include any relevant benchmark datasets.
  - **Knowledge bases or grounding sources** (if applicable)
    
    Identify the knowledge sources used to ground system behavior.  
- **Vendor models or APIs** (if applicable)
  
  Briefly identify each vendor-provided model, service, or API used.
- **Internally developed models** (if applicable)
  
  Briefly identify each internally built model and its role.
- **Prompt or orchestration layers** (if applicable)
  
  Describe any prompting, routing, planning, or orchestration logic.
- **Retrieval infrastructure** (if applicable)
  
  Describe any retrieval layer used to find or rank information.
- **Business rules, guardrails, or filters** (if applicable)
  
  Describe any rules, thresholds, filters, or policy logic applied.
- **Tool-use or action components** (if applicable)
  
  Describe any tools, actions, or external system calls the system can trigger.

For each material component, also document:
- **Software stack and version**
  
  Note the relevant software, platform, or API version.
- **Inputs and outputs**
  
  Name the main inputs received and outputs produced.
- **Key settings or parameters**
  
  Note important settings, thresholds, or configurable parameters.

#### Upstream and downstream dependencies
Identify the systems, services, data sources, and processes this system depends on or affects.

### IV. Evaluation, Testing, and Validation

#### Performance metrics and results *
Report the main metrics used and the most important results.

#### Results across relevant segments, user groups, or subpopulations
Summarize performance differences across relevant groups, segments, or contexts.

#### Adversarial testing
Describe any testing for misuse, evasion, prompt attacks, or other adversarial behavior.

#### Visualizations / labeled plots *
Include clearly labeled figures that help explain evaluation results.

#### Testing remediation steps (if applicable)
Describe any fixes, mitigations, or follow-up actions taken in response to test findings.

#### Discussion of unexpected testing results
Note any surprising, inconsistent, or unexplained evaluation outcomes.

### V. Deployment, Monitoring, and Change Control

#### Monitoring plans and mechanisms *
Describe how system performance, safety, and reliability are monitored over time.

#### Change management and version control
Explain how changes are documented, reviewed, approved, and tracked.

#### Incident response plans
Summarize how incidents are detected, escalated, investigated, and resolved.

#### Appeals, overrides, and fallback procedures
Describe how decisions can be challenged, overridden, or safely backed up.

#### Maintenance expectations *
State how the system is maintained, updated, and periodically reviewed.

#### Audit plans and mechanisms
Describe planned audits, review triggers, and evidence retained for oversight.

### VI. Transparency and User Understanding

#### Transparency and usability features *
Describe features that help users understand, question, or appropriately use the system.

#### Example walkthrough of a real input *
Show step by step how the system handles a representative input.

#### Explanation of system outputs or decisions *
Explain what the outputs mean and how they should be interpreted.

### References and Supporting Artifacts *
List supporting documents, links, reports, model cards, evaluations, or other evidence.
