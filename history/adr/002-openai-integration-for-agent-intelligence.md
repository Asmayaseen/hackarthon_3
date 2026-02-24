# ADR-002: OpenAI Integration for Agent Intelligence

**Date**: 2026-01-20
**Status**: Accepted
**Champions**: Claude (AI Assistant)

## Context

LearnFlow requires intelligent agents (Triage, Concepts, Debug, Code Review, Exercise, Progress) capable of natural language understanding, code analysis, and adaptive responses. We faced a critical decision on how to implement the AI intelligence layer.

### Requirements

- Natural language understanding for student queries
- Code analysis and generation for Python programming
- Adaptive explanations based on student skill level
- Debug hint generation (progressive disclosure, not direct solutions)
- Exercise generation with difficulty calibration
- Progress analysis and struggle detection

### Build vs. Buy Decision

**Option A**: Train custom models on Python curriculum
**Option B**: Use commercial LLM APIs (OpenAI, Anthropic, Google)

## Decision

We will integrate **OpenAI GPT models** via the official OpenAI Python SDK for all agent intelligence operations.

### Implementation Details

**Model Configuration**:
- **Triage-Service**: GPT-4o-mini for query classification (fast, cost-effective)
- **Concepts-Service**: GPT-4o-mini for explanation generation (balanced quality/cost)
- Future agents: GPT-4o or GPT-4 for complex reasoning (Debug, Code Review)

**Integration Pattern**:
```python
from openai import AsyncOpenAI

openai_client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

response = await openai_client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a Python tutor..."},
        {"role": "user", "content": query}
    ],
    response_format={"type": "json_object"}
)
```

**Prompt Engineering Strategy**:
- System prompts define agent personality and constraints
- Few-shot examples for consistent output format
- JSON response format for structured data parsing
- Temperature 0.1-0.3 for deterministic responses (classification, debugging)
- Temperature 0.4-0.7 for creative tasks (exercise generation)

**Security**:
- API keys stored in Kubernetes Secrets
- No API keys in code or environment variables in containers
- Rate limiting and cost monitoring via OpenAI dashboard

## Rationale

### Pros

✅ **State-of-the-Art Intelligence**: GPT-4 models provide best-in-class language understanding
✅ **Rapid Development**: No need to train, fine-tune, or host models
✅ **Consistent Quality**: Proven performance on Python code and explanations
✅ **Cost Predictable**: Per-token pricing allows budget forecasting
✅ **Continuous Improvement**: OpenAI improves models without our effort
✅ **Multi-Language Support**: Ready for future language expansion
✅ **Safety**: Built-in content filtering and alignment
✅ **Constitutional Compliance**: Aligns with Article III AI Agent System requirements

### Cons

❌ **Vendor Lock-in**: Dependent on OpenAI's API availability and pricing
❌ **Data Privacy**: Student queries sent to OpenAI servers
❌ **Cost at Scale**: Can become expensive with high usage
❌ **Latency**: Network calls add 500-2000ms to responses
❌ **Rate Limits**: Subject to OpenAI's rate limiting policies

### Trade-offs

We accept vendor lock-in and data privacy concerns in exchange for:
- Market-leading intelligence out-of-the-box
- Faster time-to-market (no model training/tuning)
- Consistent, high-quality responses
- Reduced operational complexity
- Future model improvements automatically

## Alternatives Considered

### Alternative 1: Fine-tune Open-Source Models

**Description**: Fine-tune models like Llama 2, CodeLlama, or StarCoder on Python curriculum

**Rejected Because**:
- Requires massive computational resources and ML expertise
- Would need continuous retraining as curriculum grows
- Quality unlikely to match GPT-4 without significant effort
- Operational complexity (model hosting, scaling, monitoring)
- Slower iteration on prompt improvements
- Cost of GPU infrastructure exceeds API costs at our scale

### Alternative 2: Prompt-Based Open-Source Models

**Description**: Use open-source models (via HuggingFace or local deployment) with prompt engineering only (no fine-tuning)

**Rejected Because**:
- Quality significantly lower than GPT-4 for complex reasoning
- Code understanding and generation not production-ready
- Would require custom hosting infrastructure
- Model loading/serving latency issues
- No enterprise support or SLAs

