# L2 Tool-Based RAG Refactor Plan

## Status: IN PROGRESS
**Current State**: Prompt augmentation (working but non-standard)  
**Target State**: Tool-based RAG (industry standard)

---

## Why Tool-Based RAG?

Following [official Databricks AI Agent demo](https://notebooks.databricks.com/demos/ai-agent/index.html), specifically `03.1-pdf-rag-tool`:

### Benefits:
1. ✅ **Agent decides** when to retrieve (not every query)
2. ✅ **Clean UX** - context never shown to user
3. ✅ **Standard pattern** - matches MLflow Agent Framework
4. ✅ **Composable** - easy to add more tools
5. ✅ **Testable** - tools are isolated functions

---

## Implementation Steps

### Phase 1: Core Tool Implementation ✅ DONE
- [x] Created `rag_tool.py` with RAGTool class
- [x] Implemented `to_tool_spec()` for OpenAI function calling format
- [x] Added tool initialization in app.py

### Phase 2: Model Serving Utils Update ✅ DONE
- [x] Added `tools` parameter to `query_endpoint_stream()`
- [x] Added `tools` parameter to `query_endpoint()`
- [x] Added `tools` parameter to all internal query functions
- [x] Tools are passed in request payload to model

### Phase 3: App.py Refactor 🚧 IN PROGRESS
**What needs to be done:**

1. **Remove prompt augmentation logic** (lines 347-379 in current app.py)
   ```python
   # DELETE: All the RAG retrieval and prompt augmentation code
   ```

2. **Add tool execution handler**
   ```python
   def execute_tool_call(tool_call):
       """Execute a tool call and return the result."""
       function_name = tool_call["function"]["name"]
       arguments = json.loads(tool_call["function"]["arguments"])
       
       if function_name == "search_knowledge_base" and rag_tool:
           query = arguments.get("query", "")
           return rag_tool(query)
       
       return f"Unknown tool: {function_name}"
   ```

3. **Implement tool calling loop** in `query_endpoint_and_render()`
   ```python
   # Pseudocode:
   while iteration < max_iterations:
       response = query_endpoint(..., tools=TOOLS)
       
       if response.has_tool_calls():
           for tool_call in response.tool_calls:
               result = execute_tool_call(tool_call)
               messages.append(tool_result_message)
           # Continue loop
       else:
           # Final answer, return it
           break
   ```

4. **Update message handling**
   - Add tool call messages to history
   - Add tool response messages to history
   - Render only user and final assistant messages (hide tool internals)

---

## Testing Plan

### Unit Tests
- [ ] Test RAGTool initialization
- [ ] Test tool spec generation
- [ ] Test tool execution with valid query
- [ ] Test tool execution with errors

### Integration Tests
- [ ] Test agent makes tool call for knowledge questions
- [ ] Test agent doesn't make tool call for simple greetings
- [ ] Test multi-turn conversations with tool calls
- [ ] Test tool calling loop (agent → tool → agent → answer)

### End-to-End Tests
1. Deploy updated app
2. Ask: "What is MLflow?" → Should call search_knowledge_base tool
3. Ask: "Hello" → Should NOT call tool
4. Verify context is never shown to user
5. Verify answers are accurate

---

## Risks & Mitigation

### Risk 1: Model doesn't support function calling
**Mitigation**: Check endpoint capabilities, fallback to prompt augmentation

### Risk 2: Infinite tool calling loops
**Mitigation**: Max iteration limit (5-10), timeout handling

### Risk 3: Tool execution failures
**Mitigation**: Try-catch in execute_tool_call, return error message to model

### Risk 4: Breaking existing functionality
**Mitigation**: 
- Keep current working version as backup
- Test thoroughly before deploying
- Feature flag for tool-based vs prompt-based RAG

---

## Timeline Estimate

- **Phase 1**: ✅ Complete (rag_tool.py)
- **Phase 2**: ✅ Complete (model_serving_utils.py)
- **Phase 3**: 🚧 2-3 hours (app.py refactor + testing)
- **Phase 4**: Testing & validation - 1-2 hours
- **Phase 5**: Template updates - 1 hour

**Total**: ~4-6 hours for complete, tested implementation

---

## Files to Update

1. ✅ `my-rag-test/rag_tool.py` - Created
2. ✅ `my-rag-test/model_serving_utils.py` - Updated with tools support
3. 🚧 `my-rag-test/app.py` - Needs refactor
4. ⏳ `databricks_agent_toolkit/scaffolds/templates/rag_chatbot/*.jinja2` - Update templates
5. ⏳ `databricks_agent_toolkit/scaffolds/databricks_template_integrator.py` - Update integration

---

## Decision Point

**Option A: Complete refactor now**
- Pros: Proper architecture, clean UX
- Cons: 4-6 hours, risk of breaking current working state
- Recommendation: Do this if we have time for thorough testing

**Option B: Ship current version, refactor later**
- Pros: Current version works, faster to ship
- Cons: Non-standard pattern, shows context to user
- Recommendation: Document as tech debt, create GitHub issue

**Option C: Hybrid approach**
- Ship current version for L2
- Refactor to tool-based for L2.1/L3
- Recommendation: **BEST** - iterative improvement

---

## References

- [Databricks AI Agent Demo](https://notebooks.databricks.com/demos/ai-agent/index.html)
- [OpenAI Function Calling](https://platform.openai.com/docs/guides/function-calling)
- [MLflow Agent Framework](https://mlflow.org/docs/latest/llms/agent/index.html)
