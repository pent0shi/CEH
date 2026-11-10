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

### 3.5 Rolling-code and jamming attacks

**What it is:** A rolling code, or hopping code, changes on each key-fob use to stop
simple reuse. The described attack combines jamming, capture, and selective replay.
Jamming means transmitting interference on the same frequency so endpoints cannot
reliably send or receive messages.

**Analogy:** An attacker blocks a mailbox, collects two signed entry slips, hands
over the first to avoid suspicion, and keeps the second unused slip.

**How the rolling-code attack works:**

1. The victim presses the fob. The attacker jams the car receiver and sniffs code one.
2. The car does not unlock, so the victim presses again.
3. The attacker captures code two and forwards code one, which unlocks the car.
4. Code two remains unused and valid in the receiver's expected sequence.
5. The attacker later replays code two to unlock the vehicle.

**How jamming works:** The attacker determines the sensor frequency, transmits random
radio energy there, and reduces the signal-to-noise ratio until communication fails.

**Real-world use:** A vehicle-security team tests a owned fleet receiver in a shielded
environment and confirms that request failure plus a second press is a warning sign.

**Tools and commands used here:** RFCrack, YardStick One, HackRF One, RTL-SDR,
`RFCrack.py -j`, and `RFCrack.py -r` with modulation and frequency options.

**Countermeasures and defense:** Use authenticated, freshness-protected protocols,
receiver-side anomaly detection, rolling-window limits, and user warnings after
repeated failed unlocks. Encryption alone does not prevent radio jamming.

> **EXAM FOCUS:** The second code is saved; the first code is forwarded to preserve
> normal behavior. Trap: a basic replay resends an old message, while this scenario
> specifically needs jamming plus capture of an unused future code.

**Memory trick:** "Jam one, Grab one; Jam two, Grab two; Send one, Save two."

### 3.6 Backdoors, Telnet, BlueBorne, and smart-grid compromise

**What it is:** A backdoor is hidden or unauthorized access that bypasses normal
authentication. Telnet is an old remote terminal protocol whose normal traffic,
including credentials, is plaintext. BlueBorne is a family of Bluetooth attacks;
the notes associate it with airborne replay, fuzzing, and jamming using SDR hardware.

**Analogy:** A phishing attachment is a fake delivery worker who quietly installs a
spare key inside the building.

**How the smart-grid example works:**

1. The attacker profiles employees using social engineering.
2. A legitimate-looking phishing email carries a malicious attachment.
3. Opening it installs a backdoor and gives access to the private network.
4. The attacker pivots to SCADA and disables a UPS or other power controls.
5. Loss of power causes operational impact.

**How Telnet access works:** Scanning or Shodan reveals TCP 23. Weak/default login
details or an unprotected service then provide a remote command session. The example
also shows a Dahua DVR and HTTP port 80, so an open web port is not itself Telnet.

**Real-world use:** A utility removes direct Telnet, requires a VPN and jump host,
and trains staff to report attachments instead of testing them on production systems.

**Tools and commands used here:** Shodan, Censys, Nmap, HackRF One, and Telnet.

**AI angle (ADDED CONTEXT):** Generative AI can make phishing grammatically convincing
and deepfake voice can support impersonation. Defenders should verify unusual requests
through a second channel. Prompt for awareness work: "List benign warning signs in
this fictional email without improving its persuasive content."

**Countermeasures and defense:** Use SSH rather than Telnet, email filtering, attachment
sandboxing, MFA, least privilege, Bluetooth patching, and restricted device discovery.

> **EXAM FOCUS:** SSH is the secure Telnet replacement. BlueBorne is Bluetooth, not
> Wi-Fi. Trap: choosing a firewall as the complete answer to phishing; user reporting
> and endpoint/email controls address the initial attachment.

**Memory trick:** "Telnet Talks in Text"; "BlueBorne Bites Bluetooth."

### 3.7 SDR attacks, local discovery, and DNS rebinding

**What it is:** Software-defined radio (SDR) implements radio functions in software.
It can inspect, modify, generate, or replay signals. DNS rebinding makes a browser
resolve one hostname first to an attacker and then to a private address, helping
malicious script reach local devices through the victim browser.

**Analogy:** SDR is a programmable musical instrument that can learn and replay many
songs. DNS rebinding is a signpost that is changed after a visitor passes the gate.

**Three SDR methods in the notes:**

1. **Replay:** discover the frequency, capture an original command, isolate the command
   sequence, and inject it back into the IoT network.
2. **Cryptanalysis:** capture and reverse-engineer the signal/protocol, requiring
   knowledge of cryptography, communication theory, and modulation.
3. **Reconnaissance:** inspect specifications and hardware; a multimeter and chipset
   inspection can identify ground pins, product IDs, and other information.

**Local device discovery steps:**

1. A user visits an attacker-controlled advertisement or page.
2. Malicious code obtains the local IP and probes available private addresses.
3. Active devices may return TCP RST; inactive ones may time out.
4. Responses reveal devices and potentially access-point UID and BSSID information.
5. A tool such as Singularity of Origin tests DNS rebinding.
6. Successful rebinding lets the page interact with local device interfaces.

