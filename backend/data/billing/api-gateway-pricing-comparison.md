---
category: billing
subcategory: pricing
service: aws
difficulty: intermediate
last_updated: 2025-11-02
source: https://aws.amazon.com/api-gateway/pricing/
---

# Amazon API Gateway pricing

Amazon API Gateway

* [Overview](/api-gateway/)

* [Features](/api-gateway/features/)

* [Pricing](/api-gateway/pricing/)

* [Getting Started](/api-gateway/getting-started/)

* [Resources](/api-gateway/resources/)

* More

* [AWS](/)›
* [API Gateway](/api-gateway/)›
* [Pricing](/api-gateway/pricing/)

Amazon API Gateway pricing
==========================

[Get started for free](https://portal.aws.amazon.com/gp/aws/developer/registration/index.html?pg=apigateprice&cta=herobtn)

[Request a pricing quote](https://aws.amazon.com/contact-us/sales-support/?pg=apigateprice&cta=herobtn)

With Amazon API Gateway, you only pay when your APIs are in use. There are no minimum fees or upfront commitments. For HTTP APIs and REST APIs, you pay only for the API calls you receive and the amount of data transferred out. There are no data transfer out charges for Private APIs.

Starting July 15, 2025, new AWS customers will receive up to $200 in AWS Free Tier credits, which can be applied towards eligible AWS services, including Amazon API Gateway. At account sign-up, you can choose between a free plan and a paid plan. The free plan will be available for 6 months after account creation. If you upgrade to a paid plan, any remaining Free Tier credit balance will automatically apply to your AWS bills. All Free Tier credits must be used within 12 months of your account creation date. To learn more about the AWS Free Tier program, refer to [AWS Free Tier website](https://aws.amazon.com/free/) and [AWS Free Tier documentation](https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/free-tier.html).

Free Tier
---------

The Amazon API Gateway free tier includes **one million API calls** received for REST APIs, **one million API calls** received for HTTP APIs, and **one million messages** and **750,000 connection minutes** for WebSocket APIs per month for **up to 12 months**. If you exceed this number of calls per month, you will be charged the API Gateway usage rates.

Starting July 15, 2025, new AWS customers will receive up to $200 in AWS Free Tier credits, which can be applied towards eligible AWS services, including Amazon API Gateway. At account sign-up, you can choose between a free plan and a paid plan. The free plan will be available for 6 months after account creation. If you upgrade to a paid plan, any remaining Free Tier credit balance will automatically apply to your AWS bills. All Free Tier credits must be used within 12 months of your account creation date. To learn more about the AWS Free Tier program, refer to [AWS Free Tier website](https://aws.amazon.com/free/) and [AWS Free Tier documentation](https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/free-tier.html).

1M REST API CALLS RECEIVED | 1M HTTP API CALLS RECEIVED | 1M MESSAGES | 750,000 CONNECTION MINUTES

*per month*

These free tier offers are only available to new AWS customers, and are available for 12 months following your AWS sign-up date. When your 12 month free usage term expires or if your application use exceeds the tiers, you simply pay standard, pay-as-you-go service rates.

[Sign up for the Free Tier](https://console.aws.amazon.com/apigateway/home?region=us-east-1#/welcome)

HTTP APIs
---------

Pay only for the API calls you receive and the amount of data transferred out.

REST APIs
---------

Pay only for the API calls you receive and the amount of data transferred out. There are no data transfer out charges for Private APIs. However, [AWS PrivateLink](https://aws.amazon.com/vpc/pricing/) charges apply when using Private APIs in API Gateway. API Gateway also provides optional data caching charged at an hourly rate that varies based on the cache size you select.

WebSocket APIs
--------------

Pay only for messages sent and received and the total number of connection minutes. You may send and receive messages up to 128 kilobytes (KB) in size. Messages are metered in 32 KB increments. So, a 33 KB message is metered as two messages.

Additional Charges
------------------

You may incur additional charges if you use API Gateway in conjunction with other AWS services or transfer data out of AWS. For details on AWS service pricing, see the pricing section of the relevant AWS service detail pages. Links to pricing for some of the commonly used services are listed below.

[Data transfer](/ec2/pricing/)

*If you use external data transfers, you will be charged at the EC2 data transfer rate*

[AWS PrivateLink](https://aws.amazon.com/privatelink/pricing/)

*Includes pricing for each hour that your VPC endpoint is provisioned in each Availability Zone*

[AWS Lambda](/lambda/pricing/)

*Includes pricing for requests and duration*

[Amazon CloudWatch](/cloudwatch/pricing/)

*Includes pricing for metrics and dashboards*

Pricing Examples
----------------

### HTTP APIs

**Pricing Example 1:** An API is used in a Serverless Web Application that invokes Lambda to return dynamic webpage content. The site gets 10,000 page loads per minute. Each API request is 12KB and the response is 46 KB.

10,000 page loads/minute \* 60 minutes/hour \* 24 hours/day \* 30 days/month / 1,000,000 = 432 million requests per month.  
 300 million \* $1.00/million = $300  
 132 million \* $0.90/million = $118.8  
 Total = **$418.8 ($0.97 per million)**

**Pricing Example 2:** An API is used for uploading data into your HTTPS backend. The API is called 25 times per minute to upload documents. Each document is, on average, 4.5 MB in size.

25 call/minute \* 60 minutes/hour \* 24 hours/day \* 30 days/month \* 4.5 MB/512 KB/request = 9,720,000 requests per month \* $1/million = $9.72  
 **Total = $9.72**

### REST APIs

**Edge Optimized and Regional APIs**

An Edge Optimized or Regional API receives five million API calls per month, with each API call returning responses of 3 kilobytes (KB) in size with no caching.

*Example below reflects pricing for US East (N. Virginia, Ohio), US West (Oregon), Asia Pacific (Mumbai)*

Amazon API Gateway API call charges = 5 million \* $3.50/million = **$17.50**

Total size of data transfers = 3 KB \* 5 million = 15 million/KB = 14.3 GB

Amazon API Gateway data transfer charges = 14.3 GB \* $0.09 = **$1.29**

**Total Amazon API Gateway charges = $17.50 + $1.29 = $18.79**

**Edge Optimized and Regional APIs**

An Edge Optimized or Regional API receives 15 billion API calls per month, with each API call returning responses of 4 kilobytes (KB) in size with no caching.

*Example below reflects pricing for US East (N. Virginia, Ohio), US West (Oregon), Asia Pacific (Mumbai)*

Amazon API Gateway API call charges = 333 million \* $3.50/million = $1,165.50

                                                                     667 million \* $2.80/million = $1,867.60

                                                                     14 billion \* $2.38/million = $33,320.00

Total Amazon API call charges = $1,165.50 + $1,867.60 + $33,320.00 = **$36,353.10**

Total size of data transfers = 4 KB \* 15 billion = 57,220.46 GB

Amazon API Gateway data transfer charges = 57,220.46 GB \* $0.09 = **$5,149.84**

**Total Amazon API Gateway charges = $36,353.10 + $5,149.84 = $41,502.94**

**Private APIs**

A Private API receives five million API calls, with each API call having a request size of 0.3 kilobytes (KB) and returning responses of 3 kilobytes (KB). A VPC endpoint is provisioned in 1 Availability Zone (AZ) for the whole month (720 hours).

*Example below reflects pricing for US East, US West (Oregon)*

Amazon API Gateway API call charges = 5 million \* $3.50/million = **$17.50**

**Total Amazon API Gateway charges = $17.50**

Total size of data transfers (Request + Response) = (3 KB + 0.3 KB) \* 5 million = 16.5 million/KB = 15.7 GB

VPC Endpoint charges = 720 hours \* $0.01/AZ/hr = $7.20

VPC Endpoint data processing charges = 15.7 GB \* $0.01/GB = $0.16

**Total Amazon VPC (AWS PrivateLink) charges = $7.20 + $0.16 = $7.36**

**Total charges = $17.50 + $7.36 = $24.86**

**Pricing Example with Caching Required (US East, US West, EU (Ireland))**

If your API needs 1.5 GB of cache for its data, you can provision a 1.6 GB cache at $0.038/hr.

**$0.038 \* 24 = $0.912/day**

### WebSocket APIs

Chat Application: 1000 users are connected to the chat application for 12 hours in a day. Each user sends 100 messages and receives 500 messages per day. Each message size is 3KB.

*Example below reflects pricing in US East (N. Virginia)*

**Messaging Cost**

Total messages per month = (100 (sent msgs) + 500 (received msgs)) \* 1000 (users) \* 30 (days) = 18M

*Total messaging cost* = 18,000,000/1,000,000 \* $1.00 (per million) = $18

**Connectivity Cost**

Total connection minutes per month = 1000 (users) \* 12 (hrs) \* 60 (mins) \* 30 (days) = 21,600,000

*Total connectivity cost* = 21,600,000/1,000,000 \* 0.25 (cost per million) = $5.40

**Total Cost = $18 (Messaging cost) + $5.40 (Connectivity cost) = $23.40**

Additional pricing resources
----------------------------

[AWS Pricing Calculator](https://calculator.aws/)

Easily calculate your monthly costs with AWS

[Get Pricing Assistance](/contact-us/sales-support-pricing/)

Contact AWS specialists to get a personalized quote

Get started with Amazon API Gateway
-----------------------------------

![Next-Steps-Create-account](https://d1.awsstatic.com/onedam/marketing-channels/website/aws/public/development/pricing/webteam/product-pages/Next-Steps-Icon_Create-account.b8428f72dbf8227b0dc9e11abfb6ab415b1386b8.png "Next-Steps-Create-account")

**[Sign up for an AWS account](/free/)**

Instantly get access to the
[AWS Free Tier](/free/).

![Next-Steps-Icon_Tutorial](https://d1.awsstatic.com/onedam/marketing-channels/website/aws/public/development/pricing/webteam/product-pages/Next-Steps-Icon_Tutorial.cb7ace7b1156f2501902b027022e037b2e47a8a1.png "Next-Steps-Icon_Tutorial")

**[Learn through tutorials](https://docs.aws.amazon.com/apigateway/latest/developerguide/getting-started.html)**

Explore and learn with
[simple tutorials](https://docs.aws.amazon.com/apigateway/latest/developerguide/getting-started.html).

![Next Steps Icon](https://d1.awsstatic.com/onedam/marketing-channels/website/aws/public/development/pricing/webteam/product-pages/Next-Steps-Icon_Login.4ad2acc24677f43b1a357bfe7c49dba67cf0e321.png "Next Steps Icon")

**[Start building with AWS](https://console.aws.amazon.com/apigateway/home?region=us-east-1#/welcome)**

Visit the [AWS Management Console.](https://console.aws.amazon.com/apigateway/home?region=us-east-1#/welcome)