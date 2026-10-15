package main

import (
	"crypto/rand"
	"encoding/hex"
	"encoding/json"
	"fmt"
	"io"
	"log"
	"net"
	"net/http"
	"os"
	"path/filepath"
	"strings"
	"sync"
	"time"
)

type User struct {
	ID       string `json:"id"`
	Email    string `json:"email"`
	Name     string `json:"name"`
	Password string `json:"password"`
	Role     string `json:"role"`
	PIN      string `json:"pin"`
}

type OrderItem struct {
	DetailID string `json:"detail_id"`
	ItemID   int    `json:"item_id"`
	Name     string `json:"name"`
	Price    int    `json:"price"`
	Qty      int    `json:"qty"`
}

type Order struct {
	OrderID      string      `json:"order_id"`
	TableName    string      `json:"table_name"`
	OrderTime    string      `json:"order_time"`
	WaiterName   string      `json:"waiter_name"`
	WaiterEmail  string      `json:"waiter_email"`
	CustomerName string      `json:"customer_name"`
	Items        []OrderItem `json:"items"`
	SubTotal     int         `json:"sub_total"`
	Discount     int         `json:"discount"`
	Total        int         `json:"total"`
	PaidAmount   int         `json:"paid_amount"`
	DueAmount    int         `json:"due_amount"`
	PaymentType  string      `json:"payment_type"`
	Note         string      `json:"note"`
}

type ItemData struct {
	ID       int    `json:"id"`
	Name     string `json:"name"`
	Price    int    `json:"price"`
	Category string `json:"category"`
	Image    string `json:"image"`
}

type MenuDB struct {
	Categories []string   `json:"categories"`
	Items      []ItemData `json:"items"`
	Tables     []string   `json:"tables"`
}

type Config struct {
	OwnerPIN      string `json:"owner_pin"`
	CaptainPIN    string `json:"captain_pin"`
	ShopName      string `json:"shop_name"`
	ShopTagline   string `json:"shop_tagline"`
	ShopPhone     string `json:"shop_phone"`
	KpayPhone     string `json:"kpay_phone"`
	ReceiptFooter string `json:"receipt_footer"`
	PrinterName   string `json:"printer_name"`
	PaperSize     string `json:"paper_size"`
	PrintMode     string `json:"print_mode"`
	ServerIP      string `json:"server_ip"`
}

var mu sync.Mutex

func generateID(n int) string {
	b := make([]byte, n)
	rand.Read(b)
	return hex.EncodeToString(b)
}

func getLocalIP() string {
	addrs, err := net.InterfaceAddrs()
	if err == nil {
		for _, address := range addrs {
			if ipnet, ok := address.(*net.IPNet); ok && !ipnet.IP.IsLoopback() {
				if ipnet.IP.To4() != nil {
					return ipnet.IP.String()
				}
			}
		}
	}
	return "localhost"
}

func getConfig() Config {
	cfg := Config{
		OwnerPIN:      "1234",
		CaptainPIN:    "2222",
		ShopName:      "Sky Mother",
		ShopTagline:   "Hotel & Restaurant",
		ShopPhone:     "09-340339520",
		KpayPhone:     "09-783222755",
		ReceiptFooter: "Have a wonderful day! Thank You",
		PrinterName:   "Printer001",
		PaperSize:     "80mm",
		PrintMode:     "rawbt",
	}
	data, err := os.ReadFile("config.json")
	if err == nil {
		json.Unmarshal(data, &cfg)
	}
	if cfg.PrintMode == "" {
		cfg.PrintMode = "rawbt"
	}
	return cfg
}

func saveConfig(cfg Config) {
	data, _ := json.MarshalIndent(cfg, "", "  ")
	os.WriteFile("config.json", data, 0644)
}

