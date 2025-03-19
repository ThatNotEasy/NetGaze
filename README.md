# NetGaze

![NetGaze Logo](https://via.placeholder.com/150) <!-- Replace with your logo -->

**NetGaze** is a powerful yet lightweight tool designed to capture and analyze network traffic on Android devices without requiring root access. Built using **mitmproxy** and **ADB**, NetGaze provides a seamless way to monitor, log, and inspect HTTP/HTTPS traffic in real-time.

---

## Features

- 🚀 **Non-Root Capture**: Capture network traffic on Android devices without the need for root privileges.
- 🔒 **HTTPS Support**: Decrypt and inspect HTTPS traffic using **mitmproxy**.
- 📊 **Real-Time Monitoring**: View live network traffic with detailed information about requests and responses.
- 📂 **Traffic Logging**: Save captured traffic to a file for offline analysis.
- 🛠️ **Developer-Friendly**: Easily debug and analyze network behavior of your Android apps.
- 🌐 **Multi-Protocol Support**: Monitor HTTP, HTTPS, DNS, and other common protocols.
- 📱 **Lightweight**: Minimal impact on device performance and battery life.

---

## Use Cases

- **App Development**: Debug and optimize network requests in your Android apps.
- **Security Auditing**: Inspect network traffic for potential vulnerabilities or data leaks.
- **Privacy Monitoring**: Track which apps are sending data and where it's being sent.
- **Educational Purposes**: Learn about network protocols and how data is transmitted over the internet.

---

## How It Works

NetGaze uses **mitmproxy** as a man-in-the-middle (MITM) proxy to capture and analyze network traffic. The tool leverages **ADB** to configure the Android device to route traffic through the proxy without requiring root access. Here's a high-level overview:

1. **mitmproxy** acts as an intermediary between the Android device and the internet.
2. **ADB** is used to set up the device's network settings to route traffic through the proxy.
3. NetGaze provides a user-friendly interface to start/stop capturing, view live traffic, and export logs for further analysis.

---

## Getting Started

### Prerequisites

- Android device running Android 5.0 (Lollipop) or higher.
- Python 3.x installed on your computer.
- **mitmproxy** installed (`pip install mitmproxy`).
- **ADB** installed and configured on your computer.
- Basic knowledge of Android development and networking.