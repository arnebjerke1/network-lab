// ===== BATCH 8: DOMAIN 6 — CONNECTIVITY & SECURITY (ids 6031–6060) =====
// Paste into your QUESTIONS array.

{
  id: 6031, cat: "D6: Connectivity",
  q: "Why is it valuable to baseline normal remote-access patterns (locations, times, volumes)?",
  opts: ["Baselines are useless", "Deviations from the baseline (e.g., access at odd hours from new countries) can indicate compromise", "Patterns never change", "To disable monitoring"],
  a: 1,
  why: "Establishing what normal remote access looks like makes anomalies — logins from unexpected countries, unusual hours, or abnormal data volumes — stand out as possible compromise. Baselining turns raw logs into meaningful detection of suspicious remote-access behavior."
},
{
  id: 6032, cat: "D6: Connectivity",
  q: "How does a hub-and-spoke vs. direct-to-cloud (SASE) model differ for branch connectivity security?",
  opts: ["They are identical", "Hub-and-spoke backhauls traffic to a central site for inspection; SASE inspects in the cloud near the branch, reducing latency", "SASE has no inspection", "Hub-and-spoke needs no security"],
  a: 1,
  why: "Traditional hub-and-spoke backhauls branch traffic to a central data center for inspection, adding latency. SASE applies security in distributed cloud locations near the branch, enabling secure direct-to-cloud access with better performance — a key modernization for branch connectivity."
},
{
  id: 6033, cat: "D6: Connectivity",
  q: "Why should certificates used for decryption be properly trusted by endpoints?",
  opts: ["Trust is irrelevant", "Without endpoint trust of the firewall's CA, users get certificate errors when traffic is decrypted", "It disables decryption", "Endpoints never check certificates"],
  a: 1,
  why: "When the firewall decrypts outbound traffic (forward proxy), it re-signs certificates with its CA. If endpoints don't trust that CA, users see certificate warnings and apps may break. Deploying the CA to endpoints (via MDM/group policy) makes decryption seamless and trusted."
},
{
  id: 6034, cat: "D6: Connectivity",
  q: "What is the benefit of integrating remote-access identity with the organization's directory (e.g., for User-ID)?",
  opts: ["It hides identity", "Access and logs are tied to real users/groups, enabling identity-based policy and clearer auditing", "It disables authentication", "It only uses IP addresses"],
  a: 1,
  why: "Integrating with the directory lets remote-access policy and logs reference actual users and groups (via User-ID), enabling identity-based least-privilege policy and meaningful auditing. This is far more robust and clear than managing access by IP, especially for a dynamic remote workforce."
},
{
  id: 6035, cat: "D6: Connectivity",
  q: "Why is it important to secure and monitor the connectivity between cloud workloads (east-west) in addition to north-south traffic?",
  opts: ["East-west traffic is always safe", "Attackers move laterally between cloud workloads, so east-west inspection/segmentation limits spread", "Only internet traffic matters", "Cloud needs no segmentation"],
  a: 1,
  why: "Just as on-prem, attackers pivot laterally (east-west) between cloud workloads after initial access. Securing and monitoring east-west traffic — via segmentation and inspection (e.g., VM/CN-Series) — contains lateral movement in the cloud, not just perimeter (north-south) protection."
},
{
  id: 6036, cat: "D6: Connectivity",
  q: "How does policy tuning help reduce 'alert fatigue' and improve security operations?",
  opts: ["By generating more noise", "By refining rules/detections to reduce false positives, so real issues get attention", "By disabling alerts entirely", "By ignoring all alerts"],
  a: 1,
  why: "Untuned policies and detections can flood analysts with false positives, causing alert fatigue where real threats are missed. Tuning reduces noise and sharpens signal, so genuine security events stand out and receive timely response — improving both efficiency and effectiveness."
},
{
  id: 6037, cat: "D6: Connectivity",
  q: "Why is it recommended to encrypt management/administrative connectivity to firewalls and gateways?",
  opts: ["Management traffic is unimportant", "Management access is highly sensitive; encryption protects credentials and configuration from interception", "Encryption exposes management", "It disables management"],
  a: 1,
  why: "Administrative access to firewalls is extremely sensitive — compromise grants control of security itself. Encrypting management connectivity (e.g., HTTPS/SSH) protects admin credentials and configuration data from interception, a basic but critical safeguard for the management plane."
},
{
  id: 6038, cat: "D6: Connectivity",
  q: "A company must ensure remote contractors can reach only one specific internal application. Which is the most secure design?",
  opts: ["Full network VPN access", "ZTNA granting access strictly to that one application based on identity/policy", "Open access to the data center", "No access controls"],
  a: 1,
  why: "ZTNA grants narrowly scoped access to just the required application based on identity and policy, exposing nothing else. For contractors especially, this least-privilege, app-specific access is far safer than full-network VPN, which would let a compromised contractor reach much more."
},
{
  id: 6039, cat: "D6: Connectivity",
  q: "Why is continuous monitoring of VPN/remote-access tunnels important for availability?",
  opts: ["Tunnels never fail", "Detecting tunnel failures/degradation quickly enables remediation before users are significantly impacted", "Monitoring causes outages", "Availability is irrelevant"],
  a: 1,
  why: "VPN/remote-access tunnels can fail or degrade due to certificate issues, link problems, or misconfiguration. Continuous monitoring detects these quickly so admins can remediate before users are widely affected — supporting the availability that remote workers depend on."
},
{
  id: 6040, cat: "D6: Connectivity",
  q: "How does segmentation between IT and OT networks support both connectivity and security?",
  opts: ["By merging them into one zone", "By allowing only necessary, controlled communication between IT and OT, protecting fragile OT systems", "By disabling OT entirely", "By removing all controls"],
  a: 1,
  why: "OT systems are often fragile and unpatchable, so segmenting them from IT — permitting only essential, inspected communication — protects them while still enabling required data flows. This controlled connectivity balances operational needs with strong security for critical OT environments."
},
{
  id: 6041, cat: "D6: Connectivity",
  q: "Why should an organization regularly review and remove stale remote-access accounts and rules?",
  opts: ["Stale items improve security", "Unused accounts/rules expand attack surface and may be exploited; removing them enforces least privilege", "They should never be removed", "It disables access"],
  a: 1,
  why: "Stale remote-access accounts (e.g., for departed staff or old contractors) and unused rules are prime targets and unnecessary risk. Regularly reviewing and removing them shrinks the attack surface and maintains least privilege — part of good identity and policy lifecycle hygiene."
},
{
  id: 6042, cat: "D6: Connectivity",
  q: "What is the benefit of using a consistent set of security profiles for traffic regardless of where it originates (on-prem, cloud, remote)?",
  opts: ["Inconsistent protection", "Uniform threat inspection everywhere prevents any origin from being an unprotected entry path", "It only protects on-prem", "It disables inspection"],
  a: 1,
  why: "Applying consistent security profiles across all traffic origins ensures uniform threat inspection, so no path (cloud, remote, on-prem) is left unprotected. Consistency closes gaps that attackers seek — a unified protection posture across the hybrid environment."
},
{
  id: 6043, cat: "D6: Connectivity",
  q: "Why is it important that remote-access solutions scale to handle peak concurrent users?",
  opts: ["Scale is irrelevant", "Insufficient capacity can deny legitimate users access or degrade performance during peaks (e.g., events, emergencies)", "Fewer users is always fine", "It disables security"],
  a: 1,
  why: "Remote-access demand can spike (e.g., during emergencies or company-wide remote events). Solutions must scale to peak concurrency so legitimate users aren't denied access or slowed — cloud-delivered options (Prisma Access) help by elastically scaling capacity to demand."
},
{
  id: 6044, cat: "D6: Connectivity",
  q: "How does logging the applications accessed by remote users support security?",
  opts: ["It hides usage", "It provides visibility into what remote users actually access, enabling anomaly detection and policy refinement", "Only IPs matter", "It disables App-ID"],
  a: 1,
  why: "Application-level logging (via App-ID) shows what remote users genuinely access, helping detect anomalous or unauthorized application use and informing policy tuning toward least privilege. This richer visibility is more actionable than IP/port logs alone for securing remote access."
},
{
  id: 6045, cat: "D6: Connectivity",
  q: "Why is mutual TLS or certificate pinning sometimes used for sensitive application connectivity?",
  opts: ["To weaken security", "To strongly verify endpoints and resist man-in-the-middle/impersonation for high-value connections", "To disable encryption", "To allow any certificate"],
  a: 1,
  why: "For sensitive connections, mutual TLS (both sides authenticate) and certificate pinning (expecting a specific certificate) provide strong assurance against impersonation and man-in-the-middle attacks. These measures harden connectivity for high-value applications where trust is paramount."
},
{
  id: 6046, cat: "D6: Connectivity",
  q: "What is a primary reason to enforce posture-based conditional access for remote connections?",
  opts: ["Device state doesn't matter", "Access decisions should consider device health/compliance, granting or limiting access based on risk", "It blocks all devices", "It disables identity checks"],
  a: 1,
  why: "Conditional access evaluates device posture (and other context) alongside identity, so a non-compliant or risky device can be denied or restricted while healthy devices get full access. This risk-based, adaptive approach strengthens Zero Trust for remote connectivity beyond identity alone."
},
{
  id: 6047, cat: "D6: Connectivity",
  q: "Why is it beneficial to inspect traffic between cloud environments (e.g., multi-cloud) and on-prem consistently?",
  opts: ["Inter-cloud traffic is always safe", "Threats and lateral movement can traverse these links, so consistent inspection prevents gaps", "Only on-prem needs inspection", "It disables connectivity"],
  a: 1,
  why: "Connections between clouds and on-prem can carry threats or enable lateral movement across environments. Inspecting them consistently (not just internet-facing traffic) prevents attackers from exploiting trusted inter-environment links as unguarded pathways — essential in multi-cloud/hybrid designs."
},
{
  id: 6048, cat: "D6: Connectivity",
  q: "How does centralized certificate and PKI management reduce risk in a large environment?",
  opts: ["By ignoring certificates", "By ensuring consistent issuance, renewal, and revocation, preventing expired/untrusted certs and unmanaged sprawl", "By using only self-signed certs everywhere", "By disabling encryption"],
  a: 1,
  why: "Centralized PKI/certificate management ensures certificates are consistently issued, renewed before expiry, and revoked when compromised — avoiding outages from expired certs and security gaps from unmanaged or untrusted certificates. At scale, this governance is essential for reliable, secure connectivity."
},
{
  id: 6049, cat: "D6: Connectivity",
  q: "Why should remote-access policy distinguish between managed corporate devices and personal (BYOD) devices?",
  opts: ["They pose identical risk", "Personal devices are less controlled/higher-risk, so they may warrant more restricted access or stricter conditions", "BYOD should get full access", "Device type is irrelevant"],
  a: 1,
  why: "Personal/BYOD devices are typically less controlled and harder to verify than managed corporate devices, posing higher risk. Distinguishing them lets policy apply stricter conditions or more limited access (e.g., agentless/Enterprise Browser, restricted downloads) — matching access to device trust level."
},
{
  id: 6050, cat: "D6: Connectivity",
  q: "What is the security value of automatically revoking a remote user's access when their account is disabled?",
  opts: ["Revocation is unnecessary", "It immediately closes access for departed/compromised users, preventing misuse of lingering access", "It should be delayed", "It disables the network"],
  a: 1,
  why: "Promptly revoking remote access when an account is disabled (e.g., on termination or compromise) prevents the ex-user or an attacker from misusing lingering access. Tight integration between identity lifecycle and access enforcement closes a common, dangerous gap quickly."
},
{
  id: 6051, cat: "D6: Connectivity",
  q: "Why is it important to test failover for remote-access gateways/VPN in HA designs?",
  opts: ["Failover always works untested", "Verifying failover ensures remote access remains available if a gateway fails, avoiding surprise outages", "Testing causes failures", "Availability is irrelevant"],
  a: 1,
  why: "HA for remote-access gateways only helps if failover actually works when needed. Testing failover validates that remote users retain access during a gateway failure, avoiding unpleasant surprises during a real outage. Verified resilience is essential for critical remote-access infrastructure."
},
{
  id: 6052, cat: "D6: Connectivity",
  q: "How does applying Zero Trust principles to connectivity change the default assumption about internal network traffic?",
  opts: ["Internal traffic is fully trusted", "No traffic is implicitly trusted by location; internal flows are also verified and least-privilege", "Only external traffic is checked", "All internal traffic is blocked"],
  a: 1,
  why: "Zero Trust removes the assumption that internal/network-location equals trust. Internal (east-west) traffic is verified and constrained by least-privilege policy just like external traffic, so a foothold inside can't move freely. This reshapes connectivity from implicit internal trust to continuous verification."
},
{
  id: 6053, cat: "D6: Connectivity",
  q: "Why is it useful to correlate remote-access logs with endpoint and threat data?",
  opts: ["Correlation hides threats", "Combining signals gives richer context to detect compromised remote sessions and respond effectively", "Only one data source is ever needed", "It disables logging"],
  a: 1,
  why: "Correlating remote-access activity with endpoint posture and threat detections provides context to spot compromised sessions (e.g., a risky device plus anomalous access) and respond decisively. Holistic, correlated visibility beats isolated logs for detecting and investigating remote-access incidents."
},
{
  id: 6054, cat: "D6: Connectivity",
  q: "What is the benefit of enforcing encryption standards (e.g., strong TLS/IPsec settings) via decryption/connectivity profiles?",
  opts: ["Weaker encryption is fine", "Blocking weak/outdated ciphers and protocols ensures connections meet a strong security baseline", "It disables encryption", "It allows any protocol"],
  a: 1,
  why: "Enforcing strong encryption standards (rejecting weak ciphers, deprecated protocols, expired/untrusted certs) ensures connections meet a secure baseline and resist downgrade or interception attacks. Profiles that enforce these settings raise the cryptographic security of connectivity across the environment."
},
{
  id: 6055, cat: "D6: Connectivity",
  q: "Why is it important to provide secure connectivity options for diverse endpoints (laptops, mobile, IoT, third parties)?",
  opts: ["One method fits all perfectly", "Different endpoints have different capabilities/risks, so varied secure options ensure all can connect safely", "Only laptops matter", "IoT needs no connectivity security"],
  a: 1,
  why: "A modern environment includes many endpoint types with differing capabilities and risk profiles. Offering appropriate secure connectivity for each (client agents, agentless browser access, IoT segmentation) ensures every endpoint connects safely, rather than forcing an ill-fitting single method that leaves gaps."
},
{
  id: 6056, cat: "D6: Connectivity",
  q: "How does monitoring data egress patterns help detect data exfiltration over remote connections?",
  opts: ["Egress patterns are meaningless", "Unusual outbound volumes or destinations can indicate exfiltration, prompting investigation", "Only inbound matters", "It disables DLP"],
  a: 1,
  why: "Abnormal egress — large data volumes, transfers to unusual destinations, or odd timing — can signal data exfiltration via a compromised remote session. Monitoring these patterns (alongside DLP) provides early warning of data theft, enabling investigation before significant loss occurs."
},
{
  id: 6057, cat: "D6: Connectivity",
  q: "Why should security policy for remote access follow the principle of explicit allow with default deny?",
  opts: ["Allow everything by default", "Permitting only explicitly required access and denying the rest minimizes attack surface and unintended exposure", "Deny everything including needed access", "Policy order is irrelevant"],
  a: 1,
  why: "An explicit-allow, default-deny model grants only the access that's specifically required and blocks everything else, minimizing attack surface and preventing unintended exposure. This positive-enforcement approach is foundational to secure remote-access policy and Zero Trust generally."
},
{
  id: 6058, cat: "D6: Connectivity",
  q: "What is a key reason to ensure consistent logging/monitoring coverage across all connectivity paths?",
  opts: ["Gaps in visibility are fine", "Blind spots in any path let threats operate undetected; consistent coverage ensures full visibility", "Only one path needs monitoring", "It disables security"],
  a: 1,
  why: "If some connectivity paths lack logging/monitoring, threats can operate there undetected. Consistent visibility across all paths (on-prem, cloud, remote, inter-environment) eliminates blind spots, ensuring no avenue is unwatched — critical for reliable detection and response across a hybrid environment."
},
{
  id: 6059, cat: "D6: Connectivity",
  q: "How does integrating connectivity (SD-WAN) with security (SASE) benefit a branch's overall posture?",
  opts: ["It separates them into silos", "Converged connectivity and security provide consistent protection and optimized performance from an integrated solution", "It removes security", "It only optimizes WAN with no security"],
  a: 1,
  why: "Converging SD-WAN connectivity with cloud-delivered security (SASE) means branch traffic is both optimally routed and consistently secured by one integrated solution, improving both performance and protection while simplifying the branch. This integration is the essence of the SASE value proposition."
},
{
  id: 6060, cat: "D6: Connectivity",
  q: "Overall, how do segmentation, secure remote access, certificates, policy tuning, and monitoring combine in Domain 6?",
  opts: ["They work in isolation", "They collectively ensure connectivity across on-prem, cloud, and remote is secure, trusted, least-privilege, and continuously visible", "They replace the firewall", "They only manage licensing"],
  a: 1,
  why: "Domain 6 unifies the elements of secure connectivity: segmentation enforces trust boundaries, secure remote access (with certificates and MFA) connects users safely, policy tuning maintains least privilege, and monitoring provides continuous visibility. Together they keep hybrid connectivity secure, trusted, and observable end to end."
}