func getUsers() []User {
	var users []User
	data, err := os.ReadFile("users.json")
	if err == nil {
		json.Unmarshal(data, &users)
	}
	if len(users) == 0 {
		users = []User{
			{ID: "usr_owner", Email: "soeaung.boy.zoe@gmail.com", Name: "Sky Mother", Password: "123", Role: "owner", PIN: "1234"},
			{ID: "usr_cap", Email: "captain@gmail.com", Name: "Captain", Password: "123", Role: "captain", PIN: "2222"},
			{ID: "usr_waiter", Email: "waiter1@gmail.com", Name: "Waiter 1", Password: "123", Role: "waiter", PIN: ""},
		}
		saveUsers(users)
	}
	return users
}

func saveUsers(users []User) {
	data, _ := json.MarshalIndent(users, "", "  ")
	os.WriteFile("users.json", data, 0644)
}

func getMenuDB() MenuDB {
	var db MenuDB
	data, err := os.ReadFile("data.json")
	if err == nil {
		json.Unmarshal(data, &db)
	}
	return db
}

func saveMenuDB(db MenuDB) {
	data, _ := json.MarshalIndent(db, "", "  ")
	os.WriteFile("data.json", data, 0644)
}

func autoRepairTablesAndDB() {
	mu.Lock()
	defer mu.Unlock()

	db := getMenuDB()
	db.Tables = []string{
		"A1", "A2", "Table 1", "Table 2", "Table 3", "Table 4", "Table 5", "Table 6", "Table 7", "Table 8", "Table 9", "V1", "V2",
		"K2", "K3",
		"101", "102", "103", "104", "105", "106", "107", "108", "109", "110",
		"201", "202", "203", "204", "205", "206", "207", "208", "209", "210",
	}

	usedIDs := make(map[int]bool)
	curID := 1001
	for i := range db.Items {
		if db.Items[i].ID <= 0 || usedIDs[db.Items[i].ID] {
			for usedIDs[curID] {
				curID++
			}
			db.Items[i].ID = curID
			curID++
		}
		usedIDs[db.Items[i].ID] = true
	}
	saveMenuDB(db)
	getUsers()
}

func getActiveOrders() map[string]Order {
	active := make(map[string]Order)
	data, err := os.ReadFile("active_orders.json")
	if err == nil {
		json.Unmarshal(data, &active)
	}
	return active
}

func saveActiveOrders(active map[string]Order) {
	data, _ := json.MarshalIndent(active, "", "  ")
	os.WriteFile("active_orders.json", data, 0644)
}

// Login Handler (Forgiving matching: Email, Role or Name, Password or PIN)
func loginHandler(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	if r.Method != http.MethodPost {
		w.WriteHeader(http.StatusMethodNotAllowed)
		json.NewEncoder(w).Encode(map[string]string{"error": "Method not allowed"})
		return
	}

	var req struct {
		Email    string `json:"email"`
		Password string `json:"password"`
	}
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		w.WriteHeader(http.StatusBadRequest)
		json.NewEncoder(w).Encode(map[string]string{"error": "Invalid JSON format"})
		return
	}

	mu.Lock()
	users := getUsers()
	mu.Unlock()

	reqInput := strings.ToLower(strings.TrimSpace(req.Email))
	reqPass := strings.TrimSpace(req.Password)

	for _, u := range users {
		matchUser := (strings.ToLower(u.Email) == reqInput || strings.ToLower(u.Role) == reqInput || strings.ToLower(u.Name) == reqInput)
		matchPass := (u.Password == reqPass || (u.PIN != "" && u.PIN == reqPass))
		if matchUser && matchPass {
			safeUser := map[string]interface{}{
				"id":    u.ID,
				"email": u.Email,
				"name":  u.Name,
				"role":  u.Role,
				"pin":   u.PIN,
			}
			json.NewEncoder(w).Encode(map[string]interface{}{"status": "success", "user": safeUser})
			return
		}
	}

	w.WriteHeader(http.StatusUnauthorized)
	json.NewEncoder(w).Encode(map[string]string{"error": "အကောင့် သို့မဟုတ် စကားဝှက် မှားယွင်းနေပါသည်"})
}

