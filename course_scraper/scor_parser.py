"""Parse Cisco SCOR exam questions and PDF exhibits for the study app."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import struct
import zlib
from collections import Counter
from pathlib import Path

from pypdf import PdfReader

ROOT = Path(__file__).resolve().parent
PDF_PATH = ROOT / "920062385-SCOR-PDF.pdf"
OUTPUT_PATH = ROOT / "netsec-pro-app" / "scor-questions.js"
REPORT_PATH = ROOT / "scor_parse_report.md"
EXHIBITS_PATH = ROOT / "netsec-pro-app" / "scor-exhibits"
HEADER = re.compile(r"(?m)^Topic\s*(\d+)\s*Question\s*#\s*(\d+)\s*$")
OPTION = re.compile(r"^([A-E])\.\s*(.*)$")
ANSWER = re.compile(r"^[A-E]{1,5}$")

DRAGDROP_TRANSCRIPTIONS = {
    29: {
        "items": [
            "Detection, blocking, tracking, analysis, and remediation to protect against targeted persistent malware attacks",
            "Superior threat prevention and mitigation for known and unknown threats",
            "Application-layer control and ability to enforce usage and tailor detection policies based on custom applications and URLs",
            "Combined integrated solution of strong defense and web protection, visibility, and controlling solutions",
        ],
        "targets": [
            "Next Generation Intrusion Prevention System",
            "Advanced Malware Protection",
            "Application control and URL filtering",
            "Cisco Web Security Appliance",
        ],
        "mapping": ["target-2", "target-1", "target-3", "target-4"],
    },
    33: {
        "items": [
            "Standard includes NAT-T",
            "Uses six packets in main mode to establish phase 1 and phase 2",
            "Uses four packets to establish phase 1 and phase 2",
            "Uses three packets in aggressive mode to establish phase 1 and phase 2",
            "Uses EAP for authenticating remote access clients",
        ],
        "targets": ["IKEv1", "IKEv2"],
        "mapping": ["target-1", "target-1", "target-2", "target-1", "target-2"],
    },
    48: {
        "items": ["DoS/DDoS", "Insecure APIs", "Data breach", "Compromised credentials"],
        "targets": [
            "A stolen customer database that contained social security numbers and was published online.",
            "A phishing site appearing to be a legitimate login page captures user login information.",
            "An application attack using botnets from multiple remote locations that flood a web application causing degraded performance or a complete outage.",
            "A malicious user gained access to an organization's database from a cloud-based API that lacked strong authentication controls.",
        ],
        "mapping": ["target-3", "target-4", "target-1", "target-2"],
    },
    89: {
        "items": [
            "Provides detection, blocking, tracking, analysis and remediation to protect against targeted persistent malware attacks",
            "Provides superior threat prevention and mitigation for known and unknown threats",
            "Provides outbreak control through custom detections",
            "Provides the root cause of a threat based on the indicators of compromise seen",
            "Provides the ability to perform network discovery",
            "Provides intrusion prevention before malware compromises the host",
        ],
        "targets": ["Cisco Firepower", "Cisco AMP"],
        "mapping": ["target-2", "target-1", "target-2", "target-2", "target-1", "target-1"],
    },
    50: {
        "items": ["Phishing", "Botnet", "Spam", "Worm"],
        "targets": [
            "A software program that copies itself from one computer to another without human interaction.",
            "Unwanted messages in an email inbox.",
            "A group of Internet-connected computers compromised by a hacker using a virus or Trojan horse.",
            "Fraudulent attempts by cyber criminals to obtain private information.",
        ],
        "mapping": ["target-4", "target-3", "target-2", "target-1"],
    },
    110: {
        "items": [
            "Privilege escalation",
            "User login suspicious behavior",
            "Interesting file access",
            "File access from a different user",
        ],
        "targets": [
            "Tetration platform learns the normal behavior of users.",
            "Tetration platform is armed to look at sensitive files.",
            "Tetration platform watches user access failures and methods.",
            "Tetration platform watches for movement in the process lineage tree.",
        ],
        "mapping": ["target-3", "target-1", "target-2", "target-4"],
    },
    123: {
        "items": ["Version 1", "Version 5", "Version 8", "Version 9"],
        "targets": [
            "Appropriate only for legacy systems.",
            "Appropriate only for the main cache.",
            "Introduced extensibility.",
            "Introduced support for aggregation caches.",
        ],
        "mapping": ["target-1", "target-2", "target-4", "target-3"],
    },
    149: {
        "items": ["PortScan Detection", "Port Sweep", "Decoy PortScan", "Distributed PortScan"],
        "targets": [
            "Many-to-one PortScan in which multiple hosts query a single host for open ports.",
            "One-to-one PortScan where an attacker mixes spoofed source IP addresses with the actual scanning IP address.",
            "One-to-many sweep: an attacker scans a single port on multiple target hosts.",
            "One-to-one PortScan against one or a few hosts to scan one or multiple ports.",
        ],
        "mapping": ["target-4", "target-3", "target-2", "target-1"],
    },
    167: {
        "items": [
            "Install monitoring extension for AWS EC2",
            "Restart the Machine Agent",
            "Update config.yaml",
            "Configure a Machine Agent or SIM Agent",
        ],
        "targets": ["Step 1", "Step 2", "Step 3", "Step 4"],
        "mapping": ["target-2", "target-4", "target-3", "target-1"],
    },
    177: {
        "items": [
            "User entity behavior assessment",
            "Cloud data protection assessment",
            "Cloud security strategy workshop",
            "Cloud security architecture assessment",
        ],
        "targets": [
            "Develop a cloud security strategy and roadmap aligned to business priorities.",
            "Identify strengths and areas for improvement in the current security architecture during onboarding.",
            "Understand the security posture of data or activity in public cloud deployments.",
            "Detect potential anomalies in user behavior that suggest malicious behavior in a SaaS application.",
        ],
        "mapping": ["target-4", "target-3", "target-1", "target-2"],
    },
    286: {
        "items": ["Cisco Stealthwatch", "Cisco ISE", "Cisco TrustSec", "Cisco Umbrella"],
        "targets": [
            "Obtains contextual identity and profiles for all users and devices connected on a network.",
            "Software-defined segmentation using SGTs to scale and enforce policies across the network.",
            "Collects and analyzes NetFlow and telemetry data for visibility into network traffic.",
            "Cloud secure Internet gateway protecting on- and off-network endpoints with DNS.",
        ],
        "mapping": ["target-3", "target-1", "target-2", "target-4"],
    },
    305: {
        "items": [
            "Validate user credentials",
            "Check device compliance with security policy",
            "Grant appropriate access with compliant device",
            "Apply updates or take other necessary action",
            "Permit just enough for the posture assessment",
        ],
        "targets": ["Step 1", "Step 2", "Step 3", "Step 4", "Step 5"],
        "mapping": ["target-1", "target-3", "target-5", "target-4", "target-2"],
    },
    337: {
        "items": ["Full Context Awareness", "NGIPS", "AMP", "Collective Security Intelligence"],
        "targets": [
            "Detection, blocking, and remediation to protect the enterprise against targeted malware attacks.",
            "Policy enforcement based on complete visibility of users and communication between virtual machines.",
            "Real-time threat intelligence and security protection.",
            "Threat prevention and mitigation for known and unknown threats.",
        ],
        "mapping": ["target-2", "target-4", "target-1", "target-3"],
    },
    394: {
        "items": ["Path traversal", "Cross-site request forgery", "SQL injection", "Buffer overflow"],
        "targets": [
            "Causes memory access errors.",
            "Makes the client the target of attack.",
            "Gives unauthorized access to web server files.",
            "Accesses or modifies application data.",
        ],
        "mapping": ["target-3", "target-2", "target-4", "target-1"],
    },
    402: {
        "items": ["Routed", "Passive", "Passive with ERSPAN", "Transparent"],
        "targets": [
            "A GRE tunnel is utilized in this solution.",
            "Allows inspection between hosts on the same subnet.",
            "Attacks are not prevented with this solution.",
            "Does not provide filtering between hosts on the same subnet.",
        ],
        "mapping": ["target-4", "target-3", "target-1", "target-2"],
    },
    407: {
        "items": ["esp-3des", "esp-aes-256", "esp-md5-hmac", "esp-sha-hmac"],
        "targets": ["Authentication", "Encryption"],
        "mapping": ["target-2", "target-2", "target-1", "target-1"],
    },
    417: {
        "items": ["Full contextual awareness", "NGIPS", "Cisco AMP for Endpoints", "Collective Security Intelligence"],
        "targets": [
            "Detection, blocking, tracking, analysis, and remediation against targeted persistent malware.",
            "Policy enforcement based on visibility of users, devices, apps, VM communication, vulnerabilities, threats, and URLs.",
            "Security and web reputation intelligence provides real-time threat intelligence and protection.",
            "Superior threat prevention and mitigation for known and unknown threats.",
        ],
        "mapping": ["target-2", "target-4", "target-1", "target-3"],
    },
    466: {
        "items": ["Guest services", "Profiling", "Posture assessment", "BYOD"],
        "targets": [
            "Requires probes to collect attributes of connected endpoints.",
            "Sponsor Portal used to gain access to network resources.",
            "My Devices portal allows users to register their devices.",
            "Results in a compliant or noncompliant status.",
        ],
        "mapping": ["target-2", "target-1", "target-4", "target-3"],
    },
    491: {
        "items": [
            "Cisco AnyConnect client",
            "ISR with CWS connector",
            "NGFW with CWS connector",
            "WSAv with CWS connector",
        ],
        "targets": [
            "Location-independent, bandwidth-efficient option.",
            "Extends identity information and on-premises features to the cloud.",
            "Provides user-group granularity and supports cloud-based scanning.",
            "Supports cached credentials and provides directory information off-premises.",
        ],
        "mapping": ["target-1", "target-2", "target-3", "target-4"],
        "needs_review": True,
        "review_reason": "One transcribed source label (NGFW) is uncertain in the exhibit image.",
    },
    509: {
        "items": ["Requires secret keys", "Requires more time", "Diffie-Hellman exchange"],
        "targets": ["Asymmetric", "Symmetric", "3DES"],
        "mapping": ["target-2", "target-3", "target-1"],
    },
    542: {
        "items": ["RSA", "AES", "SHA-1", "ISAKMP"],
        "targets": [
            "Ensures data integrity.",
            "Defines IKE SAs.",
            "Ensures data confidentiality.",
            "Provides authentication.",
        ],
        "mapping": ["target-4", "target-3", "target-1", "target-2"],
    },
    550: {
        "items": [
            "tacacs-server key",
            "aaa new-model",
            "aaa authentication ppp test group tacacs+ local",
            "tacacs-server host 10.1.1.10",
        ],
        "targets": [
            "Enable the AAA security services.",
            "Define the shared encryption password.",
            "Specify which TACACS server to use.",
            "Define the authentication method.",
        ],
        "mapping": ["target-2", "target-1", "target-4", "target-3"],
    },
    643: {
        "items": [
            "Lowers the cost of deploying in highly distributed networks",
            "Highest levels of data protection",
            "Highest levels of service availability",
            "Respond instantly to increasing traffic growth",
        ],
        "targets": ["Cloud", "Virtual"],
        "mapping": ["target-1", "target-2", "target-2", "target-1"],
    },
    671: {
        "items": [
            "Provider responsible for operating system patching",
            "Customer responsible for operating system patching",
            "Customer responsible for application patching",
            "Provider responsible for application patching",
        ],
        "targets": ["IaaS", "SaaS"],
        "mapping": ["target-2", "target-1", "target-1", "target-2"],
    },
    686: {
        "items": [
            "The device acts as a secured bridge that switches traffic from one interface to another.",
            "Firewall cannot filter packets that traverse from one host to another in the same LAN segment.",
            "Firewall requires a new network segment when inserted into a network.",
            "The firewall can optionally inspect Layer 2 traffic and filter unwanted traffic.",
        ],
        "targets": ["Routed Firewalls", "Transparent Firewalls"],
        "mapping": ["target-2", "target-1", "target-1", "target-2"],
    },
    463: {
        "items": [
            "Configure the ip flow-top-talkers command.",
            "Configure the ip flow command on an interface.",
            "Configure IP routing and enable Cisco Express Forwarding.",
            "Set the top-talkers sorting criterion.",
            "Specify the maximum number of top talkers.",
        ],
        "targets": ["Step 1", "Step 2", "Step 3", "Step 4", "Step 5"],
        "mapping": ["target-2", "target-5", "target-1", "target-4", "target-3"],
    },
}

IMAGE_OPTION_TRANSCRIPTIONS = {
    611: {
        "choices": [
            "aaa-server SERVERGROUP (external) host 4.4.4.2 key Cisco4512!",
            "aaa-server SERVERGROUP (inside) host 192.168.10.1 key Cisco4512!",
            "aaa-server SERVERGROUP (internal) host 192.168.10.10 key Cisco4512!",
        ],
        "answers": ["C"],
        "needs_review": True,
        "review_reason": "Correct option is inferred from the exhibit; verify the image-based answer key.",
    },
    612: {
        "choices": [
            "POST /dna/intent/api/v1/onboarding/pnp-device/site-claim",
            "POST /dna/intent/api/v1/onboarding/pnp-device/import",
            "GET /dna/intent/api/v1/discovery/{discovery_id}/network-device",
            "GET /dna/intent/api/v1/topology/site-topology",
            "POST /dna/intent/api/v1/discovery",
        ],
        "answers": ["A", "B"],
    },
    636: {
        "choices": [
            "Content-Type: application/json/wnd.yang-data",
            "Content-Type: application/vnd.yang-data+json",
            "Content-Type: application/vnd.yang-data",
            "Content-Type: application/vnd.yang-data+api",
        ],
        "answers": ["B"],
        "needs_review": True,
        "review_reason": "Choice text was transcribed from an image and needs verification.",
    },
    659: {
        "choices": [
            "snmp-server enable traps; snmp-server group trapgroup v3 auth; snmp-server host 10.1.1.161 traps version 3 auth trapuser",
            "snmp-server user trapuser trapgroup v3 auth sha AuthPass",
            "snmp-server user trap trapgroup v3 auth sha AuthPass",
            "snmp-server user trapuser trapgroup version 3 AuthPass",
        ],
        "answers": ["B"],
    },
    669: {
        "choices": [
            "POST /dna/intent/api/v1/discovery",
            "POST /dna/intent/api/v1/template-programmer/project/{project_id}/template",
            "GET /dna/intent/api/v1/global-pool",
            "POST /dna/intent/api/v1/template-programmer/template/version",
            "GET /dna/intent/api/v1/global-credential/{credential_id}",
        ],
        "answers": ["B", "D"],
    },
    670: {
        "choices": [
            "access-list HTTP-ONLY extended permit tcp 192.168.1.0 255.255.255.0 any",
            "access-list extended permit tcp 192.168.1.0 255.255.255.0 any eq 80",
            "access-list HTTP-ONLY extended permit tcp 192.168.1.0 255.255.255.0 any eq 80",
            "access-list permit http 192.168.1.0 255.255.255.0 any",
        ],
        "answers": ["C"],
    },
    679: {
        "choices": [
            "show cdp neighbors detail",
            "show cdp neighbors",
            "cdp neighbors detail",
            "cdp neighbors",
        ],
        "answers": ["A"],
        "needs_review": True,
        "review_reason": "Choice text was reconstructed from exhibit images and needs verification.",
    },
    687: {
        "choices": [
            "access-list 102 permit tcp 192.168.1.0 0.0.0.255 eq 53 any",
            "access-list 102 permit tcp 192.168.1.0 0.0.0.255 eq domain",
            "access-list 102 permit tcp 192.168.1.0 0.0.0.255 eq 53",
            "access-list 102 permit tcp 192.168.1.0 0.0.0.255 any eq domain",
        ],
        "answers": ["D"],
    },
}

# Image-object indexes are one-based. Most drag-and-drop pages contain the
# assignment image followed by its answer image; these pages also contain
# unrelated/preceding question images.
DRAGDROP_IMAGE_PAIRS = {
    402: (2, 3),
    550: (2, 3),
    671: (5, 6),
}
DRAGDROP_SUPPORTING_IMAGES = {
    550: (1,),
}
IMAGE_OPTION_PAGE_INDEXES = {
    670: (1, 2, 3, 4),
}

_CURRENT_PAGES = []
_PAGE_COUNT = 0


def clean_text(value: str) -> str:
    """Repair common broken ligatures found in the source PDF."""
    fixes = {
        "tra\ufffdc": "traffic", "con\ufffdguration": "configuration",
        "con\ufffdguring": "configuring", "con\ufffdgured": "configured",
        "con\ufffdgures": "configures", "con\ufffdgurations": "configurations",
        "con\ufffdgure": "configure", "\ufffdles": "files", "\ufffdle": "file",
        "certi\ufffdcates": "certificates", "certi\ufffdcate": "certificate",
        "\ufffdrewalls": "firewalls", "\ufffdrewall": "firewall",
        "bene\ufffdts": "benefits", "bene\ufffdt": "benefit",
        "\ufffdltering": "filtering", "\ufffdlters": "filters",
        "\ufffdow-export": "flow-export", "\ufffdow": "flow",
        "\ufffdooding": "flooding", "\ufffdood": "flood", "\ufffdaw": "flaw",
        "over\ufffdows": "overflows", "over\ufffdow": "overflow",
        "de\ufffdnitions": "definitions", "de\ufffdned": "defined",
        "de\ufffdnes": "defines", "de\ufffdne": "define",
        "speci\ufffded": "specified", "speci\ufffdc": "specific",
        "pro\ufffdling": "profiling", "pro\ufffdled": "profiled", "pro\ufffdle": "profile",
        "ex\ufffdltration": "exfiltration", "ex\ufffdltrate": "exfiltrate",
        "con\ufffddentiality": "confidentiality", "\ufffdexible": "flexible",
        "identi\ufffdcation": "identification", "identi\ufffdes": "identifies",
        "identi\ufffded": "identified", "spoof\ufffdng": "spoofing",
        "\ufffdrst": "first", "modi\ufffded": "modified", "\ufffdelds": "fields",
        "\ufffdagged": "flagged", "uni\ufffded": "unified", "noti\ufffdcation": "notification",
        "work\ufffdow": "workflow", "\ufffdnd": "find", "di\ufffdculty": "difficulty",
        "o\ufffdce": "office", "buffer over\ufffdows": "buffer overflows",
    }
    for source, replacement in fixes.items():
        value = value.replace(source, replacement)
        value = value.replace(source.capitalize(), replacement.capitalize())
    value = re.sub(r"\bC1\$c0445915422!", "[example password]", value, flags=re.IGNORECASE)
    return re.sub(r"\s+", " ", value.replace("\ufffd", " ")).strip()


def _png_chunk(kind: bytes, data: bytes) -> bytes:
    return (struct.pack("!I", len(data)) + kind + data
            + struct.pack("!I", zlib.crc32(kind + data) & 0xFFFFFFFF))


def _image_png(obj) -> bytes | None:
    width, height = int(obj.get("/Width", 0)), int(obj.get("/Height", 0))
    channels = {"/DeviceRGB": 3, "/DeviceGray": 1}.get(str(obj.get("/ColorSpace")))
    if not width or not height or channels is None or int(obj.get("/BitsPerComponent", 8)) != 8:
        return None
    pixels = obj.get_data()
    if len(pixels) != width * height * channels:
        return None
    color_type = 2 if channels == 3 else 0
    rows = b"".join(
        b"\0" + pixels[y * width * channels:(y + 1) * width * channels]
        for y in range(height)
    )
    return (b"\x89PNG\r\n\x1a\n"
            + _png_chunk(b"IHDR", struct.pack("!IIBBBBB", width, height, 8, color_type, 0, 0, 0))
            + _png_chunk(b"IDAT", zlib.compress(rows))
            + _png_chunk(b"IEND", b""))


def _page_images(page, page_number: int) -> list[str]:
    """Extract supported PDF images, returning app-relative paths."""
    resources = page.get("/Resources")
    if not resources:
        return []
    xobjects = resources.get_object().get("/XObject")
    if not xobjects:
        return []
    EXHIBITS_PATH.mkdir(parents=True, exist_ok=True)
    paths = []
    for index, (_, reference) in enumerate(xobjects.get_object().items(), start=1):
        image = reference.get_object()
        if image.get("/Subtype") != "/Image":
            continue
        png = _image_png(image)
        if png is None:
            continue
        name = f"page-{page_number + 1:03d}-{index:02d}.png"
        (EXHIBITS_PATH / name).write_bytes(png)
        paths.append(f"./scor-exhibits/{name}")
    return paths


def _parse_block(topic: str, number: int, block: str, page_number: int) -> dict:
    lines = [line.strip() for line in block.splitlines()]
    question_lines = []
    choices = []
    answer_code = ""
    explanation_lines = []
    current_choice = None
    after_answer = False
    collecting_explanation = False

    for line in lines:
        if not line:
            continue
        if re.match(r"^(Community vote distribution|350-701 Exam)", line, re.I):
            break
        if line.lower().startswith("explanation:"):
            after_answer = True
            collecting_explanation = True
            explanation_lines.append(line.split(":", 1)[1].strip())
            continue
        if line.lower().startswith("reference:"):
            after_answer = True
            collecting_explanation = False
            continue
        if after_answer:
            if collecting_explanation:
                explanation_lines.append(line)
            continue
        if line.upper().startswith("DRAG DROP"):
            continue
        if line.lower().startswith(("drag and drop", "select and place")):
            question_lines.append(line)
            continue
        match = OPTION.match(line)
        if match:
            current_choice = {"id": match.group(1), "text": match.group(2).strip()}
            choices.append(current_choice)
            continue
        if choices and ANSWER.fullmatch(line):
            answer_code = line
            after_answer = True
            continue
        if choices and current_choice:
            current_choice["text"] = (current_choice["text"] + " " + line).strip()
        elif not choices and line != "Select and Place:":
            question_lines.append(line)

    question = clean_text(" ".join(question_lines))
    choices = [{"id": c["id"], "text": clean_text(c["text"])} for c in choices]
    answers = [letter for letter in dict.fromkeys(answer_code)
               if any(c["id"] == letter for c in choices)]
    dragdrop = not choices and ("DRAG DROP" in block.upper() or "DRAG AND DROP" in block.upper())
    has_exhibit = "refer to the exhibit" in question.lower()
    page_images = _page_images(_CURRENT_PAGES[page_number], page_number) if (
        dragdrop or has_exhibit or any(not choice["text"] for choice in choices)
    ) else []
    exhibit_paths = page_images

    record = {
        "id": f"scor-{number:03d}",
        "topic": f"Topic {topic}",
        "question": question,
        "type": "dragdrop" if dragdrop else ("multiple" if len(answers) > 1 else "single"),
        "choices": choices,
        "correct_answers": answers,
        "explanation": clean_text(" ".join(explanation_lines)),
        "items": [],
        "targets": [],
        "mapping": {},
        "exhibits": exhibit_paths,
        "assignment_image": None,
        "answer_image": None,
        "needs_review": False,
        "source_question": number,
    }
    if dragdrop:
        assignment_index, answer_index = DRAGDROP_IMAGE_PAIRS.get(number, (1, 2))
        if len(page_images) >= answer_index:
            record["assignment_image"] = page_images[assignment_index - 1]
            record["answer_image"] = page_images[answer_index - 1]
            record["exhibits"] = [
                page_images[index - 1]
                for index in DRAGDROP_SUPPORTING_IMAGES.get(number, ())
                if index <= len(page_images)
            ]
        else:
            record["needs_review"] = True
            record["review_reason"] = "Could not find both drag-and-drop assignment and answer images."
    elif number in IMAGE_OPTION_PAGE_INDEXES:
        record["exhibits"] = [
            page_images[index - 1]
            for index in IMAGE_OPTION_PAGE_INDEXES[number]
            if index <= len(page_images)
        ]
    image_options = IMAGE_OPTION_TRANSCRIPTIONS.get(number)
    if image_options:
        record["choices"] = [
            {"id": chr(65 + index), "text": text}
            for index, text in enumerate(image_options["choices"])
        ]
        record["correct_answers"] = image_options["answers"]
        record["type"] = "multiple" if len(record["correct_answers"]) > 1 else "single"
        record["needs_review"] = image_options.get("needs_review", False)
        if record["needs_review"]:
            record["review_reason"] = image_options["review_reason"]
    if dragdrop:
        transcription = DRAGDROP_TRANSCRIPTIONS.get(number)
        if transcription:
            record["items"] = [
                {"id": f"item-{index}", "text": text}
                for index, text in enumerate(transcription["items"], start=1)
            ]
            record["targets"] = [
                {"id": f"target-{index}", "text": text}
                for index, text in enumerate(transcription["targets"], start=1)
            ]
            record["mapping"] = {
                item["id"]: target_id
                for item, target_id in zip(record["items"], transcription["mapping"])
            }
            record["needs_review"] = transcription.get("needs_review", False)
            if record["needs_review"]:
                record["review_reason"] = transcription.get("review_reason", "Manual transcription needs verification.")
        else:
            record["needs_review"] = True
            record["review_reason"] = "Drag-and-drop labels or mapping are not fully available as selectable PDF text."
    elif (not question or not record["choices"] or not record["correct_answers"]
          or any(not choice["text"] for choice in record["choices"])):
        record["needs_review"] = True
        record["review_reason"] = "Question, choices, or correct answer could not be extracted with confidence."
    if has_exhibit and not exhibit_paths:
        record["needs_review"] = True
        record["review_reason"] = "The question refers to an exhibit, but no extractable image was found on its PDF page."
    return record


def parse_pdf(path: Path = PDF_PATH) -> list[dict]:
    global _CURRENT_PAGES, _PAGE_COUNT
    reader = PdfReader(str(path))
    _CURRENT_PAGES = reader.pages
    _PAGE_COUNT = len(reader.pages)
    if EXHIBITS_PATH.exists():
        shutil.rmtree(EXHIBITS_PATH)
    page_texts = [page.extract_text() or "" for page in reader.pages]
    starts = []
    for page_number, text in enumerate(page_texts):
        starts.extend((page_number, match.start(), match.group(1), match.group(2), match.end())
                      for match in HEADER.finditer(text))

    questions = []
    for index, (page_number, offset, topic, number, header_end) in enumerate(starts):
        next_page, next_offset = starts[index + 1][:2] if index + 1 < len(starts) else (len(page_texts), 0)
        block = page_texts[page_number][header_end:]
        if next_page == page_number:
            block = block[:next_offset - header_end]
        else:
            block += "\n" + "\n".join(page_texts[page_number + 1:next_page])
            if next_page < len(page_texts):
                block += "\n" + page_texts[next_page][:next_offset]
        questions.append(_parse_block(topic, int(number), block, page_number))
    return questions


def write_outputs(questions: list[dict], output: Path = OUTPUT_PATH, report: Path = REPORT_PATH) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        "/* Generated by course_scraper/scor_parser.py. Do not edit by hand. */\n"
        "window.SCOR_QUESTIONS = " + json.dumps(questions, ensure_ascii=False, indent=2) + ";\n",
        encoding="utf-8",
    )
    counts = Counter(question["type"] for question in questions)
    review = [question for question in questions if question["needs_review"]]
    mapped = sum(question["type"] == "dragdrop" and bool(question["mapping"]) for question in questions)
    paired_images = sum(
        bool(question["type"] == "dragdrop"
             and question["assignment_image"]
             and question["answer_image"])
        for question in questions
    )
    report.write_text(
        "# SCOR PDF parse report\n\n"
        f"- PDF pages: {_PAGE_COUNT}\n- Questions parsed: {len(questions)}\n"
        f"- Single choice: {counts['single']}\n- Multiple choice: {counts['multiple']}\n"
        f"- Drag and drop: {counts['dragdrop']} ({mapped} with transcribed mappings; "
        f"{paired_images} with separate assignment and answer images)\n"
        f"- Questions needing review: {len(review)}\n\n"
        "## Questions needing review\n\n"
        + ("\n".join(f"- Q{q['source_question']}: {q.get('review_reason', 'Needs manual verification.')}"
                     for q in review) if review else "- None.")
        + "\n",
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pdf", nargs="?", type=Path, default=PDF_PATH)
    parser.add_argument("--output", type=Path, default=OUTPUT_PATH)
    parser.add_argument("--report", type=Path, default=REPORT_PATH)
    args = parser.parse_args()
    questions = parse_pdf(args.pdf)
    write_outputs(questions, args.output, args.report)
    print(f"Parsed {len(questions)} questions → {args.output}")
    print(f"Report written to {args.report}")


if __name__ == "__main__":
    main()
