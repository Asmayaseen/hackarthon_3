# Feature Specification: Progress Service and Mastery Calculation

**Feature ID**: 3-progress-service
**Created**: 2026-01-20
**Status**: Specification Complete
**Branch**: 3-progress-service

## Overview

Build the Progress Service that calculates student mastery scores and detects struggle patterns across all LearnFlow AI agents. Implements Constitution Article VI (Mastery Calculation) and Article VI.05 (Struggle Detection).

**Key Features**:
- Mastery score calculation per Constitution Article VI.04 formula
- Struggle pattern detection (completion rate, repeated failures, low scores)
- Event-driven progress tracking from Kafka events
- Teacher dashboard data aggregation
- Dapr state store integration for persistence

---

## User Scenarios & Testing

### Scenario 1: Student Progress Calculation
**Actor**: System processing student activity
**Flow**:
1. Student completes 5 exercises (3 passed, 2 failed)
2. Student receives code review score of 75
3. Student takes quiz (score: 80)
4. System calculates mastery score:
   - Exercise completion: 60% × 40% = 24.0
   - Quiz score: 80 × 30% = 24.0
   - Code quality: 75 × 20% = 15.0
   - Consistency: 5 activities × 10% = 10.0
   - **Total: 73.0%**

**Acceptance Criteria**:
- Mastery score calculates correctly per formula
- Score updates in real-time as events processed
- Student can view current mastery by topic
- Historical progress tracked over time

### Scenario 2: Struggle Detection - Low Completion Rate
**Actor**: System monitoring student A
**Flow**:
1. Over 7 days, student attempts 10 exercises but only completes 4
2. Completion rate: 40% (below 50% threshold)
3. System generates high-severity alert
4. Teacher notified to intervene

**Acceptance Criteria**:
- Alert triggered when completion rate <50% over 7 days
- Alert includes specific recommendations
- Teacher receives actionable guidance
- Student struggle pattern logged

### Scenario 3: Repeated Failures on Same Topic
**Actor**: Student struggling with recursion
**Flow**:
1. Student attempts 5 recursion exercises over 3 days
2. All 5 attempts fail
3. System detects pattern (5 failures on same topic)
4. Generates medium-severity alert with recommendations

**Acceptance Criteria**:
- Pattern detected after 3+ failures on same topic
- Alert identifies specific topic (recursion)
- Recommendations include review materials and easier exercises
- Alert severity appropriate to failure count

### Scenario 4: Consecutive Low Scores
**Actor**: Student with declining performance
**Flow**:
1. Student scores: 65, 58, 62 on last 3 graded exercises
2. All scores below 60% (failing threshold)
3. System detects 3 consecutive low scores
4. Generates medium-severity alert

**Acceptance Criteria**:
- Detects 3 consecutive scores <60%
- Alert triggered within 1 hour of third low score
- Recommendations focus on foundational review
- Dashboard shows trend line for visualization

---

## Functional Requirements

### FR1: Mastery Score Calculation (Article VI.04)
**Requirement**: Calculate mastery score using weighted formula:
- Exercise completion: 40%
- Quiz scores: 30%
- Code quality: 20%
- Consistency: 10%

**Rationale**: Holistic measure of student learning across multiple dimensions

**Acceptance Criteria**:
- Formula implemented exactly as specified in Constitution
- Recalculates on every relevant event (exercise, quiz, code review)
- Scores range: 0-100 with 2 decimal places
- Updates in Dapr state store within 500ms

### FR2: Struggle Detection - Completion Rate (Article VI.05-1)
**Requirement**: Detect when student completes <50% of exercises over 7 days.

**Rationale**: Early identification of at-risk students

**Acceptance Criteria**:
- Monitors exercise completion over rolling 7-day window
- Triggers alert when completion rate < 50%
- Alert severity: high
- Includes recommendations for intervention

### FR3: Struggle Detection - Repeated Failures (Article VI.05-2)
**Requirement**: Detect when student fails 3+ exercises on same topic.

**Rationale**: Identifies specific knowledge gaps

**Acceptance Criteria**:
- Groups failures by topic (loops, functions, classes, etc.)
- Triggers alert after 3 failures on same topic
- Alert severity: medium
- Recommendations target specific topic review

### FR4: Struggle Detection - Consecutive Low Scores (Article VI.05-3)
**Requirement**: Detect 3 consecutive scores below 60%.

**Rationale**: Indicates pattern of declining performance

**Acceptance Criteria**:
- Tracks score sequence over time
- Triggers alert after 3rd consecutive low score
- Alert severity: medium
- Recommendations focus on foundational skills

### FR5: Event-Driven Processing
**Requirement**: Process events from Kafka topics and update progress.

**Rationale**: Real-time progress tracking as students learn

**Acceptance Criteria**:
- Consumes events: exercise.*, quiz.*, code.*, learning.*
- Processes events within 500ms of receipt
- Updates state store consistently
- Publishes progress.updated events after calculations

### FR6: Student Progress Storage
**Requirement**: Store progress data in Dapr state store.

**Rationale**: Persistence across service restarts

