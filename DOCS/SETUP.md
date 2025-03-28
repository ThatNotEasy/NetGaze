# 📡 Capture Network Traffic on Android with mitmproxy

This guide will help you capture network traffic on an **Android device** using **mitmproxy** without root access while bypassing **SSL encryption (HTTPS interception)**.

---

## 🛠️ Requirements  
Before getting started, ensure you have the following:  

- 📱 **Android device** (no root required)  
- 💻 **PC/Laptop** with **mitmproxy installed**  
- 🌐 **Same WiFi network** for both Android and PC  
- 🐍 **mitmproxy**, install it via:

  ```bash
  pip install mitmproxy
  ```

---

## 🔁 Steps  

### 1️⃣ Run mitmproxy on Your PC  
Open a terminal and run one of the following commands:  

Without GUI:  
```bash
mitmproxy --mode transparent --listen-port 8080
```  
With GUI (optional):  
```bash
mitmweb --listen-port 8080
```

---

### 2️⃣ Configure Android to Use Proxy  

1. Connect your Android device to the **same WiFi network** as your PC.  
2. Go to **WiFi Settings** > **Edit network** > **Advanced Options**.  
3. Set up the proxy manually:  
   - **Proxy hostname**: Enter your **PC's IP address**  
   - **Proxy port**: `8080`  

---

### 3️⃣ Install mitmproxy Certificate on Android  

1. Open a browser on your Android device and visit:  
   ```
   http://mitm.it
   ```
2. Select **Android** and download the certificate (`mitmproxy-ca-cert.pem`).  
3. Rename the file to:  
   ```
   mitmproxy-ca-cert.crt
   ```
4. Install the certificate:  
   - **Go to Settings** > **Security** > **Encryption & credentials**  
   - Select **Install a certificate** > **CA certificate**  
   - Choose the file `mitmproxy-ca-cert.crt`  

> ⚠ **Note:**  
> Android will display a warning: **"Your network may be monitored"**.  
> This alone is **not enough to bypass SSL pinning**, only for apps that do not enforce SSL pinning.

---

## 🛑 Bypassing SSL Pinning (Without Root)

Bypassing **SSL Pinning** cannot be done with **mitmproxy alone**. You need **Frida** or other tools.

### 🔹 Option A: Using Frida (No Root)
1. **Install Frida on your PC**:  
   ```bash
   pip install frida-tools
   ```
2. **Use Frida Gadget** (since root access is unavailable):  
   - **Repack the target APK**  
   - **Inject Frida Gadget**  
   - **Run the modified app**  
   - **Hook SSL pinning**  

3. **Execute the bypass SSL Pinning script**:  
   ```bash
   frida -U -n com.target.app -l bypass-ssl.js
   ```
   You can find example `bypass-ssl.js` scripts on GitHub.

---

### 🔹 Option B: Repack APK and Remove SSL Pinning  
This method involves decompiling the APK, modifying the code, and re-signing the APK.

**Required tools:**  
- 🛠️ **apktool** (for decompiling the APK)  
- ✍ **Smali/Java editor** (to remove SSL pinning)  
- 🔄 **Zipalign & apksigner** (to re-sign the APK)  

> ⚠ **Limitations:**  
> - Some apps use **strong certificate pinning**, causing them to crash if SSL pinning is removed.  
> - **Banking & streaming apps** are typically harder to bypass without root.

---

## ✅ Recommendations  
- Test this method on **apps that do not enforce SSL pinning** first.  
- For easier bypassing, use an **Android emulator (AVD, Genymotion) + Xposed + SSLUnpinning module** (though emulators are considered semi-rooted).  

---

## ⚠ Disclaimer  
This guide is intended **for educational & debugging purposes only**. **Do not use it for illegal activities!** 🚨  

---
