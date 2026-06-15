// ===== BATCH 4: DOMAIN 3a — CLOUD-DELIVERED SECURITY SERVICES (ids 3001–3050) =====
// Paste into your QUESTIONS array.

{
  id: 3001, cat: "D3: CDSS",
  q: "An unknown executable is downloaded that no existing signature recognizes. Which CDSS service is designed to detonate it in a cloud sandbox to determine if it's malicious?",
  opts: ["Advanced URL Filtering", "Advanced WildFire", "Advanced DNS Security", "User-ID"],
  a: 1,
  why: "Advanced WildFire is the cloud-based malware analysis (sandbox) service. It executes unknown files in a safe environment to observe behavior, renders a verdict, and distributes new protections to subscribers — catching zero-day/unknown malware that signatures alone miss."
},
{
  id: 3002, cat: "D3: CDSS",
  q: "After WildFire determines a previously unknown file is malicious, what is the key benefit for ALL subscribers?",
  opts: ["Only the original firewall is protected", "New protections are generated and shared globally, so other subscribers are protected from that threat", "Nothing changes", "The file is whitelisted"],
  a: 1,
  why: "WildFire's cloud model means a new verdict benefits the entire community: once a sample is found malicious, protections propagate to all subscribers rapidly. This collective defense turns one detection into protection for everyone, shrinking the window of exposure."
},
{
  id: 3003, cat: "D3: CDSS",
  q: "What is the primary advantage of 'Advanced' WildFire's near-real-time analysis compared with older batch-style sandboxing?",
  opts: ["It analyzes nothing", "Faster verdicts and inline prevention of unknown threats rather than waiting long periods", "It only works offline", "It disables signatures"],
  a: 1,
  why: "Advanced WildFire emphasizes faster, often inline analysis so unknown threats can be blocked closer to real time, rather than discovered after the fact. Speed matters: the sooner a verdict is returned, the smaller the chance the threat succeeds."
},
{
  id: 3004, cat: "D3: CDSS",
  q: "Advanced Threat Prevention (ATP) extends traditional IPS by adding which capability?",
  opts: ["WAN optimization", "Inline, ML/AI-based detection of evasive and unknown command-and-control and exploits", "Certificate issuance", "DHCP services"],
  a: 1,
  why: "Advanced Threat Prevention augments signature-based IPS with inline machine-learning models that detect previously unknown and evasive threats (e.g., novel C2, zero-day exploit attempts) in real time. This catches threats that lack a known signature."
},
{
  id: 3005, cat: "D3: CDSS",
  q: "Why is inline (real-time) analysis in Advanced Threat Prevention valuable against modern C2 traffic?",
  opts: ["C2 is always known in advance", "Attackers constantly create new, unknown C2 that signatures haven't seen; inline ML can catch it as it happens", "It only blocks old threats", "It disables logging"],
  a: 1,
  why: "Modern command-and-control is frequently new and evasive, evading signature-only detection. Inline ML-based analysis evaluates traffic in real time to identify malicious patterns even without a prior signature — closing the gap on unknown C2 and exploits."
},
{
  id: 3006, cat: "D3: CDSS",
  q: "Advanced URL Filtering improves on legacy URL filtering primarily by:",
  opts: ["Only using a static database", "Using inline ML to analyze and categorize new/unknown and malicious URLs in real time", "Blocking all websites", "Disabling decryption"],
  a: 1,
  why: "Advanced URL Filtering adds real-time, ML-driven analysis to catch newly created and previously unknown malicious URLs (e.g., fresh phishing pages) that a static category database would miss. This is critical because attackers spin up malicious sites constantly."
},
{
  id: 3007, cat: "D3: CDSS",
  q: "A phishing site was registered minutes ago and isn't in any category database yet. Which capability is best positioned to block it?",
  opts: ["Legacy static URL lists only", "Advanced URL Filtering's inline real-time analysis", "Source NAT", "HA failover"],
  a: 1,
  why: "Brand-new (zero-hour) phishing URLs won't be in static databases. Advanced URL Filtering analyzes URLs inline in real time to detect malicious/phishing characteristics on first encounter, protecting users before the site is formally categorized."
},
{
  id: 3008, cat: "D3: CDSS",
  q: "What problem does Advanced DNS Security primarily address?",
  opts: ["Slow web pages", "Malicious use of DNS such as DNS tunneling, DGA domains, and DNS-based C2/exfiltration", "Certificate expiry", "WAN routing"],
  a: 1,
  why: "Advanced DNS Security focuses on threats that abuse DNS — domain generation algorithms (DGAs), DNS tunneling, and malicious/newly registered domains used for C2 or data exfiltration. DNS is a common covert channel, so dedicated DNS protection closes that gap."
},
{
  id: 3009, cat: "D3: CDSS",
  q: "Malware uses a Domain Generation Algorithm (DGA) to create thousands of pseudo-random domains for C2. How does DNS Security counter this?",
  opts: ["By allowing all DNS", "By using ML to detect and block algorithmically generated and malicious domains", "By disabling DNS", "By rotating certificates"],
  a: 1,
  why: "DGAs let malware rapidly cycle through many domains, making static blocklists ineffective. DNS Security uses machine learning to recognize DGA patterns and other malicious domain behaviors, blocking them predictively rather than relying on known-bad lists."
},
{
  id: 3010, cat: "D3: CDSS",
  q: "A host makes steady, tiny DNS queries to a suspicious domain around the clock, even when idle. Which CDSS service is most relevant to detect this likely tunneling/C2?",
  opts: ["Advanced URL Filtering", "Advanced DNS Security", "GlobalProtect", "NAT"],
  a: 1,
  why: "Regular, automated DNS queries to a suspicious domain are a classic sign of DNS tunneling or DNS-based C2. Advanced DNS Security analyzes DNS traffic to identify and block such tunneling/beaconing patterns that abuse the DNS protocol."
},
{
  id: 3011, cat: "D3: CDSS",
  q: "What does GlobalProtect primarily provide?",
  opts: ["A cloud sandbox", "Secure connectivity for endpoints, extending firewall/SASE policy to remote and mobile users", "URL categorization", "A container firewall"],
  a: 1,
  why: "GlobalProtect is the endpoint connectivity component that extends consistent security policy to users wherever they are — connecting them to NGFW gateways or Prisma Access. It ensures remote users get the same protection as on-network users."
},
{
  id: 3012, cat: "D3: CDSS",
  q: "Why is GlobalProtect important for enforcing Zero Trust for a remote workforce?",
  opts: ["It grants unrestricted access", "It conveys user/device identity and posture so least-privilege, policy-based access can be enforced", "It disables authentication", "It only encrypts DNS"],
  a: 1,
  why: "GlobalProtect carries identity and device context (and can check posture) to the enforcement point, enabling least-privilege, policy-driven access rather than broad network access. This identity/context awareness underpins Zero Trust for off-network users."
},
{
  id: 3013, cat: "D3: CDSS",
  q: "How do CDSS subscriptions generally enhance the base NGFW?",
  opts: ["They replace the firewall OS", "They add cloud-powered, continuously updated security services (sandboxing, threat/URL/DNS intelligence) to the firewall", "They disable App-ID", "They only manage licenses"],
  a: 1,
  why: "CDSS are subscription services that layer cloud-scale intelligence and analysis onto the NGFW — e.g., WildFire sandboxing, Advanced Threat Prevention, URL and DNS security. They keep protection current against evolving threats beyond what static, on-box signatures provide."
},
{
  id: 3014, cat: "D3: CDSS",
  q: "What is a key reason cloud delivery (vs. purely on-box) benefits services like WildFire and URL/DNS security?",
  opts: ["The cloud is slower", "Cloud scale enables massive analysis, shared intelligence, and rapid global updates from many sources", "It disables detection", "It removes the need for policy"],
  a: 1,
  why: "Cloud delivery aggregates telemetry and analysis from a huge customer base, applies large-scale compute/ML, and pushes new protections globally fast. A single firewall can't match that scale of intelligence — which is why these services are cloud-powered."
},
{
  id: 3015, cat: "D3: CDSS",
  q: "Advanced WildFire, Advanced Threat Prevention, Advanced URL Filtering, and Advanced DNS Security increasingly rely on which technology to catch unknown threats?",
  opts: ["Manual signature writing only", "Machine learning / AI-based inline and cloud analysis", "Static port lists", "DHCP"],
  a: 1,
  why: "The 'Advanced' services emphasize machine learning and AI — both inline and in the cloud — to detect novel, evasive threats that signatures alone miss. This shift to ML-based detection is central to defending against zero-day and rapidly changing attacks."
},
{
  id: 3016, cat: "D3: CDSS",
  q: "A WildFire verdict of 'malicious' on a new sample most directly results in:",
  opts: ["The sample being ignored", "New protections (e.g., signatures/intelligence) that block that threat across the platform", "The firewall rebooting", "Decryption being disabled"],
  a: 1,
  why: "When WildFire deems a sample malicious, it generates protections that propagate to subscribers, so the threat is blocked going forward. This feedback loop — analyze unknown, render verdict, distribute protection — is the core value of cloud sandboxing."
},
{
  id: 3017, cat: "D3: CDSS",
  q: "How does Advanced URL Filtering help even when traffic is encrypted (with decryption enabled)?",
  opts: ["It ignores encrypted traffic", "It can analyze the decrypted web requests/URLs inline to catch malicious sites in real time", "It blocks all HTTPS", "It only works on plaintext HTTP"],
  a: 1,
  why: "With decryption enabling visibility, Advanced URL Filtering inspects the actual web requests and applies real-time ML analysis to block malicious URLs — including those hidden in HTTPS. This pairing of decryption + advanced URL analysis is key against modern web threats."
},
{
  id: 3018, cat: "D3: CDSS",
  q: "Why is signature-only protection insufficient against today's threat landscape?",
  opts: ["Signatures are too fast", "Attackers produce huge volumes of new/unknown variants daily that have no existing signature", "Signatures block everything", "Signatures disable App-ID"],
  a: 1,
  why: "The sheer volume and rapid mutation of modern malware/threats means many are 'unknown' with no signature yet. CDSS adds behavioral analysis (WildFire) and inline ML (ATP, Advanced URL/DNS) to catch these unknowns — complementing, not replacing, signatures."
},
{
  id: 3019, cat: "D3: CDSS",
  q: "Premium GlobalProtect typically enhances remote access by providing:",
  opts: ["Fewer security features", "Advanced capabilities (e.g., expanded posture, threat, and access features) beyond the base offering", "Only LAN access", "No encryption"],
  a: 1,
  why: "The Premium GlobalProtect subscription unlocks advanced functionality (such as enhanced posture checks, mobile features, and tighter integration with security services) beyond basic VPN connectivity. It strengthens secure access for the modern, distributed workforce."
},
{
  id: 3020, cat: "D3: CDSS",
  q: "What is the relationship between Advanced Threat Prevention and WildFire?",
  opts: ["They are identical", "ATP focuses on inline real-time threat/C2/exploit detection; WildFire analyzes unknown files in a cloud sandbox — together they cover more of the threat lifecycle", "ATP replaces WildFire", "Neither detects threats"],
  a: 1,
  why: "ATP and WildFire are complementary: ATP applies inline ML to catch evasive exploits and C2 in real time, while WildFire deeply analyzes unknown files in the cloud. Used together, they provide layered detection across network behavior and file-based threats."
},
{
  id: 3021, cat: "D3: CDSS",
  q: "An organization wants to block users from reaching newly registered domains often used in attacks. Which CDSS capability is most relevant?",
  opts: ["NAT", "DNS Security / URL Filtering categorization of newly registered or malicious domains", "HA", "QoS"],
  a: 1,
  why: "Newly registered domains are frequently used in phishing and C2. DNS Security and Advanced URL Filtering can identify and block newly registered/malicious domains, reducing exposure to fresh attacker infrastructure before it's widely known-bad."
},
{
  id: 3022, cat: "D3: CDSS",
  q: "Why does WildFire support analyzing many file types and URLs rather than just executables?",
  opts: ["Threats only come as .exe", "Attackers deliver malware via documents, scripts, archives, and links, so broad coverage is needed", "To slow analysis", "To disable detection"],
  a: 1,
  why: "Malware is delivered through many vectors — malicious Office docs, PDFs, scripts, archives, and links — not just executables. WildFire analyzes a broad range of file types and URLs so threats hiding in common business file formats are also caught."
},
{
  id: 3023, cat: "D3: CDSS",
  q: "How do CDSS services support consistent protection across both NGFW and Prisma SASE?",
  opts: ["They only work on hardware", "The same cloud-delivered intelligence/services can protect on-prem firewalls and cloud SASE users uniformly", "They require different threats per platform", "They disable SASE"],
  a: 1,
  why: "Because CDSS are cloud-delivered, the same threat, URL, DNS, and sandbox intelligence can protect on-prem NGFWs and SASE (e.g., Prisma Access) users consistently. This unifies protection so remote users aren't less protected than on-network users."
},
{
  id: 3024, cat: "D3: CDSS",
  q: "A primary reason to enable WildFire forwarding on the firewall is to:",
  opts: ["Block all files by default", "Submit eligible unknown samples for analysis so unknown threats can be identified and stopped", "Disable URL filtering", "Speed up NAT"],
  a: 1,
  why: "WildFire forwarding submits eligible unknown files (and links) to the cloud sandbox for analysis. Without forwarding, the firewall can't get verdicts on truly unknown samples, leaving zero-day threats undetected. It's how the firewall taps WildFire's intelligence."
},
{
  id: 3025, cat: "D3: CDSS",
  q: "What does it mean that Advanced Threat Prevention can detect threats 'inline'?",
  opts: ["It analyzes after the session ends only", "It evaluates traffic as it passes through, enabling real-time blocking before the threat completes", "It only works in the cloud later", "It disables prevention"],
  a: 1,
  why: "Inline detection means analysis happens in the live traffic path, so malicious activity (e.g., an exploit or C2 callback) can be blocked in real time rather than merely alerted on afterward. Real-time prevention reduces the chance the attack succeeds."
},
{
  id: 3026, cat: "D3: CDSS",
  q: "Why is combining decryption with CDSS threat services (WildFire, ATP, URL, DNS) considered essential today?",
  opts: ["Threats never use encryption", "Most threats hide in encrypted traffic, so without decryption these services have limited visibility", "Decryption disables CDSS", "CDSS only works on plaintext"],
  a: 1,
  why: "Since the bulk of traffic and threats are encrypted, decryption is what lets CDSS inspect the actual content. Without it, WildFire can't extract files, ATP can't see payloads, and URL/DNS analysis is constrained — undermining the services' effectiveness."
},
{
  id: 3027, cat: "D3: CDSS",
  q: "An organization is concerned about data exfiltration disguised within DNS queries. Beyond blocking, what additional value does DNS Security provide?",
  opts: ["It speeds up exfiltration", "Visibility/analytics into DNS-based threats and the ability to sinkhole malicious domains", "It disables DNS logging", "It only blocks HTTP"],
  a: 1,
  why: "DNS Security not only blocks malicious DNS but provides visibility and can 'sinkhole' malicious domains (redirecting them), helping identify infected hosts (which keep trying to reach the bad domain). This aids detection and remediation, not just prevention."
},
{
  id: 3028, cat: "D3: CDSS",
  q: "What is 'DNS sinkholing' used for?",
  opts: ["Speeding DNS", "Redirecting malicious domain requests to a controlled address to identify and contain infected internal hosts", "Disabling DNS", "Issuing certificates"],
  a: 1,
  why: "Sinkholing redirects queries for known-malicious domains to a controlled IP, so the firewall can identify which internal hosts attempted to reach the bad domain (revealing infections) and prevent the connection. It turns blocked DNS into actionable detection."
},
{
  id: 3029, cat: "D3: CDSS",
  q: "Which best explains why 'Advanced' versions of URL/DNS/Threat services emerged over their standard predecessors?",
  opts: ["To remove features", "To add real-time ML/AI analysis for unknown and rapidly changing threats that static methods miss", "To slow the firewall", "To disable cloud intelligence"],
  a: 1,
  why: "The 'Advanced' tiers add inline machine learning and cloud AI to detect zero-hour and evasive threats in real time, addressing the gap left by static databases and signatures. Attackers' speed and volume drove this evolution toward ML-based, real-time detection."
},
{
  id: 3030, cat: "D3: CDSS",
  q: "A user receives a link to a malicious site embedded in an email opened on the corporate network. Which layered CDSS response is most complete?",
  opts: ["Do nothing", "Advanced URL Filtering blocks the malicious URL; if a file downloads, WildFire analyzes it; ATP watches for exploit/C2 activity", "Only NAT the traffic", "Disable decryption"],
  a: 1,
  why: "Layered CDSS provides depth: URL Filtering blocks the malicious link, WildFire analyzes any downloaded file, and ATP detects exploit attempts or C2 callbacks. Multiple services covering different stages give the best chance to stop a multi-step attack."
},
{
  id: 3031, cat: "D3: CDSS",
  q: "Why might WildFire return a verdict of 'grayware' for some samples?",
  opts: ["It can't analyze files", "Some software is not clearly malicious but is unwanted/risky (e.g., adware), warranting a distinct category", "All files are malicious", "Grayware means safe"],
  a: 1,
  why: "WildFire distinguishes outright malware from 'grayware' — software that isn't clearly malicious but is unwanted or risky (adware, certain PUPs). This nuance lets organizations decide how to treat such files rather than forcing a binary good/bad verdict."
},
{
  id: 3032, cat: "D3: CDSS",
  q: "How does shared global threat intelligence across CDSS benefit a single customer the FIRST time a new threat appears anywhere?",
  opts: ["It offers no benefit", "Protections derived from one detection can preempt the threat for others before they're targeted", "It only helps after the customer is breached", "It disables protection"],
  a: 1,
  why: "Because intelligence is shared, a threat detected at one organization can yield protections that defend others before they encounter it. This community/herd-immunity effect is a major advantage of cloud-delivered, intelligence-sharing security services."
},
{
  id: 3033, cat: "D3: CDSS",
  q: "What role does App-ID play in making CDSS inspection effective?",
  opts: ["It disables CDSS", "It accurately identifies the application/traffic so the right inspection and policy are applied", "It only inspects ports", "It replaces WildFire"],
  a: 1,
  why: "App-ID precisely classifies traffic so the appropriate CDSS inspection (and policy) is applied to the right flows. Accurate identification ensures, for example, that web and file transfers are inspected appropriately — App-ID and CDSS work hand in hand."
},
{
  id: 3034, cat: "D3: CDSS",
  q: "An organization wants to reduce the risk that users fall for credential-phishing pages. Which combination is most directly relevant?",
  opts: ["NAT + QoS", "Advanced URL Filtering (block phishing URLs) plus credential-phishing prevention features", "HA + DHCP", "Disabling decryption"],
  a: 1,
  why: "Advanced URL Filtering blocks phishing URLs in real time, and the platform offers credential-phishing prevention (e.g., detecting/blocking corporate credential submission to untrusted sites). Together they directly target the credential-theft phishing problem."
},
{
  id: 3035, cat: "D3: CDSS",
  q: "Why is it beneficial that CDSS services are continuously updated from the cloud rather than only at upgrade time?",
  opts: ["Threats are static", "New threats appear constantly, so continuous updates keep protection current without waiting for software upgrades", "Updates slow detection", "It disables policy"],
  a: 1,
  why: "Threats emerge continuously, so waiting for periodic software upgrades would leave dangerous gaps. Cloud-delivered, continuous updates ensure the latest intelligence and protections are applied promptly — a core advantage of the CDSS model."
},
{
  id: 3036, cat: "D3: CDSS",
  q: "What is the security purpose of WildFire analyzing a file's actual behavior (dynamic analysis) rather than only its static properties?",
  opts: ["Behavior is irrelevant", "Malware may hide malicious intent until executed; observing runtime behavior reveals it", "Static analysis catches everything", "It disables sandboxing"],
  a: 1,
  why: "Sophisticated malware can appear benign statically but reveal malicious actions only when run (e.g., contacting C2, encrypting files). Dynamic (behavioral) analysis in a sandbox detonates the sample to observe what it actually does, catching evasive threats."
},
{
  id: 3037, cat: "D3: CDSS",
  q: "How does Advanced DNS Security complement URL Filtering?",
  opts: ["They are redundant", "DNS Security secures the name-resolution layer (tunneling, DGA, malicious domains) while URL Filtering governs web access by URL/category", "DNS Security blocks all web", "URL Filtering handles DNS tunneling"],
  a: 1,
  why: "They protect different layers: DNS Security focuses on the DNS protocol (tunneling, DGAs, malicious domain resolution), while URL Filtering controls access to web content by URL/category. Together they cover both name resolution and web access threats."
},
{
  id: 3038, cat: "D3: CDSS",
  q: "A key reason to enable multiple CDSS subscriptions together is:",
  opts: ["To reduce coverage", "Defense in depth — each service addresses different threat vectors and stages for layered protection", "To disable the firewall", "To slow traffic intentionally"],
  a: 1,
  why: "Each CDSS targets a different vector — files (WildFire), exploits/C2 (ATP), web URLs (URL Filtering), DNS abuse (DNS Security). Enabling them together provides layered, defense-in-depth coverage so a threat slipping past one layer can be caught by another."
},
{
  id: 3039, cat: "D3: CDSS",
  q: "Why is inline ML in Advanced URL Filtering especially important for fast-flux and short-lived malicious sites?",
  opts: ["Such sites are permanent", "These sites appear and disappear quickly, so real-time analysis is needed since databases can't keep up", "ML disables filtering", "Databases are always current"],
  a: 1,
  why: "Attackers use fast-flux and disposable domains that exist too briefly for static databases to catalog. Inline ML evaluates the URL/site in real time on first contact, providing protection that pre-built lists can't deliver for ephemeral malicious infrastructure."
},
{
  id: 3040, cat: "D3: CDSS",
  q: "What does GlobalProtect's host information/posture capability allow policy to consider?",
  opts: ["Only the user's name", "The security state of the endpoint (e.g., patch level, disk encryption) when granting access", "Only the IP address", "Nothing about the device"],
  a: 1,
  why: "GlobalProtect can collect host information (posture) — like OS patch level, disk encryption, or running security software — so policy can require a healthy device before granting access. This adds device trust to identity, strengthening Zero Trust access decisions."
},
{
  id: 3041, cat: "D3: CDSS",
  q: "An attacker attempts a known exploit AND a brand-new variant against a server. How do signatures and ATP's ML complement each other here?",
  opts: ["Only one is needed", "Signatures catch the known exploit; ATP's inline ML can catch the unknown variant", "Both miss everything", "ML catches only known threats"],
  a: 1,
  why: "Signatures efficiently block known exploits, while ATP's inline ML detects novel/unknown variants lacking a signature. Using both means the firewall handles the broad mass of known threats and the dangerous unknowns — a complementary, layered approach."
},
{
  id: 3042, cat: "D3: CDSS",
  q: "Why is reducing the time-to-verdict in WildFire a meaningful security improvement?",
  opts: ["Slower is better", "The faster a malicious verdict is reached, the less opportunity the threat has to spread or execute", "Verdicts don't matter", "It disables analysis"],
  a: 1,
  why: "Every moment an unknown malicious file goes unidentified is an opportunity for it to execute and spread. Faster verdicts (a focus of Advanced WildFire) mean quicker protection and blocking, shrinking the threat's window of opportunity across the environment."
},
{
  id: 3043, cat: "D3: CDSS",
  q: "How does the platform use WildFire verdicts to retroactively improve protection?",
  opts: ["It ignores past traffic", "Verdicts feed updated signatures/intelligence and can inform logs/alerts about previously seen samples now known to be malicious", "It deletes logs", "It disables future detection"],
  a: 1,
  why: "Once WildFire classifies a sample as malicious, that intelligence updates protections and can surface that previously seen files (now known-bad) were encountered — aiding detection and response. The cloud feedback loop continuously improves coverage over time."
},
{
  id: 3044, cat: "D3: CDSS",
  q: "Which scenario best shows Advanced DNS Security stopping an attack chain early?",
  opts: ["Allowing malware to reach its C2 domain", "Blocking the malware's DNS lookup of its C2 domain, preventing it from establishing control", "Speeding up the C2 channel", "Ignoring DNS"],
  a: 1,
  why: "If malware can't resolve its C2 domain via DNS, it often can't establish control or exfiltrate data. Blocking the malicious DNS resolution disrupts the attack lifecycle early — a high-leverage point, since most communication starts with a DNS lookup."
},
{
  id: 3045, cat: "D3: CDSS",
  q: "Why is it advantageous that CDSS leverages telemetry from a large global customer base?",
  opts: ["Less data is better", "More telemetry improves ML accuracy and broadens threat visibility, benefiting all subscribers", "It slows updates", "It disables sharing"],
  a: 1,
  why: "A large telemetry pool means ML models train on more diverse, real-world threats, improving detection accuracy, and threats seen anywhere can protect everyone. Scale of data is a force multiplier for cloud-delivered security — hard for isolated systems to match."
},
{
  id: 3046, cat: "D3: CDSS",
  q: "What is the main reason WildFire analysis is performed in the cloud rather than entirely on each firewall?",
  opts: ["Firewalls have unlimited resources", "Cloud provides the scale, compute, and shared intelligence needed for deep, broad analysis", "The cloud is less secure", "To avoid detection"],
  a: 1,
  why: "Deep dynamic analysis at scale, across many file types and with shared global intelligence, requires far more compute and data than an individual firewall has. The cloud delivers that scale and pools intelligence, which is why WildFire is cloud-based."
},
{
  id: 3047, cat: "D3: CDSS",
  q: "How do Advanced URL Filtering and credential-phishing prevention together reduce account compromise?",
  opts: ["They allow phishing", "They block access to phishing pages and can prevent users from submitting corporate credentials to untrusted sites", "They disable MFA", "They only log events"],
  a: 1,
  why: "Blocking phishing URLs stops many attacks outright, and preventing corporate credential submission to untrusted/unknown sites adds a safety net if a user reaches one. Together they cut off a primary path to account takeover — stolen credentials."
},
{
  id: 3048, cat: "D3: CDSS",
  q: "An organization adopts SASE and wants remote users to receive the SAME WildFire/ATP/URL/DNS protection as on-prem. How is this achieved?",
  opts: ["It's impossible", "CDSS are applied via Prisma Access so cloud-delivered protection follows users wherever they connect", "Only on-prem users get protection", "By disabling CDSS remotely"],
  a: 1,
  why: "Because CDSS are cloud-delivered, they integrate with Prisma Access to protect remote users with the same intelligence as on-prem firewalls. This consistency ensures off-network users aren't a weak link — a core SASE security goal."
},
{
  id: 3049, cat: "D3: CDSS",
  q: "Why is behavioral/ML detection increasingly necessary as attackers adopt AI to generate threats?",
  opts: ["AI makes threats static", "AI helps attackers rapidly produce novel, evasive variants, so defenses need ML to detect the unknown", "ML can't help", "Signatures alone scale infinitely"],
  a: 1,
  why: "As attackers leverage automation/AI to mass-produce unique, evasive threats, signature-only defenses fall behind. ML-based detection (in WildFire, ATP, Advanced URL/DNS) generalizes to catch novel variants — an arms race that demands AI on the defensive side too."
},
{
  id: 3050, cat: "D3: CDSS",
  q: "Overall, what is the unifying value proposition of the CDSS suite?",
  opts: ["Static, occasional protection", "Continuously updated, cloud-powered, increasingly ML-driven protection across files, exploits/C2, web, and DNS — applied consistently on NGFW and SASE", "Only blocking known .exe files", "Replacing all firewall policy"],
  a: 1,
  why: "CDSS delivers layered, cloud-scale, continuously updated, ML-enhanced protection across the major threat vectors (files via WildFire, exploits/C2 via ATP, web via URL Filtering, DNS via DNS Security), consistently for both on-prem and SASE. That breadth and currency is the core value."
}