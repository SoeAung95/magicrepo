package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"os"
	"path/filepath"
	"time"
)

// Response structs
type HealthResponse struct {
	Status string `json:"status"`
	Time   string `json:"time"`
}

type WalletResponse struct {
	Status  string `json:"status"`
	Balance string `json:"balance"`
}

type APIKeysResponse struct {
	Status string            `json:"status"`
	Keys   map[string]string `json:"keys"`
}

// SecretsManager struct
type SecretsManager struct {
	secrets map[string]string
}

// Global secrets manager
var secretsManager *SecretsManager

// NewSecretsManager creates a new secrets manager
func NewSecretsManager() (*SecretsManager, error) {
	// Initialize with dummy secrets for testing
	secrets := map[string]string{
		"openai-api-key":  "sk-1234567890abcdef",
		"binance-api-key": "abc123def456ghi789",
	}
	
	return &SecretsManager{
		secrets: secrets,
	}, nil
}

// GetSecret retrieves a secret by name
func (sm *SecretsManager) GetSecret(name string) (string, error) {
	if secret, exists := sm.secrets[name]; exists {
		return secret, nil
	}
	return "", fmt.Errorf("secret %s not found", name)
}

// healthHandler handles health check requests
func healthHandler(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	w.Header().Set("Access-Control-Allow-Origin", "*")
	
	response := HealthResponse{
		Status: "healthy",
		Time:   time.Now().Format(time.RFC3339),
	}
	json.NewEncoder(w).Encode(response)
}

// walletHandler handles wallet balance requests
func walletHandler(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	w.Header().Set("Access-Control-Allow-Origin", "*")
	
	response := WalletResponse{
		Status:  "success",
		Balance: "1000.00",
	}
	json.NewEncoder(w).Encode(response)
}

// apiKeysHandler handles API keys requests with masking
func apiKeysHandler(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	w.Header().Set("Access-Control-Allow-Origin", "*")
	
	keys := make(map[string]string)
	secretNames := []string{"openai-api-key", "binance-api-key"}
	
	for _, secretName := range secretNames {
		secret, err := secretsManager.GetSecret(secretName)
		if err != nil {
			keys[secretName] = "Error: " + err.Error()
		} else {
			if len(secret) > 4 {
				keys[secretName] = secret[:4] + "****"
			} else {
				keys[secretName] = "****"
			}
		}
	}
	
	response := APIKeysResponse{
		Status: "success",
		Keys:   keys,
	}
	json.NewEncoder(w).Encode(response)
}

// frontendHandler serves static files and SPA routing
func frontendHandler(w http.ResponseWriter, r *http.Request) {
	if r.URL.Path == "/" {
		http.ServeFile(w, r, "frontend/index.html")
		return
	}
	
	filePath := filepath.Join("frontend", r.URL.Path[1:])
	if _, err := os.Stat(filePath); err == nil {
		http.ServeFile(w, r, filePath)
		return
	}
	http.ServeFile(w, r, "frontend/index.html")
}

// main function - entry point
func main() {
	var err error
	secretsManager, err = NewSecretsManager()
	if err != nil {
		fmt.Printf("Warning: %v\n", err)
	}
	
	// Register route handlers
	http.HandleFunc("/api/health", healthHandler)
	http.HandleFunc("/api/wallet", walletHandler)
	http.HandleFunc("/api/keys", apiKeysHandler)
	http.HandleFunc("/", frontendHandler)
	
	// Get port from environment or use default
	port := os.Getenv("PORT")
	if port == "" {
		port = "8080"
	}
	
	fmt.Printf("Server starting on port %s\n", port)
	log.Fatal(http.ListenAndServe(":"+port, nil))
}
