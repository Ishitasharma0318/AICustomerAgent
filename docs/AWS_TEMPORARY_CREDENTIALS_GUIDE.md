# 🔐 Using Temporary AWS Credentials (Quick Setup)

**YES! Temporary credentials work perfectly for this project!**

---

## 📋 What You Need

Temporary AWS credentials include **3 pieces** (not 2!):

```
1. AWS_ACCESS_KEY_ID       → Starts with "ASIA"
2. AWS_SECRET_ACCESS_KEY   → Long random string
3. AWS_SESSION_TOKEN       → Very long token (starts with "IQo" or "FwoG")
```

⚠️ **Missing the session token is why it's not working!**

---

## 🎯 Quick Setup (2 Options)

### Option 1: Use Our Helper Script (EASIEST)

```bash
cd backend
./setup_aws_credentials.sh
```

It will prompt you for:
- AWS_ACCESS_KEY_ID
- AWS_SECRET_ACCESS_KEY
- AWS_SESSION_TOKEN
- AWS_REGION (optional, defaults to us-east-1)

Then automatically test the connection!

### Option 2: Manual Setup

1. Get your credentials (see next section)
2. Open `backend/.env` in a text editor
3. Add these lines:

```env
AWS_ACCESS_KEY_ID=ASIA...your_key_here
AWS_SECRET_ACCESS_KEY=your_secret_here
AWS_SESSION_TOKEN=your_very_long_token_here
AWS_REGION=us-east-1
```

4. Save the file
5. Test: `python test_connections.py`

---

## 📍 Where to Get Your Credentials

### From AWS Console (Regular Account)

1. **Log in** to https://console.aws.amazon.com
2. Click your **username** (top right corner)
3. Select **"Command line or programmatic access"**
4. You'll see a section like this:

```bash
Option 1: Set AWS environment variables (macOS and Linux)

export AWS_ACCESS_KEY_ID="ASIAQ3EGSYG7EXAMPLE"
export AWS_SECRET_ACCESS_KEY="7DJIZDSg+//YrEyIbKbuhfExample"
export AWS_SESSION_TOKEN="IQoJb3JpZ2luX2VjEBQaCXVzLWVhc3QtMSJH..."
```

5. **Copy all three values!**

### From AWS Academy (Students)

1. Start your lab
2. Click **"AWS Details"** button
3. Click **"Show"** next to "AWS CLI:"
4. You'll see:

```bash
[default]
aws_access_key_id=ASIAQ3EGSYG7EXAMPLE
aws_secret_access_key=7DJIZDSg+//YrEyIbKbuhfExample
aws_session_token=IQoJb3JpZ2luX2VjEBQaCXVzLWVhc3QtMSJH...
```

5. **Copy all three values!**

### From AWS SSO/IAM Identity Center

1. Log in through your SSO portal
2. Click on the account you want to use
3. Select **"Command line or programmatic access"**
4. Choose **"Option 1: Set AWS environment variables"**
5. **Copy all three values!**

---

## ✅ Complete Example

Here's what your `.env` file should look like with temporary credentials:

```env
# OpenAI
OPENAI_API_KEY=sk-proj-your_openai_key_here

# AWS Temporary Credentials (ALL THREE REQUIRED!)
AWS_ACCESS_KEY_ID=ASIAQ3EGSYG75OQJL3G3
AWS_SECRET_ACCESS_KEY=7DJIZDSg+//YrEyIbKbuhfLxVn3PWfk2EXgPWDtB
AWS_SESSION_TOKEN=IQoJb3JpZ2luX2VjEBQaCXVzLWVhc3QtMSJHMEUCIQDJz8Z9V...
AWS_REGION=us-east-1

# Application Settings
ENVIRONMENT=development
DEBUG=True
CHROMA_PERSIST_DIRECTORY=./chroma_db
CHROMA_COLLECTION_NAME=aws_docs
API_HOST=0.0.0.0
API_PORT=8000
ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

**Key Points:**
- ✅ No spaces after equals signs
- ✅ No quotes around values
- ✅ Session token is usually 500-1000 characters long
- ✅ All on one line (no line breaks in the token)

---

## 🧪 Test Your Setup

After adding credentials:

```bash
cd backend
source venv/bin/activate
python test_connections.py
```

**Expected Output:**
```
[1/4] Checking environment variables...
  ✓ OpenAI API key found
  ✓ AWS Access Key found
  ✓ AWS Secret Key found
  ✓ AWS Region: us-east-1

