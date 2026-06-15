Generate a detailed and unique GitHub Copilot custom instructions file (in Markdown format, suitable for placement at .github/copilot-instructions.md) specific to each major path under the /rules directory.
This translates into a path specific custom instruction for each of the following paths:
- /rules/security
- /rules/code-smells
- /rules/performance
- /rules/maintainability

Each custom instructions file must include the following sections:
1. **Context** – describing the purpose of the path and its role in SonarQube rule organization
2. **Goals** – what the AI should help the user achieve within that category
3. **Constraints** – what the AI should avoid or be cautious about
4. **Examples** – at least two example user requests with expected AI behavior

The custom instructions should guide the AI assistant on how to help users create, manage, and understand SonarQube Rules Files within each specific category effectively. Each file must contain instructions that are specific to the concerns of that category and must not simply repeat generic SonarQube guidance. For example:
- /rules/security instructions should focus on OWASP/CWE mappings and severity classification
- /rules/performance instructions should focus on complexity thresholds and hotspot detection
- /rules/code-smells instructions should focus on maintainability metrics and code quality patterns
- /rules/maintainability instructions should focus on readability, complexity reduction, and refactoring guidance