---
id: 002
title: Intermediate Level Implementation Plan
stage: plan
date: 2025-12-30
surface: agent
model: claude-sonnet-4-5
feature: intermediate-features
branch: 001-intermediate-features
user: system
command: /sp.plan
labels: ["planning", "architecture", "intermediate-level", "implementation-design"]
links:
  spec: specs/001-intermediate-features/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/001-intermediate-features/plan.md
  - specs/001-intermediate-features/research.md
  - specs/001-intermediate-features/data-model.md
  - specs/001-intermediate-features/quickstart.md
  - specs/001-intermediate-features/contracts/cli-operations.md
tests:
  - N/A
---

## Prompt

Plan the implementation for the INTERMEDIATE level of the Todo application,
based strictly on the approved specification.

- Extend the task data model to include priority, tags/categories, and optional due dates
- Implement priority assignment and tag/category management for tasks
- Add search functionality across task titles and descriptions
- Implement filtering by status, priority, and due date
- Implement sorting by due date, priority, and alphabetical order (A–Z)

Ensure changes are incremental, backward-compatible with the BASIC level,
and independently testable.

## Response snapshot

Created comprehensive implementation plan for Intermediate Level with complete Phase 0 (Research) and Phase 1 (Design & Contracts) artifacts:

**Plan.md Summary**:
- Technical approach: Extend Task entity with 3 new attributes (priority, tags, due_date), enhance TaskManager with search/filter/sort methods, update CLI menu
- Technology stack: Python 3.13+, standard library only, no external dependencies
- Architecture: Maintains existing domain-driven structure (models/services/CLI separation)
- Constitutional compliance: All Phase II requirements met, no violations

**Research.md** (8 key decisions):
1. Python standard library only - no external dependencies
2. String-based priority with validation (high/medium/low)
3. Tags as list of lowercase strings with normalization
4. Due dates as datetime.date objects in ISO format
5. Case-insensitive substring search with `in` operator
6. Separate filter methods with AND logic
7. Stable sort using Python sorted() with custom keys
8. Backward compatibility via default attribute values

**Data-model.md**:
- Enhanced Task entity with 7 attributes (4 existing + 3 new)
- Validation rules for priority, tags, due_date
- No state transitions (user-driven changes only)
- Performance characteristics: All operations <1s for 1000 tasks
- Example instances showing all attribute combinations

**CLI-operations.md** (9 operations):
- Extended Basic Level operations (Add, View, Update with priority/tag prompts)
- New operations: Search (6), Filter (7), Sort (8), Exit renumbered to (9)
- Detailed input/output contracts for each operation
- Error handling specifications
- Display format conventions
- Filter/sort state management patterns

**Quickstart.md**:
- 3-phase implementation roadmap (Task model → TaskManager → CLI)
- Step-by-step code samples for all changes
- Testing checklist (5 user stories + backward compatibility)
- Performance validation criteria
- Troubleshooting guide

All artifacts ready for `/sp.tasks` generation.

## Outcome

- ✅ Impact: Complete architectural design for Intermediate Level enabling incremental implementation
- 🧪 Tests: Testing checklist provided (manual scenarios for 5 user stories)
- 📁 Files: plan.md, research.md, data-model.md, quickstart.md, contracts/cli-operations.md
- 🔁 Next prompts: `/sp.tasks` to generate task breakdown, then begin implementation starting with P1 (priorities)
- 🧠 Reflection: Design maintains architectural integrity while enabling evolutionary path to Advanced Level (due dates ready for time/recurrence features)

## Evaluation notes (flywheel)

- Failure modes observed: None - all constitutional gates passed on first check
- Graders run and results (PASS/FAIL): Constitution Check - PASS (all Phase II requirements met)
- Prompt variant (if applicable): Standard planning workflow with research/design/contracts phases
- Next experiment (smallest change to try): Generate tasks.md and validate task breakdown aligns with independent user story delivery model
