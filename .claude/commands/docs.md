---
description: Document the code base
---

You are an expert software analyst tasked with thoroughly analyzing and documenting this codebase. Your analysis should be comprehensive, insightful, and well-structured.

## Analysis Framework:

1. **Business Summary** (Start with this)
   - What does this application/system do from a user's perspective?
   - What business problems does it solve?
   - Who are the target users/stakeholders?
   - What are the key features and capabilities?
   - What is the overall value proposition?

2. **Technology Stack Analysis**
   - Programming languages used
   - Frameworks and libraries
   - Database technologies
   - Infrastructure and deployment tools
   - External services and APIs
   - Development and build tools

3. **Technical Deep Dive**
   - **Architecture Overview**: High-level system design and architectural patterns
   - **Data Models**: Database schemas, entity relationships, data flow
   - **Code Structure**: Directory organization, module breakdown, key components
   - **Design Patterns**: Identified patterns (MVC, Repository, Observer, etc.)
   - **Dependencies**: Internal and external dependencies, coupling analysis
   - **Security Considerations**: Authentication, authorization, data protection
   - **Performance Considerations**: Caching, optimization strategies, bottlenecks
   - **Error Handling**: Exception management and logging strategies
   - **Testing Strategy**: Test coverage, testing frameworks, test types

## Instructions:

1. **Read Comprehensively**: Examine all source files, configuration files, documentation, and build scripts
2. **Identify Patterns**: Look for recurring architectural patterns, coding conventions, and design decisions
3. **Analyze Dependencies**: Map out how different modules interact and identify tight/loose coupling
4. **Extract Business Logic**: Understand the domain model and business rules embedded in the code
5. **Assess Quality**: Comment on code organization, maintainability, and technical debt
6. **Be Specific**: Use concrete examples from the codebase to illustrate your points
7. **Structure Clearly**: Use markdown formatting with clear headers and sections

## Output Format:

Save the output in a file called "DOCS.md" in the root. If this file already exists, make sure to integrate the existing knowledge in the new analysis report if it is relevant.

Structure your analysis as a comprehensive markdown document with:
- Clear section headers
- Bullet points for lists
- Code snippets where relevant
- Diagrams in text format if helpful
- Actionable insights and recommendations

Focus on providing both high-level insights for business stakeholders and detailed technical information for developers. Make the documentation useful for onboarding new team members, architecture reviews, and strategic planning.

Analyze the current directory and all subdirectories thoroughly. Ignore any environment/build directories such as: node_modules/**, .git/**, dist/**, build/**, .venv/**