**Acceptance Criteria**:
- Student progress stored with student_id as key
- Includes all calculated metrics (mastery, completion, scores)
- Historical events stored for pattern analysis
- State retrievable via REST API within 200ms

### FR7: Teacher Dashboard API
**Requirement**: Provide endpoints for teacher dashboard data.

**Rationale**: Teachers need visibility into student progress

**Acceptance Criteria**:
- GET /progress/{student_id} returns complete progress data
- GET /struggles returns list of active alerts
- Supports filtering by date range
- Returns aggregated metrics for class overview

### FR8: Alert Publishing
**Requirement**: Publish struggle alerts to Kafka topic.

**Rationale**: Enables other services to react to struggles

**Acceptance Criteria**:
- Topic: struggle.detected
- Alert includes student_id, alert_type, severity, recommendations
- Published immediately after detection
- Consumable by notification service or teacher dashboard

---

## Success Criteria

### Primary Success Metrics

1. **Mastery Accuracy**: Calculated scores match manual calculation (100% accuracy)
2. **Struggle Detection**: 95% of actual struggle patterns detected
3. **False Positive Rate**: <10% false positives on struggle alerts
4. **Processing Latency**: Event to calculated score <500ms (p95)

### Secondary Success Metrics

1. **Score Updates**: 99.9% of events processed successfully
2. **Alert Timeliness**: Struggle alerts within 1 hour of detection
3. **API Performance**: Dashboard queries <200ms (p95)
4. **Data Durability**: 0% data loss with Dapr state store

---

## Key Entities

### StudentProgress
- student_id: Unique identifier
- mastery_score: 0-100 (calculated per Article VI.04)
- exercises_completed: Count of completed exercises
- total_exercises: Total attempted exercises
- average_quiz_score: Mean quiz score
- average_code_quality: Mean code review score
- consistency_score: Based on activity frequency
- last_activity: Most recent event timestamp
- topics_mastered: List of topics with >80% mastery
- topics_struggling: List of topics with <50% mastery
- recommendations: Personalized learning recommendations

### StruggleAlert
- alert_id: Unique identifier
- student_id: Reference to student
- alert_type: completion_rate | repeated_failures | low_scores
- severity: low | medium | high
- message: Human-readable alert description
- recommendations: Actionable steps for improvement
- timestamp: When detected
- resolved: Boolean (alert no longer active)

### ProgressEvent
- event_id: Unique identifier
- student_id: Reference to student
- event_type: exercise | quiz | code_review | learning
- topic: Optional topic category
- score: Optional score (for quiz, code_review)
- status: completed | failed | attempted
- timestamp: Event occurrence time

### MasteryCalculation
- calculation_id: Unique identifier
- student_id: Reference to student
- timestamp: When calculated
- exercise_completion_rate: 0-1.0 percentage
- quiz_score_weighted: Contribution to final score
- code_quality_weighted: Contribution to final score
- consistency_weighted: Contribution to final score
- final_mastery_score: 0-100 result

---

## Assumptions

1. **Event Stream**: All agent services publish events to Kafka
2. **Dapr State Store**: Configured and accessible for persistence
3. **Historical Data**: 7 days of event history available for pattern detection
4. **Topic Classification**: Events include topic metadata for categorization
5. **Time Synchronization**: System clocks synchronized across services
6. **Data Retention**: Events retained for minimum 30 days

---

## Dependencies

### External Services
- **Kafka Cluster**: For event streaming via Dapr pub/sub
- **Kubernetes**: For container orchestration
- **Dapr Runtime**: For state management and pub/sub

### Internal Dependencies
- **Dapr State Store**: For progress persistence
- **Dapr Pub/Sub**: For event consumption and alert publishing
- **Other Agent Services**: Must publish events to Kafka topics

### Event Dependencies
Services must publish events with required fields:
- Triage-Service: learning.* events
- Concepts-Service: learning.response.explanation events
- Debug-Service: code.debug.* events
- Code-Review-Service: code.review.* events
- Exercise-Service: exercise.* events

---

## Out of Scope

1. **Data Visualization**: Frontend dashboard implementation
2. **Student Notification**: Direct alerts to students (via email/push)
3. **Parent Portal**: Parent access to progress data
4. **Predictive Analytics**: ML models for performance prediction
5. **Curriculum Recommendations**: Automated curriculum adjustments
6. **Peer Comparison**: Class ranking or comparison features

---

## Acceptance Criteria Summary

✅ **Functional Requirements**: All 8 FRs implemented and tested
✅ **User Scenarios**: All 4 scenarios validated with test data
✅ **Mastery Formula**: Article VI.04 formula implemented accurately
✅ **Struggle Detection**: All 3 patterns detected per Article VI.05
✅ **Event Processing**: Sub-500ms processing latency achieved
✅ **Data Persistence**: Dapr state store integration complete
✅ **Alert System**: Struggle alerts published to Kafka
✅ **Teacher API**: Dashboard endpoints implemented

---

**Last Updated**: 2026-01-20
**Specification Version**: 1.0.0
**Status**: ✅ Complete - Ready for Implementation
