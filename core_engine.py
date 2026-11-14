"""Shared inference engine for DZ-PhishGuard. No network calls are made here."""
from __future__ import annotations
import json
import re
import unicodedata
from pathlib import Path
import joblib

ROOT = Path(__file__).resolve().parent
MODEL_PATH = ROOT / "dz_phishguard.joblib"
METRICS_PATH = ROOT / "evaluation.json"

if not MODEL_PATH.exists():
    raise FileNotFoundError("ملف النموذج غير موجود: models/dz_phishguard.joblib")

BUNDLE = joblib.load(MODEL_PATH)
MODEL = BUNDLE["pipeline"]
THRESHOLD = float(BUNDLE.get("threshold", 0.5))
try:
    METRICS = json.loads(METRICS_PATH.read_text(encoding="utf-8"))
except (OSError, json.JSONDecodeError):
    METRICS = {}

ARABIC_NORMALIZE = str.maketrans({"أ":"ا", "إ":"ا", "آ":"ا", "ٱ":"ا", "ى":"ي", "ة":"ة", "ؤ":"و", "ئ":"ي", "ـ":""})

def normalize(text: str) -> str:
    text = unicodedata.normalize("NFKC", str(text)).translate(ARABIC_NORMALIZE)
    text = re.sub(r"[\u064b-\u065f\u0670]", "", text)
    return text.lower()

PATTERNS = {
    "secret": re.compile(r"(otp|one.?time|cvv2?|cvc|pin|رمز\s*(التحقق|التاكيد|sms|السري)?|كود\s*(التحقق|sms)?|code\s*(de|sms|secret)?|mot de passe|password|كلمه السر|الرقم السري|رقم البطاقه|بيانات البطاقه|معلومات البطاقه|معلوماتك|بياناتك|معلوماتك البنكيه|بياناتك البنكيه|banking details|card details|account details|bank details|informations bancaires|coordonnees bancaires)", re.I),
    "request": re.compile(r"(ارسل|ترسل|ابعث|شارك|اعطني|اعطيني|صيفط|sifet|envoyez|envoyer|communiquez|send|share|reply with|reponds|répondez|اكتب|ادخل|اكد|أكد|تأكيد|حدث|تحديث|verify|confirm|update|validez|confirmez|vérifiez|saisissez|enter|provide)", re.I),
    "urgency": re.compile(r"(عاجل|فورا|فوراً|بسرعه|بسرعة|الان|الآن|خلال\s*\d+|اليوم|ساعة|دقيقه|دقيقة|immediatement|immédiatement|urgent|urgente|maintenant|vite|immediately|within\s*\d+|final warning|dernier avertissement|last warning|expire dans)", re.I),
    "impersonation": re.compile(r"(بريد الجزا(?:ئر|ير)|الجزائر بوست|alg[eé]rie\s*poste|baridi\s*mob|baridimob|edahabia|الذهبيه|البطاقة الذهبية|ccp|البنك|banque|bank|service client|خدمه الزبائن|الدعم التقني|support technique|security team|anti.?fraude)", re.I),
    "money": re.compile(r"(ادفع|دفع|رسوم|تحويل|حول|حوّل|مبلغ|دراهم|دج|da\b|paiement|payer|payez|frais|remboursement|virement|transfer|payment|fee|refund|claim your reward)", re.I),
    "threat": re.compile(r"(سيتم غلق|راح يتغلق|سيتم ايقاف|سيتم تعليق|حظر|تجميد|suspendu|bloque|bloqué|ferme|closed|disabled|lose access|permanently|عداله|العداله|justice|legal action)", re.I),
}
URL_RE = re.compile(r"(https?://\S+|www\.\S+|\b[a-z0-9][a-z0-9-]{1,}\.(?:com|net|org|info|site|xyz|top|example|online|click|app|dz)(?:/\S*)?)", re.I)
SAFE_NEGATION = re.compile(r"(لا\s*(تشارك|ترسل|تعطي|تعط|تبعث)|never\s+share|do not share|don.t share|ne communiquez jamais|ne partagez pas|لا تشارك)", re.I)

def analyze_indicators(message: str) -> dict:
    t = normalize(message)
    has_secret = bool(PATTERNS["secret"].search(t))
    asks_for_secret = has_secret and bool(PATTERNS["request"].search(t)) and not bool(SAFE_NEGATION.search(t))
    has_url = bool(URL_RE.search(t))
    impersonation = bool(PATTERNS["impersonation"].search(t))
    urgency = bool(PATTERNS["urgency"].search(t))
    money = bool(PATTERNS["money"].search(t))
    threat = bool(PATTERNS["threat"].search(t))
    points, items = 0, []
    if asks_for_secret:
        points += 40; items.append(("طلب بيانات حساسة أو رمز تحقق", "لا تشارك OTP أو PIN أو CVV أو بيانات البطاقة والحساب مع أي شخص."))
    if has_url:
        points += 25; items.append(("وجود رابط داخل الرسالة", "لا تفتحه من الرسالة؛ افتح التطبيق الرسمي بنفسك."))
    if impersonation:
        points += 15; items.append(("انتحال أو ذكر جهة مالية موثوقة", "ذكر اسم مؤسسة لا يثبت أن الرسالة صادرة عنها."))
    if urgency:
        points += 10; items.append(("ضغط زمني أو استعجال", "الاستعجال المصطنع قد يدفع المستخدم للتصرف دون تحقق."))
    if money:
        points += 10; items.append(("طلب دفع أو تحويل أو رسوم", "تحقق من أي طلب مالي عبر قناة مستقلة."))
    if threat:
        points += 10; items.append(("تهديد بإيقاف الحساب أو فقدان الوصول", "لا تستخدم رابط الرسالة لمعالجة التهديد."))
    points = min(100, points)
    level = "مرتفع" if points >= 65 else ("متوسط" if points >= 30 else "منخفض")
    return {"score": points, "level": level, "items": items, "asks_for_secret": asks_for_secret, "has_url": has_url}

def analyze_message(message: str) -> dict:
    message = (message or "").strip()
    if len(message) < 4:
        raise ValueError("أدخل نصًا أطول من 3 أحرف للتحليل.")
    probability = float(MODEL.predict_proba([message])[0][1])
    prediction = int(probability >= THRESHOLD)
    indicators = analyze_indicators(message)
    return {"prediction": prediction, "model_score": probability, "indicators": indicators}
