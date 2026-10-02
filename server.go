package main

import (
	"fmt"
	"net/http"
	"os/exec"
	"runtime"
)

func main() {
	port := "5500"
	url := "http://localhost:" + port + "/index.html"

	fs := http.FileServer(http.Dir("."))
	http.Handle("/", fs)

	fmt.Println("╔══════════════════════════════════════════════╗")
	fmt.Println("║   Fotocopiadora SyP — Servidor local        ║")
	fmt.Println("╠══════════════════════════════════════════════╣")
	fmt.Printf( "║   URL: http://localhost:%s/index.html       ║\n", port)
	fmt.Println("║   Presiona Ctrl+C para detener               ║")
	fmt.Println("╚══════════════════════════════════════════════╝")

	// Abrir el navegador automáticamente
	go openBrowser(url)

	if err := http.ListenAndServe(":"+port, nil); err != nil {
		fmt.Println("Error:", err)
	}
}

func openBrowser(url string) {
	var err error
	switch runtime.GOOS {
	case "windows":
		err = exec.Command("rundll32", "url.dll,FileProtocolHandler", url).Start()
	case "darwin":
		err = exec.Command("open", url).Start()
	default:
		err = exec.Command("xdg-open", url).Start()
	}
	if err != nil {
		fmt.Println("No se pudo abrir el navegador automáticamente.")
		fmt.Println("Abre manualmente:", url)
	}
}