func usersHandler(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	mu.Lock()
	defer mu.Unlock()

	users := getUsers()

	if r.Method == http.MethodGet {
		var list []map[string]interface{}
		for _, u := range users {
			list = append(list, map[string]interface{}{
				"id":    u.ID,
				"email": u.Email,
				"name":  u.Name,
				"role":  u.Role,
				"pin":   u.PIN,
			})
		}
		json.NewEncoder(w).Encode(list)
		return
	}

	if r.Method == http.MethodPost {
		var nu User
		if err := json.NewDecoder(r.Body).Decode(&nu); err != nil {
			http.Error(w, err.Error(), http.StatusBadRequest)
			return
		}
		nu.Email = strings.ToLower(strings.TrimSpace(nu.Email))
		if nu.Email == "" || nu.Password == "" || nu.Name == "" {
			http.Error(w, "အချက်အလက်များ ပြည့်စုံစွာ ဖြည့်ပါ", http.StatusBadRequest)
			return
		}
		for _, ex := range users {
			if strings.ToLower(ex.Email) == nu.Email {
				http.Error(w, "ဤ Gmail ဖြင့် အကောင့်ရှိပြီးဖြစ်ပါသည်", http.StatusBadRequest)
				return
			}
		}
		nu.ID = "usr_" + generateID(4)
		users = append(users, nu)
		saveUsers(users)
		json.NewEncoder(w).Encode(map[string]string{"status": "success"})
		return
	}

	if r.Method == http.MethodDelete {
		uid := r.URL.Query().Get("id")
		if uid == "usr_owner" {
			http.Error(w, "ပင်မ Owner အကောင့်ကို ဖျက်၍မရပါ", http.StatusBadRequest)
			return
		}
		var updated []User
		for _, u := range users {
			if u.ID != uid {
				updated = append(updated, u)
			}
		}
		saveUsers(updated)
		json.NewEncoder(w).Encode(map[string]string{"status": "deleted"})
		return
	}

	http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
}

func activeHandler(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	mu.Lock()
	defer mu.Unlock()

	active := getActiveOrders()

	if r.Method == http.MethodGet {
		json.NewEncoder(w).Encode(active)
		return
	}

	if r.Method == http.MethodPost {
		var req struct {
			TableName   string      `json:"table_name"`
			WaiterName  string      `json:"waiter_name"`
			WaiterEmail string      `json:"waiter_email"`
			Items       []OrderItem `json:"items"`
		}
		if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
			http.Error(w, err.Error(), http.StatusBadRequest)
			return
		}

		ord, exists := active[req.TableName]
		if !exists {
			ord = Order{
				OrderID:     generateID(4),
				TableName:   req.TableName,
				OrderTime:   time.Now().Format("15:04:05"),
				WaiterName:  req.WaiterName,
				WaiterEmail: req.WaiterEmail,
				Items:       []OrderItem{},
				PaymentType: "ငွေသား",
			}
		}

		if req.WaiterName != "" {
			ord.WaiterName = req.WaiterName
		}
		if req.WaiterEmail != "" {
			ord.WaiterEmail = req.WaiterEmail
		}
		ord.Items = req.Items
		total := 0
		for _, it := range ord.Items {
			total += it.Price * it.Qty
		}
		ord.SubTotal = total
		ord.Total = total - ord.Discount
		ord.PaidAmount = ord.Total
		ord.DueAmount = 0

		active[req.TableName] = ord
		saveActiveOrders(active)

		json.NewEncoder(w).Encode(map[string]interface{}{"status": "success", "order": ord})
		return
	}

	if r.Method == http.MethodDelete {
		tableName := r.URL.Query().Get("table")
		if tableName != "" {
			delete(active, tableName)
			saveActiveOrders(active)
		}
		json.NewEncoder(w).Encode(map[string]string{"status": "deleted"})
		return
	}

	http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
}

