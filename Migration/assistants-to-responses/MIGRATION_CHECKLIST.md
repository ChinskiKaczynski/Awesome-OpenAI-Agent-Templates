# Migration Checklist: Assistants → Responses

Use this checklist when migrating from Assistants API to Responses API.

## Pre-Migration

- [ ] **Inventory existing assistants**: List all assistants, their tools, and instructions
- [ ] **Identify thread usage**: How are threads created/stored? User sessions?
- [ ] **Document file attachments**: List files attached to assistants
- [ ] **Review custom functions**: Document all function tools and schemas

## Migration Steps

### 1. Model Configuration

- [ ] Replace assistant instructions with `instructions` parameter in responses
- [ ] Map assistant model to response model (usually same)
- [ ] Review temperature/top_p settings

### 2. Thread → Response Chaining

- [ ] Replace `threads.create()` with response chaining
- [ ] Use `store=True` for persistent conversations
- [ ] Chain with `previous_response_id` for multi-turn
- [ ] **Alternative**: Use `conversation` parameter for named sessions

### 3. Tools Migration

- [ ] `retrieval` → `file_search` with vector stores
- [ ] `code_interpreter` → `code_interpreter` with container config
- [ ] Custom functions → same schema, different API

### 4. File Handling

- [ ] Create vector stores for document search
- [ ] Upload files to vector stores (not directly to assistant)
- [ ] Update file references in code

### 5. Run Polling → Single Call

- [ ] Remove run creation and polling logic
- [ ] Replace with single `responses.create()` call
- [ ] Use streaming if needed for progress updates

## Post-Migration

- [ ] **Test all flows**: Verify conversation continuity
- [ ] **Compare outputs**: Check response quality matches
- [ ] **Performance test**: Measure latency differences
- [ ] **Update documentation**: Reflect new API usage
- [ ] **Remove old code**: Delete Assistants API references

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| Thread history loss | Export threads before migration |
| Different response format | Update downstream parsers |
| Cost changes | Monitor usage during transition |
| Tool behavior differences | Test edge cases thoroughly |

## Resources

- [Official Migration Guide](https://platform.openai.com/docs/guides/migrate-to-responses-api)
- [Responses API Reference](https://platform.openai.com/docs/api-reference/responses)
- [Deprecation Timeline](https://platform.openai.com/docs/deprecations)
