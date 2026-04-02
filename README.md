## 🌐 External Usage (Burp Community / Real Targets)

By default, this tool works in **internal networks**.

However, if you're using **Burp Suite Community Edition** (which does not include Burp Collaborator), you can use this tool as a **replacement for both internal and external testing**.

### 🔓 To Use Externally

You need to expose your local server to the internet.

#### Option 1 — Using ngrok (Recommended)

1. Start the tool:

```bash
python ssrf_rfi_tool.py --ip 127.0.0.1
```

2. Expose ports:

```bash
ngrok http 8000
ngrok http 9000
```

3. Use the generated public URLs:

```
https://xxxx.ngrok.io/<TOKEN>
https://xxxx.ngrok.io/rfi.php
```

---

### 🔁 Replace Internal IP with Public URL

Instead of:

```
http://192.168.1.50:8000/<TOKEN>
```

Use:

```
https://your-ngrok-url/<TOKEN>
```

---

### ⚠️ Important Notes

* SSRF requires the target server to reach your exposed URL
* Some targets block HTTP → try HTTPS (ngrok helps here)
* Use separate tunnels for ports 8000 and 9000 if needed

---

### 💡 Pro Tip

If your payload works internally but not externally:

* Target likely restricts outbound traffic
* Use **internal pivoting instead of ngrok**
