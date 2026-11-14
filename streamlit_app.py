from __future__ import annotations
import streamlit as st
from core_engine import analyze_message, METRICS

st.set_page_config(page_title="DZ-PhishGuard | الدرع الذكي", page_icon="🛡️", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800&display=swap');
html, body, [class*="css"] {font-family:'Cairo',sans-serif;}
.stApp {background: radial-gradient(circle at 12% 0%, #153452 0%, #081321 42%, #050c16 100%); color:#edf5ff;}
.block-container {max-width:1180px; padding-top:2rem; padding-bottom:3rem;}
.hero {background:linear-gradient(120deg,#15334f,#0e1c30);border:1px solid #2a4662;border-radius:24px;padding:28px 32px;margin-bottom:20px;}
.kicker {color:#43ddc5;font-size:12px;font-weight:800;letter-spacing:2px;}
.hero h1 {font-size:42px;margin:8px 0;color:#f2f8ff;font-weight:800;}
.hero p {color:#bdd0e4;line-height:1.9;margin:0;}
.card {background:#102038;border:1px solid #2a4662;border-radius:18px;padding:20px;margin:12px 0;}
.verdict {font-size:22px;font-weight:800;margin-bottom:8px;}
.good {color:#53dfc6}.bad {color:#ff8995}.muted {color:#a9bdd2;font-size:13px;line-height:1.8;}
.signal {background:#132b45;border:1px solid #294764;border-radius:12px;padding:12px;margin:8px 0;}
.signal b {color:#f2f8ff}.signal span {display:block;color:#adc2d6;font-size:12px;margin-top:4px;}
.warning {background:#153139;border-left:4px solid #43ddc5;border-radius:8px;padding:14px;color:#d9f3ef;margin-top:16px;}
.small {font-size:11px;color:#8fa7bf;line-height:1.8;}
div.stButton > button {border-radius:12px;border:1px solid #365673;background:#17324e;color:#f1f7ff;font-weight:700;}
div.stButton > button[kind="primary"] {background:linear-gradient(100deg,#1aa28e,#43ddc5);color:#06131c;border:0;}
textarea {direction:rtl;text-align:right;}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero" dir="rtl">
 <div class="kicker">ALGERIA · CYBER SAFETY · AI RESEARCH PROTOTYPE</div>
 <h1>DZ-PhishGuard 🛡️</h1>
 <p>الدرع الذكي ضد التصيّد والاحتيال المالي. يحلل الرسائل العربية والدارجة والفرنسية والإنجليزية، ويشرح مؤشرات الهندسة الاجتماعية بدل الاكتفاء بوسم مبهم.</p>
</div>
""", unsafe_allow_html=True)

with st.expander("قبل أن تبدأ — تنبيه الخصوصية", expanded=True):
    st.warning("هذه نسخة عرض مستضافة. النص الذي تدخله يُعالج على خادم الاستضافة، لذلك استخدم الأمثلة التجريبية فقط ولا تلصق رسائل شخصية أو أرقام بطاقات أو كلمات مرور أو رموز OTP. في النسخة المحلية يبقى التحليل على جهازك.")

samples = {
    "رسالة تصيّد بالعربية": "بريد الجزائر: حسابك موقوف مؤقتا. أكد معلوماتك عبر الرابط ap-update.example خلال 30 دقيقة لتجنب الغلق.",
    "إشعار تحويل سليم": "تم استلام تحويل بقيمة 3000 دج في حسابك. يمكنك مراجعة الرصيد من التطبيق الرسمي.",
    "رسالة احتيال بالفرنسية": "Votre compte bancaire sera bloqué. Envoyez le code reçu par SMS pour annuler la suspension sur banque-verif.example.",
    "رسالة دارجة مشبوهة": "BaridiMob ta3ek rah yetbloqua اليوم، ابعثلي code SMS باش نأكدلك الحساب.",
}

if "message_input" not in st.session_state:
    st.session_state.message_input = ""

left, right = st.columns([1.08, 0.92], gap="large")
with left:
    st.markdown("### افحص رسالة مشبوهة")
    st.caption("الصق نص الرسالة فقط. لا تضف معلومات شخصية أو بيانات مالية.")
    sample_choice = st.selectbox("اختر مثالًا تجريبيًا", ["— اختر مثالًا —", *samples.keys()])
    if st.button("إدراج المثال المختار", use_container_width=True):
        if sample_choice in samples:
            st.session_state.message_input = samples[sample_choice]
    message = st.text_area("نص الرسالة", key="message_input", height=190, placeholder="اكتب أو الصق رسالة تجريبية هنا...")
    analyze_clicked = st.button("حلّل الرسالة الآن", type="primary", use_container_width=True)

with right:
    st.markdown("### نتيجة التحليل")
    if analyze_clicked:
        try:
            result = analyze_message(message)
            pred = result["prediction"]
            prob = result["model_score"]
            sig = result["indicators"]
            if pred:
                st.markdown('<div class="card"><div class="verdict bad">⚠️ رسالة مشبوهة محتملة</div><div class="muted">النموذج وجد أنماطًا أقرب إلى أمثلة الاحتيال في بيانات التدريب. هذا ليس حكمًا مؤكدًا.</div></div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="card"><div class="verdict good">؟ لم يُكتشف نمط احتيال واضح</div><div class="muted">هذا لا يثبت أن الرسالة آمنة؛ قد تكون محاولة جديدة غير ممثلة في بيانات التدريب.</div></div>', unsafe_allow_html=True)
            st.metric("مؤشر النموذج للاحتيال · ليس احتمالًا مضمونًا", f"{prob*100:.1f}%")
            st.progress(max(0.0, min(1.0, prob)))
            st.metric("إشارات الخطر المستقلة", f"{sig['score']}/100 · {sig['level']}")
            st.markdown("**لماذا ظهرت هذه النتيجة؟**")
            if sig["items"]:
                for title, detail in sig["items"]:
                    st.markdown(f'<div class="signal"><b>{title}</b><span>{detail}</span></div>', unsafe_allow_html=True)
            else:
                st.info("لم تُلتقط إشارات واضحة من قواعد الفحص. افحص هوية المرسل والسياق يدويًا.")
            st.markdown('<div class="warning"><b>الإجراء الآمن الآن</b><br>لا تفتح الرابط ولا ترسل OTP أو PIN أو CVV. افتح التطبيق الرسمي بنفسك أو اتصل بالجهة عبر رقم موثوق تعرفه مسبقًا.</div>', unsafe_allow_html=True)
        except ValueError as exc:
            st.info(str(exc))
    else:
        st.markdown('<div class="card muted">أدخل رسالة تجريبية ثم اضغط «حلّل الرسالة الآن». ستظهر النتيجة وأسباب الاشتباه هنا.</div>', unsafe_allow_html=True)

st.divider()
st.markdown("## نتائج الاختبار التجريبي")
model = METRICS.get("model", {})
baseline = METRICS.get("baseline", {})
cols = st.columns(4)
cols[0].metric("رسائل الاختبار", METRICS.get("test_rows", "—"))
cols[1].metric("دقة النموذج", f"{model.get('accuracy',0)*100:.1f}%" if model else "—")
cols[2].metric("Scam F1", f"{model.get('f1_scam',0)*100:.1f}%" if model else "—")
cols[3].metric("دقة خط الأساس", f"{baseline.get('accuracy',0)*100:.1f}%" if baseline else "—")
if model:
    st.write(f"Precision للاحتيال: **{model.get('precision_scam',0)*100:.1f}%** · Recall للاحتيال: **{model.get('recall_scam',0)*100:.1f}%**")
    cm = METRICS.get("confusion_matrix", [[0,0],[0,0]])
    st.caption(f"مصفوفة الالتباس (الحقيقة × التنبؤ؛ سليم ثم احتيال): {cm}. فوّت النموذج {cm[1][0]} حالات احتيال وأطلق {cm[0][1]} إنذارات خاطئة في الاختبار.")

st.markdown("## كيف يعمل؟")
cols = st.columns(4)
for col, title, body in zip(cols,
    ["نموذج تعلّم آلي", "سياق جزائري", "تفسير الإشارات", "الخصوصية"],
    ["TF-IDF للكلمات والمحارف مع Logistic Regression.", "أمثلة عربية ودارجة وفرنسية مرتبطة بخدمات مالية محلية.", "يفحص طلب الأسرار والروابط والاستعجال والانتحال والضغط المالي.", "هذه النسخة العامة تعالج النص على خادم الاستضافة؛ لا تدخل بيانات حقيقية."]):
    with col:
        st.markdown(f'<div class="card"><b>{title}</b><p class="muted">{body}</p></div>', unsafe_allow_html=True)

st.markdown('<p class="small">تنبيه: هذا نموذج طلابي تجريبي على مجموعة اصطناعية صغيرة، وليس نظامًا مصرفيًا أو جهة رسمية ولا يثبت أن الرسالة احتيالية أو آمنة. قد يخطئ. This project is a prototype and is not financial advice.</p>', unsafe_allow_html=True)
