# Scripts

Utility scripts for maintaining the Awesome-OpenAI-Agent-Templates repository.

## generate-readme.py

Generates the Template Registry table in README.md from `registry.yml`.

### Prerequisites

```bash
pip install pyyaml
```

### Usage

```bash
python scripts/generate-readme.py
```

### How it works

1. Reads `registry.yml` from repository root
2. Generates a markdown table with all templates
3. Updates README.md between `<!-- REGISTRY_TABLE_START -->` and `<!-- REGISTRY_TABLE_END -->` markers

### Adding a new template

1. Add entry to `registry.yml`:

   ```yaml
   - id: my-new-template
     name: My New Template
     category: responses-api
     path: Responses-API/my-new-template
     languages: [python]
     difficulty: beginner
     tools: []
     status: verified
     description: Short description
   ```

2. Run the generator:

   ```bash
   python scripts/generate-readme.py
   ```

3. Commit both `registry.yml` and the updated `README.md`