func transferTableHandler(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	if r.Method != http.MethodPost {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}

	var req struct {
		FromTable string `json:"from_table"`
		ToTable   string `json:"to_table"`
	}
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}

	mu.Lock()
	defer mu.Unlock()

	active := getActiveOrders()
	ord, exists := active[req.FromTable]
	if !exists {
		http.Error(w, "မူလဝိုင်းတွင် အော်ဒါမရှိပါ", http.StatusBadRequest)
		return
	}

	ord.TableName = req.ToTable
	active[req.ToTable] = ord
	delete(active, req.FromTable)
	saveActiveOrders(active)

	json.NewEncoder(w).Encode(map[string]interface{}{"status": "success", "to_table": req.ToTable})
}

func checkoutHandler(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	if r.Method != http.MethodPost {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}

	var req struct {
		TableName    string `json:"table_name"`
		CustomerName string `json:"customer_name"`
		Discount     int    `json:"discount"`
		PaidAmount   int    `json:"paid_amount"`
		PaymentType  string `json:"payment_type"`
		Note         string `json:"note"`
		WaiterName   string `json:"waiter_name"`
		WaiterEmail  string `json:"waiter_email"`
	}
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}

	mu.Lock()
	defer mu.Unlock()

	active := getActiveOrders()
	ord, exists := active[req.TableName]
	if !exists || len(ord.Items) == 0 {
		http.Error(w, "အော်ဒါမရှိပါ", http.StatusBadRequest)
		return
	}

	sub := 0
	for _, it := range ord.Items {
		sub += it.Price * it.Qty
	}
	ord.SubTotal = sub
	ord.Discount = req.Discount
	ord.Total = sub - req.Discount
	if ord.Total < 0 {
		ord.Total = 0
	}

	ord.CustomerName = strings.TrimSpace(req.CustomerName)
	ord.PaidAmount = req.PaidAmount
	if ord.PaidAmount < 0 {
		ord.PaidAmount = 0
	}
	ord.DueAmount = ord.Total - ord.PaidAmount
	if ord.DueAmount < 0 {
		ord.DueAmount = 0
	}

	ord.PaymentType = req.PaymentType
	if ord.PaymentType == "" {
		ord.PaymentType = "ငွေသား"
	}
	ord.Note = strings.TrimSpace(req.Note)
	if req.WaiterName != "" {
		ord.WaiterName = req.WaiterName
	}
	if req.WaiterEmail != "" {
		ord.WaiterEmail = req.WaiterEmail
	}

	var paidOrders []Order
	pData, err := os.ReadFile("orders.json")
	if err == nil {
		json.Unmarshal(pData, &paidOrders)
	}
	paidOrders = append(paidOrders, ord)
	updatedPaid, _ := json.MarshalIndent(paidOrders, "", "  ")
	os.WriteFile("orders.json", updatedPaid, 0644)

	delete(active, req.TableName)
	saveActiveOrders(active)

	json.NewEncoder(w).Encode(map[string]interface{}{"status": "success", "order": ord})
}

func paidOrdersHandler(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	mu.Lock()
	defer mu.Unlock()
	data, err := os.ReadFile("orders.json")
	if err != nil {
		json.NewEncoder(w).Encode([]Order{})
		return
	}
	w.Write(data)
}

func buildCSVString() (string, []Order) {
	var orders []Order
	data, err := os.ReadFile("orders.json")
	if err == nil {
		json.Unmarshal(data, &orders)
	}

	var sb strings.Builder
	sb.WriteString("\xEF\xBB\xBF")
	sb.WriteString("Order ID,Table/Room,Time,Staff Name,Staff Email,Customer,Items Detail,SubTotal,Discount,Total,Paid,Due(Debt),Payment,Note\n")
	for _, o := range orders {
		itemsStr := ""
		for idx, it := range o.Items {
			if idx > 0 {
				itemsStr += " | "
			}
			itemsStr += fmt.Sprintf("%s x%d", it.Name, it.Qty)
		}
		sb.WriteString(fmt.Sprintf("\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",%d,%d,%d,%d,%d,\"%s\",\"%s\"\n",
			o.OrderID, o.TableName, o.OrderTime, o.WaiterName, o.WaiterEmail, o.CustomerName, itemsStr, o.SubTotal, o.Discount, o.Total, o.PaidAmount, o.DueAmount, o.PaymentType, o.Note))
	}
	return sb.String(), orders
}

