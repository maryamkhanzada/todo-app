---
description: "Task breakdown for Intermediate Level implementation"
---

# Tasks: Intermediate Level - Organization & Usability

**Input**: Design documents from `/specs/001-intermediate-features/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

**Tests**: Not requested in specification - no test tasks included

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/todo_app/` at repository root
- All changes extend existing modules: models/task.py, services/task_manager.py, cli/main.py

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Verify existing Basic Level foundation is ready for Intermediate Level changes

- [ ] T001 Verify Basic Level implementation is complete and working (run application, test CRUD operations)
- [ ] T002 Verify Python 3.13+ environment and UV package manager are available
- [ ] T003 Review existing codebase structure in src/todo_app/ (models, services, cli)

**Checkpoint**: Basic Level confirmed working - ready for Intermediate Level enhancements

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Extend Task model with new attributes that ALL user stories depend on

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T004 Add datetime import and VALID_PRIORITIES constant to src/todo_app/models/task.py
- [x] T005 Add priority, tags, and due_date parameters to Task.__init__() in src/todo_app/models/task.py
- [x] T006 Implement _validate_priority() class method in src/todo_app/models/task.py
- [x] T007 Update Task.__repr__() to include priority, tags, and due_date in src/todo_app/models/task.py
- [x] T008 Add parse_tags() static method to TaskManager in src/todo_app/services/task_manager.py
- [x] T009 Update TaskManager.add_task() signature to accept priority, tags, due_date in src/todo_app/services/task_manager.py
- [x] T010 Update TaskManager.update_task() signature to accept priority and tags in src/todo_app/services/task_manager.py

**Checkpoint**: Foundation ready - Task model extended, all user stories can now build on enhanced Task

---

## Phase 3: User Story 1 - Prioritize Tasks (Priority: P1) 🎯 MVP

**Goal**: Enable users to assign and update priority levels (high, medium, low) on tasks

**Independent Test**: Create tasks with different priorities, update priorities, verify display shows priority correctly, test invalid priority rejection

### Implementation for User Story 1

- [x] T011 [US1] Update CLI add_task handler to prompt for priority in src/todo_app/cli/main.py
- [x] T012 [US1] Add priority input validation and error handling in add_task handler in src/todo_app/cli/main.py
- [x] T013 [US1] Update CLI update_task handler to prompt for priority changes in src/todo_app/cli/main.py
- [x] T014 [US1] Add priority input validation in update_task handler in src/todo_app/cli/main.py
- [x] T015 [US1] Update CLI view_tasks handler to display priority for each task in src/todo_app/cli/main.py
- [x] T016 [US1] Format priority display as uppercase (HIGH, MEDIUM, LOW) in view_tasks in src/todo_app/cli/main.py

**Checkpoint**: At this point, User Story 1 (Prioritize Tasks) is fully functional and testable independently. Users can set priorities when adding tasks, change priorities when updating tasks, and see priorities in the task list. This is a viable MVP.

---

## Phase 4: User Story 2 - Organize with Tags (Priority: P2)

**Goal**: Enable users to add and manage multiple tags per task for categorization

**Independent Test**: Create tasks with single/multiple tags, update tags, verify display shows tags, test empty tags handling

### Implementation for User Story 2

- [x] T017 [US2] Update CLI add_task handler to prompt for tags (comma-separated) in src/todo_app/cli/main.py
- [x] T018 [US2] Parse tag input using TaskManager.parse_tags() in add_task handler in src/todo_app/cli/main.py
- [x] T019 [US2] Update CLI update_task handler to prompt for tag changes in src/todo_app/cli/main.py
- [x] T020 [US2] Parse tag input and handle tag updates in update_task handler in src/todo_app/cli/main.py
- [x] T021 [US2] Update CLI view_tasks handler to display tags for each task in src/todo_app/cli/main.py
- [x] T022 [US2] Format tags display as comma-separated list in brackets in view_tasks in src/todo_app/cli/main.py

**Checkpoint**: At this point, User Story 2 (Organize with Tags) is fully functional and testable independently. Users can add tags when creating tasks, modify tags when updating tasks, and see tags in the task list.

---

## Phase 5: User Story 3 - Search Tasks by Keyword (Priority: P3)

**Goal**: Enable users to search for tasks using keywords that match in title or description

**Independent Test**: Create tasks with various titles/descriptions, search for keywords, verify case-insensitive matching, test partial word matching, verify no results message

### Implementation for User Story 3

- [x] T023 [US3] Implement search_tasks(keyword) method in src/todo_app/services/task_manager.py
- [x] T024 [US3] Add case-insensitive substring matching logic in search_tasks in src/todo_app/services/task_manager.py
- [x] T025 [US3] Add empty keyword validation in search_tasks in src/todo_app/services/task_manager.py
- [x] T026 [US3] Add menu option 6 "Search Tasks" to main menu in src/todo_app/cli/main.py
- [x] T027 [US3] Implement search_tasks_handler() function in src/todo_app/cli/main.py
- [x] T028 [US3] Prompt user for keyword and call TaskManager.search_tasks() in search_tasks_handler in src/todo_app/cli/main.py
- [x] T029 [US3] Display search results with full task details in search_tasks_handler in src/todo_app/cli/main.py
- [x] T030 [US3] Handle no results case with "No tasks found matching '{keyword}'" message in src/todo_app/cli/main.py
- [x] T031 [US3] Handle empty keyword error with helpful message in search_tasks_handler in src/todo_app/cli/main.py

