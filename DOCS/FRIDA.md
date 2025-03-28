# 🔓 Bypass SSL Pinning via Frida Gadget (No Root)  

### 📦 What is Frida Gadget?  
**Frida Gadget** is a version of **Frida** that can be embedded **directly into an APK**, allowing you to bypass SSL pinning without root or `adb shell` access.  

---

## ✨ Steps to Bypass SSL Pinning with Frida Gadget  

### ✅ 1. Prepare the Tools  

- Install Frida on your PC:

  ```bash
  pip install frida-tools
  ```

- Download Frida Gadget (`.so` file) from 👉 [Frida Releases](https://github.com/frida/frida/releases)  
  - Choose the **Android ARM** version matching your target device (`frida-gadget-*.so.xz`).  

---

### ✅ 2. Decompile the APK  

```bash
apktool d app.apk -o app_src
```

---

### ✅ 3. Inject Frida Gadget  

- Extract `frida-gadget.so` and rename it:

  ```bash
  mv frida-gadget-*.so libfrida-gadget.so
  ```

- Create the following folder:

  ```bash
  mkdir -p app_src/lib/arm64-v8a/
  ```

- Move `libfrida-gadget.so` into that folder:
 
  ```bash
  mv libfrida-gadget.so app_src/lib/arm64-v8a/
  ```

---

### ✅ 4. Modify `AndroidManifest.xml`  

Find the `<application ...>` tag and add:  

```xml
<application android:label="..." android:hasCode="true">
    ...
    <meta-data android:name="android.app.lib_name"
               android:value="frida-gadget"/>
```

This ensures Android loads `libfrida-gadget.so` when launching the app.

---

### ✅ 5. Rebuild the APK  

```bash
apktool b app_src -o app_frida.apk
```

---

### ✅ 6. Sign the APK  

Generate a keystore:  

```bash
keytool -genkey -v -keystore test.keystore -alias testkey -keyalg RSA -keysize 2048 -validity 10000
```

Sign the APK:  

```bash
jarsigner -verbose -sigalg SHA256withRSA -digestalg SHA-256 -keystore test.keystore app_frida.apk testkey
```

---

### ✅ 7. Install the Modified APK  

```bash
adb install app_frida.apk
```

---

### ✅ 8. Run the App and Hook  

Since Frida Gadget runs in the background, you can now hook into the app:  

```bash
frida -U -n com.target.app -l bypass-ssl.js
```

---

### 🧠 Sample `bypass-ssl.js` Script  

```javascript
Java.perform(function () {
    var X509TrustManager = Java.use('javax.net.ssl.X509TrustManager');
    var SSLContext = Java.use('javax.net.ssl.SSLContext');

    var TrustManager = Java.registerClass({
        name: 'dev.asdf.TrustManager',
        implements: [X509TrustManager],
        methods: {
            checkClientTrusted: function (chain, authType) {},
            checkServerTrusted: function (chain, authType) {},
            getAcceptedIssuers: function () { return []; }
        }
    });

    var TrustManagers = [TrustManager.$new()];
    var SSLContextInit = SSLContext.init.overload('[Ljavax.net.ssl.KeyManager;', '[Ljavax.net.ssl.TrustManager;', 'java.security.SecureRandom');
    SSLContextInit.implementation = function (keyManager, trustManager, secureRandom) {
        SSLContextInit.call(this, keyManager, TrustManagers, secureRandom);
        console.log('[+] SSL Pinning Bypassed');
    };
});
```

---

# 🛠️ 5. Alternative: Repack APK & Patch SSL Pinning Manually  

If you don’t want to use Frida, you can **manually patch SSL pinning** in the APK source code.

---

### ✅ Steps:  

#### 1️⃣ Decompile APK  

```bash
apktool d app.apk -o app_patch
```

#### 2️⃣ Find SSL Pinning Code  

Look for files containing:  
- `checkServerTrusted`  
- `checkClientTrusted`  
- `HostnameVerifier`  
- `TrustManager`  

---

#### ✅ Example Smali Patch  

Original `checkServerTrusted` function:  

```smali
.method public checkServerTrusted([Ljava/security/cert/X509Certificate;Ljava/lang/String;)V
    .registers 3
    invoke...
    invoke...
    return-void
.end method
```

Modify it to **an empty function**:  

```smali
.method public checkServerTrusted([Ljava/security/cert/X509Certificate;Ljava/lang/String;)V
    .registers 3
    return-void
.end method
```

---

#### ✅ Rebuild & Sign the APK  

```bash
apktool b app_patch -o app_nossl.apk
jarsigner -keystore test.keystore app_nossl.apk testkey
```

#### ✅ Install & Run  

```bash
adb install app_nossl.apk
```

---

# 🎯 Conclusion  

| **Method**       | **Pros**                            | **Cons**                           |
|-----------------|---------------------------------|--------------------------------|
| **Frida Gadget** | No root required, dynamic, powerful | Requires APK injection & resigning |
| **Manual Patch** | No need for Frida, direct patching  | Hard if code is obfuscated       |

---

## ⚠ Disclaimer  
This guide is intended **for educational & debugging purposes only**. **Do not use it for illegal activities!** 🚨  

---
