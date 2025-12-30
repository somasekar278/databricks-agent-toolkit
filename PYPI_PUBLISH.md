# Publishing SOTA Agent Framework to PyPI

**Step-by-step guide to publish your framework to PyPI so users can `pip install` it.**

## Prerequisites

1. **PyPI Account** - Create at https://pypi.org/account/register/
2. **TestPyPI Account** (optional but recommended) - Create at https://test.pypi.org/account/register/
3. **API Token** - Create at https://pypi.org/manage/account/token/

## One-Time Setup

### 1. Install Build Tools

```bash
pip install build twine
```

### 2. Create PyPI API Token

1. Go to https://pypi.org/manage/account/token/
2. Click "Add API token"
3. Name: "SOTA Agent Framework"
4. Scope: "Entire account" (or specific project later)
5. Copy the token (starts with `pypi-...`)

### 3. Configure Credentials

Create `~/.pypirc`:

```ini
[pypi]
username = __token__
password = pypi-YOUR_TOKEN_HERE

[testpypi]
username = __token__
password = pypi-YOUR_TESTPYPI_TOKEN_HERE
```

**Or use keyring (more secure):**
```bash
pip install keyring
keyring set https://upload.pypi.org/legacy/ __token__
# Enter your token when prompted
```

## Publishing Steps

### Step 1: Update Version

Edit `pyproject.toml`:
```toml
[project]
version = "0.1.0"  # Update this for each release
```

### Step 2: Clean Previous Builds

```bash
cd "/Users/som.natarajan/SOTA Agent Framework"
rm -rf dist/ build/ *.egg-info
```

### Step 3: Build the Package

```bash
python -m build
```

This creates:
- `dist/sota_agent_framework-0.1.0.tar.gz` (source distribution)
- `dist/sota_agent_framework-0.1.0-py3-none-any.whl` (wheel)

### Step 4: Test on TestPyPI (Recommended)

```bash
# Upload to TestPyPI first
twine upload --repository testpypi dist/*

# Test install
pip install --index-url https://test.pypi.org/simple/ sota-agent-framework
```

### Step 5: Publish to PyPI

```bash
# Upload to real PyPI
twine upload dist/*
```

Enter your credentials when prompted (or use API token).

### Step 6: Verify Installation

```bash
# Test that it works
pip install sota-agent-framework

# Try the CLI
sota-generate --help
```

## After Publishing

### Users Can Now Install

```bash
pip install sota-agent-framework
```

### Users Can Generate Projects

```bash
sota-generate --domain "customer_support"
sota-generate --domain "fraud_detection" --output ./fraud-agents
```

## Updating the Package

When you make changes:

1. **Update version** in `pyproject.toml`
2. **Clean and rebuild**: 
   ```bash
   rm -rf dist/ build/ *.egg-info
   python -m build
   ```
3. **Upload**:
   ```bash
   twine upload dist/*
   ```

## Version Numbering

Follow semantic versioning (https://semver.org/):
- `0.1.0` - Initial release
- `0.1.1` - Bug fixes
- `0.2.0` - New features (backwards compatible)
- `1.0.0` - First stable release

## Package Info

After publishing, your package will be at:
- **PyPI**: https://pypi.org/project/sota-agent-framework/
- **Install**: `pip install sota-agent-framework`
- **CLI**: `sota-generate --domain "your_domain"`

## Troubleshooting

### "Package already exists"
- You can't re-upload the same version
- Increment version number and rebuild

### "Invalid credentials"
- Check your API token
- Verify `~/.pypirc` is correct
- Try: `twine upload --verbose dist/*` for details

### "Package name taken"
- Choose a different name in `pyproject.toml`
- Or add your username: `sota-agent-framework-yourname`

## Quick Reference

```bash
# Complete publish workflow
cd "/Users/som.natarajan/SOTA Agent Framework"

# 1. Update version in pyproject.toml
# 2. Clean and build
rm -rf dist/ build/ *.egg-info
python -m build

# 3. Upload
twine upload dist/*

# 4. Test
pip install sota-agent-framework
sota-generate --domain "test"
```

## Once Published

Update your README to show:

```markdown
## Installation

```bash
pip install sota-agent-framework
```

## Usage

```bash
sota-generate --domain "your_domain"
```

Done! ✅
```

---

**Ready to publish?** Run the commands in "Publishing Steps" above!