**Checkpoint**: At this point, User Story 3 (Search Tasks) is fully functional and testable independently. Users can search for tasks by keyword and see matching results.

---

## Phase 6: User Story 4 - Filter Tasks (Priority: P4)

**Goal**: Enable users to filter task list by completion status, priority level, or due date

**Independent Test**: Create tasks with various attributes, apply filters (status/priority/due date), verify filtered results, test clear filters, verify multiple filters use AND logic

### Implementation for User Story 4

- [x] T032 [US4] Implement filter_tasks(status, priority, due_date_op, due_date_value) method in src/todo_app/services/task_manager.py
- [x] T033 [US4] Add status filtering logic (completed/pending) in filter_tasks in src/todo_app/services/task_manager.py
- [x] T034 [US4] Add priority filtering logic in filter_tasks in src/todo_app/services/task_manager.py
- [x] T035 [US4] Add due date filtering logic (before/after/on) in filter_tasks in src/todo_app/services/task_manager.py
- [x] T036 [US4] Add menu option 7 "Filter Tasks" with sub-menu to main menu in src/todo_app/cli/main.py
- [x] T037 [US4] Implement filter_tasks_handler() function with sub-menu in src/todo_app/cli/main.py
- [x] T038 [US4] Add filter state tracking (active_filters dict) in main() or globally in src/todo_app/cli/main.py
- [x] T039 [US4] Implement filter by status option in filter_tasks_handler in src/todo_app/cli/main.py
- [x] T040 [US4] Implement filter by priority option in filter_tasks_handler in src/todo_app/cli/main.py
- [x] T041 [US4] Implement filter by due date option in filter_tasks_handler in src/todo_app/cli/main.py
- [x] T042 [US4] Implement clear filters option in filter_tasks_handler in src/todo_app/cli/main.py
- [x] T043 [US4] Update view_tasks handler to apply active filters when displaying tasks in src/todo_app/cli/main.py
- [x] T044 [US4] Display active filter indicator at bottom of task list in view_tasks in src/todo_app/cli/main.py
- [x] T045 [US4] Display filtered count vs total count in view_tasks in src/todo_app/cli/main.py

**Checkpoint**: At this point, User Story 4 (Filter Tasks) is fully functional and testable independently. Users can filter tasks by status, priority, or due date, and clear filters.

---

## Phase 7: User Story 5 - Sort Tasks (Priority: P5)

**Goal**: Enable users to sort task list by due date, priority, or alphabetically

**Independent Test**: Create tasks with various attributes, apply sorts (due date/priority/alphabetical), verify sort order, test tasks without due dates appear last, test stable sort

### Implementation for User Story 5

- [x] T046 [US5] Implement sort_tasks(sort_by) method in src/todo_app/services/task_manager.py
- [x] T047 [US5] Add due date sorting logic (None values last) in sort_tasks in src/todo_app/services/task_manager.py
- [x] T048 [US5] Add priority sorting logic (high > medium > low) in sort_tasks in src/todo_app/services/task_manager.py
- [x] T049 [US5] Add alphabetical sorting logic (A-Z, case-insensitive) in sort_tasks in src/todo_app/services/task_manager.py
- [x] T050 [US5] Add sort_by validation in sort_tasks in src/todo_app/services/task_manager.py
- [x] T051 [US5] Add menu option 8 "Sort Tasks" with sub-menu to main menu in src/todo_app/cli/main.py
- [x] T052 [US5] Implement sort_tasks_handler() function with sub-menu in src/todo_app/cli/main.py
- [x] T053 [US5] Add sort state tracking (active_sort variable) in main() or globally in src/todo_app/cli/main.py
- [x] T054 [US5] Implement sort by due date option in sort_tasks_handler in src/todo_app/cli/main.py
- [x] T055 [US5] Implement sort by priority option in sort_tasks_handler in src/todo_app/cli/main.py
- [x] T056 [US5] Implement sort alphabetically option in sort_tasks_handler in src/todo_app/cli/main.py
- [x] T057 [US5] Implement clear sort option in sort_tasks_handler in src/todo_app/cli/main.py
- [x] T058 [US5] Update view_tasks handler to apply active sort when displaying tasks in src/todo_app/cli/main.py
- [x] T059 [US5] Display active sort indicator at bottom of task list in view_tasks in src/todo_app/cli/main.py

**Checkpoint**: At this point, User Story 5 (Sort Tasks) is fully functional and testable independently. All Intermediate Level features are now complete.

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Final refinements and validation

