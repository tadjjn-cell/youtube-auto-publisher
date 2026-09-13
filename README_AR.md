# دليل الإعداد — YouTube Auto Publisher (نشر تلقائي على يوتيوب عبر تيليجرام)

> صافط الفيديو ديالك لـ Telegram مع caption قصيرة (الموضوع)، والبوت كيدير الباقي: بحث عن الكلمات المفتاحية، كتابة Title + Description + Hashtags بالذكاء الاصطناعي، ورفع الفيديو على يوتيوب تلقائياً. كلشي **مجاني 100%**، وكيخدم على GitHub Actions بلا ما يبقى الـ PC ديالك مشعل.

---

## كيفاش كيخدم؟

```
أنت (تيليجرام: Saved Messages) --caption + video-->
   GitHub Actions (كل 20 دقيقة) يشوف رسائل جداد
     -> كيدوّنلود الفيديو (Telethon)
     -> كيدير Keyword Research (YouTube Suggest API — مجاني، بلا مفتاح)
     -> كيولد Title/Description/Hashtags (Groq AI — نفس المفتاح اللي عندك فـ Pinterest Agent)
     -> كيرفع الفيديو على يوتيوب (YouTube Data API)
     -> كيصيفط ليك تأكيد فـ تيليجرام: "✅ تم النشر + الرابط"
```

كلشي كيخدم على سيرفرات GitHub المجانية — الـ PC ديالك خاصو يخدم غير مرة وحدة باش دير الإعداد الأولي (one-time setup).

---

## قبل ما تبدا: شنو خاصك؟

