# Configuration & Best Practices Agent - Data Directory

## Purpose
This directory contains documentation for the **Configuration & Best Practices Agent** which uses a **Pure CAG (Cache-Augmented Generation)** strategy.

## Agent Behavior
- **Retrieval Strategy**: Pure CAG
- **How it works**: All best practices and configuration guides are loaded into memory at initialization. No runtime retrieval needed.
- **Use Case**: Best practices, security guidelines, architecture patterns, static configuration advice

## Data to Collect

### Categories to Include:

1. **Lambda Best Practices**
   - Function design patterns
   - Code organization
   - Handler best practices
   - Layers and dependencies
   - Runtime selection

2. **API Gateway Best Practices**
   - API design patterns
   - Resource organization
   - Stage management
   - Caching strategies
   - Request validation

3. **Security & IAM**
   - IAM roles and policies
   - Resource-based policies
   - API Gateway authorization
   - Lambda authorizers
   - Secrets management
   - VPC configuration

4. **Architecture Patterns**
   - Serverless architectures
   - Microservices patterns
   - Event-driven design
   - API versioning strategies
   - Multi-region setup

5. **Deployment Best Practices**
   - SAM templates
   - CDK patterns
   - CloudFormation best practices
   - CI/CD pipelines
   - Blue/green deployments
   - Canary deployments

6. **CORS & Networking**
   - CORS configuration
   - Custom domains
   - SSL/TLS setup
   - Private APIs
   - Network optimization

## File Naming Convention
Use descriptive names with hyphens:
- `lambda-best-practices.md`
- `iam-security-guidelines.md`
- `api-gateway-authorization.md`
- `serverless-architecture-patterns.md`

## Metadata Template
Each file should start with:
```markdown
---
category: configuration
subcategory: best_practices | security | architecture | deployment | networking
service: lambda | api-gateway | iam | cloudformation
difficulty: beginner | intermediate | advanced
last_updated: YYYY-MM-DD
---
```

## Target: 8-12 Documents
Focus on comprehensive, static guidance that rarely changes.

