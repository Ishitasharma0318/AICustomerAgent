# Technical Support Agent - Data Directory

## Purpose
This directory contains documentation for the **Technical Support Agent** which uses a **Pure RAG (Retrieval-Augmented Generation)** strategy.

## Agent Behavior
- **Retrieval Strategy**: Pure RAG
- **How it works**: For every query, the agent searches the vector database to retrieve the most relevant technical documents, then generates a response based on that context.
- **Use Case**: Troubleshooting, debugging, error resolution, performance issues

## Data to Collect

### Categories to Include:

1. **Lambda Error Codes & Troubleshooting**
   - Common error messages
   - Timeout issues
   - Memory errors
   - Permission errors
   - Invocation errors

2. **API Gateway Error Responses**
   - 4xx client errors
   - 5xx server errors
   - Integration errors
   - Timeout errors

3. **Performance Issues**
   - Cold start optimization
   - Execution duration problems
   - Concurrency issues
   - Throttling

4. **CloudWatch & Monitoring**
   - Log interpretation
   - Debugging with CloudWatch
   - Metrics and alarms
   - X-Ray tracing

5. **Integration Problems**
   - Lambda + API Gateway integration issues
   - VPC connectivity
   - Database connections
   - Third-party service integrations

6. **Deployment Issues**
   - Package size limitations
   - Dependency problems
   - Configuration errors
   - Version management

## File Naming Convention
Use descriptive names with hyphens:
- `lambda-timeout-errors.md`
- `api-gateway-502-errors.md`
- `cold-start-optimization.md`
- `cloudwatch-debugging.md`

## Metadata Template
Each file should start with:
```markdown
---
category: technical
subcategory: error_handling | performance | monitoring | integration | deployment
service: lambda | api-gateway | cloudwatch
difficulty: beginner | intermediate | advanced
last_updated: YYYY-MM-DD
---
```

## Target: 10-15 Documents
Aim for comprehensive coverage across all categories.

