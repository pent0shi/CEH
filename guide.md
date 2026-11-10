# CEH v13 Module 18: IoT and OT Hacking

Exam-focused study guide for CEH 312-50. Based on pages 1 to 39 of the
supplied notes. Added material is marked ADDED CONTEXT.

## 1. Module at a Glance

**Module 18: IoT and OT Hacking**

- IoT connects physical objects to IP networks so they can sense and share data.
- OT monitors or changes physical industrial processes through ICS equipment.
- IoT attacks target devices, radios, firmware, cloud services, and default credentials.
- OT attacks target PLCs, HMIs, SCADA, industrial protocols, and trusted suppliers.
- Defense combines asset visibility, segmentation, secure updates, and safe monitoring.

**Why it matters:** A compromised camera can become a botnet member. A compromised
PLC can stop production or damage equipment. Confidentiality matters, but OT also
depends heavily on availability, integrity, safety, and deterministic timing.

**What the exam usually asks:** Purdue levels, ICS component roles, protocol-to-port
matches, Modbus weakness, Nmap OT scripts, Shodan filters, SDR and firmware tools,
rolling-code steps, OWASP IoT items, MITRE ATT&CK for ICS tactics, and the safest
countermeasure for a live plant.

**Ten things to remember most:**

1. Edge -> access gateway -> internet -> middleware -> application is the IoT stack.
2. Purdue Level 0 is the physical process; Level 3 is site operations; Level 3.5 is
   the industrial DMZ; Levels 4 and 5 are enterprise systems.
3. PLC executes control logic; RTU collects remote field data; HMI displays and
   accepts operator commands; SCADA supervises; DCS controls a distributed plant.
4. Modbus TCP uses port 502 and normally has no authentication or encryption.
5. DNP3 uses 20000; EtherNet/IP uses 44818; S7 uses 102; BACnet uses UDP 47808.
6. A rolling-code attack jams reception, captures codes, forwards one, and saves
   another unused valid code for later.
7. Shodan finds exposed devices; Nmap identifies services; Nessus finds known
   vulnerabilities; Malcolm analyzes network traffic.
8. UART, SPI, I2C, and JTAG are hardware interfaces. JTAG is a debug/test interface.
9. Active scanning can crash fragile OT devices. Prefer passive discovery first.
10. Zero trust means verify explicitly and grant least privilege, even inside OT.

## 2. Big Picture Map

```text
                 IoT path
 Sensors -> Edge -> Gateway -> Internet -> Middleware -> App
    |          |         |                    |
 hardware    radio    exposure              APIs/data
    |          |         |                    |
 JTAG/UART  replay   Shodan/Telnet       cloud privacy

                 OT path
 Enterprise L5/L4 -> IDMZ L3.5 -> Operations L3
                                      |
                              Supervisory L2
                                      |
                              Control L1 -> Process L0

 Assessment: passive discovery -> safe validation -> report
 Defense: inventory -> segment -> harden -> monitor -> recover
```

| Area | Main target | Typical evidence | Best first defense |
|---|---|---|---|
| IoT | Device and ecosystem | Banner, firmware, radio | Unique credentials and updates |
| OT | Physical process | Passive traffic, asset data | Zones, conduits, safe monitoring |
| Both | Availability and trust | Logs and configuration | Least privilege and recovery |

## 3. Topic-by-Topic Guide

### 3.1 Learning objectives, IoT meaning, and data flow

**What it is:** The Internet of Things (IoT), also called the Internet of Everything
(IoE) in the notes, is a network of IP-addressable objects with embedded sensors,
processors, and communication hardware. A "thing" can be natural, human-made, or
machine-made. The module objectives are IoT concepts, attacks, methodology and
defense, followed by the same four areas for OT.

**Analogy:** A smart thermometer is a receptionist who reports room temperature to
a head office and accepts instructions back.

**How it works:**

1. Industrial, wearable, healthcare, and home devices sense or collect data.
2. They send data, often through an IoT gateway, across the internet.
3. Cloud storage or servers store and analyze the data.
4. A mobile app displays results and can send a remote-control command.
5. The gateway returns the command to the device, which changes its behavior.

**Real-world use:** A factory motor reports vibration. Analytics detects an unusual
pattern, and an authorized maintenance application schedules inspection. If default
credentials protect the gateway, an outsider could instead read or alter the data.

**Tools and commands used here:** No tool is needed to define the flow. Later pages
use Shodan, Nmap, Wireshark, firmware tools, and radio tools against its weak points.