### Alternative 3: Multi-Vendor Strategy

**Description**: Use Azure OpenAI, Anthropic Claude, and Google Vertex AI simultaneously

**Rejected Because**:
- MVP complexity too high for initial launch
- Different API formats and response formats
- Added latency from routing logic
- Increased development time
- Can revisit this post-MVP for redundancy

## Consequences

### Positive

1. **Faster Development**: AI capabilities working within days vs months
2. **Predictable Behavior**: Consistent output quality across agents
3. **Cost Effective (Initial)**: Pay-per-use vs fixed infrastructure costs
4. **Focus on Domain**: Team focuses on education logic, not ML infrastructure
5. **Adaptive Intelligence**: Automatically benefits from OpenAI improvements
6. **Constitutional Alignment**: Meets Article III requirements for agent intelligence

### Negative

1. **Vendor Dependency**: Business critical dependency on OpenAI
2. **Data Residency**: Student data leaves our infrastructure
3. **Cost Uncertainty**: Usage-based pricing can spike with viral growth
4. **Latency Impact**: Adds 500-2000ms to agent responses
5. **Rate Limits**: Need backoff/retry logic, queue management
6. **Testing Costs**: Integration tests consume API credits

### Mitigation Strategies

1. **Abstraction Layer**: Wrap OpenAI client for easy vendor switching
2. **Caching**: Cache frequently requested explanations to reduce API calls
3. **Hybrid Approach**: Use smaller models for simple tasks, larger for complex
4. **Rate Limiting**: Implement client-side rate limiting to stay within quotas
5. **Budget Monitoring**: Daily cost monitoring via OpenAI dashboard
6. **Fallback Strategy**: Graceful degradation if OpenAI API unavailable
7. **Data Minimization**: Only send necessary context, not full conversation history

## Security & Privacy Considerations

### Data Handling

- **Student Queries**: Sent to OpenAI for processing
- **Code Submissions**: Sent to OpenAI for review/debug
- **No PII**: Student IDs are UUIDs, no names/emails sent
- **Audit Logs**: All API calls logged for security review

### Compliance

- **COPPA**: Designed for students 13+, parental consent required for younger
- **FERPA**: Educational records handled according to regulations
- **Data Processing Agreement**: OpenAI's DPA covers educational use

### Safety Measures

- **Content Filtering**: OpenAI's built-in safety filters prevent harmful content
- **Prompt Injection Protection**: System prompts are authoritative
- **Output Validation**: JSON parsing validates response structure
- **Human Review**: Flagged responses routed to human tutors

## Performance Considerations

### Latency Optimization

- **Async Processing**: Non-blocking API calls in FastAPI async handlers
- **Connection Pooling**: Keep OpenAI connections alive
- **Request Batching**: Group multiple classifications when possible
- **Timeout Handling**: 10-second timeout with graceful fallback

### Cost Optimization

- **Model Selection**: GPT-4o-mini for most tasks (5x cheaper than GPT-4)
- **Response Caching**: Redis cache for frequently requested explanations
- **Batch Requests**: Combine multiple student queries when possible
- **Token Counting**: Monitor and optimize prompts to reduce tokens

## References

- Constitution.md: Article VII (AI Agent System)
- OpenAI Documentation: platform.openai.com/docs
- Dapr + OpenAI Integration: dapr.io/developing-applications/integrations/openai
- Prompt Engineering Guide: platform.openai.com/docs/guides/prompt-engineering
- JSON Mode: platform.openai.com/docs/guides/structured-outputs/json-mode

## Status

✅ **Accepted** - Implemented in Triage-Service and Concepts-Service with OpenAI SDK integration

## Related ADRs

- ADR-001: Event-Driven Architecture with Dapr and Kafka
- ADR-004: Multi-Agent Specialized Architecture
- ADR-005: Token Reduction via Code Execution Pattern

## Future Considerations

**Post-MVP Enhancements**:
1. Multi-vendor integration for redundancy (Anthropic Claude, Google Gemini)
2. Fine-tune smaller models for frequent high-volume tasks
3. Implement semantic caching layer
4. Add cost attribution per student/organization
5. Custom model training if/when scale justifies it
