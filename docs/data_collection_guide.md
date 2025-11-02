# 📚 Data Collection Guide for AWS Lambda + API Gateway Customer Service AI

## Overview
This guide will help you collect and organize AWS documentation for the three specialized agents. The goal is to gather **24-37 documents** total across all three categories.

---

## 🎯 Collection Strategy

### Time Estimate: 2-3 hours total
- Technical Support: 1 hour (10-15 docs)
- Configuration: 45 minutes (8-12 docs)
- Billing: 45 minutes (6-10 docs)

---

## 📝 Technical Support Agent (Pure RAG)
**Target: 10-15 documents**

### AWS Documentation URLs to Visit:

1. **Lambda Troubleshooting**
   - https://docs.aws.amazon.com/lambda/latest/dg/lambda-troubleshooting.html
   - https://docs.aws.amazon.com/lambda/latest/dg/monitoring-functions-logs.html
   - Copy sections on: timeouts, memory errors, permission issues

2. **Lambda Error Codes**
   - https://docs.aws.amazon.com/lambda/latest/dg/API_Invoke.html#API_Invoke_Errors
   - https://docs.aws.amazon.com/lambda/latest/dg/invocation-retries.html
   - Copy: Error code tables, retry behavior

3. **API Gateway Errors**
   - https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-error-codes.html
   - https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-troubleshooting.html
   - Copy: 4xx and 5xx error descriptions, integration errors

4. **Performance & Cold Starts**
   - https://docs.aws.amazon.com/lambda/latest/dg/foundation-arch.html
   - https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html
   - Copy sections on: cold start optimization, SnapStart

5. **VPC Connectivity**
   - https://docs.aws.amazon.com/lambda/latest/dg/foundation-networking.html
   - https://docs.aws.amazon.com/lambda/latest/dg/troubleshooting-vpc.html
   - Copy: VPC configuration issues, DNS resolution

6. **CloudWatch Debugging**
   - https://docs.aws.amazon.com/lambda/latest/dg/monitoring-cloudwatchlogs.html
   - Copy: Log format, debugging techniques

### Documents to Create:
```
backend/data/technical/
├── lambda-timeout-errors.md
├── lambda-memory-errors.md
├── lambda-permission-errors.md
├── api-gateway-502-errors.md
├── api-gateway-504-errors.md
├── api-gateway-integration-errors.md
├── cold-start-optimization.md
├── cloudwatch-debugging-guide.md
├── lambda-vpc-connectivity.md
├── lambda-concurrency-issues.md
├── lambda-deployment-errors.md
├── api-gateway-cors-errors.md
└── lambda-x-ray-tracing.md
```

---

## ⚙️ Configuration & Best Practices Agent (Pure CAG)
**Target: 8-12 documents**

### AWS Documentation URLs to Visit:

1. **Lambda Best Practices**
   - https://docs.aws.amazon.com/lambda/latest/dg/best-practices.html
   - Copy entire page, focus on: function design, performance, security

2. **API Gateway Best Practices**
   - https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-api-integration-types.html
   - https://docs.aws.amazon.com/apigateway/latest/developerguide/rest-api-develop.html
   - Copy: API design patterns, integration types

3. **Security & IAM**
   - https://docs.aws.amazon.com/lambda/latest/dg/lambda-security.html
   - https://docs.aws.amazon.com/lambda/latest/dg/lambda-intro-execution-role.html
   - https://docs.aws.amazon.com/apigateway/latest/developerguide/security.html
   - Copy: IAM roles, resource policies, authorization methods

4. **Lambda Authorizers**
   - https://docs.aws.amazon.com/apigateway/latest/developerguide/apigateway-use-lambda-authorizer.html
   - Copy entire guide

5. **CORS Configuration**
   - https://docs.aws.amazon.com/apigateway/latest/developerguide/how-to-cors.html
   - Copy: CORS setup for REST and HTTP APIs

6. **Architecture Patterns**
   - https://aws.amazon.com/lambda/architecture/
   - https://docs.aws.amazon.com/lambda/latest/operatorguide/design-patterns.html
   - Copy: Common patterns, event-driven architectures

7. **Deployment Best Practices**
   - https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/what-is-sam.html
   - https://docs.aws.amazon.com/lambda/latest/dg/deploying-lambda-apps.html
   - Copy: SAM, CDK, CloudFormation patterns

### Documents to Create:
```
backend/data/configuration/
├── lambda-best-practices.md
├── lambda-security-guidelines.md
├── iam-roles-and-policies.md
├── api-gateway-best-practices.md
├── api-gateway-authorization.md
├── lambda-authorizers-guide.md
├── cors-configuration.md
├── serverless-architecture-patterns.md
├── deployment-best-practices.md
├── lambda-layers-guide.md
└── environment-variables-management.md
```

---

## 💰 Billing & Pricing Agent (Hybrid RAG/CAG)
**Target: 6-10 documents**

### AWS Documentation URLs to Visit:

1. **Lambda Pricing**
   - https://aws.amazon.com/lambda/pricing/
   - Copy entire page: request pricing, duration pricing, architecture pricing

