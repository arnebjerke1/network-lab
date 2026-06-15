// ===== BATCH 7: DOMAIN 5 — INFRA MGMT & CDSS (ids 5001–5037) =====
// Paste into your QUESTIONS array.

{
  id: 5001, cat: "D5: Infra Mgmt",
  q: "To activate a CDSS subscription's protection (e.g., Threat Prevention) on traffic, what must an admin do beyond having a valid license?",
  opts: ["Nothing else is required", "Configure the relevant security profile and attach it to allow rules", "Reboot the firewall daily", "Disable the policy"],
  a: 1,
  why: "A license enables the service, but protection only applies when the corresponding security profile (e.g., Anti-Spyware, Vulnerability Protection) is configured and attached to allow rules. Licensing + configuration + rule attachment together deliver the protection on real traffic."
},
{
  id: 5002, cat: "D5: Infra Mgmt",
  q: "Which is the recommended way to keep CDSS threat content current with minimal risk of missed updates?",
  opts: ["Manual updates only when remembered", "Scheduled automatic content updates", "Never update", "Update only during outages"],
  a: 1,
  why: "Scheduling automatic content updates ensures the firewall consistently receives the latest threat signatures without relying on manual action. For threat content especially, timely updates close exposure windows. (App-ID content may still be reviewed/staged to avoid policy surprises.)"
},
{
  id: 5003, cat: "D5: Infra Mgmt",
  q: "An admin wants new firewalls to automatically receive standardized CDSS profiles and policies. Which management approach scales best?",
  opts: ["Configure each firewall by hand", "Use Panorama (device groups/templates) or SCM to centrally define and push configuration", "Email config to each admin", "Disable management"],
  a: 1,
  why: "Centralized management (Panorama device groups/templates or Strata Cloud Manager) lets you define profiles/policies once and push them consistently to many firewalls, including new ones. Manual per-device config doesn't scale and invites drift and inconsistency."
},
{
  id: 5003, cat: "D5: Infra Mgmt",
  q: "What is the role of a security profile in the configuration/maintenance of CDSS?",
  opts: ["It assigns IP addresses", "It defines how a CDSS service inspects/acts on traffic (e.g., signatures, actions) and is applied via policy", "It manages HA only", "It replaces licensing"],
  a: 1,
  why: "Security profiles operationalize CDSS: they specify what the service inspects and how it responds (alert, block, reset), and they're attached to security rules. Maintaining CDSS largely means configuring and tuning these profiles and keeping their content updated."
},
{
  id: 5004, cat: "D5: Infra Mgmt",
  q: "Why might an admin tune a threat signature's action from 'block' to 'alert' temporarily?",
  opts: ["To permanently disable security", "To monitor a potential false positive's impact before enforcing blocking", "To delete the signature", "To speed up NAT"],
  a: 1,
  why: "Setting an action to 'alert' lets the admin observe whether a signature triggers on legitimate traffic (false positives) before enforcing 'block.' This staged tuning reduces the risk of disrupting business while validating detections — a common maintenance practice."
},
{
  id: 5005, cat: "D5: Infra Mgmt",
  q: "What does an exception (or override) in a security profile allow an admin to do?",
  opts: ["Apply one action to all traffic", "Treat a specific signature/threat differently (e.g., allow or alert) from the profile's default", "Delete all logs", "Disable the firewall"],
  a: 1,
  why: "Profile exceptions let admins handle specific signatures differently than the profile default — for example, excluding a benign trigger that causes false positives. This granular control balances strong default protection with operational needs for particular cases."
},
{
  id: 5006, cat: "D5: Infra Mgmt",
  q: "For IoT security, what does Device-ID provide that enables policy enforcement on discovered devices?",
  opts: ["A user password", "A device-based attribute so rules can match specific devices/types regardless of user or IP", "A WAN circuit", "A certificate authority"],
  a: 1,
  why: "Device-ID supplies device identity as a policy match criterion, letting admins write rules for specific devices or device categories — essential for headless IoT/OT that has no user. IoT Security supplies the device context that Device-ID then enforces."
},
{
  id: 5007, cat: "D5: Infra Mgmt",
  q: "Why are monitoring and logging critical in the configuration/maintenance of IoT security?",
  opts: ["They slow devices", "They provide visibility into device behavior and anomalies needed to detect compromise and tune policy", "They disable Device-ID", "They only track licenses"],
  a: 1,
  why: "IoT devices are often unmanaged and unpatchable, so behavioral visibility via monitoring/logging is a primary defense — it surfaces anomalies (e.g., a device contacting unexpected destinations) and informs policy tuning and incident response. Without logging, IoT threats go unseen."
},
{
  id: 5008, cat: "D5: Infra Mgmt",
  q: "An IoT camera's logs show it suddenly scanning internal subnets. What is the appropriate maintenance/response action?",
  opts: ["Ignore it", "Investigate the anomaly and tighten Device-ID policy/segmentation to contain the device", "Open all ports for it", "Delete all logs"],
  a: 1,
  why: "Internal scanning by a camera is anomalous and suggests compromise. The response is to investigate and enforce least-privilege segmentation via Device-ID, confining the device to only its legitimate communications. Monitoring detects it; policy enforcement contains it."
},
{
  id: 5009, cat: "D5: Infra Mgmt",
  q: "In Enterprise DLP, what is the role of 'data patterns' (data identifiers)?",
  opts: ["They manage HA", "They define how sensitive data types are recognized (e.g., card numbers, SSNs) within content", "They assign IPs", "They issue certificates"],
  a: 1,
  why: "Data patterns/identifiers specify the signatures of sensitive data (credit card numbers, SSNs, keywords, custom regex) that DLP looks for in traffic and files. Configuring accurate data patterns is central to DLP correctly detecting the data you need to protect."
},
{
  id: 5010, cat: "D5: Infra Mgmt",
  q: "How does access control contribute to DLP and SaaS data protection?",
  opts: ["It allows everyone full access", "It restricts who/what can access sensitive data and apps, reducing exposure (least privilege)", "It disables encryption", "It deletes data"],
  a: 1,
  why: "Access control limits access to sensitive data and SaaS apps based on identity/role/context, enforcing least privilege so fewer users/devices can reach (and potentially leak) sensitive data. Combined with content inspection, it's a key layer of data protection."
},
{
  id: 5011, cat: "D5: Infra Mgmt",
  q: "Why is data encryption an important control alongside DLP for protecting sensitive data?",
  opts: ["Encryption exposes data", "Encryption protects confidentiality at rest/in transit, so even if data is accessed improperly it isn't readable", "Encryption deletes data", "Encryption disables DLP"],
  a: 1,
  why: "Encryption ensures that sensitive data remains confidential even if intercepted or accessed by unauthorized parties. DLP prevents improper movement of data; encryption protects it if it's exposed. Together they provide complementary safeguards for sensitive information."
},
{
  id: 5012, cat: "D5: Infra Mgmt",
  q: "What is a primary function of monitoring and logging in DLP/SaaS Security maintenance?",
  opts: ["To hide policy violations", "To record data-handling events and policy violations for detection, investigation, and compliance", "To disable DLP", "To speed up uploads"],
  a: 1,
  why: "Logging DLP/SaaS events (e.g., blocked transfers, risky sharing, policy violations) provides the visibility needed to detect incidents, investigate them, tune policy, and demonstrate compliance. Effective data protection depends on seeing what's happening with sensitive data."
},
{
  id: 5013, cat: "D5: Infra Mgmt",
  q: "What is the primary purpose of Panorama in a network security environment?",
  opts: ["Endpoint antivirus", "Centralized management of multiple firewalls — configuration, policy, updates, and aggregated logging", "A WAN optimizer", "A cloud sandbox"],
  a: 1,
  why: "Panorama centrally manages many firewalls: pushing configuration and policy, distributing updates, and aggregating logs/reports. It's the on-prem-capable management platform that makes operating a large firewall fleet consistent and efficient."
},
{
  id: 5014, cat: "D5: Infra Mgmt",
  q: "In Panorama, what are 'device groups' primarily used to manage?",
  opts: ["Interface and routing settings", "Shared security policies and objects pushed to groups of firewalls", "User passwords", "WAN links"],
  a: 1,
  why: "Device groups organize firewalls so security policies and objects can be defined centrally and pushed to the group, with hierarchy for shared vs. local rules. This is how Panorama standardizes policy across many devices while allowing site-specific exceptions."
},
{
  id: 5015, cat: "D5: Infra Mgmt",
  q: "In Panorama, what do 'templates' and 'template stacks' primarily manage?",
  opts: ["Security rules only", "Network and device settings (interfaces, zones, routing, server profiles) across firewalls", "Threat signatures", "URL categories"],
  a: 1,
  why: "Templates manage device/network configuration (interfaces, zones, routing, system settings); template stacks layer templates for reuse. Combined with device groups (policy), they let Panorama fully standardize both configuration and policy at scale."
},
{
  id: 5016, cat: "D5: Infra Mgmt",
  q: "What is the benefit of aggregating logs from many firewalls into Panorama (or a cloud logging service)?",
  opts: ["Slower searches", "Centralized correlation, reporting, and faster cross-device investigation", "Less visibility", "Automatic log deletion"],
  a: 1,
  why: "Centralized logging enables correlation across the entire fleet, unified reporting, and faster investigations that span multiple sites — far more effective than searching each firewall individually. At scale, aggregation is essential for SecOps, troubleshooting, and compliance."
},
{
  id: 5017, cat: "D5: Infra Mgmt",
  q: "When adding a new firewall to Panorama management, what is a key step in onboarding?",
  opts: ["Deleting the device", "Adding/registering the device and assigning it to the appropriate device group and template stack", "Disabling its policy", "Removing its license"],
  a: 1,
  why: "Onboarding a new device involves registering it with Panorama and assigning it to the correct device group (for policy) and template stack (for config) so it inherits standardized settings. Proper assignment ensures the new firewall is consistently managed from day one."
},
{
  id: 5018, cat: "D5: Infra Mgmt",
  q: "What does Strata Cloud Manager (SCM) provide for managing Strata and SASE solutions?",
  opts: ["A physical appliance", "A cloud-delivered console for centralized configuration, visibility, and best-practice/AIOps insights", "An endpoint agent", "A WAN circuit"],
  a: 1,
  why: "SCM is the cloud-based management interface unifying configuration and visibility across Strata NGFWs and SASE, with integrated AIOps and best-practice guidance. It modernizes management by removing the need to operate the management infrastructure yourself."
},
{
  id: 5019, cat: "D5: Infra Mgmt",
  q: "A key advantage of SCM's cloud-delivered management over purely on-prem management is:",
  opts: ["It requires shipping hardware", "Always-current, centralized management/visibility across hybrid deployments without maintaining the management server", "It disables logging", "It only works offline"],
  a: 1,
  why: "Cloud-delivered management eliminates the burden of maintaining management infrastructure and provides unified, continuously updated control and visibility spanning on-prem and SASE. This suits hybrid environments and reduces operational overhead compared with self-hosted management."
},
{
  id: 5020, cat: "D5: Infra Mgmt",
  q: "Why is consistent, centralized reporting valuable across a firewall fleet?",
  opts: ["It hides problems", "It provides unified insight into traffic, threats, and compliance across all devices for decision-making", "It slows the network", "It disables policy"],
  a: 1,
  why: "Centralized reporting gives leadership and operators a consolidated view of activity, threats, and posture across the whole environment, supporting informed decisions, trend analysis, and compliance reporting. Per-device reports alone can't reveal fleet-wide patterns."
},
{
  id: 5021, cat: "D5: Infra Mgmt",
  q: "Why should CDSS profiles be applied consistently across all relevant allow rules and firewalls?",
  opts: ["To create gaps", "To avoid inconsistent inspection that leaves some traffic unprotected", "To slow specific rules", "To disable threat prevention"],
  a: 1,
  why: "Inconsistent profile application means some allowed traffic is inspected while other traffic isn't — a gap attackers exploit. Applying CDSS profiles uniformly (often via profile groups and centralized management) ensures consistent threat inspection coverage everywhere."
},
{
  id: 5022, cat: "D5: Infra Mgmt",
  q: "How does centralized management help maintain CDSS subscriptions across many firewalls?",
  opts: ["It can't manage subscriptions", "It provides visibility into license/subscription status and pushes consistent profile/policy configuration fleet-wide", "It deletes subscriptions", "It disables updates"],
  a: 1,
  why: "Centralized management offers visibility into subscription/license status and lets admins push consistent CDSS profiles and policies across the fleet, ensuring services are properly configured and active everywhere. This prevents devices from silently missing protection."
},
{
  id: 5023, cat: "D5: Infra Mgmt",
  q: "What is a primary reason to use role-based access control (RBAC) for administrators in Panorama/SCM?",
  opts: ["To share one account", "To grant admins only the permissions their role requires and maintain accountability", "To disable authentication", "To allow anonymous changes"],
  a: 1,
  why: "RBAC enforces least privilege for administrators (e.g., separating who can edit vs. commit vs. view) and provides accountability for changes. In multi-admin environments managing many firewalls, RBAC reduces risk of error/abuse and supports audit requirements."
},
{
  id: 5024, cat: "D5: Infra Mgmt",
  q: "Why is it important that IoT Security's device classifications feed the firewall's policy?",
  opts: ["So devices remain unknown", "So accurate device identity/risk informs Device-ID enforcement (segmentation, least privilege)", "To disable logging", "To remove zones"],
  a: 1,
  why: "Accurate device classification from IoT Security enables precise Device-ID policy — segmenting and restricting devices based on what they actually are and how they should behave. Discovery without enforcement provides visibility but no protection; feeding policy closes the loop."
},
{
  id: 5025, cat: "D5: Infra Mgmt",
  q: "An organization must demonstrate that sensitive data transfers are controlled for a compliance audit. Which capability provides the needed evidence?",
  opts: ["Disabling logging", "DLP/SaaS monitoring and logs showing detection and enforcement of data-handling policy", "Allowing all transfers", "Removing data patterns"],
  a: 1,
  why: "DLP and SaaS Security logs/reports document that sensitive-data policies are enforced (transfers blocked/alerted, risky sharing remediated), providing audit evidence of control. Compliance frameworks require demonstrable enforcement, which monitoring/logging supplies."
},
{
  id: 5026, cat: "D5: Infra Mgmt",
  q: "What is the value of staging/reviewing App-ID content updates in a managed environment?",
  opts: ["To break policy", "To assess how new App-IDs may reclassify traffic and adjust policy before they take effect, avoiding disruption", "To disable updates", "To delete rules"],
  a: 1,
  why: "New App-IDs can change traffic classification and thus policy matches. Reviewing/staging their adoption lets admins update policy proactively and avoid unexpected allow/deny changes — especially important across a managed fleet where impact is widespread."
},
{
  id: 5027, cat: "D5: Infra Mgmt",
  q: "Why is monitoring license/subscription expiration important for CDSS maintenance?",
  opts: ["Expired licenses improve security", "An expired subscription can stop updates/protection, creating security gaps", "Licenses never expire", "It disables logging"],
  a: 1,
  why: "If a CDSS subscription lapses, the firewall may stop receiving updates or lose the service's protection, opening a security gap. Tracking expirations (via centralized management) and renewing on time ensures continuous protection — a basic but critical maintenance task."
},
{
  id: 5028, cat: "D5: Infra Mgmt",
  q: "How does SaaS Security typically enforce access control for sanctioned cloud apps?",
  opts: ["By allowing all access", "By applying policy based on user/identity, context, and sometimes app instance (corporate vs. personal)", "By blocking the whole category", "By disabling authentication"],
  a: 1,
  why: "SaaS Security enforces access based on identity, context, and often app instance/tenant (allowing corporate accounts while restricting personal ones). This granular access control lets the business use sanctioned apps safely while preventing risky or unsanctioned usage."
},
{
  id: 5029, cat: "D5: Infra Mgmt",
  q: "Why might an admin configure different DLP actions for internal vs. external data transfers?",
  opts: ["All transfers are equal risk", "External transfers usually carry higher exfiltration risk, warranting stricter actions (block) than internal (alert/log)", "Internal transfers are always blocked", "DLP can't differentiate"],
  a: 1,
  why: "Context matters: sending sensitive data outside the organization is higher-risk than internal movement, so policy may block external transfers while only alerting/logging internal ones. Tuning actions by context balances protection with productivity — a key DLP configuration practice."
},
{
  id: 5030, cat: "D5: Infra Mgmt",
  q: "What is a benefit of using Panorama to push software/content updates to many firewalls?",
  opts: ["Each device must be updated manually", "Centralized, coordinated distribution ensures consistency and reduces administrative effort", "Updates are skipped", "It disables HA"],
  a: 1,
  why: "Panorama can centrally schedule and distribute content/software updates across managed firewalls, ensuring consistency and saving the effort of updating each device individually. Coordinated updates reduce drift and the chance that some devices fall behind on protection."
},
{
  id: 5031, cat: "D5: Infra Mgmt",
  q: "Why is device behavior baselining (in IoT Security) part of ongoing maintenance, not a one-time task?",
  opts: ["Behavior never changes", "Device behavior and the device population evolve, so baselines must update to keep anomaly detection accurate", "Baselines disable detection", "It's purely cosmetic"],
  a: 1,
  why: "As devices are added, updated, or change roles, 'normal' behavior shifts. Continuously maintaining baselines keeps anomaly detection accurate (reducing false positives/negatives). Treating it as ongoing — not one-time — ensures IoT monitoring stays effective over time."
},
{
  id: 5032, cat: "D5: Infra Mgmt",
  q: "Which best describes why centralized management improves security posture, not just convenience?",
  opts: ["It increases inconsistency", "Consistent policy/config and unified visibility reduce gaps and misconfigurations that attackers exploit", "It hides threats", "It disables profiles"],
  a: 1,
  why: "Beyond convenience, centralized management enforces consistent, correct configuration and provides fleet-wide visibility, directly reducing the misconfigurations and coverage gaps that weaken security. Consistency and oversight are themselves security benefits at scale."
},
{
  id: 5033, cat: "D5: Infra Mgmt",
  q: "What is the purpose of reporting in SCM/Panorama for a security operations team?",
  opts: ["To obscure activity", "To provide actionable insight into threats, traffic, and policy effectiveness for decisions and tuning", "To delete data", "To slow investigations"],
  a: 1,
  why: "Reports translate raw logs into actionable insight — top threats, risky applications, policy hits, and trends — helping SecOps prioritize, tune policy, and communicate posture. Good reporting turns data into decisions, improving both operations and security outcomes."
},
{
  id: 5034, cat: "D5: Infra Mgmt",
  q: "Why is it important to control which administrators can modify CDSS profiles and policies?",
  opts: ["Anyone should change them freely", "Unrestricted changes could weaken protection or cause outages; RBAC limits and tracks who can modify them", "Changes don't matter", "It disables CDSS"],
  a: 1,
  why: "CDSS profiles/policies directly affect security and availability, so changes should be limited to appropriate roles and tracked for accountability via RBAC. Uncontrolled modification risks both weakened protection and accidental disruption — change control is essential maintenance hygiene."
},
{
  id: 5035, cat: "D5: Infra Mgmt",
  q: "How does combining access control, encryption, and monitoring strengthen SaaS/DLP data protection overall?",
  opts: ["They conflict", "Access control limits exposure, encryption protects confidentiality, and monitoring detects/records issues — layered defense", "Only one is ever needed", "They disable each other"],
  a: 1,
  why: "These controls are complementary layers: access control reduces who can reach data, encryption keeps it confidential if exposed, and monitoring/logging detects misuse and provides evidence. Together they provide defense in depth for sensitive data across SaaS and the network."
},
{
  id: 5036, cat: "D5: Infra Mgmt",
  q: "An admin needs to verify all managed firewalls have the latest threat content. Where is this most efficiently checked?",
  opts: ["By logging into each firewall separately", "In centralized management (Panorama/SCM), which shows content/version status across devices", "It can't be checked", "By rebooting all devices"],
  a: 1,
  why: "Centralized management provides a consolidated view of content/software versions across all managed firewalls, so admins can quickly spot devices that are behind and push updates. Checking each device individually is slow and error-prone at scale."
},
{
  id: 5037, cat: "D5: Infra Mgmt",
  q: "Why is it important that monitoring/logging for IoT, DLP, and SaaS feed into centralized visibility?",
  opts: ["To fragment data", "So security teams get a unified view of device, data, and SaaS risks for correlation and faster response", "To hide incidents", "To disable enforcement"],
  a: 1,
  why: "Centralizing IoT, DLP, and SaaS telemetry gives a unified risk picture, enabling correlation across domains (e.g., a risky device plus a data-exfiltration attempt) and faster, more informed response. Siloed logs make it harder to see the full story of an incident."
}