**Real-world use:** A browser-security assessment uses a dedicated test network to
show why an unauthenticated local camera interface is reachable from a web page.

**Tools and commands used here:** HackRF One, RTL-SDR, RFCrack, Singularity of Origin,
Wireshark, and TCP SYN/RST responses.

**Countermeasures and defense:** Authenticate local interfaces, validate Host headers,
use DNS rebinding protections, isolate IoT networks, and require explicit user approval
for local network access where the platform supports it.

> **EXAM FOCUS:** RST can reveal a closed port on a live host; timeout gives less
> certain evidence. BSSID identifies a wireless access point radio. Trap: calling
> rebinding ordinary DNS spoofing; rebinding abuses changing answers and browser trust.

**Memory trick:** SDR does "Record, Reverse, Recon"; rebinding does "Answer, Alter,
Access."

### 3.8 Fault injection and the remaining IoT attack types

**What it is:** Fault injection, also called perturbation, deliberately disturbs
hardware so it skips checks, leaks data, or executes unintended behavior. It can be
invasive, which alters or opens the package, or non-invasive, which works externally.

**Analogy:** A momentary flicker can make a cashier skip a verification step.

**Fault methods and other attacks:**

- Optical, electromagnetic fault injection (EMFI), and body-bias injection (BBI) use
  lasers, electromagnetic pulses, or bias changes.
- Power, clock, and reset glitching disturb supply or timing.
- Voltage/frequency tampering changes operating conditions; temperature attacks alter
  the chip environment.
- Sybil uses multiple forged identities, for example to simulate traffic congestion.
- Exploit kits automate scripts against poorly patched vulnerabilities.
- MITM secretly intercepts and can modify two-party communication.
- Replay resends captured valid messages, potentially causing repeated actions or DoS.
- Forged malicious device replacement needs physical or supply-chain access.
- Side channel derives secrets from emissions or behavior rather than breaking math.
- Ransomware locks a screen or encrypts files to deny access until payment is demanded.
- Client impersonation pretends to be a legitimate client; SQL injection inserts
  database commands through unsafe input; FOTA attacks abuse firmware updates.

**Real-world use:** A hardware lab tests whether a voltage glitch bypasses secure boot
on a development board, then adds brownout detection and boot verification.

**Tools and commands used here:** Oscilloscope, signal analyzer, multimeter, glitching
equipment, and debug interfaces.

**Countermeasures and defense:** Use secure boot, signed firmware, glitch sensors,
constant-time authentication, tamper evidence, nonces and timestamps for anti-replay,
input validation, parameterized SQL, and offline backups.

> **EXAM FOCUS:** Fault injection changes execution conditions; side channel observes
> behavior. Sybil means many identities; MITM means an intermediary. Trap: selecting
> encryption as an anti-jamming control or a replay defense without freshness.

**Memory trick:** "Light, Magnet, Bias; Power, Clock, Reset; Volt, Hertz, Heat."

### 3.9 IoT malware and botnet families

**What it is:** IoT malware turns weakly protected devices into botnet members,
proxies, miners, ransomware victims, or attack platforms.

**Analogy:** One unchanged factory key can open thousands of houses of the same model.

**How it works:** KmsdBot's Kmsdx variant adds Telnet scanning/authentication, targets
SSH exposure and default credentials, and supports more CPU architectures. The notes'
Go-source analysis mentions `redress`, `main.go`, `ssh.go`, `telnet.go`, and a
`telnet.txt` credential list. These are static-analysis clues, not commands to run.
Other listed families are WailingCrab, P2PInfect, NKAbuse, IoTroop, and XorDdos.

> **ADDED CONTEXT:** IoTroop is also known as Reaper. XorDdos targets Linux systems.
> P2PInfect uses peer-to-peer propagation and has targeted Redis. NKAbuse uses NKN
> networking for decentralized communication. WailingCrab has used MQTT for C2.
> Family capabilities change, so answer from the behavior described in the question.

**Real-world use:** A defender finds repeated outbound Telnet attempts from a camera.
The response is isolation, credential replacement, firmware remediation, and checking
peer devices rather than merely deleting one suspicious process.

**Tools and commands used here:** Redress for Go binary inspection, Shodan, Censys,
network monitoring, and anti-malware tools.

**AI angle (ADDED CONTEXT):** AI can help label static functions but may hallucinate
malware capabilities. Prompt: "Describe only observable behavior in these decompiled
snippets and mark uncertain claims; do not generate propagation code."

**Countermeasures and defense:** Unique credentials, disable Telnet, restrict egress,
patch firmware, monitor unusual scanning, and rebuild compromised devices from trusted
images.

> **EXAM FOCUS:** Default credentials plus broad architecture support increase botnet
> reach. Trap: treating Telnet scanning as exploitation of SSH; they are different
> services even when one malware family targets both.

**Memory trick:** "Scan, Sign in, Spread, Serve C2."

### 3.10 Information gathering with Shodan and wireless sniffing

**What it is:** Information gathering identifies exposed devices and their protocols
before vulnerability validation. Shodan indexes internet-facing services; sniffing
observes traffic within range or on a monitored network.

**Analogy:** Shodan is a searchable directory of public shop signs; sniffing is
listening to conversations on a network you are authorized to monitor.

**How it works:**

1. Query Shodan for `webcamxp country:"US"`, `webcamxp city:"paris"`, or
   `webcamxp geo:"-50.81,201.80"` as shown in the notes.
2. Review IP, hostname, ISP, location, ports, and service banners without assuming
   that a banner proves exploitability.
3. Scan authorized ranges for HTTP ports 80, 81, 8080, and 8081.
4. Identify the wireless adapter with `ifconfig`, enable monitor mode, discover the
   target channel, then capture that channel in Wireshark.
5. The notes' capture shows MQTT Ping Request/Response and Publish exchanges, with
   destination TCP 1883.

**Real-world use:** An asset owner confirms that no camera is internet exposed and
uses an approved wireless capture to identify plaintext telemetry.

**Tools and commands used here:** Shodan, MultiPing, FCC ID Search, Censys, FOFA,
Nmap, ifconfig, Airmon-ng, Airodump-ng, Wireshark, Suphacap, and IoT sniffing tools.

**AI angle (ADDED CONTEXT):** ChatGPT or ShellGPT can explain a command before an
approved scan. Prompt: "Explain each Nmap flag in this authorized HTTP discovery
command and warn which options increase traffic." Never paste private scope or
credentials into a public model.

**Countermeasures and defense:** Remove public administration interfaces, change
identifying banners where practical, encrypt MQTT with TLS, use broker ACLs, and
monitor for unexpected monitor-mode or scanning activity.

> **EXAM FOCUS:** Shodan is search, not an exploit framework. Monitor mode captures
> wireless frames; the channel must match. Trap: `airodump-ng` scans/captures while
> `airmon-ng` configures monitor mode.

**Memory trick:** "Shodan Sees, Nmap Scans, Wireshark Watches."

### 3.11 IoT vulnerability scanning and validation

**What it is:** Vulnerability scanning checks discovered devices for default
credentials, known weaknesses, product paths, and versions.

**Analogy:** A safety inspector checks each lock model against a recall list instead
of forcing every door.

**How it works:** IoTSeeker's Perl scanner accepts IP addresses and reports device
type and whether the default password remains. Genzai identifies routers, cameras,
and HMIs, then tests default passwords and vulnerabilities based on paths and
versions. Its example mentions a TP-Link router result. Other listed tools are
beSTORM, IoTSploit, IoTVAS, and Firmalyzer.

**Real-world use:** A hospital runs an approved credentialed scan against decommissioned
test cameras and prioritizes any device still using factory credentials.

**Tools and commands used here:** IoTSeeker/IotScanner.pl, Genzai, beSTORM,
IoTSploit, IoTVAS, Firmalyzer, and Nmap.

**Countermeasures and defense:** Use an asset inventory, authenticated configuration
review, vendor advisories, firmware updates, and manual validation of high-risk results.
Avoid password attempts or intrusive scans outside authorization and maintenance windows.

> **EXAM FOCUS:** Discovery finds devices; vulnerability scanning maps them to known
> weaknesses; exploitation proves impact. Trap: treating "changed password" as proof
> that the password is strong or the device is fully patched.

**Memory trick:** "Seeker Seeks Secrets; Genzai Gathers Versions."

### 3.12 RFCrack, Open Sniffer, and HackRF One

**What it is:** These are radio test tools. RFCrack works with YardStick One for
sub-GHz tests. Open Sniffer captures IEEE 802.15.4/Zigbee frames into Wireshark and
can transmit frames. HackRF One is a half-duplex SDR covering about 1 MHz to 6 GHz.

**Analogy:** They are universal radio microscopes, with some models also able to speak.

**How it works:**

1. RFCrack live replay uses `-i`; rolling-code mode uses `-r` with `-M MOD_2FSK`
   and a frequency such as `-F 314350000`; `-U -100 -L -10` sets RSSI bounds;
   `-j -F 314000000` selects jamming.
2. Open Sniffer captures Zigbee beacon and command frames, permits visualization,
   supports user-defined replay, and can continuously emit packets for DoS testing.
3. HackRF supports receive and transmit, but not simultaneously in full duplex.
   It can inspect protocols from GSM to Z-Wave and support replay, fuzzing, or jamming.

**Real-world use:** A lab uses RFCrack on a owned sub-GHz gate controller and Open
Sniffer on an isolated Zigbee network to verify replay resistance.

**Tools and commands used here:** RFCrack.py, YardStick One, Open Sniffer, Wireshark,
HackRF One, KillerBee, and CatSniffer.

**Countermeasures and defense:** Use cryptographic authentication and freshness,
monitor spectrum anomalies, reduce radio range where possible, and test only in a
controlled RF environment.

> **EXAM FOCUS:** MOD_2FSK is modulation, frequency is in Hz, RSSI bounds select
> signal strength, and half duplex means one direction at a time. Trap: selecting
> Wireshark as the radio transmitter; it primarily decodes and analyzes captures.

**Memory trick:** "I is Immediate replay, R is Rolling, J is Jamming, F is Frequency."
