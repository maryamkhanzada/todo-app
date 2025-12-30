---
id: 002
title: Advanced Level Implementation Plan
stage: plan
date: 2025-12-30
surface: agent
model: claude-sonnet-4-5
feature: advanced-features
branch: 002-advanced-features
user: system
command: /sp.plan
labels: ["planning", "architecture", "advanced-level", "recurring-tasks", "reminders", "time-aware"]
links:
  spec: specs/002-advanced-features/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/002-advanced-features/plan.md
  - specs/002-advanced-features/research.md
  - specs/002-advanced-features/data-model.md
  - specs/002-advanced-features/contracts/cli-operations.md
  - specs/002-advanced-features/quickstart.md
tests:
  - N/A (planning phase)
---

## Prompt

Plan the implementation for the ADVANCED level of the Todo application, based strictly on the approved specification.

- Extend the task data model to support recurring tasks and due dates with time
- Implement recurrence logic for tasks with automatic rescheduling
  - Support daily, weekly, and custom intervals
- Add reminder scheduling and time-based notifications
  - Trigger notifications at or before task due time
- Update user interactions to allow creating, editing, and managing recurring tasks and reminders
- Ensure all features integrate seamlessly with existing Intermediate-level functionality and are independently testable

## Response snapshot

Generated comprehensive implementation plan with complete Phase 0 (Research) and Phase 1 (Data Model & Contracts) outputs.

**Plan Structure**:
- **Technical Context**: Python 3.13+, stdlib only, in-memory storage, CLI platform
- **Constitution Check**: All Phase III requirements satisfied, zero violations
- **Project Structure**: Extends `src/todo_app/` with new ReminderService and time utilities
- **Complexity Tracking**: No violations (empty section - all design aligns with constitution)

**Phase 0: Research (8 key decisions documented)**:
1. **Time Storage**: Hybrid approach (due_date + due_time + helper) for backward compatibility
2. **Recurrence Calc**: From original due date (prevents schedule drift)
3. **Reminder Thread**: 60s polling daemon thread (simple, adequate latency)
4. **Notifications**: Console output (zero dependencies)
5. **Data Storage**: Dicts/lists on Task (matches existing pattern)
6. **Thread Safety**: threading.Lock (correctness over performance)
7. **Timezone**: Local time only (single-user CLI context)
8. **Recurrence History**: parent_recurrence_id field (flat list consistency)

**Phase 1: Data Model & Contracts (4 new Task fields)**:
- `due_time: str | None` - HH:MM format, defaults "23:59"
- `recurrence: dict` - {"type": "none"|"daily"|"weekly"|"custom", "interval": int}
- `reminders: list[dict]` - Offset-based with sent tracking
- `parent_recurrence_id: int | None` - Links recurring occurrences

**New Service**: ReminderService with background thread for reminder checking

**CLI Operations**: Extended add/update/view/delete, new manage_recurrence and manage_reminders sub-menus

**Key Architecture Decisions**:
- Combined datetime via helper function (backward compatible)
- Recurrence from original due date (no schedule drift)
- 60-second reminder polling (adequate latency, simple)
- Console notifications (no external dependencies)
- Threading.Lock for thread safety (prevents race conditions)
- Local timezone only (no conversion complexity)

**Implementation Strategy**:
- **MVP**: Time-aware due dates (2-3 hours)
- **Milestone 2**: Recurring tasks (3-4 hours)
- **Milestone 3**: Reminders (3-4 hours)
- **Milestone 4**: Recurrence management (2-3 hours)
- **Total estimate**: 10-14 hours for complete Advanced Level

**Artifacts Created**:
1. `plan.md` (309 lines) - Main implementation plan with constitution check
2. `research.md` (437 lines) - 8 technical decisions with rationale and alternatives
3. `data-model.md` (374 lines) - Task extensions, validation rules, helper methods
4. `contracts/cli-operations.md` (526 lines) - CLI operation signatures and behaviors
5. `quickstart.md` (523 lines) - Developer guide with implementation order, patterns, pitfalls

## Outcome

- ✅ Impact: Complete implementation plan ready for task generation and coding
- 🧪 Tests: Manual test strategy defined in quickstart.md (no formal test framework per conventions)
- 📁 Files: plan.md, research.md, data-model.md, contracts/cli-operations.md, quickstart.md
- 🔁 Next prompts: `/sp.tasks` to generate detailed task breakdown for implementation
- 🧠 Reflection: Architecture prioritizes simplicity and backward compatibility. Key insight: hybrid time storage (date + time string) maintains compatibility while enabling precision. Recurrence calculation from original due date (not completion) prevents schedule drift - critical for user expectations. Background thread with 60s polling adequate for CLI use case (no need for complex timer management). All features extend existing patterns (no architectural changes), minimizing risk.

## Evaluation notes (flywheel)

- Failure modes observed: None - all decisions traced to specification requirements
- Graders run and results (PASS/FAIL): Constitution check - PASS (all Phase III requirements satisfied, zero violations)
- Prompt variant (if applicable): Standard planning workflow (Phase 0 research → Phase 1 data model/contracts)
- Next experiment (smallest change to try): Begin implementation with `/sp.tasks` to generate task breakdown, then `/sp.implement` for milestone-based delivery (MVP first: time-aware due dates)
