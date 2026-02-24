# Progress Service Tasks
Feature ID: 3-progress-service
Branch: 3-progress-service

## Phase 1: Project Setup
- [ ] T001 Create progress-service directory structure with FastAPI app in services/progress-service/app/main.py
- [ ] T002 [P] Add Dockerfile for progress-service in services/progress-service/Dockerfile
- [ ] T003 Add Dapr configuration yaml for progress-service in services/progress-service/dapr.yaml
- [ ] T004 [P] Configure Kafka pubsub component for progress topics in components/kafka-pubsub.yaml

## Phase 2: Foundational
- [X] T005 Implement Dapr state store model for StudentProgress in services/progress-service/models/student_progress.py
- [X] T006 [P] Create StruggleAlert model in services/progress-service/models/struggle_alert.py
- [X] T007 Setup Kafka event consumer using Dapr in services/progress-service/app/event_consumer.py
- [X] T008 Implement health endpoint in services/progress-service/app/main.py

## Phase 3: US1 - Student Progress Calculation (Scenario 1, FR1)
- [ ] T009 [US1] Implement mastery score calculation function in services/progress-service/services/mastery_calculator.py using Article VI.04 weights
- [ ] T010 [P] [US1] Update event handler to calculate mastery on exercise/quiz/code events in services/progress-service/app/event_consumer.py
- [ ] T011 [US1] Store mastery score in Dapr state store from event handler
- [ ] T012 [US1] Add GET /progress/{student_id} endpoint in services/progress-service/app/main.py

## Phase 4: US2 - Struggle Detection Low Completion (Scenario 2, FR2)
- [ ] T013 [P] [US2] Implement completion rate calculation over 7 days in services/progress-service/services/struggle_detector.py
- [ ] T014 [US2] Add alert trigger for <50% completion in event handler services/progress-service/app/event_consumer.py
- [ ] T015 [US2] Publish struggle.detected event via Dapr pub/sub

## Phase 5: US3 - Repeated Failures (Scenario 3, FR3)
- [ ] T016 [P] [US3] Track failures per topic in state store update logic
- [ ] T017 [US3] Trigger alert after 3+ failures on topic in services/progress-service/services/struggle_detector.py

## Phase 6: US4 - Consecutive Low Scores (Scenario 4, FR4)
- [ ] T018 [P] [US4] Track consecutive low scores in state
- [ ] T019 [US4] Trigger alert after 3 low scores

## Phase 7: Additional FRs and API
- [ ] T020 [P] Implement FR5 event processing latency checks
- [ ] T021 GET /struggles endpoint for teacher dashboard
- [ ] T022 [P] Add logging and metrics for observability

## Phase 8: Polish & Verification
- [ ] T023 Add unit tests for mastery calculator
- [ ] T024 Integration tests for event processing
- [ ] T025 Update verify.py to check progress-service health
- [ ] T026 Deploy and verify full service

Total tasks: 26
Parallel opportunities: T002, T004, T006, T010, T013, T016, T018, T020, T022
MVP: Phases 1-3 (basic progress calculation)
