"""
PCNSP Weekly Study Planner
--------------------------
Builds a personalised 9-week study schedule from the PCNSP course list
and maps existing quiz questions to each week.

Reads (optional):
  course_content.json  – from content_scraper.py (rich slide-level data)
  questions.json       – from txt_parser.py or scraper.py

Writes:
  schedule.json              – full week-by-week plan
  questions_week_1.json …    – per-week quiz question subsets
  progress.json              – initialised blank (skipped if already exists)

Usage
-----
    python weekly_planner.py
"""

import json
import os
import re
import sys

SCRIPT_DIR           = os.path.dirname(__file__)
COURSE_CONTENT_FILE  = os.path.join(SCRIPT_DIR, "course_content.json")
QUESTIONS_FILE       = os.path.join(SCRIPT_DIR, "questions.json")
SCHEDULE_FILE        = os.path.join(SCRIPT_DIR, "schedule.json")
PROGRESS_FILE        = os.path.join(SCRIPT_DIR, "progress.json")

RECAP_MINUTES = 30   # review block appended to each week

# ---------------------------------------------------------------------------
# Week definitions  (26 SCORM courses spread across 9 weeks)
# Each entry has a stable list of course ids so the plan works even without
# course_content.json.  Duration and objectives are filled from content if
# available, otherwise from the seed values below.
# ---------------------------------------------------------------------------

WEEKS = [
    {
        "week":  1,
        "title": "Networking Foundations",
        "theme_desc": (
            "Core network concepts: diagrams, traffic flows, IP addressing, "
            "OSI model, and perimeter architecture."
        ),
        "course_ids": [
            "networking_basics",
            "traffic_flow_concepts",
            "networking_and_addressing",
            "network_security",
        ],
        "keywords": [
            "network diagram", "north-south", "east-west", "router",
            "broadcast domain", "subnet", "osi", "tcp", "ip address",
            "ethernet", "encapsulation", "circuit-switch", "packet-switch",
            "layer 2", "layer 3", "layer 4", "application layer",
            "network perimeter", "acl", "access control list", "packet content",
            "traffic flow",
        ],
    },
    {
        "week":  2,
        "title": "Threat Landscape & Cybersecurity Basics",
        "theme_desc": (
            "Understand the attack lifecycle, threat actors, attacker "
            "motivations, and the full cybersecurity landscape."
        ),
        "course_ids": [
            "cybersecurity_landscape",
            "analyzing_the_threat_lifecycle",
            "attack_techniques",
        ],
        "keywords": [
            "cyberattack", "threat lifecycle", "threat actor", "exploit",
            "cybersecurity landscape", "attack technique", "phishing",
            "spear phishing", "weaponization", "acting-on-objectives",
            "kill chain", "reconnaissance",
        ],
    },
    {
        "week":  3,
        "title": "Network-Based Attacks & Asset Protection",
        "theme_desc": (
            "Common network attacks (DoS, DDoS, MitM, botnets) and "
            "strategies for protecting network assets."
        ),
        "course_ids": [
            "network_based_attacks",
            "network_asset_protection",
        ],
        "keywords": [
            "denial-of-service", "dos", "ddos", "distributed denial",
            "man-in-the-middle", "mitm", "botnet", "network-based attack",
            "asset protection", "network asset", "dmz", "firewall placement",
        ],
    },
    {
        "week":  4,
        "title": "Cloud Infrastructure & Workflows",
        "theme_desc": (
            "Cloud service models (IaaS/PaaS/SaaS/FaaS), containers, "
            "hypervisors, CI/CD, and cloud-native architectures."
        ),
        "course_ids": [
            "cloud_native_workflows",
            "elements_of_cloud_based_solutions",
        ],
        "keywords": [
            "cloud", "iaas", "saas", "paas", "faas", "serverless",
            "container", "hypervisor", "virtual machine", "ci/cd",
            "cloud-native", "cloud service model", "cloud provider",
            "public cloud", "private cloud", "hybrid cloud",
            "software-defined network", "sdн",
        ],
    },
    {
        "week":  5,
        "title": "Cloud Security Controls",
        "theme_desc": (
            "Shared responsibility model, VPC security groups, network ACLs, "
            "cloud threats, cryptojacking, and insider risks."
        ),
        "course_ids": [
            "shared_security_model",
            "threats_in_the_cloud",
        ],
        "keywords": [
            "shared responsibility", "vpc", "virtual private cloud",
            "security group", "cloud.*acl", "threats in the cloud",
            "cryptojacking", "insider", "cloud account", "cloud application",
            "api security", "logging and monitoring",
        ],
    },
    {
        "week":  6,
        "title": "Security Management & Panorama",
        "theme_desc": (
            "Centralised management challenges, Panorama deployment, "
            "single-pane-of-glass operations, and NGFW management."
        ),
        "course_ids": [
            "network_security_management_challenges",
            "ngfw_device_management_using_panorama",
        ],
        "keywords": [
            "panorama", "single-pane", "centralized management",
            "management console", "management challenge", "ngfw management",
            "third-party tool", "firewall management", "log information",
            "disconnected solution",
        ],
    },
    {
        "week":  7,
        "title": "Cloud-Delivered Security Services & URL Filtering",
        "theme_desc": (
            "WildFire, Advanced Threat Prevention, CDSS framework, "
            "Advanced URL Filtering, and PAN-DB categories."
        ),
        "course_ids": [
            "cdss_overview",
            "advanced_url_filtering",
            "advanced_url_filtering_security",
        ],
        "keywords": [
            "wildfire", "cdss", "cloud-delivered security",
            "url filter", "advanced url", "pan-db",
            "intrusion prevention", "advanced threat prevention",
            "atp", "threat prevention",
        ],
    },
    {
        "week":  8,
        "title": "SASE, SD-WAN & Digital Experience",
        "theme_desc": (
            "SASE architecture, mobile user protection, remote networks, "
            "SD-WAN resilience, and Autonomous DEM."
        ),
        "course_ids": [
            "protection_challenges_mobile_remote",
            "sase_cloud_infrastructure",
            "sase_for_mobile_users",
            "sase_for_remote_networks",
            "sdwan",
            "autonomous_digital_experience_management",
        ],
        "keywords": [
            "sase", "sd-wan", "digital experience", "dem",
            "mobile user", "remote network", "branch office",
            "secure access service", "prisma access",
            "autonomous digital",
        ],
    },
    {
        "week":  9,
        "title": "Endpoint Security, Security Models & Final Review",
        "theme_desc": (
            "Endpoint protection, malware detection, MDM, DLP, IDS/IPS, "
            "Zero Trust, security models, and a full course review."
        ),
        "course_ids": [
            "endpoint_security",
            "security_models",
        ],
        "keywords": [
            "endpoint", "mdm", "mobile device management",
            "malware detection", "dlp", "data loss prevention",
            "ids", "ips", "intrusion detection",
            "zero trust", "trust zone", "segmentation", "least privilege",
            "protect surface", "security model", "perimeter-based",
            "ransomware", "apt", "advanced persistent", "wi-fi",
            "dark web", "attack surface",
        ],
    },
]

