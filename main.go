package main import ( "bytes" 
    "encoding/json" "fmt" "io" 
    "log" "net/http" "os" 
    "path/filepath" "strings" 
    "time"
)
// ChatRequest represents the 
// incoming chat request
type ChatRequest struct { Message 
    string `json:"message"` Model 
    string 
    `json:"model,omitempty"`
}
// ChatResponse represents the 
// response structure
type ChatResponse struct { 
    Response string 
    `json:"response"` Status 
    string `json:"status"` 
    Timestamp string 
    `json:"timestamp"`
}
// OpenAI API structures
type OpenAIMessage struct { Role 
    string `json:"role"` Content 
    string `json:"content"`
}
type OpenAIRequest struct { Model 
    string `json:"model"` Messages 
    []OpenAIMessage 
    `json:"messages"`
}
type OpenAIResponse struct { 
    Choices []struct {
        Message OpenAIMessage 
        `json:"message"`
    } `json:"choices"`
}
func main() {
    // Frontend directory
    frontendDir := "frontend"
    
    // Static file server with 
    // proper headers
    fs := 
    http.FileServer(http.Dir(frontendDir)) 
    http.Handle("/", 
    http.HandlerFunc(func(w 
    http.ResponseWriter, r 
    *http.Request) {
        // Set proper MIME types
        ext := 
        filepath.Ext(r.URL.Path) 
        switch ext { case ".css":
            w.Header().Set("Content-Type", 
            "text/css; 
            charset=utf-8")
        case ".js": 
            w.Header().Set("Content-Type", 
            "application/javascript; 
            charset=utf-8")
        case ".html": 
            w.Header().Set("Content-Type", 
            "text/html; 
            charset=utf-8")
        case ".png": 
            w.Header().Set("Content-Type", 
            "image/png")
        case ".ico": 
            w.Header().Set("Content-Type", 
            "image/x-icon")
        case ".json": 
            w.Header().Set("Content-Type", 
            "application/json")
        }
        
        // Security headers
        w.Header().Set("X-Content-Type-Options", 
        "nosniff") 
        w.Header().Set("X-Frame-Options", 
        "SAMEORIGIN") 
        w.Header().Set("X-XSS-Protection", 
        "1; mode=block")
        
        fs.ServeHTTP(w, r)
    }))
    // Health check endpoint
    http.HandleFunc("/api/health", 
    func(w http.ResponseWriter, r 
    *http.Request) {
        w.Header().Set("Content-Type", 
        "application/json") 
        w.Header().Set("Access-Control-Allow-Origin", 
        "*") 
        w.WriteHeader(http.StatusOK)
        
        response := ChatResponse{ 
            Response: "🟢 
            MagicStone Web3 
            Dashboard Server is 
            healthy!", Status: 
            "healthy", Timestamp: 
            time.Now().Format(time.RFC3339),
        }
        json.NewEncoder(w).Encode(response)
    })
    // Wallet API endpoint
    http.HandleFunc("/api/wallet", 
    func(w http.ResponseWriter, r 
    *http.Request) {
        w.Header().Set("Content-Type", 
        "application/json") 
        w.Header().Set("Access-Control-Allow-Origin", 
        "*") 
        w.WriteHeader(http.StatusOK)
        
        walletData := 
        map[string]interface{}{
            "connected": true, 
            "address": 
            "0x742d35Cc6634C0532925a3b8D4C9db96590e4CAF", 
            "balance": "2.547 
            ETH", "network": 
            "Ethereum Mainnet", 
            "status": "active", 
            "timestamp": 
            time.Now().Format(time.RFC3339),
        }
        json.NewEncoder(w).Encode(walletData)
    })
    // AI Chat endpoint
    http.HandleFunc("/api/chat", 
    handleChat)
    // CORS preflight handler
    http.HandleFunc("/api/", 
    func(w http.ResponseWriter, r 
    *http.Request) {
        w.Header().Set("Access-Control-Allow-Origin", 
        "*") 
        w.Header().Set("Access-Control-Allow-Methods", 
        "GET, POST, OPTIONS") 
        w.Header().Set("Access-Control-Allow-Headers", 
        "Content-Type, 
        Authorization")
        
        if r.Method == "OPTIONS" { 
            w.WriteHeader(http.StatusOK) 
            return
        }
        
        http.NotFound(w, r)
    })
    // Port configuration
    port := os.Getenv("PORT") if 
    port == "" {
        port = "8080"
    }
    log.Printf("🚀 MagicStone Web3 
    Dashboard Starting...") 
    log.Printf("🌐 Server running 
    on port %s", port) 
    log.Printf("📂 Serving files 
    from ./%s", frontendDir) 
    log.Printf("🔗 Health: 
    http://localhost:%s/api/health", 
    port) log.Printf("💰 Wallet: 
    http://localhost:%s/api/wallet", 
    port) log.Printf("🤖 AI Chat: 
    http://localhost:%s/api/chat", 
    port)
    
    if err := 
    http.ListenAndServe(":"+port, 
    nil); err != nil {
        log.Fatal("🔥 Server 
        error:", err)
    }
}
func handleChat(w 
http.ResponseWriter, r 
*http.Request) {
    // CORS headers
    w.Header().Set("Access-Control-Allow-Origin", 
    "*") 
    w.Header().Set("Access-Control-Allow-Methods", 
    "POST, OPTIONS") 
    w.Header().Set("Access-Control-Allow-Headers", 
    "Content-Type") 
    w.Header().Set("Content-Type", 
    "application/json") if 
    r.Method == "OPTIONS" {
        w.WriteHeader(http.StatusOK) 
        return
    }
    if r.Method != "POST" { 
        http.Error(w, "Method not 
        allowed", 
        http.StatusMethodNotAllowed) 
        return
    }
    // Parse request
    var chatReq ChatRequest if err 
    := 
    json.NewDecoder(r.Body).Decode(&chatReq); 
    err != nil {
        log.Printf("Error parsing 
        request: %v", err) 
        http.Error(w, "Invalid 
        request format", 
        http.StatusBadRequest) 
        return
    }
    // Get OpenAI API key from 
    // environment
    apiKey := 
    os.Getenv("OPENAI_API_KEY") if 
    apiKey == "" {
        log.Println("⚠️ 
        OPENAI_API_KEY not found 
        in environment")
        // Return a helpful 
        // response instead of 
        // error
        response := ChatResponse{ 
            Response: "🤖 AI 
            Assistant: Hello! I'm 
            currently in demo 
            mode. To enable full 
            AI capabilities, 
            please configure the 
            OpenAI API key. How 
            can I help you with 
            Web3 and blockchain 
            questions?", Status: 
            "demo_mode", 
            Timestamp: 
            time.Now().Format(time.RFC3339),
        }
        json.NewEncoder(w).Encode(response) 
        return
    }
    // Call OpenAI API
    aiResponse, err := 
    callOpenAI(chatReq.Message, 
    apiKey) if err != nil {
        log.Printf("OpenAI API 
        error: %v", err) response 
        := ChatResponse{
            Response: "🤖 I'm 
            having trouble 
            connecting to the AI 
            service right now. 
            Please try again 
            later. In the 
            meantime, I can help 
            with basic Web3 
            questions!", Status: 
            "error", Timestamp: 
            time.Now().Format(time.RFC3339),
        }
        json.NewEncoder(w).Encode(response) 
        return
    }
    // Return successful response
    response := ChatResponse{ 
        Response: aiResponse, 
        Status: "success", 
        Timestamp: 
        time.Now().Format(time.RFC3339),
    }
    json.NewEncoder(w).Encode(response)
}
func callOpenAI(message, apiKey 
string) (string, error) {
    // Prepare OpenAI request
    openAIReq := OpenAIRequest{ 
        Model: "gpt-3.5-turbo", 
        Messages: []OpenAIMessage{
            { Role: "system", 
                Content: "You are 
                a helpful Web3 and 
                blockchain 
                assistant for 
                MagicStone 
                Dashboard. Provide 
                helpful, accurate 
                information about 
                cryptocurrency, 
                DeFi, NFTs, and 
                blockchain 
                technology.",
            },
            { Role: "user", 
                Content: message,
            },
        },
    }
    // Convert to JSON
    jsonData, err := 
    json.Marshal(openAIReq) if err 
    != nil {
        return "", err
    }
    // Create HTTP request
    req, err := 
    http.NewRequest("POST", 
    "https://api.openai.com/v1/chat/completions", 
    bytes.NewBuffer(jsonData)) if 
    err != nil {
        return "", err
    }
    // Set headers
    req.Header.Set("Content-Type", 
    "application/json") 
    req.Header.Set("Authorization", 
    "Bearer "+apiKey)
    // Make request
    client := 
    &http.Client{Timeout: 30 * 
    time.Second} resp, err := 
    client.Do(req) if err != nil {
        return "", err
    }
    defer resp.Body.Close()
    // Read response
    body, err := 
    io.ReadAll(resp.Body) if err 
    != nil {
        return "", err
    }
    // Parse OpenAI response
    var openAIResp OpenAIResponse 
    if err := json.Unmarshal(body, 
    &openAIResp); err != nil {
        return "", err
    }
    // Extract response
    if len(openAIResp.Choices) > 0 
    {
        return 
        openAIResp.Choices[0].Message.Content, 
        nil
    }
    return "I'm sorry, I couldn't 
    generate a response right 
    now.", nil
}
