# Migration Templates

Guides and examples for migrating between OpenAI APIs.

## Available Migrations

| Migration | From | To | Deadline | Status |
|-----------|------|----|---------:|--------|
| [assistants-to-responses](./assistants-to-responses/) | Assistants API | Responses API | **Aug 26, 2026** | ✅ Ready |

## Why Migrate?

### Assistants API → Responses API

The **Assistants API is being deprecated** on August 26, 2026. The Responses API is the recommended replacement, offering:

- ✅ Simpler API surface
- ✅ Built-in tools without custom implementation
- ✅ Better streaming with structured events
- ✅ Stateful conversations with `previous_response_id`
- ✅ No separate run/thread management

## Migration Timeline

```
2025-03 ────── Responses API launched
2026-01 ────── NOW (you should start migrating)
2026-08-26 ─── Assistants API shutdown ⚠️
```

## Related Resources

- [Official Migration Guide](https://platform.openai.com/docs/guides/responses-vs-chat-completions)
- [Responses API Documentation](https://platform.openai.com/docs/guides/responses)