func exportCsvHandler(w http.ResponseWriter, r *http.Request) {
	mu.Lock()
	csvStr, _ := buildCSVString()
	mu.Unlock()

	w.Header().Set("Content-Type", "text/csv; charset=utf-8")
	w.Header().Set("Content-Disposition", "attachment;filename=daily_sales.csv")
	w.Write([]byte(csvStr))
}

func itemsHandler(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	mu.Lock()
	defer mu.Unlock()

	db := getMenuDB()

	if r.Method == http.MethodGet {
		json.NewEncoder(w).Encode(db.Items)
		return
	}

	if r.Method == http.MethodPost {
		var it ItemData
		if err := json.NewDecoder(r.Body).Decode(&it); err != nil {
			http.Error(w, err.Error(), http.StatusBadRequest)
			return
		}
		maxID := 1000
		for _, ex := range db.Items {
			if ex.ID > maxID {
				maxID = ex.ID
			}
		}
		it.ID = maxID + 1
		db.Items = append(db.Items, it)
		saveMenuDB(db)
		json.NewEncoder(w).Encode(map[string]interface{}{"status": "success", "item": it})
		return
	}

	if r.Method == http.MethodPut {
		var it struct {
			Index    int    `json:"index"`
			ID       int    `json:"id"`
			Name     string `json:"name"`
			Price    int    `json:"price"`
			Category string `json:"category"`
			Image    string `json:"image"`
		}
		if err := json.NewDecoder(r.Body).Decode(&it); err != nil {
			http.Error(w, "JSON ဖတ်၍မရပါ", http.StatusBadRequest)
			return
		}

		matchedIdx := -1
		if it.Index >= 0 && it.Index < len(db.Items) {
			matchedIdx = it.Index
		} else if it.ID > 0 {
			for i := range db.Items {
				if db.Items[i].ID == it.ID {
					matchedIdx = i
					break
				}
			}
		}

		if matchedIdx == -1 {
			http.Error(w, "ပစ္စည်း ရှာမတွေ့ပါ", http.StatusNotFound)
			return
		}

		db.Items[matchedIdx].Name = it.Name
		db.Items[matchedIdx].Price = it.Price
		db.Items[matchedIdx].Category = it.Category
		if it.Image != "" {
			db.Items[matchedIdx].Image = it.Image
		}

		saveMenuDB(db)
		json.NewEncoder(w).Encode(map[string]string{"status": "updated"})
		return
	}

	if r.Method == http.MethodDelete {
		var req struct {
			ID int `json:"id"`
		}
		if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
			http.Error(w, err.Error(), http.StatusBadRequest)
			return
		}
		newItems := []ItemData{}
		for _, it := range db.Items {
			if it.ID != req.ID {
				newItems = append(newItems, it)
			}
		}
		db.Items = newItems
		saveMenuDB(db)
		json.NewEncoder(w).Encode(map[string]string{"status": "deleted"})
		return
	}

	http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
}

func uploadHandler(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	if r.Method != http.MethodPost {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}

	r.ParseMultipartForm(10 << 20)
	file, handler, err := r.FormFile("image")
	if err != nil {
		http.Error(w, "ပုံဖိုင် ဖတ်၍မရပါ", http.StatusBadRequest)
		return
	}
	defer file.Close()

	os.MkdirAll("frontend/uploads", 0755)
	ext := filepath.Ext(handler.Filename)
	if ext == "" {
		ext = ".jpg"
	}
	filename := fmt.Sprintf("%d_%s%s", time.Now().Unix(), generateID(3), ext)
	dstPath := filepath.Join("frontend/uploads", filename)

	dst, err := os.Create(dstPath)
	if err != nil {
		http.Error(w, "ဖိုင်သိမ်းဆည်း၍မရပါ", http.StatusInternalServerError)
		return
	}
	defer dst.Close()

	io.Copy(dst, file)
	json.NewEncoder(w).Encode(map[string]string{"url": "/uploads/" + filename})
}

