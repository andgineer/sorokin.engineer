---
layout: post
lang: en
ref: github_custom_actions
title: "Create Your Own GitHub Action in 5 Minutes with Python"
comments: true
tags: [github actions, Python]
---

![](/images/github-custom-actions.png){:.post-title}

# Simple GitHub Actions with Python

Creating custom GitHub Actions can seem daunting - you need to handle environment variables, inputs/outputs, 
error reporting, and more. But it doesn't have to be complicated.

The [github-custom-actions](https://andgineer.github.io/github-custom-actions/) library eliminates all the boilerplate and provides:
- Type hints for GitHub variables with autocompletion in your IDE
- Easy access to all GitHub context (repository, workflow, runner, etc.)
- Built-in Jinja templating for nice reports
- Automatic error handling and logging
- Type-safe inputs/outputs

You just write clean Python code, and the library handles all GitHub Actions integration. L

Let's see how easy it is to create your own action.

## Example: Branch Name Validator 

Here's an action that checks if branch names follow your team's conventions:

```python
from github_custom_actions.action_base import ActionBase
from github_custom_actions.inputs_outputs import ActionInputs, ActionOutputs
import re

class ValidatorInputs(ActionInputs):
    pattern: str = "^(feature|bugfix|hotfix)/[a-z0-9-]+$"
    """Branch name pattern (regex)"""

class ValidatorOutputs(ActionOutputs):
    valid: str
    """Whether branch name is valid"""

class BranchValidator(ActionBase):
    inputs: ValidatorInputs
    outputs: ValidatorOutputs

    def main(self):
        # Get current branch from GitHub environment
        branch = self.env.github_ref_name
        
        # Check if branch name matches pattern
        is_valid = bool(re.match(self.inputs.pattern, branch))
        self.outputs.valid = str(is_valid)

        # Create report using template
        self.summary.text = self.render("""
## Branch Name Check
{% raw %}
Branch: `{{ branch }}`
Pattern: `{{ inputs.pattern }}`
Status: {{ "✅ Valid" if outputs.valid == "true" else "❌ Invalid" }}
{% endraw %}
""", branch=branch)

        if not is_valid:
            raise ValueError(f"Invalid branch name: {branch}")

if __name__ == "__main__":
    BranchValidator().run()
```

Use it in your workflow:
```yaml
Copyname: Validate Branch
on: [push, pull_request]

jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: ./
        with:
          pattern: '^(feature|bugfix|hotfix)/[a-z0-9-]+$'
```

## Publishing to GitHub Marketplace

1. Create repository for your action with this file structure:
```python
my-action/
  ├── action.yml       # Action metadata
  ├── Dockerfile      # Use Python image and install your action
  ├── requirements.txt # Include github-custom-actions
  └── main.py         # Your action code
```

2. Add to `action.yml`:
```yaml
name: 'Branch Name Validator'
description: 'Validates branch names against pattern'
inputs:
  pattern:
    description: 'Branch name pattern (regex)'
    required: true
    default: '^(feature|bugfix|hotfix)/[a-z0-9-]+$'
outputs:
  valid:
    description: 'Whether branch name is valid'
runs:
  using: 'docker'
  image: 'Dockerfile'
```

3. Create `Dockerfile`:
```dockerfile
FROM python:3.9-slim
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "/main.py"]
```

4. [Publish to GitHub Marketplace](https://docs.github.com/en/actions/creating-actions/publishing-actions-in-github-marketplace)

After that anyone can use your action like this:

```yaml
- uses: your-github-name/your-action-repo@v1
  with:
    pattern: '^(feature|bugfix|hotfix)/[a-z0-9-]+$'
```