# ---------------------------------------------------------------------------
# Seed course catalog
# Used when course_content.json is not available (i.e. before running
# content_scraper.py).  Duration values are conservative estimates.
# ---------------------------------------------------------------------------

SEED_CATALOG: dict[str, dict] = {
    "networking_basics": {
        "title": "Networking Basics",
        "duration_minutes": 20,
        "status": "Completed",
        "objectives": [
            "Use network diagram components to create visual collaboration aids",
            "Describe north-south and east-west traffic flows",
            "Identify router boundaries in creating network segments",
            "Describe packet contents",
        ],
        "lessons": [
            "Lesson 1: Network Diagrams",
            "Lesson 2: Traffic Flows",
            "Lesson 3: Router Boundaries",
            "Lesson 4: Packet Contents",
        ],
    },
    "traffic_flow_concepts": {
        "title": "Traffic Flow Concepts",
        "duration_minutes": 25,
        "status": "Not started",
        "objectives": [
            "Explain inbound and outbound traffic flows",
            "Describe how traffic is inspected at network boundaries",
            "Identify traffic flow patterns in enterprise networks",
        ],
        "lessons": [
            "Lesson 1: Inbound Traffic",
            "Lesson 2: Outbound Traffic",
            "Lesson 3: Traffic Inspection",
        ],
    },
    "networking_and_addressing": {
        "title": "Networking and Addressing",
        "duration_minutes": 30,
        "status": "Not started",
        "objectives": [
            "Describe OSI and TCP/IP model layers",
            "Explain IPv4 addressing and subnetting",
            "Identify packet-switched vs circuit-switched networks",
            "Describe data encapsulation across OSI layers",
        ],
        "lessons": [
            "Lesson 1: OSI Model",
            "Lesson 2: TCP/IP Model",
            "Lesson 3: IP Addressing",
            "Lesson 4: Subnetting",
            "Lesson 5: Encapsulation",
        ],
    },
    "network_security": {
        "title": "Network Security",
        "duration_minutes": 25,
        "status": "Not started",
        "objectives": [
            "Describe traditional network security architecture",
            "Explain the role of DMZ and perimeter firewalls",
            "Identify security zones and trust levels",
        ],
        "lessons": [
            "Lesson 1: Network Security Architecture",
            "Lesson 2: DMZ Design",
            "Lesson 3: Security Zones",
        ],
    },
    "cybersecurity_landscape": {
        "title": "Cybersecurity Landscape",
        "duration_minutes": 25,
        "status": "Not started",
        "objectives": [
            "Describe the modern cybersecurity threat landscape",
            "Identify motivations and types of threat actors",
            "Explain emerging attack trends",
        ],
        "lessons": [
            "Lesson 1: Threat Landscape Overview",
            "Lesson 2: Threat Actors",
            "Lesson 3: Attack Trends",
        ],
    },
    "analyzing_the_threat_lifecycle": {
        "title": "Analyzing the Threat Lifecycle",
        "duration_minutes": 30,
        "status": "Not started",
        "objectives": [
            "Describe the cyberattack lifecycle phases",
            "Explain attacker goals at each phase",
            "Identify defensive controls for each lifecycle phase",
        ],
        "lessons": [
            "Lesson 1: Reconnaissance",
            "Lesson 2: Weaponization and Delivery",
            "Lesson 3: Exploitation",
            "Lesson 4: Command and Control",
            "Lesson 5: Acting on Objectives",
        ],
    },
    "attack_techniques": {
        "title": "Attack Techniques",
        "duration_minutes": 25,
        "status": "Not started",
        "objectives": [
            "Identify common network attack techniques",
            "Describe phishing, spear-phishing, and APT campaigns",
            "Explain ransomware and cryptojacking",
        ],
        "lessons": [
            "Lesson 1: Social Engineering",
            "Lesson 2: Phishing and Spear Phishing",
            "Lesson 3: Ransomware",
            "Lesson 4: Advanced Persistent Threats",
        ],
    },
    "network_based_attacks": {
        "title": "Network-Based Attacks",
        "duration_minutes": 25,
        "status": "Not started",
        "objectives": [
            "Describe DoS and DDoS attack mechanics",
            "Explain man-in-the-middle attacks",
            "Identify botnet structures and usage",
        ],
        "lessons": [
            "Lesson 1: DoS and DDoS",
            "Lesson 2: Man-in-the-Middle",
            "Lesson 3: Botnets",
        ],
    },
    "network_asset_protection": {
        "title": "Network Asset Protection",
        "duration_minutes": 30,
        "status": "In progress",
        "objectives": [
            "Describe strategies for protecting network assets",
            "Identify firewall types and deployment patterns",
            "Explain IDS and IPS differences",
        ],
        "lessons": [
            "Lesson 1: Asset Inventory",
            "Lesson 2: Firewall Deployment",
            "Lesson 3: IDS vs IPS",
            "Lesson 4: Segmentation",
        ],
    },
    "cloud_native_workflows": {
        "title": "Cloud-Native Workflows",
        "duration_minutes": 25,
        "status": "Not started",
        "objectives": [
            "Describe CI/CD pipelines and DevOps concepts",
            "Explain containerisation and microservices",
            "Identify cloud-native security challenges",
        ],
        "lessons": [
            "Lesson 1: CI/CD Overview",
            "Lesson 2: Containers and Microservices",
            "Lesson 3: FaaS and Serverless",
        ],
    },
    "elements_of_cloud_based_solutions": {
        "title": "Elements of Cloud-Based Solutions",
        "duration_minutes": 30,
        "status": "Not started",
        "objectives": [
            "Identify IaaS, PaaS, SaaS, and FaaS service models",
            "Describe hypervisors and virtual machines",
            "Explain logging and monitoring in cloud environments",
        ],
        "lessons": [
            "Lesson 1: Cloud Service Models",
            "Lesson 2: Virtualisation",
            "Lesson 3: Logging and Monitoring",
            "Lesson 4: SDN Concepts",
        ],
    },
    "shared_security_model": {
        "title": "Shared Security Model",
        "duration_minutes": 20,
        "status": "Not started",
        "objectives": [
            "Describe the cloud shared responsibility model",
            "Identify provider vs customer security responsibilities",
            "Explain VPC and network ACL concepts",
        ],
        "lessons": [
            "Lesson 1: Shared Responsibility",
            "Lesson 2: VPC Security",
            "Lesson 3: Security Groups vs ACLs",
        ],
    },
    "threats_in_the_cloud": {
        "title": "Threats in the Cloud",
        "duration_minutes": 25,
        "status": "Not started",
        "objectives": [
            "Identify cloud-specific security risks",
            "Describe cryptojacking and insider threats",
            "Explain API security risks",
        ],
        "lessons": [
            "Lesson 1: Cloud Risk Categories",
            "Lesson 2: Cryptojacking",
            "Lesson 3: Insider Threats",
            "Lesson 4: API Security",
        ],
    },
    "network_security_management_challenges": {
        "title": "Network Security Management Challenges",
        "duration_minutes": 25,
        "status": "Not started",
        "objectives": [
            "Describe challenges of managing disconnected security tools",
            "Explain single-pane-of-glass management benefits",
            "Identify goals of centralised security management",
        ],
        "lessons": [
            "Lesson 1: Management Challenges",
            "Lesson 2: Centralised Management",
            "Lesson 3: Tool Integration",
        ],
    },
    "ngfw_device_management_using_panorama": {
        "title": "NGFW Device Management Using Panorama",
        "duration_minutes": 30,
        "status": "Not started",
        "objectives": [
            "Describe Panorama deployment options",
            "Explain Panorama log sources and reporting",
            "Identify benefits of Panorama vs per-device management",
        ],
        "lessons": [
            "Lesson 1: Panorama Overview",
            "Lesson 2: Device Groups and Templates",
            "Lesson 3: Logging and Reporting",
        ],
    },
    "cdss_overview": {
        "title": "Cloud-Delivered Security Services (CDSS) Overview",
        "duration_minutes": 25,
        "status": "Not started",
        "objectives": [
            "Describe the CDSS framework",
            "Explain WildFire threat intelligence",
            "Identify CDSS service components",
        ],
        "lessons": [
            "Lesson 1: CDSS Framework",
            "Lesson 2: WildFire",
            "Lesson 3: Advanced Threat Prevention",
        ],
    },
    "advanced_url_filtering": {
        "title": "Advanced URL Filtering",
        "duration_minutes": 25,
        "status": "Not started",
        "objectives": [
            "Describe Advanced URL Filtering capabilities",
            "Explain PAN-DB URL category classifications",
            "Identify URL filtering policy evaluation steps",
        ],
        "lessons": [
            "Lesson 1: URL Filtering Overview",
            "Lesson 2: PAN-DB Categories",
            "Lesson 3: Policy Evaluation",
        ],
    },
    "advanced_url_filtering_security": {
        "title": "Advanced URL Filtering Security",
        "duration_minutes": 20,
        "status": "Completed",
        "objectives": [
            "Describe inline ML for URL classification",
            "Explain how URL filtering compensates for database gaps",
        ],
        "lessons": [
            "Lesson 1: ML-Based Classification",
            "Lesson 2: Inline Analysis",
        ],
    },
    "protection_challenges_mobile_remote": {
        "title": "Protection Challenges for Mobile Users and Remote Networks",
        "duration_minutes": 20,
        "status": "Not started",
        "objectives": [
            "Describe mobile user protection challenges",
            "Identify remote network connectivity issues",
            "Explain how traditional VPN falls short for modern workforces",
        ],
        "lessons": [
            "Lesson 1: Mobile User Challenges",
            "Lesson 2: Remote Network Challenges",
        ],
    },
    "sase_cloud_infrastructure": {
        "title": "SASE as a Cloud Infrastructure-Based Services Solution",
        "duration_minutes": 25,
        "status": "Not started",
        "objectives": [
            "Define SASE and its core components",
            "Explain how SASE replaces legacy perimeter security",
            "Describe SASE scalability and cost benefits",
        ],
        "lessons": [
            "Lesson 1: SASE Overview",
            "Lesson 2: SASE Architecture",
            "Lesson 3: SASE vs Traditional Security",
        ],
    },
    "sase_for_mobile_users": {
        "title": "SASE for Mobile Users",
        "duration_minutes": 20,
        "status": "Not started",
        "objectives": [
            "Describe how SASE improves mobile user security",
            "Explain seamless and transparent mobile access",
            "Identify device flexibility benefits of SASE",
        ],
        "lessons": [
            "Lesson 1: Mobile User Security",
            "Lesson 2: Transparent Access",
        ],
    },
    "sase_for_remote_networks": {
        "title": "SASE for Remote Networks",
        "duration_minutes": 20,
        "status": "Not started",
        "objectives": [
            "Describe how SASE secures branch offices",
            "Explain SASE performance optimization for branches",
            "Identify resilience features for branch connectivity",
        ],
        "lessons": [
            "Lesson 1: Branch Office Security",
            "Lesson 2: Branch Performance",
            "Lesson 3: Branch Resilience",
        ],
    },
    "sdwan": {
        "title": "Software-Defined Wide Area Networking (SD-WAN)",
        "duration_minutes": 25,
        "status": "Not started",
        "objectives": [
            "Describe SD-WAN functionality and benefits",
            "Explain application performance optimization in SD-WAN",
            "Identify SD-WAN resilience and failover features",
        ],
        "lessons": [
            "Lesson 1: SD-WAN Overview",
            "Lesson 2: Performance Optimization",
            "Lesson 3: Resilience and Failover",
            "Lesson 4: Secure Connectivity",
        ],
    },
    "autonomous_digital_experience_management": {
        "title": "Autonomous Digital Experience Management",
        "duration_minutes": 20,
        "status": "Not started",
        "objectives": [
            "Describe Autonomous DEM and its purpose",
            "Explain how DEM measures user experience",
            "Identify DEM feedback integration with SASE",
        ],
        "lessons": [
            "Lesson 1: DEM Overview",
            "Lesson 2: Experience Metrics",
            "Lesson 3: DEM and SASE",
        ],
    },
    "endpoint_security": {
        "title": "Endpoint Security",
        "duration_minutes": 30,
        "status": "Not started",
        "objectives": [
            "Describe endpoint security components",
            "Explain malware detection techniques",
            "Identify MDM features and DLP capabilities",
            "Describe host-based IDS/IPS",
        ],
        "lessons": [
            "Lesson 1: Endpoint Protection Overview",
            "Lesson 2: Malware Detection",
            "Lesson 3: Mobile Device Management",
            "Lesson 4: DLP",
        ],
    },
    "security_models": {
        "title": "Security Models",
        "duration_minutes": 25,
        "status": "Not started",
        "objectives": [
            "Describe the Zero Trust security model",
            "Explain the protect surface and trust zones",
            "Identify least privilege access principles",
            "Describe incremental Zero Trust adoption",
        ],
        "lessons": [
            "Lesson 1: Zero Trust Overview",
            "Lesson 2: Protect Surface",
            "Lesson 3: Least Privilege",
            "Lesson 4: Implementation Steps",
        ],
    },
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_questions() -> list[dict]:
    if not os.path.exists(QUESTIONS_FILE):
        print(f"[!] {QUESTIONS_FILE} not found – questions will not be mapped to weeks")
        return []
    with open(QUESTIONS_FILE, encoding="utf-8") as f:
        return json.load(f)


def load_course_content() -> dict[str, dict]:
    """
    Return a mapping of {course_title_slug: content_data} from
    course_content.json if available, otherwise an empty dict.
    """
    if not os.path.exists(COURSE_CONTENT_FILE):
        return {}
    with open(COURSE_CONTENT_FILE, encoding="utf-8") as f:
        raw = json.load(f)
    out = {}
    for entry in raw:
        slug = re.sub(r"[^a-z0-9]+", "_", entry.get("title", "").lower()).strip("_")
        if slug:
            out[slug] = entry
    return out


def _match_score(text: str, keywords: list[str]) -> int:
    """Count how many keywords appear in text (case-insensitive)."""
    t = text.lower()
    return sum(1 for kw in keywords if re.search(kw, t))


def assign_question_to_week(question_text: str) -> int:
    """Return the best-matching week number (1-9) for a question."""
    best_week  = 1
    best_score = 0
    for wk in WEEKS:
        score = _match_score(question_text, wk["keywords"])
        if score > best_score:
            best_score = score
            best_week  = wk["week"]
    return best_week


def build_week_question_map(questions: list[dict]) -> dict[int, list[int]]:
    """Map {week_number: [question_indices]}."""
    wmap: dict[int, list[int]] = {w["week"]: [] for w in WEEKS}
    for i, q in enumerate(questions):
        wk = assign_question_to_week(q.get("question", ""))
        wmap[wk].append(i)
    return wmap


def resolve_course(course_id: str, content_map: dict) -> dict:
    """
    Merge seed catalog data with richer content_scraper data if available.
    Returns a combined course dict.
    """
    seed = dict(SEED_CATALOG.get(course_id, {"title": course_id, "duration_minutes": 25}))
    seed["id"] = course_id

    # Try to find matching content by title slug
    slug = re.sub(r"[^a-z0-9]+", "_", seed.get("title", "").lower()).strip("_")
    content = content_map.get(slug) or content_map.get(course_id)
    if content:
        seed["url"]         = content.get("url", "")
        seed["slide_count"] = content.get("slide_count", 0)
        # Estimate duration from slide count if not already known
        if not seed.get("duration_minutes") and seed["slide_count"]:
            seed["duration_minutes"] = max(10, seed["slide_count"] * 1)
        # Extract lesson titles from headings in slide data
        if not seed.get("lessons") and content.get("slides"):
            lesson_headings = []
            lesson_re = re.compile(r"^Lesson\s+\d+", re.IGNORECASE)
            for slide in content["slides"]:
                for h in slide.get("headings", []):
                    if lesson_re.match(h) and h not in lesson_headings:
                        lesson_headings.append(h)
            if lesson_headings:
                seed["lessons"] = lesson_headings[:10]
    return seed


# ---------------------------------------------------------------------------
# Schedule builder
# ---------------------------------------------------------------------------

def build_schedule(questions: list[dict], content_map: dict) -> dict:
    week_q_map = build_week_question_map(questions)
    schedule_weeks = []

    for wk_def in WEEKS:
        wk_num  = wk_def["week"]
        courses = [resolve_course(cid, content_map) for cid in wk_def["course_ids"]]

        content_minutes = sum(c.get("duration_minutes", 25) for c in courses)
        total_minutes   = content_minutes + RECAP_MINUTES

        q_indices = sorted(set(week_q_map.get(wk_num, [])))
        week_qs   = [questions[i] for i in q_indices if i < len(questions)]

        schedule_weeks.append({
            "week":            wk_num,
            "title":           wk_def["title"],
            "theme_desc":      wk_def["theme_desc"],
            "content_minutes": content_minutes,
            "recap_minutes":   RECAP_MINUTES,
            "total_minutes":   total_minutes,
            "courses":         courses,
            "question_indices": q_indices,
            "question_count":  len(week_qs),
        })

    return {
        "weeks":           schedule_weeks,
        "total_courses":   sum(len(w["course_ids"]) for w in WEEKS),
        "total_questions": len(questions),
    }


def save_week_quizzes(schedule: dict, questions: list[dict]) -> None:
    """Write questions_week_N.json for each week (used by quiz_generator.py)."""
    for wk in schedule["weeks"]:
        n      = wk["week"]
        qs     = [questions[i] for i in wk["question_indices"] if i < len(questions)]
        path   = os.path.join(SCRIPT_DIR, f"questions_week_{n}.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(qs, f, ensure_ascii=False, indent=2)
        print(f"  Week {n}: {len(qs):3d} questions → {os.path.basename(path)}")


def init_progress(schedule: dict) -> None:
    """Create a fresh progress.json if it does not already exist."""
    if os.path.exists(PROGRESS_FILE):
        print(f"[*] progress.json already exists – not overwriting")
        return
    progress = {
        "weeks": {
            str(w["week"]): {
                "completed_courses": [],
                "quiz_attempts":     [],
                "latest_score":      None,
                "latest_total":      w["question_count"],
                "weak_topics":       [],
            }
            for w in schedule["weeks"]
        }
    }
    with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
        json.dump(progress, f, ensure_ascii=False, indent=2)
    print(f"[+] Created: {PROGRESS_FILE}")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("[*] Loading questions …")
    questions = load_questions()
    print(f"    {len(questions)} questions")

    print("[*] Loading course content …")
    content_map = load_course_content()
    if content_map:
        print(f"    {len(content_map)} courses from course_content.json")
    else:
        print("    course_content.json not found – using seed catalog")

    print("[*] Building schedule …")
    schedule = build_schedule(questions, content_map)

    with open(SCHEDULE_FILE, "w", encoding="utf-8") as f:
        json.dump(schedule, f, ensure_ascii=False, indent=2)
    print(f"[+] Schedule saved to: {SCHEDULE_FILE}")

    print("[*] Writing per-week quiz question files …")
    save_week_quizzes(schedule, questions)

    init_progress(schedule)
    print("[*] Run schedule_generator.py to build the HTML dashboard.")
