# Feature Specification: Exercise Agent Service

**Feature ID**: 2-exercise-service
**Created**: 2026-01-20
**Status**: Specification Complete
**Branch**: 2-exercise-service

## Overview

Build the Exercise Agent Service that generates Python coding challenges with automatic grading. The service creates exercises based on topic and difficulty level, then auto-grades student submissions with test cases.

**Key Features**:
- Topic-based exercise generation (loops, functions, classes, etc.)
- Difficulty levels: easy, medium, hard
- Auto-grading with test cases
- Progressive hints system
- Dapr Kafka integration for event-driven architecture

---

## User Scenarios & Testing

### Scenario 1: Student Requests Exercise on Specific Topic
**Actor**: Beginner student learning Python loops
**Flow**:
1. Student selects "loops" topic and "easy" difficulty
2. System generates exercise: "Write a function that sums numbers from 1 to n"
3. Student receives starter code and 3 test cases
4. Student can request hints if stuck

**Acceptance Criteria**:
- Exercise generated within 2 seconds
- Includes clear problem description
- Provides starter code scaffold
- Includes 3 test cases with inputs and expected outputs
- Offers 3 progressive hints

### Scenario 2: Student Submits Solution for Grading
**Actor**: Student completing exercise
**Flow**:
1. Student writes solution code
2. System runs code against test cases
3. Student receives immediate feedback:
   - Which tests passed/failed
   - Score (0-100)
   - Detailed error messages for failed tests
4. If score >= 70%, exercise marked as passed

**Acceptance Criteria**:
- Grading completes within 1 second
- All test cases executed in isolated environment
- Clear feedback on failures
- Score calculation accurate
- Event published to Kafka for progress tracking

### Scenario 3: Teacher Reviews Exercise Performance
**Actor**: Teacher monitoring class progress
**Flow**:
1. Teacher accesses exercise dashboard
2. Views completion rates by topic
3. Identifies topics where students struggle
4. Adjusts curriculum based on data

**Acceptance Criteria**:
- Aggregated metrics available by topic
- Average scores calculated
- Struggle patterns identified
- Data exportable for analysis

### Scenario 4: System Generates Varied Exercises
**Actor**: System serving multiple students
**Flow**:
1. Multiple students request "functions" topic
2. System generates different exercises for each student
3. Exercises vary in approach while testing same concept
4. Prevents answer sharing

**Acceptance Criteria**:
- Exercise variation implemented
- Same concept tested with different problems
- Randomization prevents duplication

---

## Functional Requirements

### FR1: Topic-Based Exercise Generation
**Requirement**: Service must generate exercises for topics: loops, functions, classes, lists, dictionaries, recursion.

**Rationale**: Covers fundamental Python programming concepts

**Acceptance Criteria**:
- Minimum 3 exercises per topic per difficulty level
- Uses OpenAI GPT-4o-mini for generation
- Fallback to template-based generation if OpenAI fails
- Generated exercises include problem description, starter code, test cases, and hints

### FR2: Difficulty Level System
**Requirement**: Support three difficulty levels: easy, medium, hard.

**Rationale**: Accommodates students at different skill levels

**Acceptance Criteria**:
- Easy: Basic concept application, 5-10 lines of code
- Medium: Multi-step problems, 10-20 lines of code
- Hard: Complex logic, 20+ lines, multiple concepts
- Difficulty clearly indicated in exercise metadata

### FR3: Auto-Grading with Test Cases
**Requirement**: Automatically grade submissions against predefined test cases.

**Rationale**: Immediate feedback accelerates learning

**Acceptance Criteria**:
- Minimum 3 test cases per exercise
- Tests cover normal cases, edge cases, and error conditions
- Code executed in isolated environment for security
- Execution timeout: 5 seconds maximum
- All tests run before determining final score

### FR4: Scoring System
**Requirement**: Calculate score as percentage of tests passed.

**Rationale**: Quantitative measure of success

**Acceptance Criteria**:
- Score = (passed_tests / total_tests) * 100
- Passing threshold: 70%
- Student receives detailed breakdown per test case
- Score published to Kafka topic `exercise.graded`

### FR5: Progressive Hints System
**Requirement**: Provide 3 hints per exercise, from general to specific.

**Rationale**: Helps students without revealing solution

**Acceptance Criteria**:
- Hint 1: General guidance about approach
- Hint 2: More specific guidance about technique
- Hint 3: Nearly complete solution guidance
- Students can request hints sequentially
- Hints usage tracked for learning analytics