2. **API Gateway Pricing**
   - https://aws.amazon.com/api-gateway/pricing/
   - Copy: REST API, HTTP API, WebSocket pricing tables

3. **CloudWatch Pricing**
   - https://aws.amazon.com/cloudwatch/pricing/
   - Copy: Logs pricing, metrics pricing (as it relates to Lambda)

4. **Cost Optimization**
   - https://docs.aws.amazon.com/lambda/latest/dg/lambda-concurrency.html
   - https://aws.amazon.com/blogs/compute/operating-lambda-performance-optimization-part-1/
   - Copy: Cost optimization strategies

5. **Free Tier**
   - https://aws.amazon.com/free/
   - Search for Lambda and API Gateway free tier details

6. **Graviton/ARM Pricing**
   - https://aws.amazon.com/lambda/pricing/ (ARM section)
   - Copy: Cost comparison between x86 and ARM

### Documents to Create:
```
backend/data/billing/
├── lambda-pricing-details.md
├── api-gateway-pricing-comparison.md
├── cloudwatch-costs.md
├── cost-optimization-strategies.md
├── free-tier-limits.md
├── graviton-arm-cost-savings.md
├── provisioned-concurrency-pricing.md
└── billing-examples-calculations.md
```

---

## 📋 How to Collect Each Document

### Step-by-Step Process:

1. **Visit the AWS documentation URL**
2. **Copy relevant sections** (don't need entire pages, just relevant parts)
3. **Create a new .md file** in the appropriate directory
4. **Add metadata header** at the top:
   ```markdown
   ---
   category: technical | configuration | billing
   subcategory: (see README in each directory)
   service: lambda | api-gateway | cloudwatch
   difficulty: beginner | intermediate | advanced
   last_updated: 2024-11-02
   source: https://docs.aws.amazon.com/...
   ---
   
   # Title of Document
   
   ## Overview
   Brief summary...
   
   ## Content sections...
   ```

5. **Format the content** nicely in markdown
6. **Remove unnecessary AWS page navigation/footers**
7. **Keep code examples** if they exist
8. **Save the file**

---

## 🎨 Markdown Template

Use this template for each document:

```markdown
---
category: technical
subcategory: error_handling
service: lambda
difficulty: intermediate
last_updated: 2024-11-02
source: https://docs.aws.amazon.com/lambda/latest/dg/lambda-troubleshooting.html
---

# Lambda Timeout Errors

## Overview
Lambda function timeout errors occur when a function exceeds its configured timeout limit. The default timeout is 3 seconds, but it can be configured up to 15 minutes (900 seconds).

## Common Causes

1. **Inefficient code**: Unoptimized algorithms or unnecessary loops
2. **External API calls**: Slow or unresponsive third-party services
3. **Database queries**: Long-running or inefficient queries
4. **Cold start overhead**: Initial invocation takes longer

## How to Diagnose

### Check CloudWatch Logs
Look for this error message:
```
Task timed out after 3.00 seconds
```

### Review Function Duration
Use CloudWatch metrics to see function duration trends.

## Solutions

### 1. Increase Timeout Value
Configure timeout in function settings (max 900 seconds):
```python
# SAM template
Timeout: 60  # seconds
```

### 2. Optimize Code
- Use efficient algorithms
- Implement caching
- Use connection pooling for databases

### 3. Async Processing
For long-running tasks, use Step Functions or SQS.

## Prevention Tips
- Monitor function duration metrics
- Set appropriate timeout values
- Test with realistic data volumes
- Implement proper error handling

## Related Documentation
- CloudWatch Logs for debugging
- Performance optimization guide
- Asynchronous invocation patterns
```

---

## ✅ Quality Checklist

Before moving to Stage 2, ensure:

- [ ] Each directory has 6-15 documents
- [ ] All documents have proper metadata headers
- [ ] Content is accurate and from official AWS docs
- [ ] Markdown formatting is clean
- [ ] Code examples are included where relevant
- [ ] Source URLs are documented
- [ ] No outdated information (verify current as of 2024)

---

## 🚀 Quick Tips

### Time Savers:
1. **Focus on quality over quantity** - Better to have 10 excellent docs than 20 mediocre ones
2. **Use AWS search** - docs.aws.amazon.com has excellent search
3. **Copy-paste is OK** - This is official documentation, just format nicely
4. **Include examples** - Code snippets are valuable for the AI
5. **Document sources** - Always include the source URL

### Common Mistakes to Avoid:
- ❌ Mixing multiple topics in one file
- ❌ Forgetting metadata headers
- ❌ Including AWS page navigation/UI elements
- ❌ Using outdated pricing information
- ❌ Files that are too short (<200 words) or too long (>3000 words)

---

## 📞 Need Help?

If you get stuck:
1. Focus on one category at a time
2. Start with the easiest (Billing has fewer docs)
3. The AI will help validate and organize your data
4. You can always add more documents later

---

## ⏭️ Next Steps

Once you've collected all documents:
1. Review the `sample_queries.json` file
2. Test a few queries mentally against your documents
3. Let me know you're ready for Stage 2!

**Estimated completion time: 2-3 hours of focused work**

Good luck! 🎉

