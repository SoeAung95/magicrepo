package main

import (
		"context"
			"encoding/json"
				"fmt"
					"log"
						"net/http"
							"os"
								"path/filepath"
									"time"

										"github.com/aws/aws-sdk-go-v2/aws"
											"github.com/aws/aws-sdk-go-v2/config"
												"github.com/aws/aws-sdk-go-v2/service/secretsmanager"
											)

											type HealthResponse struct {
													Status    string `json:"status"`
														Message   string `json:"message"`
															Timestamp string `json:"timestamp"`
														}

														type WalletResponse struct {
																Status  string `json:"status"`
																	Message string `json:"message"`
																		Balance string `json:"balance"`
																			Address string `json:"address"`
																		}

																		type APIKeysResponse struct {
																				Status string            `json:"status"`
																					Keys   map[string]string `json:"keys"`
																				}

																				type SecretsManager struct {
																						client *secretsmanager.Client
																					}

																					func NewSecretsManager() (*SecretsManager, error) {
																							cfg, err := config.LoadDefaultConfig(context.TODO())
																								if err != nil {
																											return nil, err
																												}
																													return &SecretsManager{
																																client: secretsmanager.NewFromConfig(cfg),
																																	}, nil
																																}

																																func (sm *SecretsManager) GetSecret(secretName string) (string, error) {
																																		result, err := sm.client.GetSecretValue(context.TODO(), &secretsmanager.GetSecretValueInput{
																																					SecretId: aws.String(secretName),
																																						})
																																							if err != nil {
																																										return "", err
																																											}
																																												return *result.SecretString, nil
																																											}

																																											var secretsManager *SecretsManager

																																											func healthHandler(w http.ResponseWriter, r *http.Request) {
																																													w.Header().Set("Content-Type", "application/json")
																																														w.Header().Set("Access-Control-Allow-Origin", "*")
																																															
																																															response := HealthResponse{
																																																		Status:    "healthy",
																																																				Message:   "For-iOS server",
																																																						Timestamp: time.Now().Format(time.RFC3339),
																																																							}
																																																								json.NewEncoder(w).Encode(response)
																																																							}

																																																							func walletHandler(w http.ResponseWriter, r *http.Request) {
																																																									w.Header().Set("Content-Type", "application/json")
																																																										w.Header().Set("Access-Control-Allow-Origin", "*")
																																																											
																																																											response := WalletResponse{
																																																														Status:  "connected",
																																																																Message: "Wallet connected",
																																																																		Balance: "2.547 ETH",
																																																																				Address: "0x1234...5678",
																																																																					}
																																																																						json.NewEncoder(w).Encode(response)
																																																																					}

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

																																																																																																																																				func main() {
																																																																																																																																						var err error
																																																																																																																																							secretsManager, err = NewSecretsManager()
																																																																																																																																								if err != nil {
																																																																																																																																											fmt.Printf("Warning: %v\n", err)
																																																																																																																																												}

																																																																																																																																													http.HandleFunc("/api/health", healthHandler)
																																																																																																																																														http.HandleFunc("/api/wallet", walletHandler)
																																																																																																																																															http.HandleFunc("/api/keys", apiKeysHandler)
																																																																																																																																																http.HandleFunc("/", frontendHandler)

																																																																																																																																																	port := os.Getenv("PORT")
																																																																																																																																																		if port == "" {
																																																																																																																																																					port = "8080"
																																																																																																																																																						}

																																																																																																																																																							fmt.Printf("Server starting on port %s\n", port)
																																																																																																																																																								log.Fatal(http.ListenAndServe(":"+port, nil))
																																																																																																																																																							}
