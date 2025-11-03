"use client";

import { useState, useRef, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card } from "@/components/ui/card";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Badge } from "@/components/ui/badge";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { Send, Bot, User, Trash2, AlertCircle, CheckCircle, Loader2 } from "lucide-react";
import { apiClient, type StreamEvent } from "@/lib/api-client";

interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
  agentType?: string;
  sources?: string[];
  timestamp?: string;
  isStreaming?: boolean;
}

export function ChatInterface() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [sessionId, setSessionId] = useState<string>("");
  const [error, setError] = useState<string | null>(null);
  const [backendStatus, setBackendStatus] = useState<"checking" | "online" | "offline">("checking");
  const [currentProgress, setCurrentProgress] = useState<string>("");
  const scrollRef = useRef<HTMLDivElement>(null);

  // Check backend health on mount
  useEffect(() => {
    checkBackendHealth();
  }, []);

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages, isLoading]);

  const checkBackendHealth = async () => {
    try {
      await apiClient.healthCheck();
      setBackendStatus("online");
      setError(null);
    } catch (err) {
      setBackendStatus("offline");
      setError("Cannot connect to backend. Please ensure the API server is running at http://localhost:8000");
    }
  };

  const handleSend = async () => {
    if (!input.trim() || isLoading || backendStatus === "offline") return;

    const userMessage: Message = {
      id: `user-${Date.now()}`,
      role: "user",
      content: input,
      timestamp: new Date().toISOString(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setIsLoading(true);
    setError(null);
    setCurrentProgress("");

    // Create placeholder assistant message for streaming
    const assistantMessageId = `assistant-${Date.now()}`;
    const assistantMessage: Message = {
      id: assistantMessageId,
      role: "assistant",
      content: "",
      isStreaming: true,
      timestamp: new Date().toISOString(),
    };
    setMessages((prev) => [...prev, assistantMessage]);

    try {
      let fullResponse = "";
      let finalAgentType = "supervisor";
      let finalSources: string[] = [];

      // Stream the response
      const stream = apiClient.chatStream({
        message: userMessage.content,
        session_id: sessionId || undefined,
        conversation_history: messages
          .filter((m) => !m.isStreaming)
          .map((m) => ({
            role: m.role,
            content: m.content,
            agent_type: m.agentType,
          })),
      });

      for await (const event of stream) {
        handleStreamEvent(event, assistantMessageId, (content, agentType, sources) => {
          if (content) fullResponse += content; // Accumulate content chunks
          if (agentType) finalAgentType = agentType;
          if (sources) finalSources = sources;
        });
      }

      // Update final message
      setMessages((prev) =>
        prev.map((m) =>
          m.id === assistantMessageId
            ? {
                ...m,
                content: fullResponse,
                agentType: finalAgentType,
                sources: finalSources,
                isStreaming: false,
              }
            : m
        )
      );

      setCurrentProgress("");
    } catch (err) {
      console.error("Error sending message:", err);
      setError(err instanceof Error ? err.message : "An error occurred while processing your request");

      // Remove the streaming message on error
      setMessages((prev) => prev.filter((m) => m.id !== assistantMessageId));

      // Add error message
      const errorMessage: Message = {
        id: `error-${Date.now()}`,
        role: "assistant",
        content: "Sorry, I encountered an error processing your request. Please try again.",
        timestamp: new Date().toISOString(),
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleStreamEvent = (
    event: StreamEvent,
    messageId: string,
    updateCallback: (content: string, agentType?: string, sources?: string[]) => void
  ) => {
    switch (event.type) {
      case "metadata":
        if (event.session_id && !sessionId) {
          setSessionId(event.session_id);
        }
        break;

      case "progress":
        if (event.node) {
          setCurrentProgress(`Processing with ${event.node} agent...`);
        }
        break;

      case "content":
        if (event.content) {
          setMessages((prev) =>
            prev.map((m) =>
              m.id === messageId
                ? { ...m, content: m.content + event.content }
                : m
            )
          );
          updateCallback(event.content);
        }
        break;

      case "complete":
        if (event.agent_type || event.sources) {
          setMessages((prev) =>
            prev.map((m) =>
              m.id === messageId
                ? {
                    ...m,
                    agentType: event.agent_type,
                    sources: event.sources,
                  }
                : m
            )
          );
          updateCallback("", event.agent_type, event.sources);
        }
        setCurrentProgress("");
        break;

      case "error":
        setError(event.error || "An error occurred");
        break;
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const handleClearSession = async () => {
    if (!sessionId) {
      setMessages([]);
      return;
    }

    try {
      await apiClient.clearSession(sessionId);
      setMessages([]);
      setSessionId("");
      setError(null);
    } catch (err) {
      console.error("Error clearing session:", err);
      setError("Failed to clear session");
    }
  };

  const getAgentBadgeVariant = (agentType?: string) => {
    switch (agentType) {
      case "technical":
        return "technical";
      case "configuration":
        return "configuration";
      case "billing":
        return "billing";
      case "supervisor":
        return "supervisor";
      default:
        return "default";
    }
  };

  const getAgentDisplayName = (agentType?: string) => {
    switch (agentType) {
      case "technical":
        return "Technical Support";
      case "configuration":
        return "Configuration";
      case "billing":
        return "Billing & Pricing";
      case "supervisor":
        return "Supervisor";
      default:
        return "AI Assistant";
    }
  };

  return (
    <div className="flex flex-col h-screen max-w-4xl mx-auto p-4">
      {/* Header */}
      <Card className="p-6 mb-4">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold mb-2">AWS Support AI Assistant</h1>
            <p className="text-muted-foreground">
              Multi-agent system for Lambda and API Gateway support
            </p>
          </div>
          <div className="flex items-center gap-3">
            {/* Backend Status */}
            <div className="flex items-center gap-2">
              {backendStatus === "checking" && (
                <>
                  <Loader2 className="w-4 h-4 animate-spin text-yellow-500" />
                  <span className="text-sm text-muted-foreground">Checking...</span>
                </>
              )}
              {backendStatus === "online" && (
                <>
                  <CheckCircle className="w-4 h-4 text-green-500" />
                  <span className="text-sm text-green-600">Backend Online</span>
                </>
              )}
              {backendStatus === "offline" && (
                <>
                  <AlertCircle className="w-4 h-4 text-red-500" />
                  <span className="text-sm text-red-600">Backend Offline</span>
                </>
              )}
            </div>
            {/* Clear Session Button */}
            {messages.length > 0 && (
              <Button
                variant="outline"
                size="sm"
                onClick={handleClearSession}
                className="gap-2"
              >
                <Trash2 className="w-4 h-4" />
                Clear Chat
              </Button>
            )}
          </div>
        </div>
        {/* Session ID Display */}
        {sessionId && (
          <div className="mt-2 text-xs text-muted-foreground">
            Session: {sessionId.slice(0, 8)}...
          </div>
        )}
      </Card>

      {/* Error Alert */}
      {error && (
        <Alert variant="destructive" className="mb-4">
          <AlertCircle className="h-4 w-4" />
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}

      {/* Chat Messages */}
      <Card className="flex-1 mb-4 p-4 overflow-hidden">
        <ScrollArea className="h-full pr-4" ref={scrollRef}>
          {messages.length === 0 ? (
            <div className="flex flex-col items-center justify-center h-full text-center text-muted-foreground">
              <Bot className="w-16 h-16 mb-4 opacity-50" />
              <h2 className="text-xl font-semibold mb-2">
                Welcome to AWS Support AI
              </h2>
              <p className="max-w-md mb-4">
                Ask me anything about AWS Lambda, API Gateway, pricing, or best
                practices. I&apos;ll route your question to the right specialist!
              </p>
              <div className="flex flex-wrap gap-2 justify-center max-w-lg">
                <Badge variant="technical">Technical Support</Badge>
                <Badge variant="configuration">Configuration</Badge>
                <Badge variant="billing">Billing & Pricing</Badge>
              </div>
            </div>
          ) : (
            <div className="space-y-4">
              {messages.map((message) => (
                <div
                  key={message.id}
                  className={`flex ${
                    message.role === "user" ? "justify-end" : "justify-start"
                  }`}
                >
                  <div
                    className={`flex gap-3 max-w-[80%] ${
                      message.role === "user" ? "flex-row-reverse" : "flex-row"
                    }`}
                  >
                    <div
                      className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center ${
                        message.role === "user"
                          ? "bg-primary text-primary-foreground"
                          : "bg-muted"
                      }`}
                    >
                      {message.role === "user" ? (
                        <User className="w-5 h-5" />
                      ) : (
                        <Bot className="w-5 h-5" />
                      )}
                    </div>
                    <div
                      className={`rounded-lg p-4 ${
                        message.role === "user"
                          ? "bg-primary text-primary-foreground"
                          : "bg-muted"
                      }`}
                    >
                      <p className="whitespace-pre-wrap">
                        {message.content}
                        {message.isStreaming && (
                          <span className="inline-block w-2 h-4 ml-1 bg-current animate-pulse" />
                        )}
                      </p>
                      {message.agentType && (
                        <div className="mt-2 flex items-center gap-2">
                          <Badge variant={getAgentBadgeVariant(message.agentType) as any}>
                            {getAgentDisplayName(message.agentType)}
                          </Badge>
                        </div>
                      )}
                      {message.sources && message.sources.length > 0 && (
                        <div className="mt-2 text-xs opacity-70">
                          <p className="font-semibold mb-1">Sources:</p>
                          <ul className="list-disc list-inside">
                            {message.sources.slice(0, 3).map((source, idx) => (
                              <li key={idx}>{source}</li>
                            ))}
                          </ul>
                        </div>
                      )}
                    </div>
                  </div>
                </div>
              ))}
              {isLoading && currentProgress && (
                <div className="flex justify-start">
                  <div className="flex gap-3 max-w-[80%]">
                    <div className="flex-shrink-0 w-8 h-8 rounded-full bg-muted flex items-center justify-center">
                      <Bot className="w-5 h-5" />
                    </div>
                    <div className="rounded-lg p-4 bg-muted">
                      <div className="flex items-center gap-2">
                        <Loader2 className="w-4 h-4 animate-spin" />
                        <span className="text-sm">{currentProgress}</span>
                      </div>
                    </div>
                  </div>
                </div>
              )}
            </div>
          )}
        </ScrollArea>
      </Card>

      {/* Input Area */}
      <Card className="p-4">
        <div className="flex gap-2">
          <Input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Ask about Lambda, API Gateway, pricing, or best practices..."
            disabled={isLoading || backendStatus === "offline"}
            className="flex-1"
          />
          <Button
            onClick={handleSend}
            disabled={isLoading || !input.trim() || backendStatus === "offline"}
          >
            {isLoading ? (
              <Loader2 className="w-4 h-4 animate-spin" />
            ) : (
              <Send className="w-4 h-4" />
            )}
          </Button>
        </div>
        {backendStatus === "offline" && (
          <p className="text-xs text-red-600 mt-2">
            Backend is offline. Please start the API server.
          </p>
        )}
      </Card>
    </div>
  );
}

