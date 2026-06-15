// ===== BATCH 8: DOMAIN 6 — CONNECTIVITY & SECURITY (ids 6001–6030) =====
// Paste into your QUESTIONS array.

{
  id: 6001, cat: "D6: Connectivity",
  q: "An organization wants to securely connect two on-premises sites over the internet so traffic is encrypted in transit. Which technology is most appropriate?",
  opts: ["An open, unencrypted link", "A site-to-site IPsec VPN tunnel", "A public file share", "Disabling the firewall"],
  a: 1,
  why: "A site-to-site IPsec VPN encrypts traffic between two sites across the untrusted internet, providing confidentiality and integrity. It's the standard way to securely interconnect locations without a private circuit. Open links would expose data; IPsec protects it in transit."
},
{
  id: 6002, cat: "D6: Connectivity",
  q: "In a hybrid network (on-prem + cloud), why is consistent network segmentation important across both environments?",
  opts: ["To create inconsistency", "So security boundaries and least-privilege controls apply uniformly, preventing gaps attackers exploit", "To slow the cloud", "To disable on-prem security"],
  a: 1,
  why: "Hybrid environments span on-prem and cloud, and inconsistent segmentation creates gaps where attackers can move. Applying consistent segmentation and least-privilege policy across both ensures uniform security boundaries, so the cloud isn't a weaker link than on-prem (or vice versa)."
},
{
  id: 6003, cat: "D6: Connectivity",
  q: "What is the primary role of digital certificates in securing network connectivity (e.g., VPNs, TLS)?",
  opts: ["To slow connections", "To authenticate identities and enable encrypted, trusted communications", "To store passwords in plaintext", "To disable encryption"],
  a: 1,
  why: "Certificates bind a public key to an identity, enabling authentication (proving a server/peer is who it claims) and establishing encrypted sessions (TLS/IPsec). They are foundational to trusted, confidential connectivity — verifying identity and bootstrapping encryption."
},
{
  id: 6004, cat: "D6: Connectivity",
  q: "Why is it important to monitor certificate expiration dates on firewalls and gateways?",
  opts: ["Certificates never expire", "An expired certificate can break VPNs, decryption, or app access, causing outages", "Expired certs improve security", "It disables logging"],
  a: 1,
  why: "Expired certificates can cause connectivity failures — broken VPN tunnels, decryption errors, or blocked app access — leading to outages. Proactively tracking and renewing certificates before expiry prevents these avoidable disruptions, a key operational practice."
},
{
  id: 6005, cat: "D6: Connectivity",
  q: "A remote employee needs secure access to corporate resources from home. Which Palo Alto Networks component provides this client-based connectivity?",
  opts: ["A site-to-site VPN only", "GlobalProtect agent connecting to a gateway or Prisma Access", "An open guest network", "Disabling authentication"],
  a: 1,
  why: "GlobalProtect provides client-based secure remote access, connecting the user's endpoint to an NGFW gateway or to Prisma Access. It extends consistent security policy to remote users, ensuring their traffic is protected like on-network users — the standard remote-access approach."
},
{
  id: 6006, cat: "D6: Connectivity",
  q: "What advantage does connecting remote users to Prisma Access provide over backhauling all traffic to a central data center?",
  opts: ["Higher latency", "Security applied in the cloud near the user, avoiding hairpinning and improving performance", "No security", "More on-prem hardware"],
  a: 1,
  why: "Routing remote-user traffic through Prisma Access applies cloud-delivered security close to the user, avoiding the latency and bottleneck of backhauling everything to a central site. Users get consistent protection with better performance — a core SASE benefit for remote access."
},
{
  id: 6007, cat: "D6: Connectivity",
  q: "How does GlobalProtect support Zero Trust for remote users beyond just creating a tunnel?",
  opts: ["It grants full network access automatically", "It conveys user/device identity and posture so least-privilege, policy-based access can be enforced", "It disables policy", "It only encrypts DNS"],
  a: 1,
  why: "GlobalProtect carries identity and device-posture context to the enforcement point, enabling least-privilege, policy-driven access (including ZTNA to specific apps) rather than broad network access. This identity/context awareness is what makes it Zero Trust-capable, not just a VPN."
},
{
  id: 6008, cat: "D6: Connectivity",
  q: "Why might an organization use certificates (rather than only passwords) to authenticate VPN connections?",
  opts: ["Certificates are weaker", "Certificate-based authentication is stronger and resists credential theft/phishing better than passwords alone", "To disable encryption", "Passwords can't be used for VPNs"],
  a: 1,
  why: "Certificate-based authentication provides strong, cryptographic proof of identity that's much harder to steal or phish than passwords. Using certificates (often with MFA) strengthens VPN/remote-access security against credential-based attacks — a recommended practice for sensitive access."
},
{
  id: 6009, cat: "D6: Connectivity",
  q: "What is the purpose of network segmentation in a data center protected by NGFWs?",
  opts: ["To allow all internal traffic", "To divide the data center into zones and restrict east-west traffic, limiting lateral movement", "To remove firewalls", "To slow applications intentionally"],
  a: 1,
  why: "Segmentation divides the data center into zones with least-privilege policy controlling east-west (internal) traffic, so a compromise in one segment can't freely spread. This containment of lateral movement is central to Zero Trust and limits breach blast radius."
},
{
  id: 6010, cat: "D6: Connectivity",
  q: "After deploying a new remote-access setup, why is security policy tuning an ongoing task?",
  opts: ["Policy is perfect on day one", "Real usage reveals needed adjustments (over-permissive or over-restrictive rules) to balance security and access", "Tuning weakens security", "Policy never changes"],
  a: 1,
  why: "Initial policies rarely perfectly match real-world needs; monitoring actual usage reveals rules that are too permissive (risk) or too restrictive (blocking legitimate work). Ongoing tuning refines policy toward least privilege without disrupting users — a continuous improvement cycle."
},
{
  id: 6011, cat: "D6: Connectivity",
  q: "Why are monitoring and logging essential for remote-user connectivity security?",
  opts: ["They slow connections", "They provide visibility into remote access activity to detect anomalies, troubleshoot, and support investigations", "They disable VPNs", "They only track licenses"],
  a: 1,
  why: "Logging remote-access activity (who connected, from where, what they accessed) enables detection of suspicious behavior (e.g., impossible travel, unusual access), troubleshooting connectivity issues, and forensic investigation. Visibility into remote access is critical as the workforce distributes."
},
{
  id: 6012, cat: "D6: Connectivity",
  q: "An organization extends its network into a public cloud. Which deployment secures cloud-hosted workloads where on-prem hardware can't be placed?",
  opts: ["A physical PA-Series in the office only", "VM-Series and/or Cloud NGFW deployed in the cloud environment", "No security in the cloud", "Disabling cloud workloads"],
  a: 1,
  why: "Cloud-hosted workloads need security where they live, and you can't insert on-prem hardware into a public cloud. VM-Series (self-managed) or Cloud NGFW (managed) bring NGFW protection natively into the cloud, extending consistent security to those workloads."
},
{
  id: 6013, cat: "D6: Connectivity",
  q: "Why is consistent security policy across on-prem, cloud, and remote users important in a hybrid architecture?",
  opts: ["To create gaps", "So protection follows applications and users everywhere, avoiding weak points and inconsistent enforcement", "To slow the network", "To disable remote access"],
  a: 1,
  why: "In hybrid environments, users and apps span many locations. Consistent policy ensures the same protections apply everywhere — on-prem, cloud, and remote — so there are no weak points or inconsistent enforcement that attackers can target. Unified management makes this achievable."
},
{
  id: 6014, cat: "D6: Connectivity",
  q: "What does a certificate authority (CA) provide in a PKI used for network security?",
  opts: ["It stores plaintext passwords", "It issues and signs certificates, establishing trust in the identities they represent", "It disables encryption", "It blocks all traffic"],
  a: 1,
  why: "A CA issues and digitally signs certificates, vouching for the binding between a public key and an identity. Trust in the CA underpins trust in the certificates it issues, enabling authentication and encryption across VPNs, TLS, and decryption. PKI relies on this chain of trust."
},
{
  id: 6015, cat: "D6: Connectivity",
  q: "Why is it important that remote-access solutions verify device posture (e.g., via GlobalProtect) before granting access?",
  opts: ["Device health is irrelevant", "A compromised or non-compliant device could introduce threats; posture checks enforce device trust", "Posture checks block all devices", "It disables authentication"],
  a: 1,
  why: "Allowing any device — even an infected or non-compliant one — to connect can introduce threats into the network. Posture checks (patch level, encryption, security software) enforce a minimum device trust before access, adding a critical layer beyond user identity for Zero Trust."
},
{
  id: 6016, cat: "D6: Connectivity",
  q: "A company wants to replace broad legacy VPN access with access to only specific applications per user. Which approach achieves this?",
  opts: ["Full-tunnel VPN to the whole network", "ZTNA (e.g., via Prisma Access) granting least-privilege access to specific apps", "Open access to all servers", "Disabling all access"],
  a: 1,
  why: "ZTNA grants users access to specific applications based on identity and policy, rather than placing them on the whole network as legacy VPNs often do. Prisma Access can broker this least-privilege app access, dramatically reducing the attack surface compared with broad VPN access."
},
{
  id: 6017, cat: "D6: Connectivity",
  q: "Why is encrypting traffic between on-prem and cloud (e.g., via IPsec) important in hybrid connectivity?",
  opts: ["Encryption exposes data", "It protects data confidentiality/integrity as it traverses untrusted networks between environments", "It slows the cloud for no reason", "It disables segmentation"],
  a: 1,
  why: "Traffic between on-prem and cloud often crosses the public internet or shared infrastructure. Encrypting it (e.g., with IPsec) preserves confidentiality and integrity against interception or tampering in transit, ensuring hybrid connectivity is secure end to end."
},
{
  id: 6018, cat: "D6: Connectivity",
  q: "What is a key reason to tune security policy based on monitoring data after deployment?",
  opts: ["To ignore real usage", "To remove unused/over-permissive rules and tighten access toward least privilege based on observed traffic", "To allow all traffic", "To disable logging"],
  a: 1,
  why: "Monitoring reveals which rules are actually used and whether any are overly broad. Tuning based on this data lets admins tighten or remove rules, moving toward least privilege and reducing attack surface — turning observed reality into improved, right-sized policy."
},
{
  id: 6019, cat: "D6: Connectivity",
  q: "Why is it beneficial to apply the same threat prevention (CDSS) to remote-user traffic as to on-prem traffic?",
  opts: ["Remote users need less protection", "Remote users face the same threats, so consistent protection prevents them from being a weak entry point", "Threats avoid remote users", "It disables on-prem security"],
  a: 1,
  why: "Remote users encounter the same threats (malware, phishing, C2) as on-network users; protecting them consistently (via Prisma Access/CDSS) prevents remote endpoints from becoming an unguarded entry point into the organization. Consistent protection everywhere is a core SASE/Zero Trust goal."
},
{
  id: 6020, cat: "D6: Connectivity",
  q: "What is the purpose of using security zones when defining connectivity between on-prem, cloud, and remote networks?",
  opts: ["To allow unrestricted flow", "To establish trust boundaries and enforce default-deny between them, permitting only required flows", "To remove policy", "To slow connections"],
  a: 1,
  why: "Zones define trust boundaries across the hybrid environment, with inter-zone traffic denied by default. This ensures only explicitly permitted flows occur between on-prem, cloud, and remote segments — enforcing least privilege and clear, intentional connectivity rather than open access."
},
{
  id: 6021, cat: "D6: Connectivity",
  q: "Why might an organization use both client-based (GlobalProtect) and clientless/agentless access methods?",
  opts: ["They are identical", "Different scenarios (managed employees vs. unmanaged third parties/BYOD) call for different access methods", "Clientless access is always best", "To disable remote access"],
  a: 1,
  why: "Managed employee devices suit client-based access (GlobalProtect) with full posture/control, while unmanaged or third-party devices may need agentless options (e.g., Enterprise Browser, clientless access). Offering both covers diverse use cases securely — matching the method to the user/device context."
},
{
  id: 6022, cat: "D6: Connectivity",
  q: "How does certificate-based mutual authentication enhance a VPN connection?",
  opts: ["Only the client is verified", "Both endpoints verify each other's certificates, ensuring neither side is an impostor", "Neither side is verified", "It disables encryption"],
  a: 1,
  why: "Mutual (two-way) certificate authentication has both the client and the gateway prove their identities via certificates, preventing impersonation of either side (e.g., a rogue gateway or unauthorized client). This strengthens trust in the connection beyond one-way authentication."
},
{
  id: 6023, cat: "D6: Connectivity",
  q: "Why is logging remote-access authentication events (successes and failures) valuable?",
  opts: ["It hides attacks", "Patterns like repeated failures or unusual logins can indicate brute-force/credential attacks needing response", "Only successes matter", "To disable VPNs"],
  a: 1,
  why: "Authentication logs reveal attack indicators — bursts of failed logins (brute force), logins from unexpected locations, or impossible travel — enabling detection and response. Capturing both successes and failures provides the full picture needed to spot credential-based attacks on remote access."
},
{
  id: 6024, cat: "D6: Connectivity",
  q: "A hybrid organization wants unified visibility into connectivity and security across on-prem and cloud. Which approach helps most?",
  opts: ["Separate, unintegrated tools", "Centralized management (Panorama/SCM) providing unified policy and visibility across environments", "No monitoring", "Disabling cloud security"],
  a: 1,
  why: "Centralized management (Panorama/SCM) gives unified policy enforcement and visibility spanning on-prem and cloud, so admins see and control the whole hybrid environment cohesively. Disconnected tools fragment visibility and invite inconsistency — centralization addresses both."
},
{
  id: 6025, cat: "D6: Connectivity",
  q: "Why is least-privilege access especially important for remote and third-party users?",
  opts: ["They should have full access", "They're outside the traditional perimeter and higher-risk, so limiting access reduces potential damage from compromise", "Access level doesn't matter", "It disables connectivity"],
  a: 1,
  why: "Remote and third-party users connect from outside the controlled environment and may use less-trusted devices, raising risk. Granting only the minimum necessary access (ideally specific apps via ZTNA) limits the damage if their access is compromised — a key Zero Trust safeguard."
},
{
  id: 6026, cat: "D6: Connectivity",
  q: "What is the security benefit of terminating and inspecting remote-user traffic (with decryption and CDSS) rather than passing it through blindly?",
  opts: ["Blind pass-through is safer", "Inspection catches threats in remote-user traffic that would otherwise enter undetected", "It disables protection", "Threats avoid remote traffic"],
  a: 1,
  why: "Inspecting remote-user traffic (decryption + threat prevention) detects and blocks malware, phishing, and C2 that would otherwise ride in undetected from remote endpoints. Passing traffic through blindly leaves a major blind spot; inspection ensures remote access doesn't bypass security."
},
{
  id: 6027, cat: "D6: Connectivity",
  q: "Why is it important to segment remote-access users from sensitive internal systems by default?",
  opts: ["Remote users need full reach", "Default segmentation limits what a compromised remote session can reach, containing potential breaches", "Segmentation blocks all access", "It disables VPNs"],
  a: 1,
  why: "If a remote session is compromised, default segmentation (least privilege) prevents it from reaching sensitive systems it doesn't need, containing the breach. Granting remote users only the specific access required — not broad internal reach — is a fundamental Zero Trust remote-access practice."
},
{
  id: 6028, cat: "D6: Connectivity",
  q: "How does consistent certificate management across the environment support secure connectivity?",
  opts: ["By ignoring certificates", "By ensuring valid, trusted certificates are deployed/renewed everywhere, preventing trust failures and outages", "By disabling encryption", "By using expired certs"],
  a: 1,
  why: "Managing certificates consistently — deploying trusted certs, renewing before expiry, and maintaining proper trust chains — prevents authentication failures, decryption errors, and outages across VPNs, TLS, and gateways. Centralized, proactive certificate management keeps secure connectivity reliable."
},
{
  id: 6029, cat: "D6: Connectivity",
  q: "Why might split tunneling be carefully evaluated for remote access security?",
  opts: ["It always improves security", "It can let some traffic bypass inspection, so the security trade-off must be weighed against performance benefits", "It blocks all traffic", "It has no security implications"],
  a: 1,
  why: "Split tunneling routes some traffic directly (not through the security stack) for performance, but that bypassed traffic isn't inspected — a potential security gap. Organizations must weigh the performance benefit against reduced visibility/control and decide what should be tunneled and inspected."
},
{
  id: 6030, cat: "D6: Connectivity",
  q: "What is a key reason to use multi-factor authentication (MFA) for remote access?",
  opts: ["To rely on passwords alone", "To require an additional factor so stolen credentials alone can't grant access", "To disable authentication", "To slow logins for no benefit"],
  a: 1,
  why: "Remote access is a prime target for credential theft. MFA requires a second, independent factor, so a stolen or phished password alone won't grant access — substantially reducing account-takeover risk. MFA is a baseline best practice for securing remote and privileged access."
}