**AI angle (ADDED CONTEXT):** AI can classify sensor anomalies and summarize asset
inventory. An attacker can use AI to prioritize exposed devices from public banners.
Example defensive prompt: "Group these authorized asset records by protocol, owner,
patch status, and internet exposure. Do not suggest active tests."

**Countermeasures and defense:** Know every data producer and consumer. Authenticate
devices and users, encrypt transport, restrict commands, and log administrative changes.

> **EXAM FOCUS:** IoT is not only smart homes. The key property is embedded sensing
> or control plus network communication. A gateway translates or connects devices;
> it is not the same as cloud middleware. Trap: assuming every device directly uses
> a full TCP/IP stack and talks directly to an app.

**Memory trick:** "Sense, Send, Store, Study, Steer" describes sense, transmit,
store, analyze, and command.

### 3.2 IoT architecture, technologies, operating systems, and protocols

**What it is:** The five layers separate physical sensing from user applications.

**Analogy:** A parcel moves from a local shop, through a regional depot and roads,
to a sorting warehouse, and finally to the customer.

**How it works:**

1. **Edge technology:** sensors, devices, machines, and intelligent edge nodes.
2. **Access gateway:** protocol translation and messaging between local and IP networks.
3. **Internet:** connectivity between endpoints and remote services.
4. **Middleware:** device management and information management.
5. **Application:** delivers applications to different IoT users.

**Technology groups from the notes:**

- Short range: BLE, Li-Fi, NFC, QR codes and barcodes, RFID, Thread, Wi-Fi,
  Wi-Fi Direct, Z-Wave, Zigbee, and ANT.
- Medium range: HaLow and LTE-Advanced.
- Long range: LPWAN, LoRaWAN, 6LoWPAN, Sigfox, Neul, VSAT, cellular, and NB-IoT.
- Wired: Ethernet, MoCA, and power-line communication (PLC), which is unrelated
  to a programmable logic controller with the same abbreviation.
- Operating systems: Windows 10 IoT, Amazon FreeRTOS, Fuchsia, RIOT, Ubuntu Core,
  ARM Mbed OS, Zephyr, Embedded Linux, NuttX RTOS, Integrity RTOS, and Tizen.
- Application protocols: CoAP, Edge, LWM2M, Physical Web, XMPP, Mihini/M3DA, and MQTT.

**Real-world use:** A battery soil sensor can use Zigbee to a gateway. The gateway
uses IP networking to reach middleware, where MQTT messages become application data.

**Tools and commands used here:** Wireshark can decode MQTT and Zigbee. Open Sniffer,
CatSniffer, and KillerBee examine low-power wireless traffic.

> **ADDED CONTEXT:** MQTT is lightweight publish/subscribe messaging through a
> broker. CoAP is a REST-like protocol for constrained devices. LWM2M adds device
> management. XMPP is extensible XML messaging. 6LoWPAN adapts IPv6 to IEEE
> 802.15.4 links; it is not simply a long-range radio like LoRaWAN.

**AI angle (ADDED CONTEXT):** A model can explain a decoded protocol or flag an
unexpected topic. Example prompt: "Explain this authorized MQTT packet capture field
by field and identify plaintext metadata without inventing payload contents."

**Countermeasures and defense:** Authenticate the gateway and broker, restrict topics,
encrypt where supported, and remove unused radio and management services.

> **EXAM FOCUS:** Match the function to the layer. Protocol translation means access
> gateway; device management means middleware; sensors mean edge. Trap: placing MQTT
> at the physical layer. It is an application protocol, normally carried over TCP.

**Memory trick:** "Every Access Internet Message Arrives": Edge, Access, Internet,
Middleware, Application.

### 3.3 OWASP IoT Top 10, attack surfaces, and device vulnerabilities

**What it is:** OWASP lists recurring weaknesses, not a sequence of attacks.

**Analogy:** A building risk register lists unlocked doors, copied keys, old cameras,
and unguarded loading bays before describing individual burglaries.

**OWASP Top 10 IoT threats in notes order:**

1. Weak, guessable, or hardcoded passwords.
2. Insecure network services.
3. Insecure ecosystem interfaces.
4. Lack of secure update mechanisms.
5. Use of insecure or outdated components.
6. Insufficient privacy protection.
7. Insecure data transfer and storage.
8. Lack of device management.
9. Insecure default settings.
10. Lack of physical hardening.

**Eighteen attack surfaces:** ecosystem, device memory, physical interfaces, web
interface, firmware, network services, administrative interface, local storage,
cloud web interface, third-party backend APIs, update mechanism, mobile application,
vendor backend APIs, ecosystem communication, network traffic,
authentication/authorization, privacy, and hardware sensors.