- [x] T060 Update main menu to renumber Exit from option 6 to option 9 in src/todo_app/cli/main.py
- [x] T061 Test all Basic Level operations still work (Add, View, Update, Delete, Complete)
- [x] T062 Verify backward compatibility: existing tasks display with default priority=medium, tags=[], due_date=None
- [x] T063 Test combined filter + sort operations work correctly
- [x] T064 Test edge cases: empty searches, no filter matches, duplicate tags, invalid inputs
- [x] T065 Performance test with 100+ tasks: verify search/filter/sort complete in <1 second
- [x] T066 Review all error messages for clarity and helpfulness
- [x] T067 Final manual walkthrough of all 5 user stories

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phases 3-7)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed) or sequentially in priority order (P1 → P2 → P3 → P4 → P5)
- **Polish (Phase 8)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1 - Priorities)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2 - Tags)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 3 (P3 - Search)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 4 (P4 - Filter)**: Can start after Foundational (Phase 2) - No dependencies on other stories (though filtering by priority is more useful after US1)
- **User Story 5 (P5 - Sort)**: Can start after Foundational (Phase 2) - No dependencies on other stories (though sorting by priority is more useful after US1)

### Within Each User Story

- All tasks within a user story modify the same files (task.py, task_manager.py, main.py)
- Tasks should be completed sequentially within each user story
- Service layer tasks (TaskManager methods) should complete before CLI tasks
- CLI tasks may have dependencies (e.g., menu option before handler, handler before display)

### Parallel Opportunities

**Between User Stories** (if team capacity allows):
- After Phase 2 completes, ALL 5 user stories can start in parallel if different developers work on each
- Each story modifies the same files but in isolated sections (different methods/handlers)
- Merge conflicts can be resolved by combining changes from different stories

**Within Foundational Phase**:
- T004-T007 (Task model changes) must be sequential (same class)
- T008-T010 (TaskManager changes) must be sequential (same class)
- No parallel opportunities within Foundational phase

**Within User Stories**:
- Limited parallelization due to same-file modifications
- Service method can be written in parallel with CLI planning
- Display formatting (view updates) can be written in parallel with handler logic preparation

---

## Parallel Example: After Foundational Phase

```bash
# If you have 5 developers, launch all user stories in parallel after Phase 2:

Developer A: Phase 3 (US1 - Priorities)      - T011 to T016
Developer B: Phase 4 (US2 - Tags)            - T017 to T022
Developer C: Phase 5 (US3 - Search)          - T023 to T031
Developer D: Phase 6 (US4 - Filter)          - T032 to T045
Developer E: Phase 7 (US5 - Sort)            - T046 to T059

# Each developer works independently on their story
# Merge all changes together at the end
# Run Phase 8 (Polish) to test integration
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

**Fastest path to working Intermediate Level features:**

1. Complete Phase 1: Setup (T001-T003) - ~5 minutes
2. Complete Phase 2: Foundational (T004-T010) - ~30-45 minutes
3. Complete Phase 3: User Story 1 (T011-T016) - ~30-45 minutes
4. **STOP and VALIDATE**: Test priority features independently
5. Deploy/demo if ready

**Total MVP time**: ~90 minutes for basic priority management

### Incremental Delivery

**Recommended approach for staged rollout:**

1. **Sprint 1**: Setup + Foundational + US1 (Priorities) → Deploy MVP
2. **Sprint 2**: Add US2 (Tags) → Deploy with priorities + tags
3. **Sprint 3**: Add US3 (Search) → Deploy with search capability
4. **Sprint 4**: Add US4 (Filter) + US5 (Sort) → Deploy full Intermediate Level
5. **Sprint 5**: Polish (Phase 8) → Final validation and optimization

Each sprint adds value without breaking previous features.

### Parallel Team Strategy

**If you have multiple developers available:**

1. Team completes Setup + Foundational together (T001-T010)
2. Once Foundational is done:
   - Developer A: User Story 1 (T011-T016)
   - Developer B: User Story 2 (T017-T022)
   - Developer C: User Story 3 (T023-T031)
   - Developer D: User Stories 4 & 5 (T032-T059)
3. Merge all changes
4. Team completes Polish together (T060-T067)

**Timeline**: Can complete all Intermediate Level features in 1-2 days with parallel development.

---

## Notes

- **[P] tasks**: Different files or isolated sections, no dependencies - CAN run in parallel
- **[Story] label**: Maps task to specific user story for traceability and independent testing
- **File paths**: All tasks include exact file paths for clarity
- **Tests**: Not included because specification does not request testing framework
- **Backward compatibility**: Phase 2 ensures all new attributes have defaults
- Each user story is independently completable and testable
- Commit after each user story phase for clean incremental history
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same-method conflicts, cross-story dependencies that break independence

---

## Validation Checklist

Before marking implementation complete, verify:

- [ ] All 67 tasks completed
- [ ] All 5 user stories independently testable
- [ ] All Basic Level operations still work (backward compatibility)
- [ ] Priority validation rejects invalid values
- [ ] Tags parse and normalize correctly
- [ ] Search is case-insensitive with partial matching
- [ ] Filters use AND logic when combined
- [ ] Sorts are stable (preserve order for equal values)
- [ ] Performance: search/filter/sort <1s for 100+ tasks
- [ ] Error messages are clear and helpful
- [ ] Menu options 1-9 all work correctly
- [ ] Exit option renumbered to 9
