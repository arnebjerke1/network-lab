// ===== BATCH 8 FUN FACTS (12) — Domain 6 — paste into your FACTS array =====

"A site-to-site IPsec VPN encrypts traffic between two locations over the public internet — giving you private-circuit-like security without the private circuit.",
"Digital certificates do two jobs at once: they PROVE identity (authentication) and BOOTSTRAP encryption (TLS/IPsec) — which is why expired certs cause sudden outages.",
"GlobalProtect is more than a VPN — it carries the user's identity AND device posture (patch level, disk encryption) so access can be granted on a Zero Trust, least-privilege basis.",
"ZTNA flips the old VPN model: instead of dropping a remote user onto the whole network, it grants access to ONE specific app based on identity and policy.",
"Connecting branches and remote users to Prisma Access avoids 'backhauling' — you inspect traffic in the cloud near the user instead of dragging it back to HQ first.",
"Mutual TLS means BOTH ends authenticate with certificates — so not only does the client prove itself, the gateway proves it isn't a rogue impostor.",
"Split tunneling boosts performance by sending some traffic directly to the internet — but that traffic skips inspection, so it's a security trade-off to weigh carefully.",
"MFA is a must for remote access because remote logins are a top target — a second factor means a stolen password alone won't get an attacker in.",
"'Impossible travel' — logging in from two distant countries minutes apart — is a classic remote-access red flag that monitoring and baselining can catch.",
"For decryption to work smoothly, endpoints must TRUST the firewall's CA certificate — otherwise users get a wall of certificate warnings.",
"Promptly revoking access when an account is disabled closes a dangerous gap: lingering remote access for ex-employees is a favorite attacker entry point.",
"Zero Trust rewrites the rule for internal traffic too — being 'inside' the network no longer means 'trusted'; east-west flows get verified and least-privileged just like external ones."