### FR6: Event-Driven Architecture
**Requirement**: All operations publish events to Kafka via Dapr.

**Rationale**: Enables loose coupling and progress tracking

**Acceptance Criteria**:
- Topics: `exercise.generate`, `exercise.generated`, `exercise.grade`, `exercise.graded`
- Events follow CloudEvents specification
- Dapr pub/sub component configured
- Raw payload disabled for structured events

### FR7: Exercise Database
**Requirement**: Store generated exercises for reuse and analytics.

**Rationale**: Prevents regenerating same exercises, enables analytics

**Acceptance Criteria**:
- Exercises stored with unique ID
- Metadata: topic, difficulty, generation timestamp
- Solution code stored securely (not accessible to students)
- Usage statistics tracked (attempts, average score)

---

## Success Criteria

### Primary Success Metrics

1. **Generation Speed**: Exercise generated within 2 seconds (p95)
2. **Grading Speed**: Submissions graded within 1 second (p95)
3. **Test Coverage**: Minimum 3 test cases per exercise
4. **Scoring Accuracy**: 100% match between expected and actual output

### Secondary Success Metrics

1. **Exercise Quality**: 90% of generated exercises rated "good" by teacher review
2. **Hint Effectiveness**: 70% of students who use hints successfully complete exercise
3. **System Uptime**: 99.5% availability
4. **Scalability**: Supports 500 concurrent students

---

## Key Entities

### Exercise
- exercise_id: Unique identifier (UUID)
- title: Short descriptive title
- description: Problem statement
- topic: loops | functions | classes | lists | dictionaries | recursion
- difficulty: easy | medium | hard
- starter_code: Optional code scaffold
- test_cases: List of test case objects
- hints: List of 3 hint strings
- solution: Reference solution (not exposed to students)
- generated_at: Timestamp

### TestCase
- test_id: Unique identifier
- input: Code to execute (string)
- expected_output: Expected result
- description: What this test validates

### CodeSubmission
- submission_id: Unique identifier
- student_id: Reference to student
- exercise_id: Reference to exercise
- code: Student's submitted code
- submitted_at: Timestamp

### GradingResult
- result_id: Unique identifier
- student_id: Reference to student
- exercise_id: Reference to exercise
- score: 0-100 percentage
- total_tests: Number of test cases
- passed_tests: Number of passed tests
- test_results: Detailed results per test
- passed: Boolean (score >= 70%)
- graded_at: Timestamp

### Hint
- hint_id: Unique identifier
- exercise_id: Reference to exercise
- level: 1 | 2 | 3 (progressive)
- content: Hint text

---

## Assumptions

1. **OpenAI API**: GPT-4o-mini available with sufficient rate limits
2. **Kafka Cluster**: Running and accessible via Dapr pub/sub
3. **Dapr Runtime**: Dapr sidecar injection configured
4. **OpenAI API Key**: Available as Kubernetes secret
5. **Code Isolation**: Safe execution environment for student code
6. **Network**: All services can communicate via Kubernetes service mesh

---

## Dependencies

### External Services
- **OpenAI API**: For exercise generation
- **Kafka Cluster**: For event streaming (via Dapr pub/sub)
- **Kubernetes**: For container orchestration

### Internal Dependencies
- **Dapr Runtime**: For service-to-service communication
- **Dapr Pub/Sub**: For event-driven messaging
- **Dapr State Store**: For exercise persistence

---

## Out of Scope

1. **Code Execution Sandbox**: Advanced security isolation beyond basic restrictions
2. **Collaborative Coding**: Multi-student exercise solving
3. **Gamification**: Points, badges, leaderboards
4. **Mobile App**: Native mobile application
5. **Advanced Analytics**: Machine learning on exercise performance
6. **Content Management**: Teacher interface for manual exercise creation

---

## Acceptance Criteria Summary

✅ **Functional Requirements**: All 7 FRs implemented
✅ **User Scenarios**: All 4 scenarios validated
✅ **Success Metrics**: Generation <2s, grading <1s, test coverage adequate
✅ **Architecture**: Stateless service with Dapr sidecar
✅ **Event-Driven**: Kafka topics configured and publishing events
✅ **Exercise Quality**: Generated exercises reviewed and validated
✅ **Security**: Code execution in isolated environment

---

**Last Updated**: 2026-01-20
**Specification Version**: 1.0.0
**Status**: ✅ Complete - Ready for Implementation
