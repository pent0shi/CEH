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

### 3.13 HackRF replay and hardware communication buses

**What it is:** A replay capture stores radio samples and transmits them again. Hardware
buses expose internal communications and debugging functions.

**Analogy:** A sample file is an audio recording of a radio conversation. UART, SPI,
I2C, and JTAG are different service hatches on the circuit board.

**How it works:**

1. FCC ID records or an RTL-SDR help identify a target transmitter's frequency.
2. `hackrf_transfer -r` receives raw samples; `-t` transmits a capture; `-f` sets
   frequency, and gain options control receive or transmit amplification.
3. `hackrf_info` confirms board identity and firmware version.
4. BUS Auditor scans pin combinations and voltage settings for UART or I2C.
5. UART output can reveal RX/TX pins and baud rate such as 9600; I2C output reveals
   device address plus SCL clock and SDA data pins.

**Interface meanings:** UART is asynchronous serial communication. SPI is synchronous
serial communication with a controller and peripherals. I2C is addressed two-wire
communication. JTAG is a test/debug interface useful for firmware and execution access.
DIVA is a training application, and a PCB is the physical circuit board inspected.

**Real-world use:** A product team locates an enabled debug UART on a prototype,
observes boot logs, and disables sensitive console access before release.

**Tools and commands used here:** HackRF One, RTL-SDR, BUS Auditor, DIVA, multimeter,
GDB, and OpenOCD.

**Countermeasures and defense:** Lock or disable debug interfaces in production,
require authenticated debug unlock, use tamper detection, and never rely on hidden
test points as a security boundary.

> **EXAM FOCUS:** UART commonly leads to a console; JTAG commonly leads to debugging;
> I2C uses SCL and SDA. Trap: confusing a baud rate with radio frequency.

**Memory trick:** "UART Usually A Root Terminal; JTAG Joins Test And Debug Gates."

### 3.14 NAND glitching, CamOver, and Telnet access

**What it is:** NAND glitching interrupts boot by grounding a serial I/O pin of flash
memory, with the goal of bypassing normal startup and gaining root. CamOver targets
certain network-camera password-disclosure weaknesses.

**Analogy:** NAND glitching distracts a guard during the first seconds of a shift.
CamOver uses a known defective desk procedure to ask for the administrator key.

**How it works:**

1. For NAND glitching, identify the flash and timing, disturb serial I/O during boot,
   and inspect whether a privileged console appears. Results are hardware dependent.
2. Start CamOver with `camover`; choose one address with `-a`, input files with `-i`,
   output with `-o`, threads with `-t`, or internet results through Shodan/ZoomEye.
3. For Telnet, identify open TCP 23 and use only authorized credentials. Shodan or
   Censys may expose a device banner before any login attempt.

**Real-world use:** An authorized camera audit verifies whether a patched firmware
release removes password disclosure and whether Telnet is fully disabled.

**Tools and commands used here:** CamOver, Shodan, ZoomEye, Censys, Nmap, Telnet,
multimeter, and hardware-glitching tools.

**Countermeasures and defense:** Patch camera firmware, restrict management networks,
replace Telnet with SSH, require strong unique credentials, and add boot/flash glitch
detection.

> **EXAM FOCUS:** CamOver is a camera exploitation tool, not a generic camera search
> engine. `-a` is one address; `-t` means threads in its usage, not target.
> Trap: trying Shodan API access without a key when a local `-a` test is intended.

**Memory trick:** "Camera Address = CamOver -a; Telnet Twenty-Three = Text."

### 3.15 Maintaining access through firmware modification

**What it is:** Firmware is the low-level software that runs a device. An attacker who
modifies and reinstalls it can persist across ordinary account changes.

**Analogy:** Instead of keeping a copied house key, the intruder replaces the lock's
internal instructions so it always admits them.

**How it works:**

1. After authorized access in an assessment, obtain the firmware image.
2. Firmware Mod Kit's `extract-firmware.sh` identifies and extracts components.
3. The DD-WRT example shows a TRX header, gzip/LZMA compressed data, and a Squashfs
   filesystem, plus a checksum and offsets.
4. Modify files only in an owned lab image, reconstruct it, and verify whether the
   device accepts unsigned or improperly validated firmware.
5. The security finding is an update-verification failure with persistence impact.

**Real-world use:** A vendor test shows that a modified image is rejected because
secure boot checks a trusted signature. This proves the control, not an attack success.

**Tools and commands used here:** Firmware Mod Kit, Binwalk, dd, file, strings,
hexdump, mount, GDB, and QEMU.

**Countermeasures and defense:** Require signed images, verify a hardware root of
trust, use rollback protection, protect update storage, and reflash compromised
devices from known-good media.

> **EXAM FOCUS:** Firmware modification is maintaining access, not initial access.
> Squashfs is a compressed filesystem; TRX is a router firmware image format.
> Trap: assuming password removal deletes implanted firmware.

**Memory trick:** "Extract, Examine, Edit, Encode, Evaluate."

### 3.16 Firmware analysis and reverse engineering

**What it is:** Static analysis inspects an image without running it. Dynamic analysis
observes emulated or real execution. Reverse engineering reconstructs behavior.

**Analogy:** Static analysis opens and catalogs a machine; dynamic analysis runs it
behind safety glass.

**How it works:**

1. Obtain firmware from the device or vendor and verify the MD5 value as an integrity
   comparison, not as collision-resistant security.
2. Run `file`, `strings`, and `hexdump` on the `.bin`; use Binwalk to identify and
   extract embedded data, and `dd` for precise byte ranges.
3. Create `rootfs`, mount the extracted filesystem when appropriate, and inspect
   `etc/passwd`, `etc/shadow`, and `etc/ssl`.
4. Search recursively for password, admin, root, `.conf`, `.pem`, and `.crt` data.
5. Emulate binaries with `qemu-mipsel`, `qemu-arm`, or the matching QEMU architecture
   and `-L` library prefix. Test the web interface dynamically.

**Goals from the notes:** passwords, API tokens, endpoints, vulnerable services,
backdoor accounts, configuration files, private keys, and stored data.

**Real-world use:** An assessor recovers an API token from a vendor-supplied image
and proves exposure without touching production cameras.

**Tools and commands used here:** File, MD5 tools, strings, hexdump, Binwalk, dd,
mount, grep, find, QEMU, GDB, Radare2, Ghidra, and IDA Pro.

**AI angle (ADDED CONTEXT):** AI can suggest likely meanings for strings or decompiled
functions. Prompt: "Summarize evidence in this firmware string listing and distinguish
hardcoded secrets from harmless words containing 'key'."

**Countermeasures and defense:** Strip secrets, use per-device credentials, protect
keys in secure hardware, remove debug artifacts, sign firmware, and manage third-party
components.

> **EXAM FOCUS:** Binwalk extracts; QEMU emulates; strings finds printable sequences;
> grep searches content; find searches names. Trap: choosing QEMU for static extraction
> or Binwalk for full processor emulation.

**Memory trick:** "Get, Verify, View, Unpack, Mount, Mine, Mimic."

### 3.17 General IoT hacking and device-management tools

**What it is:** Each tool serves a different assessment surface.

**Analogy:** A radio stethoscope, protocol screwdriver, and router toolbox are not
interchangeable just because all are used on smart devices.

**How it works:** CatSniffer passively monitors IoT traffic and supported CC1352-based
radio protocols. KillerBee assesses Zigbee/IEEE 802.15.4. JAGulator helps identify
JTAG pinouts. `wiz_exploit` is listed as an IoT exploitation project; PENIOT tests
IoT device penetration; RouterSploit targets embedded devices and routers. Device
management platforms onboard, monitor, permission, and remotely update fleets.

**Management products in the notes:** SeaCat.io, Armis Centrix, Oracle Fusion Cloud
IoT, Golioth, AWS IoT Device Management, IBM Watson IoT Platform, openBalena, and
Microsoft Azure IoT Central shown in the dashboard.

**Real-world use:** A retailer uses a management platform to inventory devices, enforce
unique identities, roll out signed updates, and revoke a lost gateway.

**Tools and commands used here:** CatSniffer, KillerBee, JAGulator, wiz_exploit,
PENIOT, RouterSploit, and the management platforms above.

**Countermeasures and defense:** Device management itself needs MFA, role separation,
signed updates, audit logs, and secure decommissioning because it has fleet-wide power.

> **EXAM FOCUS:** Armis emphasizes asset visibility; JAGulator is JTAG; RouterSploit
> is embedded/router exploitation. Trap: calling a management platform a vulnerability
> scanner only.

**Memory trick:** "Cat Catches packets, KillerBee knows Zigbee, JAGulator finds JTAG."

### 3.18 IoT countermeasures, manufacturer guidance, and hardware practice

**What it is:** Defense covers accounts, network exposure, updates, physical access,
and operational lifecycle.

**Analogy:** Good IoT security is building security plus key control plus maintenance,
not one stronger lock.

**The fourteen defenses in the notes:**

1. Disable guest and demo accounts.
2. Lock accounts after excessive invalid logins.
3. Use strong authentication.
4. Place control networks behind firewalls and isolate them from business networks.
5. Deploy IDS/IPS.
6. Use end-to-end encryption and PKI.
7. Use VPN architecture for secure communication.
8. Deploy security as an integrated system.
9. Permit only trusted internet source IPs where appropriate.
10. Disable Telnet on port 23.
11. Disable UPnP on routers.
12. Prevent physical tampering.
13. Patch and update firmware regularly.
14. Monitor TCP 48101 because the cited infected devices spread malicious files there.

**Manufacturer and OWASP solutions:** Use TLS and certificate/revocation checks,
strong passwords, lockout, simple secure updates, application allowlisting, and a
secure boot chain. Close ports, disable UPnP, assess APIs, validate input/output,
verify update source/integrity, notify users, remove unused dependencies, minimize
and anonymize data, protect stored/transferred data, manage assets and
decommissioning, change defaults, restrict remote access, protect BIOS/firmware
with unique passwords, control boot order, and minimize USB exposure. Avoid
proprietary encryption.

**Hardware practices:** Limit entry points, tamper protection, secure-boot monitoring,
patches, interface management, restricted hardware access, protected keys and
credentials, event logs, anti-malware, isolation from regular supply units, and a
root of trust.

> **EXAM FOCUS:** A hardware root of trust anchors secure boot. Lockout slows online
> guessing but can enable lockout abuse, so combine it with monitoring and MFA.
> Trap: selecting UPnP disablement as a firmware-integrity control.

**Memory trick:** "Accounts, Access, Algorithms, Updates, Assets, Anatomy" groups
identity, network, crypto, patching, management, and hardware.

### 3.19 OT, ICS components, and IT/OT convergence

**What it is:** Operational technology (OT) is hardware and software that detects or
causes change in industrial operations by monitoring or controlling physical devices.
An industrial control system (ICS) is the collection of systems, networks, devices,
and controls that automate industrial processes.

**Analogy:** IT manages information; OT manages the movement and condition of the
physical world.

**Components:**

- PLC: programmable logic controller executing local deterministic control logic.
- RTU: remote terminal unit collecting field data and issuing control at remote sites.
- SCADA: supervisory control and data acquisition across geographically distributed
  processes.
- DCS: distributed control system coordinating controllers within a plant/process.
- HMI: human-machine interface for display and operator commands.
- BPCS: basic process control system; SIS: safety instrumented system for safe states.
- IED: intelligent electronic device; VFD: variable-frequency drive for motor speed.
- PID: proportional-integral-derivative control used to hold a process at a setpoint.

**IT/OT convergence and IIoT:** Integration links OT monitoring/control with IT storage
and processing such as SQL, Java, and Python to improve security, quality, efficiency,
and productivity. Industry 4.0 uses these ideas for smart manufacturing. IIoT is IoT
applied to industrial operations, supply chains, manufacturing, and management.

**Real-world use:** A plant historian sends carefully brokered production data to IT
analytics without allowing the analytics server to directly write to a safety PLC.

**Tools and commands used here:** Malcolm, Wireshark, Nmap OT scripts, Nessus,
Skybox, and Microsoft Defender for IoT support later assessments.

**AI angle (ADDED CONTEXT):** Predictive maintenance models can detect failing motors.
Poisoned sensor training data could hide failure. Prompt: "Identify data-quality checks
for this maintenance dataset and do not recommend changes to live control setpoints."

**Countermeasures and defense:** Keep safety functions independent, broker IT/OT data
through controlled zones, and design for availability and safe failure.

> **EXAM FOCUS:** HMI is the operator window; PLC is local logic; SCADA supervises
> wide-area operations; DCS distributes plant control. Trap: treating SIS as an ordinary
> business availability system instead of a safety system.

**Memory trick:** "PLC Performs, RTU Reaches, SCADA Supervises, DCS Distributes,
HMI Helps Humans."

### 3.20 Purdue model and OT protocol placement

**What it is:** The Purdue Enterprise Reference Architecture (PERA) inspired a model
of ICS zones and dependencies. The enterprise zone and manufacturing zone are
separated by an industrial DMZ (IDMZ).

**Analogy:** A factory has public offices, a controlled reception, operations rooms,
supervisor desks, machine controllers, and the machines themselves.

**Levels:**

1. Level 5: enterprise network.
2. Level 4: business logistics systems.
3. Level 3.5: IDMZ, the brokered boundary between IT and OT.
4. Level 3: operations systems/site operations.
5. Level 2: control systems/area supervisory control.
6. Level 1: basic control/intelligent devices.
7. Level 0: physical process, sensors, and actuators.

**Protocol mapping from the notes:**

- Levels 4/5: DCOM, FTP/SFTP, GE-SRTP, IPv4/IPv6, OPC UA, TCP/IP, Wi-Fi, SMTP,
  HTTP/HTTPS.
- Level 3: CC-Link, GE-SRTP, HSCP, ICCP (IEC 60870-6), IEC 61850, IEC 60870-5-104,
  ISA/IEC 62443, Modbus, NTP, Profinet, SuiteLink, Tase.2, TCP/IP, ControlNet,
  Profibus PA/DP.
- Level 2: 6LoWPAN, CC-Link, DNP3, DNS/DNSSEC, FTE, HART-IP, IEC 60870-5-101/104,
  IPv4/IPv6, ISA/IEC 62443, OPC, NTP, SOAP, TCP/IP, DeviceNet, AS-Interface.
- Levels 0/1: BACnet, EtherCAT, CANopen, Crimson v3, GE-SRTP, Zigbee, ISA/IEC 62443,
  ISA SP100, MELSEC-Q, Modbus, Niagara Fox, Omron FINS, PCWorx, Profibus, Profinet,
  Sercos II, S7 Communications, WiMAX, and FOUNDATION Fieldbus.

> **ADDED CONTEXT:** ISA/IEC 62443 is a security standard series, not a wire protocol.
> Protocols can appear at multiple levels depending on architecture. Learn the slide's
> representative placement, not an absolute rule that a protocol can exist at one level.

**Real-world use:** A design team places a patch broker and historian replica in the
IDMZ rather than connecting the enterprise directly to Level 1 controllers.

**Tools and commands used here:** Firewalls, data diodes where suitable, protocol-aware
monitoring, Malcolm, and securely configured jump hosts.

**Countermeasures and defense:** Define zones by function and risk, permit only required
conduit traffic, and block direct enterprise-to-controller access.

> **EXAM FOCUS:** Level 0 is physical process, not basic controller; Level 3.5 is IDMZ.
> Trap: placing business email at Level 2 or a PLC at Level 4.

**Memory trick:** "Five Enterprise, Four Business, Three Operations, Two Supervise,
One Control, Zero Physical."
