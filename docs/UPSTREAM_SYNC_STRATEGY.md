# Upstream Sync Strategy

> **Upstream**: https://github.com/databricks/app-templates
> **Goal**: Stay compatible with official Databricks UI templates
> **Status**: Automated monitoring via GitHub Actions

---

## 🎯 The Challenge

**Official Databricks app-templates repository changes:**
- 📝 Existing templates updated
- ✨ New templates added
- 🗑️ Templates deprecated
- 💥 Breaking API changes

**We need to:**
1. **Detect** changes automatically
2. **Test** compatibility with our toolkit
3. **Document** any required updates
4. **Notify** maintainers and users

---

## 🤖 Automated Monitoring Solution

### **GitHub Actions Workflow**

**File**: `.github/workflows/monitor-app-templates.yml`

**What it does:**
```
Daily (9 AM UTC):
┌─────────────────────────────────────────────────┐
│ 1. Clone databricks/app-templates               │
│ 2. Compare with last known commit               │
│ 3. If changes detected:                         │
│    ├── Analyze what changed                     │
│    ├── Test our backend compatibility           │
│    ├── Create GitHub issue with details         │
│    └── Update tracking file                     │
└─────────────────────────────────────────────────┘
```

**Triggers:**
- ⏰ **Scheduled**: Daily at 9 AM UTC
- 🔘 **Manual**: Via GitHub Actions UI

---

## 📊 What We Track

### **1. Template Inventory**

Monitor these chatbot templates:
- `streamlit-chatbot-app`
- `gradio-chatbot-app`
- `dash-chatbot-app`
- `shiny-chatbot-app`
- `e2e-chatbot-app`
- `e2e-chatbot-app-next`

### **2. API Contract**

Verify our backend compatibility:
```python
# Our backend must provide:
✅ POST /api/invocations      # OpenAI API format
✅ GET  /health                # Health check
✅ GET  /docs                  # OpenAPI schema
✅ GET  /openapi.json          # OpenAPI JSON
✅ SSE streaming support       # For stream=true
```

### **3. Changes That Matter**

**High Priority (Breaking):**
- API endpoint changes
- Request/response format changes
- Authentication pattern changes
- Deployment structure changes

**Medium Priority (Features):**
- New templates added
- New features in existing templates
- Documentation updates

**Low Priority (Cosmetic):**
- UI style changes
- Example updates
- README improvements

---

## 🔔 Notification Flow

```
Change Detected
     │
     ▼
GitHub Issue Created
     │
     ├── Title: "🔔 New changes in databricks/app-templates"
     ├── Body: Detailed change report
     ├── Labels: compatibility, monitoring, upstream-sync
     └── Checklist: Compatibility verification steps
     │
     ▼
Maintainer Reviews
     │
     ├── No action needed → Close issue
     ├── Doc update needed → Update docs, close issue
     ├── Code change needed → Create PR, link to issue
     └── Breaking change → Plan migration, communicate to users
     │
     ▼
Issue Closed (tracked in .github/app-templates-version.txt)
```

---

## 🧪 Compatibility Testing

### **Automated Tests (In CI)**

```bash
# 1. Generate test scaffold
databricks-agent-toolkit generate chatbot test-bot

# 2. Start backend
cd test-bot
python start_server.py &

# 3. Test endpoints
curl -X POST http://localhost:8000/api/invocations \
  -H "Content-Type: application/json" \
  -d '{"input": [{"role": "user", "content": "test"}]}'

curl http://localhost:8000/health
curl http://localhost:8000/docs
curl http://localhost:8000/openapi.json

# 4. Test streaming
curl -X POST http://localhost:8000/api/invocations \
  -H "Content-Type: application/json" \
  -d '{"input": [...], "stream": true}'
```

### **Manual Testing (When Changes Detected)**

```bash
# 1. Clone updated template
git clone https://github.com/databricks/app-templates.git
cd app-templates/streamlit-chatbot-app

# 2. Generate our backend
databricks-agent-toolkit generate chatbot test-integration

# 3. Point template UI to our backend
# (Update config to use localhost:8000)

# 4. Test end-to-end
# - Start backend: python start_server.py
# - Start UI: streamlit run app.py (or other framework)
# - Verify: Chat functionality, streaming, error handling

# 5. Document findings in GitHub issue
```

---

## 📁 Version Tracking

