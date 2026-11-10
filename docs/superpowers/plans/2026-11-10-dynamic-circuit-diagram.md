# Dynamic Circuit Diagram Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the circuit diagram dynamic by overlaying user-inputted values onto the schematic.

**Architecture:** Update the HTML to include `<span>` elements positioned absolutely over the existing SVG schematic, and use a small inline JavaScript script to update these values whenever the user submits the form.

**Tech Stack:** HTML5, CSS3, JavaScript.

**Spec:** Dynamic update to existing `templates/index.html` and `static/style.css`.

## Global Constraints

- No changes to Python engineering logic required.
- Diagram must remain responsive (maintain proportions/relative positioning).
- JavaScript should run after the page loads or form submission completes.

## Review Focus

- JavaScript fails to run (ensure script is embedded properly in `index.html`).
- Dynamic labels overlap with circuit lines (fine-tune CSS positioning).
- Values don't update correctly on re-submit (verify ID mapping).

---

### Task 1: Update HTML Structure for Dynamic Labels

**Files:**
- Modify: `templates/index.html`

- [ ] **Step 1: Wrap schematic and add labels**

Add `position: relative` to `circuit-diagram-container` and add `<span class="dyn-val" id="label-r1">` elements positioned absolute at coordinates corresponding to the circuit components.

- [ ] **Step 2: Commit**

```bash
git add templates/index.html
git commit -m "feat: add dynamic labels container to circuit schematic"
```

---

### Task 2: Implement Dynamic Update Logic

**Files:**
- Modify: `templates/index.html` (add script)

- [ ] **Step 1: Write JS function**

Add a script to update `label-r1`, `label-r2`, etc., based on form field values when the page loads (using Jinja2 context) or via JS `document.getElementById` mapping.

- [ ] **Step 2: Commit**

```bash
git add templates/index.html
git commit -m "feat: implement JS logic for dynamic circuit value updates"
```
