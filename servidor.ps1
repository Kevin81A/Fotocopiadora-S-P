$puerto = 5500
$carpeta = $PSScriptRoot
$url = "http://localhost:$puerto/"

$listener = New-Object System.Net.HttpListener
$listener.Prefixes.Add($url)
$listener.Start()

Write-Host "Servidor iniciado en: http://localhost:$puerto/index.html" -ForegroundColor Green
Write-Host "Presiona Ctrl+C para detener" -ForegroundColor Yellow

Start-Process "http://localhost:$puerto/index.html"

$mimeTypes = @{
    ".html" = "text/html; charset=utf-8"
    ".css"  = "text/css; charset=utf-8"
    ".js"   = "application/javascript; charset=utf-8"
    ".json" = "application/json"
    ".png"  = "image/png"
    ".jpg"  = "image/jpeg"
    ".jpeg" = "image/jpeg"
    ".gif"  = "image/gif"
    ".svg"  = "image/svg+xml"
    ".ico"  = "image/x-icon"
    ".woff" = "font/woff"
    ".woff2"= "font/woff2"
    ".ttf"  = "font/ttf"
    ".map"  = "application/json"
}

while ($listener.IsListening) {
    $context = $listener.GetContext()
    $request = $context.Request
    $response = $context.Response

    $path = $request.Url.LocalPath
    if ($path -eq "/" -or $path -eq "") {
        $path = "/index.html"
    }

    $filePath = Join-Path $carpeta ($path.TrimStart("/").Replace("/", "\"))

    Write-Host "$(Get-Date -Format 'HH:mm:ss') $($request.HttpMethod) $path"

    if (Test-Path $filePath -PathType Leaf) {
        $ext = [System.IO.Path]::GetExtension($filePath).ToLower()
        $mime = $mimeTypes[$ext]
        if (-not $mime) { $mime = "application/octet-stream" }

        $bytes = [System.IO.File]::ReadAllBytes($filePath)
        $response.ContentType = $mime
        $response.ContentLength64 = $bytes.Length
        $response.StatusCode = 200
        $response.OutputStream.Write($bytes, 0, $bytes.Length)
    } else {
        $response.StatusCode = 404
        $msg = "404 - Not found: $path"
        $body = [System.Text.Encoding]::UTF8.GetBytes($msg)
        $response.ContentLength64 = $body.Length
        $response.OutputStream.Write($body, 0, $body.Length)
    }

    $response.OutputStream.Close()
}