**The seventeen vulnerability lessons:**

- Username enumeration reveals valid names through different authentication responses.
- Weak passwords such as 1234 and unchanged factory passwords permit guessing.
- No lockout after three to five failures permits continued guessing.
- Unencrypted services expose traffic; weak implementations such as SSLv2 are not
  adequate merely because encryption is present.
- Missing two-factor authentication leaves one stolen secret sufficient.
- Updates without TLS or file encryption, and world-writable update storage, allow
  tampering. No manual check or no update mechanism leaves flaws unresolved.
- Denial of service can disable one service or the entire device.
- Removable storage and firmware extraction can reveal source, binaries, passwords,
  and SSH keys. Hidden firmware version and update date hinder risk decisions.
- JTAG with a debugger can alter execution; side channels can leak or change behavior.
- Serial console access can yield a full shell even when boot protections exist.
- Outdated BusyBox, OpenSSL, SSH, or web server components carry known weaknesses.

**Real-world use:** An authorized reviewer extracts a camera firmware image, finds a
hardcoded credential, and reports it before the same credential is used at scale.

**Tools and commands used here:** Binwalk, Firmware Mod Kit, strings, hexdump, GDB,
OpenOCD, BUS Auditor, Shodan, and Nmap appear in later topics.

**AI angle (ADDED CONTEXT):** AI can map findings to OWASP categories, but evidence
must support each mapping. Prompt: "Classify these verified findings under the OWASP
IoT Top 10 and quote the supporting observation for each."

**Countermeasures and defense:** Unique credentials, lockout, MFA, signed updates,
component inventory, data minimization, encrypted storage, lifecycle management,
secure defaults, disabled debug ports, and tamper resistance address the list.

> **EXAM FOCUS:** An insecure mobile app, cloud API, or backend belongs to the IoT
> ecosystem too. Trap: choosing only the physical device. Hardcoded password is a
> credential flaw; outdated OpenSSL is an insecure/outdated component.

**Memory trick:** For the Top 10, group them as "Secrets, Services, Surrounding
interfaces, Software updates and Supply components; Privacy, Protection of data,
Provisioning, Presets, Physical access."

### 3.4 IoT threat catalogue, DDoS botnets, and HVAC pivoting

**What it is:** The notes list 21 threats: DDoS, HVAC attack, rolling code,
BlueBorne, jamming, backdoor remote access, Telnet remote access, Sybil, exploit kits,
MITM, replay, forged malicious device, side channel, ransomware, client
impersonation, SQL injection, SDR-based attack, fault injection, network pivoting,
DNS rebinding, and firmware-over-the-air (FOTA) update attack.

**Analogy:** A botnet is a crowd of compromised smart devices all knocking on one
door at the attacker's signal.

**How an IoT DDoS works:**

1. The attacker exploits device weaknesses and installs malicious software.
2. Remote access turns many devices into bots, collectively an army of botnets.
3. A command-and-control (C2 or C&C) center sends instructions.
4. Distributed bots send a large request volume to the target.
5. The server exhausts resources, goes offline, or cannot process further requests.

**HVAC attack steps:**

1. Shodan identifies an exposed, vulnerable industrial control or HVAC system.
2. Default credentials provide access to the ICS/HVAC interface.
3. The attacker changes temperature or uses the trusted connection to enter the LAN.
4. The compromised building system becomes a network-pivoting foothold.

**Real-world use:** An assessor finds that a facilities network can reach finance.
The safest result is a segmentation finding, not an attempt to alter temperature.

**Tools and commands used here:** Shodan, Censys, Nmap, botnet malware, and the
iRidium interface shown in the HVAC example.

**AI angle (ADDED CONTEXT):** Attackers can generate convincing phishing content for
initial compromise. Defenders can cluster traffic to identify bot-like behavior.
Prompt: "Summarize common timing and destination features in this authorized flow
export and list benign explanations."

**Countermeasures and defense:** Remove internet exposure, change credentials, patch,
segment facilities networks, rate-limit, filter egress, and prepare DDoS absorption
with the ISP or upstream provider.

> **EXAM FOCUS:** C2 coordinates bots; the target server is the victim of the flood.
> HVAC is often the initial access or pivot, not the final target. Trap: calling
> every large infection a DDoS before a flood is launched.

**Memory trick:** DDoS chain is "Break in, Bot, Beacon, Blast, Blackout."
