---
category: configuration
subcategory: best_practices
service: lambda
difficulty: intermediate
last_updated: 2025-11-02
source: https://docs.aws.amazon.com/lambda/latest/dg/best-practices.html
---

# Best practices for working with AWS Lambda functions

Best practices for working with AWS Lambda functions
====================================================

The following are recommended best practices for using AWS Lambda:

###### Topics

* [Function code](#function-code)
* [Function configuration](#function-configuration)
* [Function scalability](#function-scalability)
* [Metrics and alarms](#alarming-metrics)
* [Working with streams](#stream-events)
* [Security best practices](#security-best-practices)

Function code
-------------

**Take advantage of execution environment reuse to improve the performance of your
function.** Initialize SDK clients and database connections outside of the function handler, and
cache static assets locally in the `/tmp` directory. Subsequent invocations processed by
the same instance of your function can reuse these resources. This saves cost by reducing function run time.

To avoid potential data leaks across invocations, don’t use the execution environment to store user data,
events, or other information with security implications. If your function relies on a mutable state that can’t
be stored in memory within the handler, consider creating a separate function or separate versions of a
function for each user.

**Use a keep-alive directive to maintain persistent connections.** Lambda purges idle connections over time.
Attempting to reuse an idle connection when invoking a function will result in a connection error. To maintain your persistent connection, use the
keep-alive directive associated with your runtime.
For an example, see [Reusing Connections with Keep-Alive in Node.js](https://docs.aws.amazon.com/sdk-for-javascript/v3/developer-guide/node-reusing-connections.html).

**Use [environment variables](./configuration-envvars.html) to pass operational parameters to your function.** For example, if
you are writing to an Amazon S3 bucket, instead of hard-coding the bucket name you are writing to, configure the
bucket name as an environment variable.

**Avoid using recursive invocations** in your Lambda function, where the function
invokes itself or initiates a process that may invoke the function again. This could lead to unintended volume of
function invocations and escalated costs. If you see an unintended volume of invocations, set the function reserved concurrency
to `0` immediately to throttle all invocations to the function, while you update the
code.

**Do not use non-documented, non-public APIs** in your Lambda function code.
For AWS Lambda managed runtimes, Lambda periodically applies security and functional updates to Lambda's internal APIs.
These internal API updates may be backwards-incompatible, leading to unintended consequences such as invocation
failures if your function has a dependency on these non-public APIs. See
[the API reference](https://docs.aws.amazon.com/lambda/latest/api/welcome.html) for a list of
publicly available APIs.

**Write idempotent code.** Writing idempotent code for your functions ensures that
duplicate events are handled the same way. Your code should properly validate events and gracefully handle
duplicate events. For more information, see
[How do I make
my Lambda function idempotent?](https://aws.amazon.com/premiumsupport/knowledge-center/lambda-function-idempotent/).

###### Note

You can use Powertools for AWS Lambda to make functions idempotent. For more information, see:

* [Python - Idempotency utility](https://docs.aws.amazon.com/powertools/python/latest/utilities/idempotency/)
* [TypeScript - Idempotency utility](https://docs.aws.amazon.com/powertools/typescript/latest/features/idempotency/)
* [Java - Idempotency utility](https://docs.aws.amazon.com/powertools/java/latest/utilities/idempotency/)
* [.NET - Idempotency utility](https://docs.aws.amazon.com/powertools/dotnet/utilities/idempotency/)

For language-specific code best practices, refer to the following sections:

* [Code best practices for Node.js Lambda functions](./nodejs-handler.html#nodejs-best-practices)
* [Code best practices for TypeScript Lambda functions](./typescript-handler.html#typescript-best-practices)
* [Code best practices for Python Lambda functions](./python-handler.html#python-handler-best-practices)
* [Code best practices for Ruby Lambda functions](./ruby-handler.html#ruby-best-practices)
* [Code best practices for Java Lambda functions](./java-handler.html#java-best-practices)
* [Code best practices for Go Lambda functions](./golang-handler.html#go-best-practices)
* [Code best practices for C# Lambda functions](./csharp-handler.html#csharp-best-practices)
* [Code best practices for Rust Lambda functions](./rust-handler.html#rust-best-practices)

Function configuration
----------------------

**Performance testing your Lambda function** is a crucial part in ensuring
you pick the optimum memory size configuration. Any increase in memory size triggers an equivalent increase in
CPU available to your function. The memory usage for your function is determined per-invoke and can be viewed
in [Amazon CloudWatch](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/WhatIsCloudWatchLogs.html). On each invoke a
`REPORT:` entry will be made, as shown below:

```
REPORT RequestId: 3604209a-e9a3-11e6-939a-754dd98c7be3	Duration: 12.34 ms	Billed Duration: 100 ms Memory Size: 128 MB	Max Memory Used: 18 MB
```

By analyzing the `Max Memory Used:` field, you can determine if your function needs more memory
or if you over-provisioned your function's memory size.

**To find the right memory configuration** for your functions, we recommend
using the open source AWS Lambda Power Tuning project. For more information, see
[AWS Lambda Power Tuning](https://github.com/alexcasalboni/aws-lambda-power-tuning) on GitHub.

To optimize function performance, we also recommend deploying libraries that can leverage
Advanced Vector Extensions 2 (AVX2). This allows you to process demanding workloads, including
machine learning inferencing, media processing, high performance computing (HPC), scientific
simulations, and financial modeling. For more information, see
[Creating faster AWS Lambda functions with AVX2](https://aws.amazon.com/blogs/compute/creating-faster-aws-lambda-functions-with-avx2/).

**Load test your Lambda function** to determine an optimum timeout value. It
is important to analyze how long your function runs so that you can better determine any problems with a
dependency service that may increase the concurrency of the function beyond what you expect. This is
especially important when your Lambda function makes network calls to resources that may not handle Lambda's
scaling. For more information about load testing your application, see
[Distributed Load Testing on AWS](https://aws.amazon.com/solutions/implementations/distributed-load-testing-on-aws/).

**Use most-restrictive permissions when setting IAM policies.** Understand
the resources and operations your Lambda function needs, and limit the execution role to these permissions. For
more information, see [Managing permissions in AWS Lambda](./lambda-permissions.html).

**Be familiar with [Lambda quotas](./gettingstarted-limits.html).** Payload
size, file descriptors and /tmp space are often overlooked when determining runtime resource limits.

**Delete Lambda functions that you are no longer using.** By doing so, the
unused functions won't needlessly count against your deployment package size limit.

**If you are using Amazon Simple Queue Service** as an event source, make sure the value of the
function's expected invocation time does not exceed the [Visibility Timeout](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-visibility-timeout.html) value on the queue. This applies both to [CreateFunction](https://docs.aws.amazon.com/lambda/latest/api/API_CreateFunction.html) and
[UpdateFunctionConfiguration](https://docs.aws.amazon.com/lambda/latest/api/API_UpdateFunctionConfiguration.html).

* In the case of **CreateFunction**, AWS Lambda will fail the function
  creation process.
* In the case of **UpdateFunctionConfiguration**, it could result in
  duplicate invocations of the function.

Function scalability
--------------------

**Be familiar with your upstream and downstream throughput constraints.**
While Lambda functions scale seamlessly with load, upstream and downstream dependencies may not have the
same throughput capabilities. If you need to limit how high your function can scale, you can
[configure reserved concurrency](./configuration-concurrency.html) on your function.

**Build in throttle tolerance.** If your synchronous function
experiences throttling due to traffic exceeding Lambda's scaling rate, you can use the following
strategies to improve throttle tolerance:

* **Use [timeouts, retries, and backoff with jitter](https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/)**. Implementing these strategies
  smooth out retried invocations, and helps ensure Lambda can scale up within seconds to minimize
  end-user throttling.
* **Use [provisioned concurrency](./provisioned-concurrency.html)**.
  Provisioned concurrency is the number of pre-initialized execution environments that Lambda
  allocates to your function. Lambda handles incoming requests using provisioned concurrency
  when available. Lambda can also scale your function above and beyond your provisioned
  concurrency setting if required. Configuring provisioned concurrency incurs additional charges
  to your AWS account.

Metrics and alarms
------------------

**Use [Using CloudWatch metrics with Lambda](./monitoring-metrics.html) and
 [CloudWatch Alarms](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/AlarmThatSendsEmail.html)** instead of creating or
updating a metric from within your Lambda function code. It's a much more efficient way to track the health of
your Lambda functions, allowing you to catch issues early in the development process. For instance, you can
configure an alarm based on the expected duration of your Lambda function invocation in order to address
any bottlenecks or latencies attributable to your function code.

**Emit custom metrics asynchronously using Embedded Metric Format (EMF).**
Instead of making synchronous API calls to CloudWatch, use EMF to emit metrics through your function's logs.
This approach reduces latency and improves performance. The Metrics utility in Powertools for AWS Lambda
handles EMF formatting automatically. For more information, see
[Python](https://docs.aws.amazon.com/powertools/python/latest/core/metrics/),
[TypeScript](https://docs.aws.amazon.com/powertools/typescript/latest/features/metrics/),
[Java](https://docs.aws.amazon.com/powertools/java/latest/core/metrics/), or
[.NET](https://docs.aws.amazon.com/powertools/dotnet/core/metrics/)
Metrics utilities in the Powertools for AWS Lambda documentation. For information on using EMF to generate metric format logs,
see [Publishing logs with the embedded metric format](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Embedded_Metric_Format_Generation.html) in the Amazon CloudWatch User Guide.

**Use structured JSON logging for better observability.**
Structured logging makes it easier to search, filter, and analyze your function's logs. Consider using
the Logger utility from Powertools for AWS Lambda to automatically format logs in JSON. For more information, see
[Python](https://docs.aws.amazon.com/powertools/python/latest/core/logger/),
[TypeScript](https://docs.aws.amazon.com/powertools/typescript/latest/features/logger/),
[Java](https://docs.aws.amazon.com/powertools/java/latest/core/logging/), or
[.NET](https://docs.aws.amazon.com/powertools/dotnet/core/logging/)
Logger utilities in the Powertools for AWS Lambda documentation.

**Leverage your logging library and [AWS Lambda Metrics and Dimensions](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/lam-metricscollected.html)** to catch
app errors (e.g. ERR, ERROR, WARNING, etc.)

**Use [AWS Cost Anomaly Detection](https://docs.aws.amazon.com/cost-management/latest/userguide/manage-ad.html)** to detect unusual activity on your account.
Cost Anomaly Detection uses machine learning to continuously monitor your cost and usage while minimizing false positive alerts. Cost Anomaly Detection uses data from AWS Cost Explorer, which has a delay of up to 24 hours.
As a result, it can take up to 24 hours to detect an anomaly after usage occurs. To get started with Cost Anomaly Detection, you must first  [sign up for Cost Explorer](https://docs.aws.amazon.com/cost-management/latest/userguide/ce-enable.html).
Then, [access Cost Anomaly Detection](https://docs.aws.amazon.com/cost-management/latest/userguide/settingup-ad.html#access-ad).

Working with streams
--------------------

**Test with different batch and record sizes** so that the polling frequency
of each event source is tuned to how quickly your function is able to complete its task. The
[CreateEventSourceMapping](https://docs.aws.amazon.com/lambda/latest/api/API_CreateEventSourceMapping.html) BatchSize parameter controls the maximum number of
records that can be sent to your function with each invoke. A larger batch size can often more efficiently
absorb the invoke overhead across a larger set of records, increasing your throughput.

By default, Lambda invokes your function as soon as records are available. If the batch
that Lambda reads from the event source has only one record in it, Lambda sends only one record to the function. To avoid invoking the function
with a small number of records, you can tell the event source to buffer records for up to 5 minutes by configuring a
*batching window*. Before invoking the function, Lambda continues to read records from the event source
until it has gathered a full batch, the batching window expires, or the batch reaches the payload limit of 6 MB. For more information,
see [Batching behavior](./invocation-eventsourcemapping.html#invocation-eventsourcemapping-batching).

###### Warning

Lambda event source mappings process each event at least once, and duplicate processing of records can occur. To avoid potential issues
related to duplicate events, we strongly recommend that you make your function code idempotent. To learn more, see [How do I make my Lambda function idempotent](https://repost.aws/knowledge-center/lambda-function-idempotent)
in the AWS Knowledge Center.

**Enable partial batch response for stream processing.**
When processing batches of records from streams like Kinesis or DynamoDB Streams, enable partial batch response
to allow Lambda to retry only the failed records instead of the entire batch. This improves processing
efficiency and reduces unnecessary reprocessing. You can optionally use the Batch utility from Powertools
for AWS Lambda to simplify batch processing patterns.

###### Note

You can use Powertools for AWS Lambda for batch processing. For more information, see:

* [Python - Batch Processing](https://docs.aws.amazon.com/powertools/python/latest/utilities/batch/)
* [TypeScript - Batch Processing](https://docs.aws.amazon.com/powertools/typescript/latest/features/batch/)
* [Java - Batch Processing](https://docs.aws.amazon.com/powertools/java/latest/utilities/batch/)
* [.NET - Batch Processing](https://docs.aws.amazon.com/powertools/dotnet/utilities/batch-processing/)

**Increase Kinesis stream processing throughput by adding shards.** A
Kinesis stream is composed of one or more shards. The rate at which Lambda can read data from Kinesis
scales linearly with the number of shards. Increasing the number of shards will directly increase
the number of maximum concurrent Lambda function invocations and can increase your Kinesis stream
processing throughput. For more information about the relationship between shards and function
invocations, see [Polling and batching streams](./with-kinesis.html#kinesis-polling-and-batching). If you are increasing the number of
shards in a Kinesis stream, make sure you have picked a good partition key (see [Partition Keys](https://docs.aws.amazon.com/streams/latest/dev/key-concepts.html#partition-key)) for your data, so that
related records end up on the same shards and your data is well distributed.

**Use [Amazon CloudWatch](https://docs.aws.amazon.com/streams/latest/dev/monitoring-with-cloudwatch.html)** on IteratorAge to determine if your Kinesis stream is being processed. For
example, configure a CloudWatch alarm with a maximum setting to 30000 (30 seconds).

Security best practices
-----------------------

**Monitor your usage of AWS Lambda as it relates to security best practices by using
AWS Security Hub.** Security Hub uses security controls to evaluate resource configurations and security standards to help
you comply with various compliance frameworks. For more information about using Security Hub to evaluate Lambda
resources, see [AWS Lambda controls](https://docs.aws.amazon.com/securityhub/latest/userguide/lambda-controls.html) in the AWS Security Hub User Guide.

**Monitor Lambda network activity logs using Amazon GuardDuty Lambda Protection.** GuardDuty Lambda protection
helps you identify potential security threats when Lambda functions are invoked in your AWS account. For example, if one of your
functions queries an IP address that is associated with cryptocurrency-related activity. GuardDuty monitors the network activity logs that
are generated when a Lambda function is invoked. To learn more, see [Lambda protection](https://docs.aws.amazon.com/guardduty/latest/ug/lambda-protection.html)
in the *Amazon GuardDuty User Guide*.