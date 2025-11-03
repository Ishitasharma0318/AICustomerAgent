/**
 * API Client for Backend Communication
 * Handles all API requests to the FastAPI backend
 */

export interface Message {
  role: "user" | "assistant";
  content: string;
  agent_type?: string;
}

export interface ChatRequest {
  message: string;
  session_id?: string;
  conversation_history?: Message[];
}

export interface ChatResponse {
  response: string;
  agent_type: string;
  session_id: string;
  sources?: string[];
}

export interface StreamEvent {
  type: "metadata" | "progress" | "content" | "complete" | "error";
  session_id?: string;
  timestamp?: string;
  node?: string;
  content?: string;
  agent_type?: string;
  sources?: string[];
  duration?: number;
  error?: string;
}

export interface SessionHistory {
  session_id: string;
  message_count: number;
  history: Array<{
    role: string;
    content: string;
    agent_type?: string;
    timestamp: string;
  }>;
}

// Configuration
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

/**
 * API Client Class
 */
export class APIClient {
  private baseUrl: string;

  constructor(baseUrl: string = API_BASE_URL) {
    this.baseUrl = baseUrl;
  }

  /**
   * Send a chat message (non-streaming)
   */
  async chat(request: ChatRequest): Promise<ChatResponse> {
    const response = await fetch(`${this.baseUrl}/api/chat`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(request),
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({
        error: "Unknown error",
      }));
      throw new Error(error.error || `HTTP ${response.status}`);
    }

    return response.json();
  }

  /**
   * Send a chat message with streaming response
   */
  async *chatStream(request: ChatRequest): AsyncGenerator<StreamEvent, void, unknown> {
    const response = await fetch(`${this.baseUrl}/api/chat/stream`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(request),
    });

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }

    if (!response.body) {
      throw new Error("No response body");
    }

    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    let buffer = "";

    try {
      while (true) {
        const { done, value } = await reader.read();

        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split("\n");
        buffer = lines.pop() || "";

        for (const line of lines) {
          if (line.startsWith("data: ")) {
            const data = line.slice(6);
            try {
              const event: StreamEvent = JSON.parse(data);
              yield event;
            } catch (e) {
              console.error("Failed to parse SSE data:", e);
            }
          }
        }
      }
    } finally {
      reader.releaseLock();
    }
  }

  /**
   * Get session history
   */
  async getSessionHistory(sessionId: string): Promise<SessionHistory> {
    const response = await fetch(
      `${this.baseUrl}/api/sessions/${sessionId}/history`
    );

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }

    return response.json();
  }

  /**
   * Clear session
   */
  async clearSession(sessionId: string): Promise<void> {
    const response = await fetch(`${this.baseUrl}/api/sessions/${sessionId}`, {
      method: "DELETE",
    });

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }
  }

  /**
   * Health check
   */
  async healthCheck(): Promise<{ status: string; version: string }> {
    const response = await fetch(`${this.baseUrl}/health`);

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }

    return response.json();
  }
}

// Export singleton instance
export const apiClient = new APIClient();

