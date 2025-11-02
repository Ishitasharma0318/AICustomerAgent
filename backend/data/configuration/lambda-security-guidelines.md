---
category: configuration
subcategory: security
service: lambda
difficulty: intermediate
last_updated: 2025-11-02
source: https://docs.aws.amazon.com/lambda/latest/dg/lambda-security.html
---

# Security in AWS Lambda

Security in AWS Lambda
======================

Cloud security at AWS is the highest priority. As an AWS customer, you benefit from a data center and
network architecture that is built to meet the requirements of the most security-sensitive organizations.

Security is a shared responsibility between AWS and you. The [shared responsibility model](https://aws.amazon.com/compliance/shared-responsibility-model/) describes this as security
*of* the cloud and security *in* the cloud:

* **Security of the cloud** – AWS is responsible for protecting the
  infrastructure that runs AWS services in the AWS Cloud. AWS also provides you with services that you can
  use securely. Third-party auditors regularly test and verify the effectiveness of our security as part of the
  [AWS compliance programs](https://aws.amazon.com/compliance/programs/). To learn about the
  compliance programs that apply to AWS Lambda, see [AWS services in Scope by Compliance Program](https://aws.amazon.com/compliance/services-in-scope/).
* **Security in the cloud** – Your responsibility is determined by the
  AWS service that you use. You are also responsible for other factors including the sensitivity of your data,
  your company’s requirements, and applicable laws and regulations.

This documentation helps you understand how to apply the shared responsibility model when using Lambda. The
following topics show you how to configure Lambda to meet your security and compliance objectives. You also learn how
to use other AWS services that help you to monitor and secure your Lambda resources.

For more information about applying security principles to Lambda applications, see
[Security](https://serverlessland.com/content/service/lambda/guides/aws-lambda-operator-guide/security-ops)
in Serverless Land.

###### Topics

* [Data protection in AWS Lambda](./security-dataprotection.html)
* [Identity and Access Management for AWS Lambda](./security-iam.html)
* [Create a governance strategy for Lambda functions and layers](./governance-concepts.html)
* [Compliance validation for AWS Lambda](./security-compliance.html)
* [Resilience in AWS Lambda](./security-resilience.html)
* [Infrastructure security in AWS Lambda](./security-infrastructure.html)
* [Securing workloads with public endpoints](./security-public-endpoints.html)
* [Using code signing to verify code integrity with Lambda](./configuration-codesigning.html)