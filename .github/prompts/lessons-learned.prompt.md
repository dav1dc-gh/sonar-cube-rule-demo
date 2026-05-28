Append the following instruction to `.github/copilot-instructions.md`; if that file does not exist, create it:

## Lessons Learned Workflow

1. **Before starting any file-modifying or command-running task:** Read `AI-HISTORY.md` from the Git repository root if it exists, and review recent entries to avoid repeating mistakes.

2. **After completing each task:** Append a concise `## Lessons Learned` entry to `AI-HISTORY.md` in the Git repository root. Do not include the lessons-learned entry in the chat response unless the user asks to see it.

3. **Entry format:** Use this structure for each entry:
   ```
   ## YYYY-MM-DD - Task Summary
   
   **Worked:** What succeeded and why.
   
   **Failed:** What did not work or caused issues.
   
   **Rationale:** Why specific approaches were chosen.
   
   **Future Action:** How to apply this learning to avoid repeating mistakes or build on successes.
   ```

4. **When there are no meaningful lessons:** If a task produces no new actionable insight, append `No new actionable lessons learned.` instead of inventing lessons.

5. **File initialization:** If `AI-HISTORY.md` does not exist, create it with the heading `# AI History` before appending the first entry.

6. **File size management:** If `AI-HISTORY.md` exceeds approximately 60,000 characters, summarize the key insights from older entries and remove entries older than 30 days, retaining recent entries to keep the file manageable and focused.

7. **Error handling:** If file access is unavailable, state that `AI-HISTORY.md` could not be updated and provide the exact text the user can paste into the file.