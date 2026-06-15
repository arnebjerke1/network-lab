// ===== BATCH 5: DOMAIN 3b — IoT, DLP, SaaS, SD-WAN, EFFICACY (ids 3051–3095) =====
// Paste into your QUESTIONS array.

{
  id: 3051, cat: "D3: IoT/DLP/SaaS",
  q: "A hospital network has hundreds of unmanaged IoMT devices (infusion pumps, imaging systems) with no agents possible. What does Palo Alto Networks IoT Security primarily provide first?",
  opts: ["Endpoint antivirus on each device", "Discovery and visibility — identifying and profiling every connected device", "Replacing all the devices", "Disabling the network"],
  a: 1,
  why: "You can't secure what you can't see. IoT Security's foundation is discovery and visibility: it identifies, classifies, and profiles every connected device (including unmanaged IoT/IoMT/OT) without agents. From that inventory, behavior baselines and policy recommendations follow."
},
{
  id: 3052, cat: "D3: IoT/DLP/SaaS",
  q: "How does Palo Alto Networks IoT Security identify and classify devices without installing software on them?",
  opts: ["By guessing randomly", "By analyzing network traffic/behavior (often with ML) to fingerprint device type, vendor, and model", "By asking the user", "By scanning barcodes"],
  a: 1,
  why: "IoT Security uses agentless, ML-driven analysis of network traffic to fingerprint devices — inferring type, vendor, model, OS, and behavior from how they communicate. This is essential for headless devices that can't run agents, building an accurate inventory passively."
},
{
  id: 3053, cat: "D3: IoT/DLP/SaaS",
  q: "After profiling a device's normal behavior, how does IoT Security help detect compromise?",
  opts: ["It ignores behavior", "It baselines normal behavior and flags anomalies that deviate from the device's expected pattern", "It blocks all devices", "It only logs once a year"],
  a: 1,
  why: "By learning each device's normal communication patterns, IoT Security can detect anomalies — e.g., a camera suddenly scanning the network or contacting an unusual destination — that may indicate compromise. Behavioral baselining is key since IoT devices have predictable, narrow roles."
},
{
  id: 3054, cat: "D3: IoT/DLP/SaaS",
  q: "Which capability lets the firewall enforce policy on IoT devices discovered by IoT Security, even though they have no user?",
  opts: ["User-ID", "Device-ID", "Source NAT", "QoS only"],
  a: 1,
  why: "Device-ID provides a device-centric policy handle, so rules can be written for specific devices/device types regardless of user. IoT Security feeds device context to the firewall, and Device-ID enforces least-privilege segmentation for those headless devices."
},
{
  id: 3055, cat: "D3: IoT/DLP/SaaS",
  q: "IoT Security recommends policies to restrict a smart thermostat to only its required communications. This best embodies which principle?",
  opts: ["Allow-all convenience", "Least-privilege segmentation to limit attack surface and lateral movement", "Disabling logging", "Open trust"],
  a: 1,
  why: "Confining a device to only its necessary communications is least-privilege segmentation. For IoT/OT — often unpatchable and vulnerable — this containment is critical: if compromised, the device can't reach much else, limiting blast radius and lateral movement."
},
{
  id: 3056, cat: "D3: IoT/DLP/SaaS",
  q: "Why is IoT Security especially valuable for operational technology (OT) and medical (IoMT) devices?",
  opts: ["They are easy to patch", "They often can't be patched or run agents, so network-based visibility and segmentation are the main defenses", "They have no value", "They never get attacked"],
  a: 1,
  why: "OT/IoMT devices are frequently fragile, long-lived, and unpatchable, and they can't run endpoint agents. Network-based discovery, behavioral monitoring, and segmentation become the primary protective controls — exactly what IoT Security plus Device-ID provide."
},
{
  id: 3057, cat: "D3: IoT/DLP/SaaS",
  q: "What is the primary purpose of Enterprise Data Loss Prevention (DLP)?",
  opts: ["To speed up downloads", "To detect and prevent sensitive data (e.g., PII, financial, health) from leaving the organization improperly", "To block all traffic", "To manage HA"],
  a: 1,
  why: "Enterprise DLP identifies sensitive data (credit card numbers, SSNs, health records, intellectual property) and enforces policy to prevent its unauthorized exposure or exfiltration — across network and SaaS. It protects confidentiality and supports compliance (e.g., PCI, HIPAA, GDPR)."
},
{
  id: 3058, cat: "D3: IoT/DLP/SaaS",
  q: "How does DLP typically recognize sensitive content like credit card numbers within traffic or files?",
  opts: ["By file size only", "Using data patterns/identifiers (e.g., regex, predefined data patterns, keywords, ML) to match sensitive data types", "By blocking everything", "By IP address"],
  a: 1,
  why: "DLP uses content inspection techniques — predefined data patterns, regular expressions, keywords, and ML classifiers — to recognize sensitive data types (e.g., card numbers passing validation, SSNs). This content awareness is what distinguishes DLP from simple network controls."
},
{
  id: 3059, cat: "D3: IoT/DLP/SaaS",
  q: "An employee tries to upload a spreadsheet of customer credit card numbers to a personal cloud drive. With DLP enabled, the expected outcome is:",
  opts: ["The upload is always allowed", "DLP can detect the sensitive data and block or alert on the transfer per policy", "DLP deletes the firewall", "Nothing is inspected"],
  a: 1,
  why: "DLP inspects the content, recognizes the cardholder data, and enforces policy — blocking or alerting on the risky upload to an unsanctioned destination. This is a classic data-exfiltration/insider-risk scenario DLP is designed to stop."
},
{
  id: 3060, cat: "D3: IoT/DLP/SaaS",
  q: "Why is Enterprise DLP being cloud-delivered and integrated across the platform advantageous?",
  opts: ["It only works on one firewall", "Consistent data-protection policies can be enforced across network, SaaS, and remote users from a unified service", "It disables inspection", "It slows compliance"],
  a: 1,
  why: "A unified, cloud-delivered DLP applies consistent data-classification and protection policies everywhere data flows — on-prem, in SaaS, and for remote users — rather than maintaining separate, inconsistent DLP per channel. Consistency reduces gaps and simplifies compliance."
},
{
  id: 3061, cat: "D3: IoT/DLP/SaaS",
  q: "What is the primary goal of SaaS Security (e.g., SaaS Security/CASB capabilities)?",
  opts: ["To block all SaaS", "To provide visibility and control over sanctioned and unsanctioned SaaS app usage and protect data within them", "To speed up the WAN", "To manage certificates"],
  a: 1,
  why: "SaaS Security (CASB) gives visibility into which SaaS apps are used (including unsanctioned 'shadow IT'), enforces access/usage policy, and protects sensitive data within sanctioned apps. As business moves to SaaS, controlling app usage and data exposure is essential."
},
{
  id: 3062, cat: "D3: IoT/DLP/SaaS",
  q: "What does 'Shadow IT' refer to in the context of SaaS Security?",
  opts: ["Approved corporate apps", "Unsanctioned SaaS applications used by employees without IT approval/oversight", "The IT help desk", "Firewall shadow rules"],
  a: 1,
  why: "Shadow IT is the use of unsanctioned apps/services without IT's knowledge or approval, creating data-exposure and compliance risks. SaaS Security discovers this usage so organizations can assess risk and bring it under policy — a primary CASB use case."
},
{
  id: 3063, cat: "D3: IoT/DLP/SaaS",
  q: "An organization discovers employees storing sensitive files in unsanctioned cloud apps. Which combination addresses this best?",
  opts: ["NAT + QoS", "SaaS Security (to discover/control the apps) plus DLP (to protect the sensitive data)", "HA + DHCP", "Disabling logging"],
  a: 1,
  why: "SaaS Security surfaces and controls the unsanctioned apps (shadow IT), while DLP detects and protects the sensitive data itself. Used together, they govern both the application usage and the data within/leaving it — a layered data-protection approach."
},
{
  id: 3064, cat: "D3: IoT/DLP/SaaS",
  q: "How can SaaS Security protect data within sanctioned apps (e.g., a corporate file-sharing service)?",
  opts: ["By ignoring the app", "By scanning for sensitive data, risky sharing/exposure, and enforcing policy (often via API integration)", "By blocking the whole app", "By disabling DLP"],
  a: 1,
  why: "API-based (inline and out-of-band) SaaS Security can scan content in sanctioned apps for sensitive data, detect risky public/external sharing, and enforce remediation — without blocking the app entirely. This secures data in apps the business legitimately uses."
},
{
  id: 3065, cat: "D3: IoT/DLP/SaaS",
  q: "What is the difference between inline and API-based (out-of-band) SaaS Security approaches?",
  opts: ["They are identical", "Inline controls traffic in real time as users access apps; API-based connects to the SaaS to scan data/config already stored", "API-based blocks traffic in real time", "Inline only scans stored data"],
  a: 1,
  why: "Inline (proxy) controls access and data in transit in real time, while API-based integration connects directly to the SaaS provider to inspect data at rest, sharing settings, and configurations. Combining both gives comprehensive coverage of SaaS usage and stored data."
},
{
  id: 3066, cat: "D3: IoT/DLP/SaaS",
  q: "PAN-OS SD-WAN (the SD-WAN capability integrated into PAN-OS firewalls) primarily enables:",
  opts: ["Only logging", "Intelligent path selection and WAN optimization directly on the NGFW for branch connectivity", "Cloud sandboxing", "Certificate issuance"],
  a: 1,
  why: "PAN-OS SD-WAN integrates software-defined WAN functionality into the NGFW itself, enabling app-aware path selection, link health monitoring, and failover across multiple WAN links — combining security and SD-WAN on one platform for branches."
},
{
  id: 3067, cat: "D3: IoT/DLP/SaaS",
  q: "A benefit of running SD-WAN within PAN-OS (rather than a separate appliance) is:",
  opts: ["More boxes to manage", "Converged security + SD-WAN on one platform, simplifying the branch and unifying policy", "Less security", "No path selection"],
  a: 1,
  why: "Integrating SD-WAN into the NGFW consolidates connectivity and security into a single platform at the branch, reducing hardware sprawl and unifying management/policy. This convergence is a practical step toward a simpler, secure branch architecture."
},
{
  id: 3068, cat: "D3: IoT/DLP/SaaS",
  q: "How does PAN-OS SD-WAN improve application experience for a branch with multiple internet links?",
  opts: ["By using one link only", "By steering each application over the best-performing path based on real-time metrics and failing over on degradation", "By blocking applications", "By disabling monitoring"],
  a: 1,
  why: "It measures link quality (latency, jitter, loss) and dynamically routes applications over the optimal path, with automatic failover if a link degrades. Loss/latency-sensitive apps (voice, video) especially benefit, improving experience over static single-path routing."
},
{
  id: 3069, cat: "D3: IoT/DLP/SaaS",
  q: "When evaluating 'security efficacy' of the NGFW and Prisma SASE, which factors matter most?",
  opts: ["Only price", "How effectively policies, App-ID, User-ID, decryption, and threat services detect/prevent threats with accurate visibility", "Cable color", "Number of reboots"],
  a: 1,
  why: "Security efficacy is about how well the platform actually prevents threats and provides accurate visibility — driven by correct policy, App-ID/User-ID accuracy, decryption coverage, and threat-prevention performance. High efficacy means real threats are caught with minimal gaps."
},
{
  id: 3070, cat: "D3: IoT/DLP/SaaS",
  q: "Why does enabling decryption significantly increase the security efficacy of threat services?",
  opts: ["It reduces visibility", "It removes the encrypted blind spot so App-ID, DLP, and threat services can inspect the actual content", "It disables App-ID", "Threats avoid encryption"],
  a: 1,
  why: "Without decryption, encrypted traffic is a blind spot where threats and data exfiltration hide. Decryption restores content visibility, dramatically improving the efficacy of App-ID, DLP, and CDSS threat services on the majority of traffic that is now encrypted."
},
{
  id: 3071, cat: "D3: IoT/DLP/SaaS",
  q: "How does accurate App-ID contribute to overall security efficacy?",
  opts: ["It mislabels traffic", "Correctly identifying applications ensures the right policy and inspection are applied, reducing both risk and false outcomes", "It only checks ports", "It disables profiles"],
  a: 1,
  why: "Precise application identification ensures policies and inspection target the right traffic, enabling correct enforcement (allow the right apps, inspect them properly) and reducing misclassification. Accurate App-ID is foundational to effective, low-error security outcomes."
},
{
  id: 3072, cat: "D3: IoT/DLP/SaaS",
  q: "An IoT camera begins communicating with an external server in a foreign country it never contacted before. How does IoT Security plus segmentation respond ideally?",
  opts: ["Allow it silently", "Flag the anomalous behavior and, via Device-ID policy, restrict the device to its expected communications", "Delete all logs", "Disable the firewall"],
  a: 1,
  why: "IoT Security detects the behavioral anomaly (new, unexpected external contact), and Device-ID-based least-privilege policy confines the camera to its normal communications — blocking the suspicious connection. Visibility plus enforced segmentation contains potential compromise."
},
{
  id: 3073, cat: "D3: IoT/DLP/SaaS",
  q: "Why is DLP important even for traffic to sanctioned, trusted cloud apps?",
  opts: ["Trusted apps can't leak data", "Sensitive data can still be improperly shared or exposed within/through sanctioned apps, so content inspection is needed", "DLP only works on blocked apps", "Sanctioned apps need no controls"],
  a: 1,
  why: "Even sanctioned apps can become channels for improper data exposure (oversharing, wrong recipients, public links). DLP inspects content regardless of the app's trust status, enforcing data-handling policy so sensitive information isn't mishandled even in approved services."
},
{
  id: 3074, cat: "D3: IoT/DLP/SaaS",
  q: "What is a key compliance driver for deploying Enterprise DLP?",
  opts: ["There are none", "Regulations (e.g., PCI DSS, HIPAA, GDPR) require protecting specific sensitive data types from unauthorized exposure", "To slow the network", "To disable encryption"],
  a: 1,
  why: "Many regulations mandate safeguarding particular data (cardholder data for PCI, health data for HIPAA, personal data for GDPR). DLP helps enforce and demonstrate these controls by detecting and preventing improper handling of regulated data — directly supporting compliance."
},
{
  id: 3075, cat: "D3: IoT/DLP/SaaS",
  q: "How does combining IoT Security with the broader platform improve threat response for a compromised device?",
  opts: ["It isolates nothing", "Device context and risk can drive automated/enforced policy (e.g., segmentation, blocking) to contain the device", "It only sends an email yearly", "It disables Device-ID"],
  a: 1,
  why: "IoT Security shares device identity, risk, and behavior with the platform, so enforcement (segmentation, blocking via Device-ID policy) can contain a compromised device quickly. Integrating discovery with enforcement turns visibility into actionable, automated protection."
},
{
  id: 3076, cat: "D3: IoT/DLP/SaaS",
  q: "Which best describes why unmanaged devices are a growing security concern that IoT Security targets?",
  opts: ["There are fewer of them each year", "Their numbers are exploding, they often lack built-in security, and they expand the attack surface", "They can all run antivirus", "They are never connected"],
  a: 1,
  why: "Unmanaged IoT/OT/IoMT devices are proliferating, frequently ship with weak or no security, can't run traditional protections, and dramatically expand the attack surface. IoT Security exists precisely to discover, assess, and help contain this hard-to-manage population."
},
{
  id: 3077, cat: "D3: IoT/DLP/SaaS",
  q: "A SaaS Security solution flags that a sensitive document in a sanctioned app is shared via a public, anyone-with-the-link URL. The ideal response is to:",
  opts: ["Ignore it", "Alert/remediate the risky exposure per policy (e.g., revoke public sharing)", "Delete the firewall", "Block all SaaS permanently"],
  a: 1,
  why: "Public 'anyone with the link' sharing of sensitive data is a common SaaS exposure. SaaS Security can detect and remediate it (alerting, revoking the public link, or restricting access) per policy — protecting data without blocking the legitimate app."
},
{
  id: 3078, cat: "D3: IoT/DLP/SaaS",
  q: "Why is behavioral anomaly detection particularly effective for IoT devices compared with general-purpose computers?",
  opts: ["IoT behavior is unpredictable", "IoT devices have narrow, predictable functions, so deviations are easier to spot as anomalies", "Computers never change behavior", "IoT devices have no network traffic"],
  a: 1,
  why: "IoT devices typically perform a few specific functions with consistent communication patterns, making baseline 'normal' tight and deviations stand out clearly. General-purpose computers vary widely, so anomaly detection is comparatively noisier there. Predictability is an IoT-security advantage."
},
{
  id: 3079, cat: "D3: IoT/DLP/SaaS",
  q: "How does the platform's unified approach to DLP across network and SaaS reduce risk compared with point solutions?",
  opts: ["It creates inconsistency", "One consistent data-classification and policy set covers multiple channels, closing gaps that siloed tools leave", "It only covers email", "It disables SaaS"],
  a: 1,
  why: "Disjointed point DLP tools often apply inconsistent rules across channels, leaving gaps attackers/insiders exploit. A unified DLP applies the same data definitions and policy across network and SaaS, ensuring consistent protection and simpler management."
},
{
  id: 3080, cat: "D3: IoT/DLP/SaaS",
  q: "What does it mean that IoT Security provides a 'risk score' or risk assessment for devices?",
  opts: ["It ranks device color", "It evaluates factors (vulnerabilities, behavior, criticality) to prioritize which devices pose the most risk", "It measures power use only", "It disables risky devices automatically forever"],
  a: 1,
  why: "Risk scoring helps prioritize attention by weighing known vulnerabilities, anomalous behavior, exposure, and device criticality. With potentially thousands of devices, risk-based prioritization focuses remediation and segmentation efforts where they matter most."
},
{
  id: 3081, cat: "D3: IoT/DLP/SaaS",
  q: "Why might PAN-OS SD-WAN steer a real-time voice application differently than a bulk file backup?",
  opts: ["They have identical needs", "Voice is sensitive to latency/jitter/loss while bulk transfer tolerates them, so paths are chosen per application requirements", "Backups need the fastest path always", "SD-WAN ignores app type"],
  a: 1,
  why: "App-aware SD-WAN matches each application to a suitable path: latency/jitter-sensitive voice gets the most stable link, while throughput-oriented backups can use higher-capacity or lower-priority paths. Tailoring path selection to app needs optimizes experience and link use."
},
{
  id: 3082, cat: "D3: IoT/DLP/SaaS",
  q: "How does SaaS Security help enforce that only sanctioned instances of an app are used (e.g., corporate vs. personal accounts)?",
  opts: ["It can't distinguish them", "It can apply tenant/instance-aware controls to allow the corporate instance and restrict personal ones", "It blocks the entire app category", "It disables authentication"],
  a: 1,
  why: "SaaS Security can be instance/tenant-aware, allowing the sanctioned corporate account of an app while restricting personal or unsanctioned instances. This prevents data from flowing into personal tenants while keeping the legitimate business app fully usable."
},
{
  id: 3083, cat: "D3: IoT/DLP/SaaS",
  q: "What is the relationship between IoT Security's discovery and the firewall's enforcement?",
  opts: ["They are unrelated", "IoT Security discovers/classifies devices and shares context so the firewall (via Device-ID) can enforce appropriate policy", "The firewall discovers; IoT Security enforces", "Neither enforces policy"],
  a: 1,
  why: "IoT Security provides the visibility and device intelligence, which feeds the firewall's Device-ID so enforcement (segmentation, least-privilege rules) can be applied. Discovery and enforcement work together: see the devices, then control them appropriately."
},
{
  id: 3084, cat: "D3: IoT/DLP/SaaS",
  q: "Why is content-aware inspection (App-ID + Content-ID + DLP) more effective than blocking apps wholesale for data protection?",
  opts: ["Blocking everything is best", "It allows legitimate business use while still preventing sensitive-data exposure, balancing productivity and security", "It disables business apps", "It ignores data"],
  a: 1,
  why: "Wholesale blocking harms productivity and drives shadow IT. Content-aware controls permit legitimate use of apps while inspecting for and preventing sensitive-data exposure — a precise balance that protects data without crippling the business. Granularity beats blunt blocking."
},
{
  id: 3085, cat: "D3: IoT/DLP/SaaS",
  q: "An organization wants to reduce the chance that a vulnerable IoT device becomes a pivot point into critical systems. The MOST effective control is:",
  opts: ["Putting all devices on one flat network", "Segmenting IoT devices away from critical systems with least-privilege policy (informed by IoT Security)", "Disabling logging", "Allowing all internal traffic"],
  a: 1,
  why: "Segmenting IoT/OT devices from critical systems and enforcing least-privilege communication prevents a compromised, unpatchable device from pivoting deeper. IoT Security informs which devices exist and how they should behave, enabling precise segmentation — the strongest practical control."
},
{
  id: 3086, cat: "D3: IoT/DLP/SaaS",
  q: "How does DLP typically handle different policy actions for sensitive data (e.g., block vs. alert vs. log)?",
  opts: ["Only one action is possible", "Policy can be tuned per data type/context — e.g., block external transfers but only alert on internal ones", "It always blocks everything", "It only logs once"],
  a: 1,
  why: "DLP supports graduated responses based on data sensitivity and context: block high-risk exfiltration, alert on borderline cases, or simply log for visibility. Tuning actions prevents excessive disruption while still protecting the most sensitive data — a practical, risk-based approach."
},
{
  id: 3087, cat: "D3: IoT/DLP/SaaS",
  q: "Why is visibility into unsanctioned SaaS (shadow IT) a prerequisite for reducing SaaS risk?",
  opts: ["You can secure unknown apps automatically", "You can't assess or control apps you don't know are being used, so discovery comes first", "Discovery is unnecessary", "Blocking comes before discovery"],
  a: 1,
  why: "You can't govern what you can't see. Discovering which SaaS apps employees actually use is the first step to assessing their risk and applying policy (allow, restrict, or block). SaaS Security's discovery turns invisible shadow IT into a manageable, risk-ranked inventory."
},
{
  id: 3088, cat: "D3: IoT/DLP/SaaS",
  q: "What is a key advantage of integrating SD-WAN, security, and SaaS/data controls within one platform/ecosystem?",
  opts: ["More silos and complexity", "Unified visibility and consistent policy across connectivity, threats, and data, simplifying operations", "Less security", "No policy at all"],
  a: 1,
  why: "An integrated platform provides one coherent view and consistent policy spanning WAN connectivity, threat prevention, and data protection — reducing the complexity, gaps, and inconsistencies of stitching together separate products. This is central to the SASE/platform value proposition."
},
{
  id: 3089, cat: "D3: IoT/DLP/SaaS",
  q: "How does monitoring and logging contribute to validating ongoing security efficacy?",
  opts: ["It hides results", "Logs/metrics reveal what threats were detected/blocked and where gaps exist, enabling tuning and proof of effectiveness", "It disables detection", "It only stores errors"],
  a: 1,
  why: "Monitoring and logging show real outcomes — threats caught, policies hit, anomalies seen — which lets teams measure efficacy, find blind spots, tune policy, and demonstrate value/compliance. Without this feedback, you can't verify the security controls are actually working."
},
{
  id: 3090, cat: "D3: IoT/DLP/SaaS",
  q: "Why is identifying the specific device model and firmware (via IoT Security) useful for vulnerability management?",
  opts: ["It isn't useful", "Knowing exact models/firmware lets you correlate known vulnerabilities and prioritize mitigation/segmentation", "It only matters for laptops", "Firmware is irrelevant"],
  a: 1,
  why: "Precise device identification (model, firmware/OS) allows correlation with known vulnerabilities (CVEs) for that device, so you can prioritize patching (where possible), compensating controls, or segmentation. Accurate fingerprinting underpins effective IoT vulnerability management."
},
{
  id: 3091, cat: "D3: IoT/DLP/SaaS",
  q: "A company allows a corporate file-sharing SaaS but must prevent regulated data from being downloaded to unmanaged personal devices. Which approach fits best?",
  opts: ["Block the app entirely", "Use SaaS Security/access controls (and DLP) to allow access but restrict risky downloads based on device/context", "Allow all downloads", "Disable the firewall"],
  a: 1,
  why: "Context-aware SaaS controls (combined with DLP) can permit the sanctioned app while restricting risky actions — like blocking sensitive downloads to unmanaged devices — based on device posture/context. This protects regulated data without banning a needed business app."
},
{
  id: 3092, cat: "D3: IoT/DLP/SaaS",
  q: "How does the combination of Device-ID and IoT Security support Zero Trust for devices?",
  opts: ["It trusts all devices by default", "It verifies device identity and confines each device to least-privilege access based on its known, expected behavior", "It removes all policy", "It only applies to users"],
  a: 1,
  why: "Zero Trust extends to devices: IoT Security establishes device identity and expected behavior, and Device-ID enforces least-privilege access accordingly — never implicitly trusting a device just because it's on the network. This contains risk from compromised or rogue devices."
},
{
  id: 3093, cat: "D3: IoT/DLP/SaaS",
  q: "Why is DLP content inspection often paired with decryption?",
  opts: ["DLP works only on plaintext and most data flows are encrypted, so decryption is needed to inspect them", "Decryption disables DLP", "DLP never needs to see content", "Encryption helps DLP read data"],
  a: 0,
  why: "DLP must inspect the actual content to detect sensitive data, but most traffic (web uploads, SaaS) is encrypted. Decryption exposes the content so DLP can analyze it; without decryption, sensitive data could be exfiltrated inside TLS unseen. The two are commonly paired."
},
{
  id: 3094, cat: "D3: IoT/DLP/SaaS",
  q: "Which statement best captures the overall purpose of Domain 3's CDSS and data/SaaS/IoT services together?",
  opts: ["They each work in isolation with no synergy", "They extend the platform with specialized, cloud-powered protections (threats, data, SaaS, IoT) for comprehensive, consistent security", "They replace the firewall entirely", "They only apply to on-prem hardware"],
  a: 1,
  why: "These services layer specialized, cloud-delivered protections onto the platform — covering threats (CDSS), data (DLP), SaaS usage, and IoT/OT devices — to deliver comprehensive, consistent security across modern environments. Together they address the breadth of today's attack surface."
},
{
  id: 3095, cat: "D3: IoT/DLP/SaaS",
  q: "A manufacturer wants to secure both its IT network and OT/IoT factory devices with consistent visibility and policy. Which platform approach is most appropriate?",
  opts: ["Separate, unintegrated tools with no shared context", "Use NGFW/SASE with IoT Security and Device-ID to discover, segment, and enforce policy across IT and OT consistently", "Leave OT devices unmonitored", "Block all factory devices"],
  a: 1,
  why: "Securing converged IT/OT requires unified visibility and consistent enforcement. The platform's NGFW/SASE with IoT Security (discovery, behavior, risk) and Device-ID (enforcement) lets the manufacturer segment and protect fragile OT/IoT alongside IT — without unmanageable, siloed tools."
}