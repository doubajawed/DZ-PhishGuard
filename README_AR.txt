DZ-PhishGuard — نسخة رابط الموقع للحكام
========================================

هذه النسخة مختلفة عن ملف BAT المحلي: بعد نشرها تحصل على رابط موقع يفتح مباشرة في المتصفح.

الملفات الخمسة المطلوبة للنشر:
- streamlit_app.py
- core_engine.py
- requirements.txt
- dz_phishguard.joblib
- evaluation.json

ويوجد أيضًا DZ-PhishGuard_Full_Source.zip ويحتوي المشروع الكامل وبياناته ودفتر التدريب والتوثيق.

الخطوة 1 — إنشاء GitHub repository
1. افتح https://github.com/new
2. Repository name: DZ-PhishGuard
3. اجعل Public.
4. اضغط Create repository.

الخطوة 2 — ارفع ملفات الموقع
1. داخل المستودع اختر Add file ثم Upload files.
2. فك ضغط DZ-PhishGuard_Website_Deploy.zip على جهازك أولًا.
3. اسحب الملفات الخمسة المذكورة أعلاه وملف DZ-PhishGuard_Full_Source.zip إلى صفحة الرفع.
   (لا ترفع README_AR.txt إذا لا ترغب أن يكون هو الصفحة الرئيسية؛ يمكن رفعه كدليل عربي إضافي.)
4. اضغط Commit changes.

الخطوة 3 — الحصول على رابط الموقع
1. افتح https://share.streamlit.io/
2. سجّل الدخول باستخدام GitHub ووافق على الربط.
3. اختر Create app ثم Yup, I have an app.
4. اختر المستودع DZ-PhishGuard والفرع main.
5. Main file path: streamlit_app.py
6. اضغط Deploy.
7. بعد اكتمال البناء، انسخ رابط الموقع الذي ينتهي بـ streamlit.app.

ملاحظات مهمة:
- قد يستغرق أول بناء بعض الوقت بسبب تنزيل المكتبات.
- إذا ظهر Build failed، افتح Manage app ثم Logs وانسخ رسالة الخطأ الأخيرة لمراجعتها.
- اجعل المستودع Public حتى يستطيع الحكام رؤية الكود.
- النسخة العامة تعالج النص على خادم الاستضافة؛ استخدم الأمثلة الاصطناعية فقط ولا تدخل رسائل حقيقية أو بيانات شخصية أو OTP أو PIN أو CVV.
- لا تقدّم نتائج الاختبار الاصطناعي على أنها دقة ميدانية.

المصدر الرسمي للنشر:
https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy
