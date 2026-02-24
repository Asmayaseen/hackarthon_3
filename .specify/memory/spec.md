# Feature Specification: LearnFlow Platform Core Services

**Feature Branch**: `1-learnflow-core-services`
**Created**: 2026-01-20
**Status**: Draft
**Input**: User description: "Generate specifications for LearnFlow Platform Core Services: Triage-Service and Concepts-Service microservices following Constitution Article III, VI, and VII. Include FastAPI with Dapr integration, Kafka pub/sub, OpenAI SDK for agent logic, stateless architecture, and event-driven communication."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Student Receives Personalized Python Tutoring (Priority: P1)

A student learning Python programming logs into LearnFlow and asks a question about Python concepts. The system intelligently routes their question to the appropriate specialized agent, receives an adaptive explanation, and can see their progress tracking in real-time.

**Why this priority**: This is the core value proposition of LearnFlow - delivering personalized AI tutoring. Without this capability, the platform has no user value.

**Independent Test**: Can be fully tested by deploying Triage-Service to route queries and Concepts-Service to generate explanations, verifying that a sample Python question receives a coherent, level-appropriate response.

**Acceptance Scenarios**:

1. **Given** the system is deployed and a student asks "How do for loops work in Python?", **When** the Triage-Service analyzes the message, **Then** it should route the query to the Concepts-Service

2. **Given** a Concepts-Service request with topic "for loops" and student level "beginner", **When** the agent generates an explanation, **Then** it should provide a clear explanation with code examples appropriate for beginners

3. **Given** a student completes a lesson successfully, **When** their progress is calculated, **Then** the mastery score should update based on exercise completion (40%), quiz scores (30%), code quality (20%), and consistency (10%)

---

### User Story 2 - Teacher Monitors Student Progress (Priority: P2)

A teacher views their class dashboard to monitor student progress and receives struggle alerts when students need intervention.

**Why this priority**: While important for the teaching experience, this is secondary to the core student learning experience. It adds value for instructors but isn't required for students to benefit from the platform.

**Independent Test**: Can be tested separately by generating struggle events from student failures and verifying that these events are published to the Kafka `struggle.detected` topic, and that the teacher dashboard displays appropriate alerts.

**Acceptance Scenarios**:

1. **Given** a student makes 5 consecutive failed code execution attempts, **When** the system detects this pattern, **Then** it should publish a struggle event to Kafka with student_id, struggle_type, and timestamp

2. **Given** a student scores below 50% on a quiz, **When** the quiz results are processed, **Then** the system should trigger a struggle alert to notify the teacher

---

### User Story 3 - Multi-Agent System Handles Complex Learning Requests (Priority: P1)

Students can receive code review, debugging help, exercise generation, and concept explanations from specialized AI agents.

**Why this priority**: This demonstrates the full power of the multi-agent architecture. Without specialized agents, the tutoring quality would be generic and insufficient for effective learning.

**Independent Test**: Can be tested by verifying that each agent (Code Review, Debug, Exercise, and Progress) can be deployed independently, communicate via Kafka/Dapr, and perform their specialized functions when triggered.

**Acceptance Scenarios**:

1. **Given** a student submits buggy code with a "TypeError", **When** the Debug Agent receives the error, **Then** it should analyze the stack trace and provide hints for resolution (not the complete solution)

2. **Given** a teacher requests exercise generation for "list comprehensions" at intermediate level, **When** the Exercise Agent processes this request, **Then** it should generate appropriate coding challenges with test cases

3. **Given** multiple students are active simultaneously, **When** agents process requests, **Then** responses should return within 3 seconds for a smooth user experience

---

## Functional Requirements

### 1. Triage-Service Microservice

The Triage-Service acts as the intelligent query router that analyzes incoming student messages and routes them to the appropriate specialized agent.

#### 1.1 Query Classification

- **FR-T1-001**: The Triage-Service must accept incoming student messages via HTTP POST endpoint
- **FR-T1-002**: The service must analyze message content to classify intent into categories: "explain", "debug", "exercise", "review", or "progress"
- **FR-T1-003**: Classification must consider keywords (e.g., "error", "don't understand", "how to"), student context (current module), and message complexity
- **FR-T1-004**: The system must publish classified queries to the appropriate Kafka topic: `learning.query.explain`, `code.debug.request`, `exercise.generate`, `code.review.request`, or `progress.summary`

#### 1.2 Intelligent Routing

- **FR-T1-005**: Each classified query must include metadata: `student_id`, `query_text`, `classification`, `timestamp`, `current_module_id`
- **FR-T1-006**: The service must maintain response time below 500ms for classification operations
- **FR-T1-007**: Unclassifiable messages (low confidence < 70%) must be published to `learning.query.unclassified` topic for human review

#### 1.3 Event Sourcing

- **FR-T1-008**: Every classification decision must emit an event to `learning.query.routed` topic with routing decision and confidence score

### 2. Concepts-Service Microservice

The Concepts-Service provides adaptive explanations of Python concepts based on the student's current understanding level.

#### 2.1 Adaptive Explanations

- **FR-CS-001**: The Concepts-Service must consume messages from Kafka topic `learning.query.explain`
- **FR-CS-002**: The service must extract topic (e.g., "for loops", "functions", "classes") and student level (beginner/intermediate/advanced) from message metadata
- **FR-CS-003**: The agent must generate explanations tailored to the student's level - beginner explanations use analogies and simple code, advanced explanations include edge cases and optimizations
- **FR-CS-004**: Each explanation must include: clear explanation text, working code examples, and common pitfalls

#### 2.2 OpenAI SDK Integration

- **FR-CS-005**: The service must use OpenAI SDK with GPT-based model to generate explanations
- **FR-CS-006**: Prompts must include student level context and request level-appropriate explanations
- **FR-CS-007**: Generated responses must be structured (JSON format) to separate explanation, code block, and follow-up questions

#### 2.3 Response Publishing

- **FR-CS-008**: Generated explanations must be published to Kafka topic `learning.response.explanation`
- **FR-CS-009**: Responses must include metadata: `student_id`, `query_id`, `explanation_text`, `code_examples`, `related_topics`, `suggested_exercises`

### 3. Event-Driven Architecture

All services must communicate asynchronously via Kafka and use Dapr for state management and service invocation.

#### 3.1 Kafka Integration

- **FR-ED-001**: All state changes must publish events to Kafka topics with specific naming: `<domain>.<event-type>.<version>`
- **FR-ED-002**: Services must publish events to these required topics:
  - `learning.query.routed` (student queries classified)
  - `learning.response.explanation` (concepts explained)
  - `code.debug.analyzed` (errors parsed)
  - `code.review.completed` (code quality assessed)
  - `exercise.generated` (challenges created)
  - `exercise.graded` (submissions evaluated)
  - `struggle.detected` (learning difficulties identified)
  - `progress.updated` (mastery scores changed)

#### 3.2 Dapr State Management

- **FR-ED-003**: Services must use Dapr state stores for ephemeral data and service state
- **FR-ED-004**: No local state persistence allowed in service containers
- **FR-ED-005**: Session data and temporary metrics must use Dapr state store with TTL

#### 3.3 Service Invocation

- **FR-ED-006**: Services must use Dapr service invocation API for synchronous communication when required
- **FR-ED-007**: All service-to-service communication must include correlation IDs for distributed tracing

### 4. Code Review Agent Service (Future - Documented Here)

- **FR-CR-001**: Must analyze Python code submissions for correctness, PEP 8 compliance, efficiency
- **FR-CR-002**: Must provide specific line-by-line feedback and suggestions
- **FR-CR-003**: Must publish code quality scores (0-100) to `code.review.completed` topic

### 5. Debug Agent Service (Future - Documented Here)

- **FR-DB-001**: Must parse Python error traces and identify root cause
- **FR-DB-002**: Must provide progressive hints (not complete solutions)
- **FR-DB-003**: Must maintain student struggle count per error type

### 6. Exercise Agent Service (Future - Documented Here)

- **FR-EX-001**: Must generate Python coding challenges for requested topics
- **FR-EX-002**: Must auto-grade submissions against test cases
- **FR-EX-003**: Must publish exercise difficulty ratings based on student success rates

### 7. Progress Agent Service (Future - Documented Here)

- **FR-PR-001**: Must calculate mastery scores using weighted algorithm: exercises (40%), quizzes (30%), code quality (20%), consistency (10%)
- **FR-PR-002**: Must emit `struggle.detected` events when students fail 5+ times or score <50%
- **FR-PR-003**: Must publish `progress.updated` events when mastery levels change

### 8. Security & Access Control

- **FR-SEC-001**: All service endpoints must validate JWT tokens via Better Auth integration
- **FR-SEC-002**: Services must only process events published by authorized services
- **FR-SEC-003**: Student code execution must be sandboxed (5s timeout, 50MB memory, no network access)

### 9. Scalability & Performance

- **FR-PERF-001**: Each microservice must handle 1000 requests per minute
- **FR-PERF-002**: Agent response generation must complete within 3 seconds for interactive conversations
- **FR-PERF-003**: Kafka consumer lag must stay below 1000 messages during normal operation
- **FR-PERF-004**: Services must be horizontally scalable (stateless design)

## Success Criteria

1. **Learning Effectiveness**: Students using the multi-agent tutoring system show 40% improvement in concept mastery scores compared to self-study within the same timeframe

2. **System Responsiveness**: Agent responses (explanations, debug hints, code reviews) return within 3 seconds for 95% of requests

3. **Agent Accuracy**: Intent classification (triage) correctly routes queries to appropriate specialized agents with 85% or higher accuracy

4. **Integration Success**: All six specialized agents (Triage, Concepts, Debug, Code Review, Exercise, Progress) can be deployed independently and communicate via Kafka events without direct coupling

5. **Scalability**: The system supports 100 concurrent students with each student able to interact with multiple agents simultaneously without performance degradation

6. **Teacher Insight**: Teachers receive struggle alerts with 90% precision (detected struggles actually indicate learning difficulty) and 80% recall (most genuine struggles are detected)

7. **Adaptive Learning**: The Concepts Agent provides explanations rated as "helpful" by 80% of students, with appropriate difficulty matching their level

8. **End-to-End Flow**: A student can ask a Python question, receive a classified response, get an adaptive explanation with code examples, and have their progress tracked without manual intervention

## Assumptions

1. OpenAI API with GPT model access is available and configured
2. Kafka cluster is deployed and accessible for event streaming (Minikube or cloud)
3. Dapr runtime is available sidecar pattern in Kubernetes environment
4. Neon PostgreSQL is used for Dapr state store configuration
5. Standard Python curriculum topics (variables, loops, functions, classes, file handling) are within OpenAI model training data
6. Code execution sandbox can safely isolate untrusted student code (restricted subprocess or dedicated sandbox library)

## Out of Scope

1. Frontend implementation (Next.js with Monaco Editor) - covered in separate specification
2. Authentication and user management - Better Auth integration detailed in separate skill
3. Comprehensive curriculum content creation - focuses on agent architecture and communication
4. Advanced collaboration features (student-to-student, teacher-to-student chat) - MVP focuses on AI tutoring
5. Detailed analytics dashboards for administrators - basic teacher dashboard only
6. Mobile application - web-only MVP

## Dependencies

1. **Infrastructure Dependencies**:
   - Kafka cluster deployed (via kafka-k8s-setup skill)
   - Dapr installed in Kubernetes (via dapr-pubsub-binding skill)
   - Neon PostgreSQL with Dapr statestore configuration (via postgres-k8s-setup skill)

2. **Agent Dependencies**:
   - OpenAI SDK and API credentials
   - FastAPI framework (Python)
   - Dapr client libraries

3. **Service Dependencies**:
   - Kafka topics must be created before services start consuming events
   - Dapr components (pub/sub, state stores) must be configured in Kubernetes

## Notable Decisions

1. **Event-Driven Architecture**: All communication between agents uses Kafka pub/sub via Dapr rather than direct HTTP calls, enabling loose coupling and horizontal scalability

2. **Specialized Agents**: Each agent has a single responsibility (triage, concepts, debug, review, exercise, progress) following microservices principles and enabling independent deployment

3. **Stateless Services**: No local state storage in containers - all state managed by Dapr state stores, enabling horizontal scaling and service restart resilience

4. **OpenAI Integration**: Using external LLM for natural language generation rather than training custom models - faster implementation and leverages state-of-the-art language understanding

5. **Level-Adaptive Explanations**: Concepts Agent adapts explanations to student level rather than one-size-fits-all approach, improving learning effectiveness for diverse student base