| المتطلب | من فين | مجاني؟ |
|---|---|---|
| حساب GitHub | [github.com](https://github.com) | نعم |
| Telegram API ID/Hash | [my.telegram.org](https://my.telegram.org) | نعم |
| مفتاح Groq API | [console.groq.com](https://console.groq.com) — نفس المفتاح اللي عندك فـ Pinterest Agent يخدم هنا | نعم |
| Google Cloud project + YouTube Data API | [console.cloud.google.com](https://console.cloud.google.com) | نعم (حصة/quota مجانية) |
| Python 3.11+ على PC ديالك (غير للإعداد الأولي) | [python.org](https://www.python.org/downloads/) | نعم |

---

## الخطوة 1: جيب Telegram API ID/Hash + Session

1. دخل [my.telegram.org](https://my.telegram.org) بنمرة التيليفون ديالك.
2. دوز على **"API Development Tools"**، عمر الفورم (اسم الأبليكاسيون: أي حاجة، مثلا "YT Publisher").
3. غادي يعطيك **`api_id`** و **`api_hash`** — احتافظ بيهم.
4. حل CMD/PowerShell فـ فولدر المشروع، ودير:

```bash
pip install -r setup/requirements.txt
python setup/get_telegram_session.py
```

5. غادي يطلب منك الـ API_ID و API_HASH (اللي جبتيهم فوق)، من بعد نمرة التيليفون وكود التأكيد اللي غادي يجيك فـ تيليجرام.
6. فالأخير غادي يطبع ليك **session string** طويلة — نسخها وحتافظ بيها مزيان (هي بحال password ديال الحساب ديالك).

> ⚠️ لا تشارك session string مع حتى واحد — كيعطي accès كامل للحساب ديالك.

---

## الخطوة 2: جيب مفتاح Groq (إلا ما عندكش)

إلا كنت ديجا خدام بـ Pinterest_Growth_Agent، عندك ديجا `GROQ_API_KEY` — نفسو يخدم هنا، ماشي خاصك وحد جديد.

إلا ماعندكش: [console.groq.com](https://console.groq.com) → API Keys → Create API Key.

---

## الخطوة 3: Google Cloud — فعّل YouTube Data API

1. دخل [console.cloud.google.com](https://console.cloud.google.com), دير **New Project**.
2. من "APIs & Services" > "Library" قلب على **"YouTube Data API v3"** وضغط **Enable**.
3. دوز لـ "APIs & Services" > **"OAuth consent screen"**:
   - User Type: **External**
   - عمر المعلومات المطلوبة (اسم الأبليكاسيون، إيميلك)
   - فـ "Test users" زيد الإيميل ديال Google اللي فيه شانو ديال يوتيوب
4. دوز لـ "APIs & Services" > **"Credentials"** > **Create Credentials** > **OAuth client ID**:
   - Application type: **Desktop app**
   - حمّل ملف JSON (زر التحميل)، سميه `client_secret.json`، وحطو فـ فولدر `setup/`.

### ⚠️ ملاحظة مهمة بزاف — Verification

طالما الأبليكاسيون فـ وضعية **"Testing"** (ماشي "In production")، الـ refresh token غادي يخدم غير **7 أيام** ومن بعد خاصك تعاود الخطوة 4 باش تجدد. باش يخدم للأبد بلا توقف:
- دوز لـ "OAuth consent screen" وضغط **"Publish App"** (نشر الأبليكاسيون).
- بحال الـ scope ديالنا (`youtube.upload`) هو "Sensitive" ماشي "Restricted"، فـ أغلب الأحيان Google كيسمح بالنشر بلا "verification review" طويلة إلا كان الاستعمال شخصي بعدد قليل ديال users — غادي تشوف تحذير "unverified app" مرة وحدة كتدوز عليه فالخطوة الجاية، عادي.

---

## الخطوة 4: جيب YouTube Refresh Token

```bash
pip install -r setup/requirements.txt
python setup/get_youtube_token.py
```

غادي يحل المتصفح، دخل بحساب Google ديال شانو يوتيوب، عطي الصلاحية. من بعد غادي يطبع ليك فـ terminal:

```
YOUTUBE_CLIENT_ID=...
YOUTUBE_CLIENT_SECRET=...
YOUTUBE_REFRESH_TOKEN=...
```

احتافظ بيهم.

---

## الخطوة 5: دير المشروع GitHub Repo

```bash
git init
git add .
git commit -m "Initial commit: YouTube Auto Publisher"
```

من بعد دير repo جديد فـ GitHub (private أحسن)، وربطو:

```bash
git remote add origin https://github.com/<username>/<repo-name>.git
git branch -M main
git push -u origin main
```

### فعّل الصلاحية ديال الكتابة (مهم!)

فـ GitHub repo: **Settings** > **Actions** > **General** > **Workflow permissions** → اختار **"Read and write permissions"** → Save.

(هادشي خاص باش الـ workflow يقدر يحفظ `data/state.json` بعد كل run، باش ما يعاودش يرفع نفس الفيديو مرتين.)

---

## الخطوة 6: زيد Secrets فـ GitHub

فـ repo: **Settings** > **Secrets and variables** > **Actions** > **New repository secret** — زيد وحدة وحدة:

| Secret name | القيمة |
|---|---|
| `GROQ_API_KEY` | مفتاح Groq |
| `TELEGRAM_API_ID` | من الخطوة 1 |
| `TELEGRAM_API_HASH` | من الخطوة 1 |
| `TELEGRAM_SESSION` | session string من الخطوة 1 |
| `TELEGRAM_SOURCE_CHAT` | `me` (Saved Messages) — أو `@channel_username` |
| `YOUTUBE_CLIENT_ID` | من الخطوة 4 |
| `YOUTUBE_CLIENT_SECRET` | من الخطوة 4 |
| `YOUTUBE_REFRESH_TOKEN` | من الخطوة 4 |

---

## الخطوة 7: جرب

فـ GitHub repo: **Actions** tab > **YouTube Auto Publisher** > **Run workflow** (زر أزرق على اليمين) — هادي test يدوي بلا ما تستنى الجدول الزمني.

صيفط فيديو + caption قصيرة (مثلا: "recette كسكس بالخضرة") لـ **Saved Messages** ديالك فـ Telegram، من بعد شغل الـ workflow يدوياً باش تشوف واش خدام.

إلا خدام مزيان: غادي توصلك رسالة فـ Telegram "✅ Uploaded" مع رابط الفيديو، من بعد يمشي وحدو كل 20 دقيقة (`*/20 * * * *` فـ `.github/workflows/publish.yml`).

---

## الاستعمال اليومي

غير صافط فيديو + caption قصيرة (الموضوع، بحال "workout للمبتدئين") لـ Saved Messages، وستنى ~20 دقيقة. رد بلاصتك تشوف Telegram للتأكيد.

---

## حدود مهمة (Limits)

- **YouTube API quota**: مجانية 10,000 units/يوم، رفع فيديو وحد = 1600 unit → **~6 فيديوهات فـ اليوم** ماكسيموم (مجاني). إلا بغيتي أكثر، خاصك تطلب "quota increase" من Google (مجاني بصح كيتطلب وقت).
- `max_uploads_per_run: 2` فـ `config.yaml` — كيحدد شحال فيديو يرفع فـ كل run باش ميتفاجاش quota.
- الفيديوهات اللي فشلات (error فـ الرفع) كيتصيفط ليك تنبيه فـ Telegram، ولكن ماكيتعاودوش يتحاولو أوتوماتيكياً — عاود صافط الفيديو إلا بغيتي تعاود تجرب.

---

## تخصيص (Config)

حرر `config.yaml`:
- `youtube.privacy_status`: `public` / `unlisted` / `private`
- `youtube.category_id`: [لائحة الكاتيغوريات](https://developers.google.com/youtube/v3/docs/videoCategories/list) (22 = People & Blogs)
- `telegram.source_chat`: `me` أو `@channel_username`
- `limits.max_uploads_per_run`: عدد الفيديوهات فـ كل run

---

## مشاكل شائعة

| المشكلة | الحل |
|---|---|
| ما توصلش رسالة تأكيد | شوف "Actions" tab فـ GitHub، دخل لـ آخر run، شوف الـ logs |
| "Missing required environment variable" | نسيتي تزيد secret واحد — راجع الخطوة 6 |
| الفيديو ما تلا9ش | تأكد `TELEGRAM_SOURCE_CHAT` صافي (`me` كتب بحروف صغار) |
| Refresh token خدام 7 أيام غير | راجع "ملاحظة Verification" فـ الخطوة 3 — نشر (Publish) الأبليكاسيون |
