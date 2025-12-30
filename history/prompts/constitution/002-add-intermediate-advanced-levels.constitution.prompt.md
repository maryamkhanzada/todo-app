---
id: 002
title: Add Intermediate and Advanced Levels to Constitution
stage: constitution
date: 2025-12-30
surface: agent
model: claude-sonnet-4-5
feature: none
branch: main
user: system
command: /sp.constitution
labels: ["constitution", "evolution", "phase-expansion"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
  - N/A
---

## Prompt

 Overview
This Constitution defines the evolutionary stages of the Todo application.
The **Basic level is already completed and stable**.
This document specifies the **Intermediate** and **Advanced** levels only.

Each level builds incrementally on the previous one and must remain
independently testable and stable.

---

## Intermediate Level
### Organization & Usability

The Intermediate level focuses on improving task organization and overall usability
to make the application more polished and practical.

### Capabilities

The system SHALL provide:

- **Task Priorities**
  - Fixed priority levels: `high`, `medium`, `low`
- **Tags / Categories**
  - Optional labels such as `work`, `home`, `personal`
- **Search**
  - Keyword-based search across task titles and descriptions
- **Filtering**
  - By completion status (`completed`, `pending`)
  - By priority level
  - By due date
- **Sorting**
  - By due date
  - By priority
  - Alphabetical order (A–Z)

### Guarantees

- All features MUST build upon existing Basic-level functionality
- Behavior MUST remain deterministic and user-driven
- No intelligent automation or notifications are introduced at this level
- UI styling and persistence are out of scope

---

## Advanced Level
### Intelligent Features

The Advanced level introduces time-aware and intelligent task management features.

### Capabilities

The system SHALL provide:

- **Recurring Tasks**
  - Support for repeating tasks (e.g., daily, weekly, custom intervals)
  - Completing a recurring task MUST automatically schedule the next occurrence
- **Due Dates**
  - Tasks may include both date and time
- **Reminders**
  - Time-based

## Response snapshot

Constitution successfully amended from version 1.0.0 to 1.1.0.

Key changes:
1. Renamed Principle V from "Phase I Scope Constraints" to "Phase I - Basic Level (In-Memory CLI Foundation)" and marked Phase I as complete and stable
2. Added Principle XI: "Phase II - Intermediate Level (Organization & Usability)" with capabilities for priorities, tags, search, filtering, and sorting
3. Added Principle XII: "Phase III - Advanced Level (Intelligent Features)" with capabilities for recurring tasks, due dates, and reminders
4. Updated Principle X "Success Definition" to include generic phase completion criteria

All template validations passed:
- .specify/templates/plan-template.md supports multi-phase validation
- .specify/templates/spec-template.md aligns with phase-based requirements
- .specify/templates/tasks-template.md supports incremental delivery

Version bump rationale: MINOR version (1.0.0 → 1.1.0) because new principles were added expanding the evolutionary roadmap without breaking existing governance.

## Outcome

- ✅ Impact: Constitution expanded to define Intermediate (Phase II) and Advanced (Phase III) evolutionary levels with clear capabilities and guarantees
- 🧪 Tests: N/A - constitution is a governance document
- 📁 Files: Updated .specify/memory/constitution.md (v1.1.0)
- 🔁 Next prompts: Use /sp.specify or /sp.plan to create feature specifications for Intermediate or Advanced level capabilities
- 🧠 Reflection: Clear phase separation enables incremental feature development while maintaining architectural integrity and backward compatibility

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): Template alignment validation - PASS
- Prompt variant (if applicable): Standard constitution amendment workflow
- Next experiment (smallest change to try): Begin Phase II (Intermediate) specification with priority feature as first increment