[2/4] Testing OpenAI connection...
  ✓ OpenAI connected successfully!

[3/4] Testing AWS Bedrock connection...
  ✓ AWS Bedrock connected successfully!

[4/4] Testing ChromaDB connection...
  ✓ ChromaDB connected successfully!

======================================================================
🎉 ALL TESTS PASSED!
======================================================================
```

---

## ⏰ How Long Do Temporary Credentials Last?

| Source | Duration | Refresh Method |
|--------|----------|----------------|
| AWS Console | 1-12 hours | Get new credentials |
| AWS Academy | Until lab stops | Restart lab → Get new credentials |
| AWS SSO | 1-12 hours | Re-login → Get new credentials |

### When Credentials Expire

You'll see this error:
```
ExpiredTokenException: The security token included in the request is expired
```

**Fix:** Just get new credentials and update `.env` file!

---

## 🎯 Will This Work for Your Project?

### ✅ YES! Perfect for:
- Development and testing
- Learning and experimentation
- Short coding sessions (1-12 hours)
- AWS Academy students
- This specific project

### ⚠️ Limitations:
- Need to refresh every few hours
- Can't use for production deployment
- Need to update `.env` each session

### 💡 Pro Tip:
Create a permanent IAM user later if you want:
- No expiration
- More convenient
- But temporary credentials work great for now!

---

## 🚀 Quick Start Commands

```bash
# Navigate to backend
cd /Users/ishitasharma/Documents/GitHub/AI_Customer_Agent/backend

# Option A: Use helper script
./setup_aws_credentials.sh

# Option B: Edit .env manually
nano .env
# (Add AWS_SESSION_TOKEN line)
# (Save and exit)

# Test
python test_connections.py

# If all tests pass, you're ready for Stage 4!
```

---

## ❓ FAQ

**Q: My credentials have spaces after the equals sign, does that matter?**  
A: YES! No spaces allowed. Use:
```env
AWS_ACCESS_KEY_ID=ASIA...  ✅
NOT: AWS_ACCESS_KEY_ID= ASIA...  ❌
```

**Q: The session token is really long, is that normal?**  
A: Yes! Session tokens are typically 500-1000 characters. That's correct.

**Q: Can I commit my .env file?**  
A: NO! Never commit credentials to Git. `.env` is already in `.gitignore`.

**Q: Do I need to restart my terminal after updating .env?**  
A: No, but you need to rerun your Python script so it reloads the .env file.

**Q: Can I export these to my terminal instead?**  
A: Yes, but `.env` file is cleaner:
```bash
export AWS_ACCESS_KEY_ID="ASIA..."
export AWS_SECRET_ACCESS_KEY="..."
export AWS_SESSION_TOKEN="..."
```

**Q: Will these credentials work with boto3?**  
A: Yes! Boto3 automatically reads from .env via python-dotenv.

---

## 📞 Still Not Working?

Try this diagnostic:

```bash
cd backend
source venv/bin/activate

python << 'EOF'
import os
from dotenv import load_dotenv
load_dotenv()

print("Checking credentials...")
print(f"Access Key: {os.getenv('AWS_ACCESS_KEY_ID')[:10]}...")
print(f"Secret Key: {'✓ Present' if os.getenv('AWS_SECRET_ACCESS_KEY') else '✗ Missing'}")
print(f"Session Token: {'✓ Present' if os.getenv('AWS_SESSION_TOKEN') else '✗ Missing'}")
print(f"Region: {os.getenv('AWS_REGION')}")
EOF
```

**Expected Output:**
```
Access Key: ASIAQ3EGS...
Secret Key: ✓ Present
Session Token: ✓ Present
Region: us-east-1
```

If Session Token shows "✗ Missing", that's your issue!

---

**Created:** November 3, 2025  
**For:** AI Customer Service Agent Project  
**Works with:** AWS Console, AWS Academy, AWS SSO

