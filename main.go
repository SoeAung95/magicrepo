<<<<<<< HEAD
mkdir frontend
cd frontend
nano index.html
nano style.css
nano wallet.js
=======
package main

import (
	"log"
	"net/http"
)

func main() {
	fs := http.FileServer(http.Dir("frontend"))
	http.Handle("/", fs)

	port := ":8080"
	log.Println("🌐 Server running at http://localhost" + port + " ...")

	err := http.ListenAndServe(port, nil)
	if err != nil {
		log.Fatal("🔥 Server error:", err)
	}
}
>>>>>>> a0e12f3 (Initial commit)
