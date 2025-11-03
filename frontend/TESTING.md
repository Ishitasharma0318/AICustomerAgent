# Frontend Testing Guide

## Prerequisites

Before testing the frontend, ensure:
1. Backend API is running on `http://localhost:8000`
2. ChromaDB is populated with data
3. Environment variables are set

## Setup

### 1. Install Dependencies

```bash
cd frontend
npm install
```

### 2. Create Environment File

Create `frontend/.env.local` with:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 3. Start Development Server

```bash
npm run dev
```

The frontend will be available at: `http://localhost:3000`

---

## Manual Testing Checklist

### ✅ Backend Connection Test

**Steps**:
1. Open `http://localhost:3000`
2. Check backend status indicator in header

**Expected**:
- If backend is running: Green "Backend Online" indicator
- If backend is down: Red "Backend Offline" indicator with error message

---

### ✅ Technical Support Query (Pure RAG)

**Test Query**: "My Lambda function is timing out after 3 seconds"

**Expected Results**:
- [ ] Query sent to backend
- [ ] Progress indicator shows "Processing with supervisor agent..."
- [ ] Progress indicator shows "Processing with technical agent..."
- [ ] Response streams character by character
- [ ] Blue "Technical Support" badge displayed
- [ ] Source documents listed (if available)
- [ ] Session ID appears in header

---

### ✅ Configuration Query (Pure CAG)

**Test Query**: "What are Lambda security best practices?"

**Expected Results**:
- [ ] Query sent to backend
- [ ] Progress indicators appear
- [ ] Response streams in
- [ ] Green "Configuration" badge displayed
- [ ] Comprehensive best practices provided

---

### ✅ Billing Query (Hybrid RAG/CAG)

**Test Query 1**: "How much does Lambda cost per million requests?"

**Expected Results**:
- [ ] First query uses RAG (retrieves pricing docs)
- [ ] Purple "Billing & Pricing" badge displayed
- [ ] Pricing information provided

**Test Query 2** (same session): "What about API Gateway costs?"

**Expected Results**:
- [ ] Second query uses cached data (CAG)
- [ ] Faster response
- [ ] Purple "Billing & Pricing" badge displayed

---

### ✅ Multi-turn Conversation

**Test**:
1. Ask: "How much does Lambda cost?"
2. Follow up: "What are some cost optimization strategies?"
3. Follow up: "Can you explain the free tier?"

**Expected Results**:
- [ ] All queries maintain conversation context
- [ ] Session ID remains consistent
- [ ] Responses reference previous messages
- [ ] History builds up in chat window

---

### ✅ Session Management

**Test**:
1. Send several messages
2. Click "Clear Chat" button

**Expected Results**:
- [ ] All messages cleared from UI
- [ ] Session ID cleared
- [ ] Ready for new conversation
- [ ] No errors

---

### ✅ Streaming Display

**Test**: Send any query and watch the response

**Expected Results**:
- [ ] Blinking cursor appears while waiting
- [ ] Text streams in character by character
- [ ] Progress indicator shows which agent is processing
- [ ] Smooth animation
- [ ] Final message includes agent badge

---

### ✅ Error Handling

**Test 1**: Stop the backend and send a message

**Expected Results**:
- [ ] Backend status changes to "Offline"
- [ ] Red error alert appears
- [ ] Input field disabled
- [ ] Helpful error message displayed

**Test 2**: Start backend again and refresh page

**Expected Results**:
- [ ] Backend status changes to "Online"
- [ ] Error message disappears
- [ ] Input field enabled
- [ ] Can send messages

---

### ✅ UI/UX Features

**Loading States**:
- [ ] Spinning loader in send button while processing
- [ ] Progress indicator with agent name
- [ ] Blinking cursor in streaming message
- [ ] Disabled input while processing

**Agent Badges**:
- [ ] Blue badge for Technical Support
- [ ] Green badge for Configuration
- [ ] Purple badge for Billing & Pricing
- [ ] Gray badge for Supervisor (if any)

**Sources Display**:
- [ ] Sources section appears for RAG queries
- [ ] Up to 3 sources listed
- [ ] Styled appropriately

**Auto-scroll**:
- [ ] Chat automatically scrolls to new messages
- [ ] Works during streaming
- [ ] Smooth scrolling behavior

---

## Keyboard Shortcuts

- `Enter`: Send message
- `Shift + Enter`: New line (if multi-line input enabled)

---

## Sample Test Queries

### Technical Support
- "My API Gateway is returning 502 errors"
- "Lambda function timing out"
- "How do I debug cold starts?"
- "VPC connectivity issues with Lambda"

### Configuration
- "Lambda best practices"
- "How to configure CORS in API Gateway?"
- "IAM roles for Lambda"
- "Lambda deployment strategies"

### Billing
- "Lambda pricing"
- "API Gateway costs"
- "Free tier limits"
- "Cost optimization strategies"

---

## Performance Expectations

| Action | Expected Time |
|--------|--------------|
| Backend health check | <500ms |
| Send message | <100ms |
| Receive first token | 1-3s |
| Complete response | 3-6s |
| Clear session | <100ms |

---

## Common Issues

### Issue: "Cannot connect to backend"
**Solution**: 
1. Check if backend is running: `curl http://localhost:8000/health`
2. Start backend: `cd backend && python main.py`

### Issue: Streaming not working
**Solution**: 
1. Check browser console for errors
2. Verify NEXT_PUBLIC_API_URL is set correctly
3. Check backend logs for streaming endpoint

### Issue: No agent badges showing
**Solution**: 
1. Verify backend is returning agent_type in response
2. Check browser console for errors
3. Ensure Badge component is imported correctly

### Issue: Messages not auto-scrolling
**Solution**: 
1. Check scrollRef is attached to ScrollArea
2. Verify useEffect dependencies include messages

---

## Browser Compatibility

Tested on:
- ✅ Chrome 120+
- ✅ Firefox 120+
- ✅ Safari 17+
- ✅ Edge 120+

---

## Screenshots Checklist

For documentation/demo, capture:
- [ ] Welcome screen (empty chat)
- [ ] Technical query with response
- [ ] Configuration query with response
- [ ] Billing query with response
- [ ] Multi-turn conversation
- [ ] Streaming in progress
- [ ] Agent badges display
- [ ] Sources display
- [ ] Error state (backend offline)
- [ ] Session ID display

---

## Accessibility

- [ ] All buttons have accessible labels
- [ ] Keyboard navigation works
- [ ] Screen reader friendly
- [ ] Color contrast meets WCAG standards
- [ ] Focus indicators visible

---

## Next Steps

After manual testing:
1. Fix any identified bugs
2. Improve UX based on findings
3. Add any missing features
4. Prepare for demo video
5. Document any limitations

---

**Testing Status**: Ready for comprehensive testing
**Last Updated**: November 3, 2025