**File**: `.github/app-templates-version.txt`

```
# Last known commit from databricks/app-templates
abc123def456...
```

**Updated by:**
- GitHub Actions workflow (automated)
- Maintainers (manual verification)

**Used for:**
- Detecting new changes
- Creating diff links in issues
- Historical tracking

---

## 🛠️ Maintenance Workflow

### **When Changes Detected**

**Step 1: Review Issue** (Auto-created by CI)
- Read change summary
- Check linked diff on GitHub
- Assess impact (breaking/feature/cosmetic)

**Step 2: Test Locally**
```bash
# Clone both repos
git clone https://github.com/databricks/app-templates.git
cd app-templates
git checkout <new-commit>

# Test with our toolkit
databricks-agent-toolkit generate chatbot test-new
# Manual integration testing...
```

**Step 3: Update If Needed**

**No changes needed** (most common):
```bash
# Close issue with comment
"✅ Verified compatibility. No changes needed to our toolkit."
```

**Documentation update needed**:
```bash
# Update relevant docs
vi docs/UI_FRAMEWORK_INTEGRATION.md
git commit -m "docs: update for app-templates changes"
```

**Code changes needed**:
```bash
# Create PR
git checkout -b fix/app-templates-compat
# Make changes...
git commit -m "fix: update for app-templates API changes"
# Link PR to issue
```

**Step 4: Close Issue**
- Document findings
- Link to PR if code changed
- Update `.github/app-templates-version.txt`

---

## 🚨 Breaking Change Protocol

**If breaking changes detected:**

1. **Immediate Actions**
   - Create urgent GitHub issue
   - Pin affected versions in docs
   - Test impact on existing scaffolds

2. **Communication**
   - Update README with compatibility note
   - Create migration guide if needed
   - Post to discussions/community

3. **Release Planning**
   - Plan patch release if critical
   - Update affected templates
   - Add compatibility layer if possible

4. **User Notification**
   - PyPI release notes
   - GitHub release notes
   - Documentation updates

---

## 📋 Manual Check Procedure

**Monthly (or on-demand):**

```bash
# 1. Check for new templates
curl -s https://api.github.com/repos/databricks/app-templates/contents \
  | jq -r '.[] | select(.type=="dir") | .name' \
  | grep -i chatbot

# 2. Compare with our docs
# docs/UI_FRAMEWORK_INTEGRATION.md

# 3. Test new templates
# Follow manual testing procedure above

# 4. Update documentation
# Add new templates to README, integration docs
```

---

## 🎯 Success Metrics

**Monitoring Effectiveness:**
- ✅ Changes detected within 24 hours
- ✅ Compatibility tested within 48 hours
- ✅ Documentation updated within 1 week
- ✅ No user reports of incompatibility

**Compatibility:**
- ✅ 100% of official chatbot templates supported
- ✅ All API contracts honored
- ✅ Zero breaking changes missed

---

## 🔮 Future Enhancements

**v0.3.0+:**
- [ ] Automated compatibility tests for each template
- [ ] Automated PR creation for doc updates
- [ ] Slack/Discord notifications for changes
- [ ] Dashboard showing compatibility status
- [ ] Integration tests in CI/CD

**v0.4.0+:**
- [ ] Auto-generate integration code from templates
- [ ] Version pinning for specific template commits
- [ ] Compatibility matrix in docs
- [ ] Community contribution workflow

---

## 📚 Related Documents

- **Integration Guide**: `docs/UI_FRAMEWORK_INTEGRATION.md`
- **Compliance Report**: `docs/APP_TEMPLATES_COMPLIANCE.md`
- **E2E Integration**: `docs/E2E_CHATBOT_APP_INTEGRATION.md`
- **Monitoring Workflow**: `.github/workflows/monitor-app-templates.yml`

---

## ✅ Current Status (v0.2.0)

**Backend Compatibility:** ✅ **100% Compatible**
- OpenAI API format (`/api/invocations`)
- Streaming support (SSE)
- Health endpoint (`/health`)
- OpenAPI schema (`/docs`, `/openapi.json`)

**Monitoring:** ✅ **Active**
- Daily automated checks
- Issue creation on changes
- Version tracking in place

**Documentation:** ✅ **Complete**
- README updated with all 6 templates
- Integration guides available
- Manual integration instructions

**Next:** Ship v0.2.0 to PyPI! 🚀
