# OpenAI API Demo

A minimal Python application that demonstrates sending a request to OpenAI's gpt-3.5-turbo model.

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set your OpenAI API key as an environment variable:**

   **On Windows (Command Prompt):**
   ```cmd
   set OPENAI_API_KEY=your-api-key-here
   ```

   **On Windows (PowerShell):**
   ```powershell
   $env:OPENAI_API_KEY="your-api-key-here"
   ```

   **On Linux/Mac:**
   ```bash
   export OPENAI_API_KEY=your-api-key-here
   ```

## Usage

Run the demo script:
```bash
python openai_demo.py
```

The script will send a simple message to the OpenAI API and print the response.

## Note

Make sure you have a valid OpenAI API key. You can get one from [OpenAI's platform](https://platform.openai.com/api-keys).

---

# AWS Bedrock API Demo

A minimal Python application that demonstrates sending a request to Amazon Bedrock's Nova Micro model using boto3.

## Setup
1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
2. **Configure your AWS credentials:**
   - Set up AWS credentials (Access Key ID, Secret Access Key, and region) via `aws configure` or environment variables.
   - You may also set `AWS_BEARER_TOKEN_BEDROCK` if your organization requires a bearer token for Bedrock.
3. **Run the demo script:**
   ```bash
   python aws_demo.py
   ```

The script will send a simple message to the Amazon Bedrock Nova Micro model and print the response.

## Note
You need appropriate AWS permissions for Bedrock. See https://docs.aws.amazon.com/bedrock/latest/userguide/ for more info.



