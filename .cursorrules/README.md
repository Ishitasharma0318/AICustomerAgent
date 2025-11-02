# Cursor AI Rules

This directory contains custom Cursor AI rules (`.mdc` files) to enhance AI-assisted development for this project.

## Available Rules

### 1. `testing-developer.mdc`
**Purpose**: Automated test generation  
**Usage**: Generates unit tests for backend (pytest) and frontend (jest)  
**Behavior**: Creates professional test suites and reports status without attempting fixes

### 2. `technical-writing-assistant.mdc`
**Purpose**: Documentation writing assistance  
**Usage**: Helps write clear, professional technical documentation  
**Behavior**: Maintains consistent tone and structure across docs

### 3. `create-prd.mdc`
**Purpose**: Product Requirements Document generation  
**Usage**: Creates structured PRDs for new features  
**Behavior**: Follows standard PRD format with clear sections

### 4. `generate-tasks.mdc`
**Purpose**: Task breakdown and planning  
**Usage**: Breaks down features into actionable tasks  
**Behavior**: Creates structured task lists with priorities

### 5. `process-task-list.mdc`
**Purpose**: Task management and tracking  
**Usage**: Helps organize and track task completion  
**Behavior**: Maintains task status and dependencies

### 6. `keep-functionality-related-to-model-by-file.mdc`
**Purpose**: Code organization guidance  
**Usage**: Ensures proper separation of concerns  
**Behavior**: Keeps model-related code properly organized

## How to Use

These rules are automatically available in Cursor AI when working in this project directory. To use a specific rule:

1. Use `@` mentions in Cursor chat to reference rules
2. Rules with `alwaysApply: false` need to be explicitly activated
3. Rules with `alwaysApply: true` are active by default

## Adding New Rules

To add a new rule:
1. Create a `.mdc` file in this directory
2. Add frontmatter with `alwaysApply` setting
3. Write clear instructions for the AI
4. Update this README

## Project Context

These rules are tailored for the **AWS Lambda + API Gateway Customer Service AI** project, which uses:
- Backend: Python, FastAPI, LangChain, ChromaDB
- Frontend: Next.js, TypeScript, React
- AI: Multi-agent system with LangGraph