func backupHandler(w http.ResponseWriter, r *http.Request) {
	mu.Lock()
	defer mu.Unlock()

	backupData := map[string]interface{}{
		"backup_time":   time.Now().Format("2006-01-02 15:04:05"),
		"config":        getConfig(),
		"users":         getUsers(),
		"menu_db":       getMenuDB(),
		"active_orders": getActiveOrders(),
	}

	var paidOrders []Order
	pData, err := os.ReadFile("orders.json")
	if err == nil {
		json.Unmarshal(pData, &paidOrders)
	}
	backupData["paid_orders"] = paidOrders

	w.Header().Set("Content-Type", "application/json")
	w.Header().Set("Content-Disposition", fmt.Sprintf("attachment;filename=skymother_backup_%s.json", time.Now().Format("20060102_150405")))
	json.NewEncoder(w).Encode(backupData)
}

func configHandler(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	mu.Lock()
	defer mu.Unlock()

	cfg := getConfig()

	if r.Method == http.MethodGet {
		cfg.ServerIP = fmt.Sprintf("http://%s:8080", getLocalIP())
		json.NewEncoder(w).Encode(cfg)
		return
	}

	if r.Method == http.MethodPost {
		var req Config
		json.NewDecoder(r.Body).Decode(&req)

		if req.ShopName != "" {
			cfg.ShopName = req.ShopName
		}
		if req.ShopTagline != "" {
			cfg.ShopTagline = req.ShopTagline
		}
		if req.ShopPhone != "" {
			cfg.ShopPhone = req.ShopPhone
		}
		if req.KpayPhone != "" {
			cfg.KpayPhone = req.KpayPhone
		}
		if req.ReceiptFooter != "" {
			cfg.ReceiptFooter = req.ReceiptFooter
		}
		if req.PrinterName != "" {
			cfg.PrinterName = req.PrinterName
		}
		if req.PaperSize != "" {
			cfg.PaperSize = req.PaperSize
		}
		if req.PrintMode != "" {
			cfg.PrintMode = req.PrintMode
		}

		saveConfig(cfg)
		json.NewEncoder(w).Encode(map[string]string{"status": "success"})
		return
	}

	http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
}

func frontendHandler(w http.ResponseWriter, r *http.Request) {
	if r.URL.Path == "/" {
		http.ServeFile(w, r, "frontend/index.html")
		return
	}
	filePath := filepath.Join("frontend", filepath.Clean(r.URL.Path))
	if fi, err := os.Stat(filePath); err == nil && !fi.IsDir() {
		http.ServeFile(w, r, filePath)
		return
	}
	http.ServeFile(w, r, "frontend/index.html")
}

func main() {
	autoRepairTablesAndDB()

	http.HandleFunc("/api/login", loginHandler)
	http.HandleFunc("/api/users", usersHandler)
	http.HandleFunc("/api/active", activeHandler)
	http.HandleFunc("/api/transfer-table", transferTableHandler)
	http.HandleFunc("/api/checkout", checkoutHandler)
	http.HandleFunc("/api/orders", paidOrdersHandler)
	http.HandleFunc("/api/export-csv", exportCsvHandler)
	http.HandleFunc("/api/items", itemsHandler)
	http.HandleFunc("/api/upload", uploadHandler)
	http.HandleFunc("/api/backup", backupHandler)
	http.HandleFunc("/api/config", configHandler)
	http.HandleFunc("/", frontendHandler)

	port := os.Getenv("PORT")
	if port == "" {
		port = "8080"
	}
	fmt.Printf("Sky Mother POS Server running on port %s\n", port)
	log.Fatal(http.ListenAndServe(":"+port, nil))
}
