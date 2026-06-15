// ===== BATCH 6: DOMAIN 3c — AIOps/BPA, NGTS, QUANTUM, AI SECURITY (ids 3096–3135) =====
// Paste into your QUESTIONS array.

{
  id: 3096, cat: "D3: AIOps/NGTS/AI",
  q: "What is the primary purpose of AIOps for NGFW/SASE in the Palo Alto Networks platform?",
  opts: ["To replace all admins", "To proactively surface issues, health, and best-practice recommendations using AI/ML-driven analytics", "To block all traffic", "To issue certificates"],
  a: 1,
  why: "AIOps applies AI/ML to operational and security telemetry to predict and prevent problems, assess deployment health, and recommend best-practice improvements before issues impact users. It shifts operations from reactive firefighting to proactive optimization."
},
{
  id: 3097, cat: "D3: AIOps/NGTS/AI",
  q: "What does a Best Practice Assessment (BPA) evaluate?",
  opts: ["Internet speed", "How well a firewall/configuration aligns with Palo Alto Networks recommended security best practices, with gaps and recommendations", "Cable quality", "Employee attendance"],
  a: 1,
  why: "A BPA reviews the configuration against recommended best practices, highlighting gaps (e.g., rules without inspection, decryption coverage, missing protections) and providing prioritized recommendations. It helps organizations strengthen posture and adopt the platform fully."
},
{
  id: 3098, cat: "D3: AIOps/NGTS/AI",
  q: "An organization runs a BPA and finds many allow rules have no security profiles attached. What does this indicate?",
  opts: ["The configuration is optimal", "A gap: allowed traffic isn't being inspected for threats, weakening efficacy", "Profiles are unnecessary", "The firewall is broken"],
  a: 1,
  why: "Allow rules without security profiles permit traffic without threat inspection — a meaningful gap the BPA flags. Best practice is to attach inspection profiles (AV, anti-spyware, vulnerability, URL, etc.) to allow rules so permitted traffic is still scanned for threats."
},
{
  id: 3099, cat: "D3: AIOps/NGTS/AI",
  q: "How does AIOps help prevent outages before they happen?",
  opts: ["By ignoring telemetry", "By analyzing trends/anomalies (e.g., capacity, errors) and alerting on predicted issues proactively", "By rebooting randomly", "By disabling monitoring"],
  a: 1,
  why: "AIOps analyzes telemetry to spot patterns indicating emerging problems — resource exhaustion, configuration drift, error trends — and alerts admins proactively. Predictive insight lets teams remediate before a minor issue becomes an outage, improving reliability."
},
{
  id: 3100, cat: "D3: AIOps/NGTS/AI",
  q: "Why is aligning to best practices (via BPA/AIOps) important for security efficacy?",
  opts: ["Best practices reduce security", "Misconfigurations and gaps undermine protection; closing them ensures the platform's capabilities are actually effective", "It only affects speed", "It disables threat prevention"],
  a: 1,
  why: "Even powerful security features fail to protect if misconfigured or unused (e.g., decryption off, profiles missing). BPA/AIOps identify and help close these gaps, ensuring deployed capabilities deliver their intended protection — directly improving real-world efficacy."
},
{
  id: 3101, cat: "D3: AIOps/NGTS/AI",
  q: "Where are AIOps and best-practice insights commonly surfaced for unified visibility?",
  opts: ["Only on paper", "In Strata Cloud Manager (SCM) dashboards", "Only via email once a year", "Nowhere"],
  a: 1,
  why: "Strata Cloud Manager (SCM) provides dashboards that present AIOps insights and best-practice assessments centrally, giving admins a unified view of health, posture, and recommendations across the deployment. This consolidates operational and security guidance in one place."
},
{
  id: 3102, cat: "D3: AIOps/NGTS/AI",
  q: "What does Next-Generation Trust Security (NGTS) broadly aim to support across the enterprise platform?",
  opts: ["Removing all trust decisions", "Identity governance, trust relationships, and adaptive security decisions", "Only WAN routing", "Only certificate storage"],
  a: 1,
  why: "NGTS focuses on identity governance, managing trust relationships, and enabling adaptive (context-aware) security decisions across the platform. It extends Zero Trust by continuously evaluating identity and context to inform dynamic access and security decisions enterprise-wide."
},
{
  id: 3103, cat: "D3: AIOps/NGTS/AI",
  q: "How does 'adaptive security' (a goal of NGTS) differ from static, fixed policy?",
  opts: ["It never changes", "It adjusts access/security decisions based on real-time context (identity, risk, behavior) rather than fixed rules alone", "It ignores identity", "It removes policy"],
  a: 1,
  why: "Adaptive security dynamically tailors decisions using current context — who the user is, device posture, risk signals, and behavior — instead of relying solely on static rules. This enables tighter, context-appropriate access (e.g., step-up authentication when risk rises), advancing Zero Trust."
},
{
  id: 3104, cat: "D3: AIOps/NGTS/AI",
  q: "Why is identity governance a foundational element of NGTS and Zero Trust?",
  opts: ["Identity is irrelevant", "Trust decisions hinge on accurate identity; governing who has access to what is essential for least privilege", "It only matters for guests", "It disables authentication"],
  a: 1,
  why: "Zero Trust and NGTS make decisions based on identity, so governing identities — who exists, what they can access, and whether that's appropriate — is foundational. Poor identity governance (excess privilege, stale accounts) directly weakens trust decisions and least privilege."
},
{
  id: 3105, cat: "D3: AIOps/NGTS/AI",
  q: "A 'harvest now, decrypt later' (HNDL) attack involves an adversary doing what?",
  opts: ["Decrypting data instantly today", "Capturing/storing encrypted data now to decrypt later once quantum computers can break today's encryption", "Deleting data", "Blocking encryption"],
  a: 1,
  why: "In HNDL, attackers collect encrypted data today and store it, anticipating that future quantum computers will break current public-key cryptography, letting them decrypt it later. This makes long-lived sensitive data at risk now, even if quantum computers aren't here yet."
},
{
  id: 3106, cat: "D3: AIOps/NGTS/AI",
  q: "Why is 'harvest now, decrypt later' a present-day concern even though large quantum computers don't widely exist yet?",
  opts: ["It isn't a concern", "Data with long-term sensitivity captured today could be decrypted years later when quantum capability arrives", "Quantum computers can't break encryption", "Encryption is unbreakable forever"],
  a: 1,
  why: "Data that must stay confidential for years (secrets, IP, personal data) is at risk if captured now and decrypted later. Because the threat is to data's future confidentiality, organizations must begin preparing today — even before quantum computers are practical."
},
{
  id: 3107, cat: "D3: AIOps/NGTS/AI",
  q: "What does 'post-quantum readiness' refer to?",
  opts: ["Removing all encryption", "Preparing systems to use cryptography that resists attacks from quantum computers", "Using only legacy ciphers", "Disabling decryption"],
  a: 1,
  why: "Post-quantum readiness means adopting quantum-resistant (post-quantum) cryptographic algorithms and architectures so data remains protected even against future quantum attacks. It's a proactive migration to algorithms believed to be secure against quantum-capable adversaries."
},
{
  id: 3108, cat: "D3: AIOps/NGTS/AI",
  q: "What is 'hybrid cryptography' in the context of post-quantum transition?",
  opts: ["Using no cryptography", "Combining traditional and post-quantum algorithms so protection holds even if one is later found weak", "Only quantum algorithms", "Only classical algorithms"],
  a: 1,
  why: "Hybrid cryptography uses both classical and post-quantum algorithms together during the transition, so data stays protected if either approach has an undiscovered weakness. It's a pragmatic bridge that hedges risk while standards and confidence in post-quantum algorithms mature."
},
{
  id: 3109, cat: "D3: AIOps/NGTS/AI",
  q: "Which quantum-related capability would a security platform offer to address HNDL risk for traffic it protects?",
  opts: ["Weaker encryption", "Support for post-quantum/hybrid cryptography to protect data against future quantum decryption", "Disabling all encryption", "Storing data in plaintext"],
  a: 1,
  why: "To counter HNDL, the platform can support post-quantum and hybrid cryptography for protected sessions, so intercepted traffic remains secure against future quantum attacks. Strengthening the cryptography protecting data-in-transit today is the direct mitigation for harvest-now-decrypt-later."
},
{
  id: 3110, cat: "D3: AIOps/NGTS/AI",
  q: "Employees begin pasting sensitive source code and customer data into public AI chatbots. What is the primary risk?",
  opts: ["Faster coding with no downside", "Sensitive data exposure — confidential information leaving the organization into third-party AI services", "Improved security automatically", "No risk at all"],
  a: 1,
  why: "Submitting sensitive data to public/external AI tools can expose confidential information outside the organization's control (and potentially into training data). This 'sensitive data exposure via AI' is a leading AI-related risk that data-protection controls must address."
},
{
  id: 3111, cat: "D3: AIOps/NGTS/AI",
  q: "How can the platform help control the risk of employees sharing sensitive data with AI applications?",
  opts: ["By ignoring AI traffic", "By discovering AI app usage and applying access controls and DLP to monitor/limit sensitive-data submission", "By blocking the internet entirely", "By disabling logging"],
  a: 1,
  why: "The platform can discover which AI apps are used, control access to them, and apply DLP to detect/prevent sensitive data from being submitted — governing AI use rather than ignoring or blanket-blocking it. This balances enabling AI productivity with protecting data."
},
{
  id: 3112, cat: "D3: AIOps/NGTS/AI",
  q: "What does 'AI application access' control aim to manage?",
  opts: ["Nothing", "Which AI applications/services users can access and how, to reduce risk while enabling sanctioned use", "Only printer access", "Cable management"],
  a: 1,
  why: "AI application access control governs which AI tools are permitted and under what conditions, allowing sanctioned, safer AI services while restricting risky or unsanctioned ones. As 'shadow AI' grows, this visibility and control is essential to manage AI-related risk."
},
{
  id: 3113, cat: "D3: AIOps/NGTS/AI",
  q: "What are 'AI-enabled threats'?",
  opts: ["Threats that can't use AI", "Attacks enhanced by AI — e.g., more convincing phishing, faster malware generation, automated evasion", "Only old-style viruses", "Threats that disable AI"],
  a: 1,
  why: "Attackers use AI to scale and sharpen attacks: highly convincing phishing/deepfakes, rapid generation of malware variants, and automated evasion. These AI-enabled threats raise the bar, which is why defenders increasingly rely on AI/ML-based detection to keep pace."
},
{
  id: 3114, cat: "D3: AIOps/NGTS/AI",
  q: "Why does the rise of AI-enabled threats reinforce the need for ML-based defenses (like the 'Advanced' CDSS services)?",
  opts: ["AI threats are easy to block with static lists", "AI lets attackers mass-produce novel, evasive attacks, so defenses need ML to detect unknowns at scale", "ML can't help against AI", "Signatures alone are sufficient"],
  a: 1,
  why: "AI enables attackers to generate large volumes of unique, evasive threats that defeat static signatures. ML-based defenses generalize to detect novel patterns and unknown threats, making them essential to counter AI-accelerated attacks — an AI-vs-AI dynamic."
},
{
  id: 3115, cat: "D3: AIOps/NGTS/AI",
  q: "An organization wants to 'discover, monitor, control, and secure' its AI usage. Which platform approach aligns with this?",
  opts: ["Ban all technology", "Gain visibility into AI apps/usage, apply access policy and DLP, and monitor for risky behavior", "Ignore AI entirely", "Disable the network"],
  a: 1,
  why: "Securing AI use follows discover → monitor → control → secure: see what AI is used, watch how, enforce access and data policies (DLP), and protect against AI-related threats. The platform's visibility and control capabilities operationalize this lifecycle rather than ignoring or blanket-banning AI."
},
{
  id: 3116, cat: "D3: AIOps/NGTS/AI",
  q: "How does NGTS's adaptive approach help when a normally low-risk user suddenly exhibits high-risk behavior?",
  opts: ["It keeps access unchanged", "It can adjust trust/access dynamically (e.g., require step-up auth or restrict access) based on the elevated risk", "It deletes the user", "It ignores behavior"],
  a: 1,
  why: "Adaptive security reacts to changing risk: if a trusted user's behavior becomes anomalous, NGTS can tighten access, require additional verification, or restrict actions in real time. This continuous, context-driven adjustment is more resilient than fixed, one-time trust decisions."
},
{
  id: 3117, cat: "D3: AIOps/NGTS/AI",
  q: "Why is proactive best-practice adoption (via BPA) often more cost-effective than reactive incident response?",
  opts: ["It isn't", "Preventing misconfigurations/gaps avoids breaches and outages that are far costlier to handle after the fact", "Incidents are free", "Best practices cause incidents"],
  a: 1,
  why: "Closing gaps proactively (proper decryption, profiles, segmentation) prevents incidents that are expensive and disruptive to remediate. Prevention via best practices is generally far cheaper than responding to a breach or outage — a core argument for BPA/AIOps."
},
{
  id: 3118, cat: "D3: AIOps/NGTS/AI",
  q: "Which best describes the relationship between AIOps insights and administrative action?",
  opts: ["AIOps replaces all admin decisions automatically with no oversight", "AIOps provides data-driven recommendations and alerts that inform and guide admins' decisions", "AIOps hides information from admins", "AIOps only logs errors"],
  a: 1,
  why: "AIOps augments administrators with predictive insights, health scores, and prioritized recommendations, guiding better, faster decisions. It's decision support — surfacing what matters — while humans retain oversight and act on the guidance. This human-plus-AI model improves operations."
},
{
  id: 3119, cat: "D3: AIOps/NGTS/AI",
  q: "Why must organizations inventory where long-lived sensitive data is encrypted today as part of quantum preparedness?",
  opts: ["Inventory is pointless", "To identify what's vulnerable to HNDL and prioritize migrating those protections to post-quantum cryptography", "To delete all data", "Quantum risk doesn't involve data"],
  a: 1,
  why: "Knowing where long-term-sensitive data is protected (and by which algorithms) lets you prioritize what to migrate to post-quantum/hybrid cryptography first, since that data is most exposed to harvest-now-decrypt-later. You can't plan a crypto migration without understanding your crypto footprint."
},
{
  id: 3120, cat: "D3: AIOps/NGTS/AI",
  q: "A key reason to govern (not just block) AI tools is:",
  opts: ["AI has no business value", "AI offers real productivity benefits, so the goal is safe, sanctioned use rather than outright prohibition that drives shadow AI", "Blocking is always best", "Governance reduces productivity"],
  a: 1,
  why: "AI delivers genuine productivity gains, and blanket bans push usage underground ('shadow AI'). Governing AI — allowing sanctioned tools with data protections and monitoring — captures the benefits while managing risk, mirroring how SaaS shadow IT is best handled with visibility and control."
},
{
  id: 3121, cat: "D3: AIOps/NGTS/AI",
  q: "How does data loss prevention (DLP) directly support securing AI usage?",
  opts: ["It allows all data to AI", "It can detect and block sensitive data being submitted to AI applications", "It disables AI detection", "It only inspects email"],
  a: 1,
  why: "DLP inspects content destined for AI apps and can block or alert when sensitive data (PII, source code, secrets) is being submitted, preventing exposure to external AI services. This makes DLP a core control in the discover-monitor-control-secure approach to AI risk."
},
{
  id: 3122, cat: "D3: AIOps/NGTS/AI",
  q: "Why is continuous monitoring central to both NGTS adaptive security and AI risk management?",
  opts: ["One-time checks are enough", "Risk and context change constantly, so ongoing monitoring is needed to adjust trust and catch emerging AI/data risks", "Monitoring disables security", "Context never changes"],
  a: 1,
  why: "Trust and risk are not static — users, devices, behaviors, and AI usage evolve continuously. Ongoing monitoring enables adaptive decisions (NGTS) and timely detection of risky AI/data activity, whereas one-time checks quickly become outdated. Continuous visibility is foundational to both."
},
{
  id: 3123, cat: "D3: AIOps/NGTS/AI",
  q: "Which scenario best illustrates AIOps improving security posture rather than just uptime?",
  opts: ["Only predicting hardware failure", "Detecting that decryption coverage is low and recommending expanding it to close a threat-visibility gap", "Measuring fan speed", "Counting cables"],
  a: 1,
  why: "Beyond operational health, AIOps/BPA can identify security-relevant gaps — like insufficient decryption leaving threats hidden — and recommend remediation. Surfacing and guiding closure of such posture weaknesses directly strengthens security, not merely availability."
},
{
  id: 3124, cat: "D3: AIOps/NGTS/AI",
  q: "What is a primary benefit of the platform addressing quantum, AI, and trust risks in an integrated way rather than as separate point tools?",
  opts: ["More silos", "Unified visibility and consistent policy across emerging risks, reducing gaps and complexity", "Less protection", "No policy"],
  a: 1,
  why: "Handling emerging risks (quantum-safe crypto, AI usage governance, adaptive trust) within one platform provides consistent policy and unified visibility, avoiding the gaps and operational burden of disconnected point solutions. Integration is key as the threat landscape broadens rapidly."
},
{
  id: 3125, cat: "D3: AIOps/NGTS/AI",
  q: "Why is post-quantum cryptography considered a journey/migration rather than a single switch?",
  opts: ["It happens instantly everywhere", "Migrating algorithms across many systems takes time, testing, and hybrid approaches to maintain security throughout", "It requires no planning", "Encryption never changes"],
  a: 1,
  why: "Transitioning cryptography across diverse systems, protocols, and partners is complex and gradual, requiring inventory, testing, and hybrid methods to stay secure during the change. Treating it as a phased journey — starting now — is essential given the HNDL threat to long-lived data."
},
{
  id: 3126, cat: "D3: AIOps/NGTS/AI",
  q: "An AI-enabled phishing campaign produces flawless, personalized emails at scale. Which defensive shift does this motivate?",
  opts: ["Rely only on spotting typos", "Strengthen technical controls (ML-based URL/phishing detection, credential protection) since human spotting of 'obvious' phishing is less reliable", "Disable email", "Ignore phishing"],
  a: 1,
  why: "AI removes the tell-tale errors users were taught to spot, making phishing far more convincing. This shifts reliance toward technical controls — ML-driven URL/phishing detection, credential-submission protection, and DLP — rather than depending on users to recognize 'obvious' fakes."
},
{
  id: 3127, cat: "D3: AIOps/NGTS/AI",
  q: "How does NGTS extend Zero Trust beyond initial authentication?",
  opts: ["By trusting users permanently after login", "By continuously evaluating identity, context, and risk to make ongoing, adaptive trust decisions", "By removing authentication", "By ignoring context"],
  a: 1,
  why: "Traditional models often trust a user after initial login; NGTS continuously reassesses identity, context, and risk to adapt access throughout the session. This 'never trust, always verify — continuously' approach closes gaps that one-time authentication leaves open."
},
{
  id: 3128, cat: "D3: AIOps/NGTS/AI",
  q: "Why is visibility into 'shadow AI' analogous to visibility into 'shadow IT'?",
  opts: ["Neither matters", "Both involve unsanctioned tools used without oversight, creating data-exposure risk that requires discovery before control", "Shadow AI is always safe", "They are unrelated concepts"],
  a: 1,
  why: "Shadow AI mirrors shadow IT: employees adopt unsanctioned AI tools without approval, risking data exposure. As with SaaS, you must first discover the usage, then assess risk and apply controls. The same discover-then-govern playbook applies to emerging AI tools."
},
{
  id: 3129, cat: "D3: AIOps/NGTS/AI",
  q: "What makes AI/ML especially well-suited to AIOps for large firewall/SASE deployments?",
  opts: ["Humans can easily process all the data manually", "The volume and complexity of telemetry exceed manual analysis, so ML can find patterns and anomalies at scale", "ML reduces visibility", "Telemetry is tiny"],
  a: 1,
  why: "Large deployments generate vast, complex telemetry that humans can't fully analyze manually. ML excels at detecting patterns, trends, and anomalies across that scale, enabling proactive insights and recommendations that would be impractical to derive by hand — the essence of AIOps."
},
{
  id: 3130, cat: "D3: AIOps/NGTS/AI",
  q: "Which combination best secures an enterprise adopting AI tools broadly?",
  opts: ["No controls at all", "AI app discovery + access control + DLP + ML-based threat detection for AI-enabled attacks", "Only a firewall reboot", "Blocking the entire internet"],
  a: 1,
  why: "Comprehensive AI security layers discovery (see AI usage), access control (govern which tools), DLP (protect sensitive data submitted to AI), and ML-based detection (counter AI-enabled threats). Together they let the enterprise embrace AI while managing its multifaceted risks."
},
{
  id: 3131, cat: "D3: AIOps/NGTS/AI",
  q: "Why might an organization prioritize protecting certain data with post-quantum cryptography sooner than other data?",
  opts: ["All data has equal urgency", "Data that must remain confidential for many years is most exposed to harvest-now-decrypt-later and should be prioritized", "Short-lived data is highest priority", "Quantum risk ignores data lifespan"],
  a: 1,
  why: "HNDL risk is greatest for data whose confidentiality must persist for years (state secrets, IP, long-term personal records), because it could be decrypted once quantum capability matures. Prioritizing such long-lived sensitive data for post-quantum protection addresses the highest risk first."
},
{
  id: 3132, cat: "D3: AIOps/NGTS/AI",
  q: "How do AIOps best-practice recommendations relate to the BPA?",
  opts: ["They are unrelated", "Both assess alignment to recommended practices and guide remediation; AIOps adds continuous, proactive analysis", "BPA disables AIOps", "AIOps ignores best practices"],
  a: 1,
  why: "BPA and AIOps both measure adherence to best practices and recommend improvements; AIOps brings continuous, AI-driven analysis and proactive alerting on top of point-in-time assessment. Together they help organizations continuously align configuration with recommended, secure practices."
},
{
  id: 3133, cat: "D3: AIOps/NGTS/AI",
  q: "A core reason adaptive, identity-centric security (NGTS) is increasingly important is:",
  opts: ["Perimeters fully protect modern enterprises", "Users, devices, and apps are distributed beyond the perimeter, so identity and context must drive trust decisions", "Identity is obsolete", "Static rules handle all cases"],
  a: 1,
  why: "With cloud, SaaS, and remote work, the traditional network perimeter no longer contains everything, so security must center on identity and real-time context. NGTS's adaptive, identity-driven trust decisions fit this perimeter-less reality far better than static, location-based rules."
},
{
  id: 3134, cat: "D3: AIOps/NGTS/AI",
  q: "Which statement best summarizes the platform's approach to emerging risks (quantum, AI) in Domain 3?",
  opts: ["Ignore them until they're mainstream", "Proactively identify the risks and provide capabilities (post-quantum/hybrid crypto, AI discovery/control/DLP) to address them now", "Block all new technology", "Wait for a breach first"],
  a: 1,
  why: "The platform's stance is proactive: recognize emerging risks (HNDL/quantum, AI exposure and AI-enabled threats) and offer concrete capabilities to mitigate them today — post-quantum/hybrid cryptography and AI discovery, control, and DLP. Acting early reduces exposure before these risks fully materialize."
},
{
  id: 3135, cat: "D3: AIOps/NGTS/AI",
  q: "Overall, how do AIOps, NGTS, quantum, and AI-security capabilities collectively advance the platform's value?",
  opts: ["They add unrelated noise", "They extend protection to operations (AIOps), trust (NGTS), future cryptography (quantum), and AI risk — keeping security effective as the landscape evolves", "They replace the firewall", "They only matter for logging"],
  a: 1,
  why: "These capabilities future-proof the platform: AIOps optimizes operations and posture, NGTS modernizes trust decisions, post-quantum readiness protects against future cryptographic threats, and AI-security controls manage AI's risks. Together they keep the platform effective against both current and emerging challenges."
}