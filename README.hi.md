<!-- Translated from README.md at v0.6.0 -->
<div align="center">

# WriteLikeHuman

**रोज़ की लिखाई ऐसी लगे जैसे आपने ख़ुद लिखी हो।**

Email, WhatsApp reply, letter, resume, post और आपकी रोज़ की files के लिए एक free Claude skill.

[![Latest release](https://img.shields.io/github/v/release/thisiskurubaran/WriteLikeHuman?label=release&color=2ea44f)](https://github.com/thisiskurubaran/WriteLikeHuman/releases/latest)
[![License: MIT](https://img.shields.io/github/license/thisiskurubaran/WriteLikeHuman?color=blue)](LICENSE)
[![Claude Skill](https://img.shields.io/badge/Claude-Skill-D97757?logo=claude&logoColor=white)](https://support.claude.com/en/articles/12512180-use-skills-in-claude)
[![Works on](https://img.shields.io/badge/works%20on-web%20%7C%20desktop%20%7C%20mobile-6f42c1)](INSTALL.md)
[![No coding needed](https://img.shields.io/badge/coding-not%20needed-success)](INSTALL.md)
[![PRs welcome](https://img.shields.io/badge/PRs-welcome-brightgreen)](CONTRIBUTING.md)

[Install](#install) · [क्या पूछ सकते हैं](#ask) · [Features](#features) · [सवाल-जवाब](#faq) · [Contribute](#contributing) · [Website](https://thisiskurubaran.github.io/WriteLikeHuman/)

[English](README.md) · हिंदी · [தமிழ்](README.ta.md)

</div>

> यह English [README](README.md) का हिंदी अनुवाद है। असली version English वाला है, और वह इससे नया हो सकता है। अगर आपकी भाषा हिंदी है और कुछ अटपटा लगे, तो सुधार भेजिए, [यहाँ देखें कैसे](CONTRIBUTING.md#help-wanted)।

---

## WriteLikeHuman क्यों?

आप Claude से कोई message लिखवाते हैं और वह किसी brochure जैसा लगता है। "I hope this finds you well." "It's important to note." हर जगह लंबे dash. कोई इंसान ऐसे बात नहीं करता।

WriteLikeHuman यही ठीक करता है। अपना text paste कीजिए या file लगाइए, बोलिए "make this sound less robotic", और आपको वही बात सीधे, आम शब्दों में वापस मिलेगी। आपकी बातें, नंबर और formatting वैसे के वैसे रहते हैं, और आपकी असली file कभी overwrite नहीं होती।

Code के बारे में कुछ जानने की ज़रूरत नहीं। अगर आप फ़ोटो upload कर सकते हैं, तो इसे भी install कर सकते हैं।

## फ़र्क़ देखिए

<table>
<tr>
<th width="50%">पहले</th>
<th width="50%">बाद में</th>
</tr>
<tr>
<td valign="top">

I hope this message finds you well! I wanted to reach out regarding the quarterly report. It's important to note that the deadline has been moved to 15 March. Please ensure that all inputs are submitted accordingly. Let me know if you have any questions!

</td>
<td valign="top">

Hi team, the quarterly report deadline has moved to 15 March. Please send me your inputs by then.

</td>
</tr>
</table>

हर जवाब के आख़िर में आसान शब्दों में एक छोटा note आता है:

> **What I changed**
> - Removed the stock opening and closing lines.
> - Cut "It's important to note that", which added nothing.
> - Kept the date exactly as it was.

(यह example English में है, क्योंकि text English में था। आप हिंदी में लिखेंगे तो note भी हिंदी में मिलेगा।)

और examples: [examples page](https://thisiskurubaran.github.io/WriteLikeHuman/examples.html) पर देखिए, या [before-after.md](write-like-human/examples/before-after.md) पढ़िए।

<a name="install"></a>
## दो मिनट में install

| Step | क्या करना है |
|:---:|---|
| 1 | [Releases page](https://github.com/thisiskurubaran/WriteLikeHuman/releases) से **`WriteLikeHuman.zip`** download कीजिए। इसे unzip मत कीजिए। |
| 2 | Claude में **Settings > Capabilities** खोलिए और **Code execution and file creation** चालू कीजिए। |
| 3 | **Customize > Skills** पर जाइए, **+** दबाइए, फिर **Upload a skill**, और zip चुनिए। |
| 4 | देख लीजिए कि WriteLikeHuman के आगे वाला switch on है। बस हो गया। |

एक skill, एक बार upload. आपके account में आ गया, तो Claude की phone app में भी चलेगा।

Claude Code इस्तेमाल करते हैं? इसे plugin की तरह install कीजिए:

```text
/plugin marketplace add thisiskurubaran/WriteLikeHuman
/plugin install write-like-human@writelikehuman
```

और मदद चाहिए? पूरी [install guide](INSTALL.hi.md) देखिए।

<a name="ask"></a>
## क्या पूछ सकते हैं

बस आम तरीक़े से बात कीजिए। कोई command याद नहीं करनी।

```text
Make this email sound less robotic
Humanize this Word file
Write my leave letter as a Word file
Does this sound like AI?
Write a farewell speech for my manager
Reply to this WhatsApp from my landlord
Make this simpler for my dad
Show me each change so I can approve it
```

हिंदी या Hinglish में भी पूछ सकते हैं:

```text
यह email थोड़ा natural बना दो, बहुत robotic लग रहा है
Landlord ke is WhatsApp ka reply likh do, politely
मम्मी के लिए इसे आसान हिंदी में लिख दो
```

<a name="features"></a>
## Features

### काम करने के तरीक़े

| तरीक़ा | ऐसे बोलिए |
|---|---|
| जो text है उसे ठीक करना | "Make this sound natural" |
| कुछ नया लिखवाना, जो पहली बार में ही सही लगे | "Write a thank you note to my teacher" |
| बिना बदले बताना कि क्या अटपटा लग रहा है | "Does this sound like AI?" |
| हर बदलाव एक-एक करके मंज़ूर या नामंज़ूर करना | "Show me the changes side by side" |
| पूछना कि कोई बदलाव क्यों किया | "Why did you change this line?" |
| ख़ुद ये आदतें पहचानना सीखना | "Teach me why this sounds like AI" |
| किसी और का भेजा message समझना | "How does this message from my boss sound?" |

### नई files बनाइए

File माँगिए और file मिलेगी, जिसके शब्द पहले draft से ही सहज लगेंगे। WriteLikeHuman content लिखता है और Claude अपने file tools से file बनाता है।

| आप माँगें | आपको मिलता है |
|---|---|
| "Write my leave letter as a Word file" (या "मेरी छुट्टी की चिट्ठी Word file में बना दो") | सही letter format में एक `.docx`, खोलकर edit करने के लिए तैयार |
| "Make this society notice into a PDF I can print" | print करने लायक एक `.pdf` |
| "Make 5 slides for my team meeting from these notes" | एक `.pptx`, slides पर छोटा text और speaker notes में पूरी बात |
| "Fill my company letterhead template with this letter" | आपका template, उसका look वैसा ही, बस text भर दिया जाता है |
| "Send this Diwali greeting to everyone in my sheet using each name" | हर इंसान के लिए एक draft, सब एक file में। कुछ भी भेजा नहीं जाता। |
| "Fill this visa form with my details" | PDF या Word form की भरी हुई copy। जो बात पता नहीं, वह खाली छोड़कर list कर दी जाती है |
| "Put these expenses in a spreadsheet with a notes column" | एक `.xlsx`, जिसमें आपके numbers ठीक वैसे ही हैं जैसे आपने दिए, और totals formulas में |

### आपकी पहले से मौजूद files edit कीजिए

| File | आपको क्या वापस मिलता है |
|---|---|
| Word (.docx) | वही fonts, styles, tables और lists. चाहें तो tracked changes, या हर बदलाव के साथ margin में छोटा सा note कि क्यों बदला। |
| PDF | Edit होने वाली Word copy. Scan किए हुए pages उनकी image से पढ़े जाते हैं, और नाम व नंबर आपसे पक्के करवाए जाते हैं। |
| Google Docs और Claude docs | Claude आपके Google account से जुड़ा हो तो वहीं edit, नहीं तो paste करने के लिए साफ़ copy. |
| Spreadsheets (.xlsx, .csv, Google Sheets) | सिर्फ़ text cells, notes और comments बदलते हैं। नंबर और formulas को हाथ नहीं लगाया जाता। Claude आपके Google account से जुड़ा हो तो Google Sheets वहीं edit हो जाती है। |
| Slides (.pptx, Google Slides) | Slide का text और speaker notes, layout वैसा ही। Google से जुड़ा हो तो Google Slides वहीं edit। |
| Text और Markdown (.txt, .md) | Markdown, links और code blocks जैसे थे वैसे। |
| Subtitles (.srt, .vtt) | Captions के शब्द बदलते हैं, timing नहीं, ताकि video के साथ sync रहें। |
| OpenDocument और RTF (.odt, .rtf) | Word file की तरह edit, और बताया जाता है कि वापस किस format में मिलेगी। |
| Chat और email के screenshots | Screen पर जो दिख रहा है उससे reply, किसी का phone number दोहराए बिना। |
| एक साथ कई files | हर file अलग से ठीक होती है, एक file की बात दूसरी में नहीं मिलती। |
| Apple Pages और Keynote | Convert करके edit, या पहले export करने के आसान steps. |
| Web pages (.html) | दिखने वाला text बदलता है। Tags, links और code बिल्कुल वैसे ही रहते हैं। |
| Posters और flyers | दोबारा type करने के लिए text का साफ़ version. Claude image को ख़ुद edit नहीं कर सकता। |
| हाथ से लिखे notes और whiteboard | Type किया हुआ text या Word file, जो शब्द साफ़ न पढ़े जाएँ उन पर निशान, अंदाज़ा नहीं। |
| लंबे documents (thesis, manual, लंबी reports) | एक-एक हिस्सा करके ठीक होते हैं, नाम और शब्द पूरे document में एक जैसे रहते हैं, और कुछ भी छूटता नहीं। |
| LaTeX (.tex) | Text के शब्द बदलते हैं, commands, maths और citations बिल्कुल वैसे ही रहते हैं। |
| लोगों की list वाली spreadsheet | हर इंसान के लिए उसके नाम के साथ एक draft, file में save. कुछ भी भेजा नहीं जाता, और यह सिर्फ़ उन लोगों के लिए है जिन्हें आप पहले से जानते हैं। |
| Gmail और Outlook drafts | Claude आपके mail से जुड़ा हो तो वहीं edit. कुछ भी भेजा नहीं जाता। |

हर file एक नई copy बनकर आती है, नाम होता है `yourfile-humanized`, ताकि असली file सुरक्षित रहे। "a file showing what changed" माँगेंगे तो एक Word file भी मिलेगी जिसमें हर बदलाव mark होगा।

<details>
<summary><b>किस-किस तरह की लिखाई (42)</b></summary>

<br>

| लिखाई | किस बात का ध्यान रखता है |
|---|---|
| Emails | जल्दी वाला reply, शालीनता से मना करना, follow-up, thank you, माफ़ी, कुछ माँगना, पूरी thread का reply, और interview के बाद thank-you note |
| WhatsApp और SMS | घरवालों, landlord, delivery वालों, building group को reply |
| Formal letters | छुट्टी, शिकायत, bank, सरकारी दफ़्तर और school के letters, Indian format में |
| Resume और cover letter | Buzzwords की जगह सीधे शब्द, और कोई मनगढ़ंत achievement नहीं |
| Social posts | LinkedIn, Instagram, X, WhatsApp और Facebook, हर एक की limit के अंदर |
| Bios | Instagram bio, dating profile, website का About page |
| Reports | School और office की reports, साफ़ और आपके ही शब्दों में |
| Meeting notes | कच्चे notes से पढ़ने लायक minutes |
| Speeches और toasts | शादी, birthday, farewell, बोलकर पढ़ने के हिसाब से |
| Wishes और cards | त्योहार, बधाई, और शोक संदेश, ध्यान से लिखे हुए |
| Reviews | आपका अपना असली अनुभव, आपके शब्दों में |
| Form answers | Personal statement, visa letter, scholarship के जवाब, सच के साथ |
| Voice notes | Speech-to-text transcript से पढ़ने लायक text |
| Reviews के reply | Business वाले ख़ुद अपनी तरफ़ से customer reviews का जवाब दें |
| Listings | Meesho, Etsy, Amazon, Flipkart, OLX और Instagram shop के product description, सिर्फ़ seller की दी हुई जानकारी से |
| Invitations | शादी, गृह प्रवेश, नामकरण, birthday party |
| मुश्किल बातें | माफ़ी माँगना, अपनी हद तय करना, घरवालों को मना करना |
| Job posts | सीधी, सबको शामिल करने वाली job description |
| Notices और newsletters | Housing society, school, club और office के notice |
| Freelance proposals | Upwork, Fiverr और client quotes, बिना मनगढ़ंत अनुभव के |
| Essays | School और college के essays, student के अपने शब्दों में बेहतर |
| शादी का biodata | प्यार भरा पर सच्चा matrimony profile, कुछ भी बढ़ा-चढ़ाकर नहीं |
| Cold messages | LinkedIn notes, referral माँगना, recruiters और clients को cold emails |
| Companies से शिकायत | Online shop, airline, telecom, bank, order number बिल्कुल वैसे ही |
| RTI applications | सूचना का अधिकार (RTI) की अर्ज़ी, standard Indian format में |
| किराए के posts | Flat किराए पर, PG और roommate के posts, सबके साथ बराबरी वाले शब्दों में |
| School को messages | Teacher, class group और PTA को notes |
| श्रद्धांजलि और शोक सूचना | सीधे, सच्चे शब्द, सिर्फ़ आपकी असली यादों से |
| Release notes | Changelogs और app store का "What's new" text |
| Announcements | सगाई, शादी, बच्चे के जन्म और events की सूचना |
| किराए का agreement | Clauses सीधी भाषा में समझाए या लिखे, असली clause साथ में। यह कानूनी सलाह नहीं है। |
| Product FAQs | छोटे business के FAQ pages, सिर्फ़ आपकी दी हुई बातों से |
| School circulars | School से parents को notice, तारीख़ें और fees बिल्कुल वैसी ही |
| Grievance letters | Employer या HR को शांत, तथ्यों वाली शिकायत |
| Insurance claims | Claim letters और follow-ups, कभी बढ़ा-चढ़ाकर नहीं |
| Payment reminders | शालीन follow-up और invoice notes, रकम और due date बिल्कुल वैसे ही |
| Customer support के reply | छोटे business के लिए reply, जिसमें आपकी मंज़ूरी के बिना कोई वादा नहीं |
| Out-of-office और away messages | Auto-replies, WhatsApp Business greetings और email signatures |
| Alt text | Posts, websites और slides की images के छोटे description |
| मोल-भाव और बातचीत | Salary, दाम और किराए की बात, सिर्फ़ आपके असली नंबर और वजहों के साथ |
| Recommendation letters | सिफ़ारिश करने वाले ने जो सच में देखा, उसी पर लिखे references |
| Video scripts | YouTube, Reels और Shorts के scripts, बोलकर पढ़ने के लिए लिखे हुए |

</details>

<details>
<summary><b>बदलाव जो आप माँग सकते हैं</b></summary>

<br>

| बदलाव | ऐसे बोलिए |
|---|---|
| Tone | "Friendlier", "more professional", "warmer", "short and direct", "more formal" |
| पढ़ने का level | "Simpler for my mom", "for a 10 year old", "English is their second language" |
| लंबाई | "Cut this to 200 words", "turn these notes into a paragraph" |
| पढ़ने में आसान | "Is this easy to read?" लंबे वाक्य, मुश्किल शब्द और अस्पष्ट links बताता है |
| सबको शामिल करने वाले शब्द | "Make it gender neutral" (सिर्फ़ जब आप कहें) |
| जो शब्द नहीं बदलने | "Never change 'FlexiPlan Pro'" से brand नाम, ख़ास शब्द और nicknames वैसे ही रहते हैं |
| कौन सी English | "Make it UK English" से US, UK, Australian और Indian English के बीच बदलाव, और Singapore, Nigerian, Kenyan, Philippine व South African English जैसी आप लिखते हैं वैसी ही रहती है |
| Paste के लिए तैयार | हर app में ठीक दिखने वाली line breaks और formatting |
| पढ़ने की उम्र | "What reading age is this?" से मोटा-मोटा अंदाज़ा, सिर्फ़ जब आप पूछें |
| भेजने से पहले | "Check this before I send it" बताता है: attachment छूट गया, दिन और तारीख़ मेल नहीं खाते, किसी सवाल का जवाब नहीं दिया, या [name] जैसे placeholder रह गए |
| एक जैसा लिखना | "Check this report for consistency" बताता है कि कहाँ शब्द, spelling या नंबर लिखने का तरीक़ा बीच में बदल गया |
| दूसरे देश के लोग | "Will this sound okay to my client in Germany?" बताता है कि बाहर क्या अटपटा लग सकता है |
| दो लंबाई | "Give me a short and a long version" |
| Speech का समय | "How long will this speech take?" हर हिस्से का समय बताता है |
| Easy Read | "Make this Easy Read" से एक आसान version, हर line में एक ही बात |
| Dyslexia के लिए आसान layout | "Make this Word file dyslexia friendly" से font, spacing और alignment बदलते हैं, शब्द नहीं |
| मुश्किल reply | "Reply to my landlord without sounding rude" से एक reply, और ज़रूरत हो तो थोड़ा सख़्त या नरम tone का सुझाव |

</details>

<details>
<summary><b>आपकी अपनी आवाज़</b></summary>

<br>

अपनी लिखी हुई कुछ चीज़ें दीजिए और WriteLikeHuman एक छोटा voice profile बना देता है: आपके वाक्य कितने लंबे होते हैं, कौन से शब्द आपको पसंद हैं, आप message कैसे ख़त्म करते हैं। इसे note या file की तरह रख लीजिए और अगली बार साथ लगा दीजिए। एक से ज़्यादा भी रख सकते हैं, जैसे "work me" और "personal me"। अपनी WhatsApp chat export से भी बना सकते हैं: सिर्फ़ आपके messages लिए जाते हैं, और phone number, email और links पहले ही छिपा दिए जाते हैं।

आप इसे WhatsApp, Telegram या Signal के chat export से भी बना सकते हैं, जिसमें सिर्फ़ आपके अपने messages लिए जाते हैं। हर बार attach न करना पड़े, इसके लिए इसे किसी Claude Project में रख लीजिए।

पुराने samples पास नहीं हैं? तीन छोटे messages से भी एक starter profile बन जाता है, जो आगे और samples देने पर बेहतर होता जाता है। यह आपकी लिखी Word, PDF या text files से भी सीख सकता है। Team या छोटे business के लिए एक shared house style रखिए: product के नाम, कौन से शब्द लिखने हैं और कौन से नहीं, message कैसे ख़त्म करना है। उसे साथ लगाइए और हर message उसी हिसाब से लिखा जाएगा।

</details>

<details>
<summary><b>भाषाएँ</b></summary>

<br>

| भाषा | क्या करता है |
|---|---|
| Indian English | लाख, करोड़, Indian date format और आम Indian बोलचाल बनी रहती है। ज़बरदस्ती American style नहीं। |
| Hinglish, Tanglish, Manglish, Benglish, Kanglish, Taglish और दूसरे mix | आपका mix और आपकी script वैसी ही। आपको "सुधारकर" pure English में नहीं बदलता। |
| हिंदी, तमिल, तेलुगु, कन्नड़, मलयालम, बांग्ला, मराठी, गुजराती, पंजाबी, ओड़िया, उर्दू, असमिया, नेपाली, सिंहली, कोंकणी, सिंधी, मैथिली | किताबी, अकड़ी हुई या machine से translate जैसी भाषा ठीक करता है |
| Spanish, French, German, Portuguese, Italian, Turkish, Indonesian, Arabic, Japanese, Korean, Chinese, Filipino, Vietnamese, Thai, Swahili | यही काम, हर भाषा की अपनी आम ग़लतियों के साथ |
| Translation | "Translate this into Hindi" से ऐसा version मिलता है जो सच में हिंदी जैसा लगे |
| Script बदलना | "Write this in Hindi script" से शब्द वही रहते हैं, सिर्फ़ लिपि बदलती है, हिंदी, तमिल, तेलुगु और दूसरी भारतीय लिपियों के लिए |

जब तक आप न कहें, यह translate नहीं करता। तमिल में लिखेंगे तो जवाब तमिल में आएगा।

भाषाओं वाली guides अभी तक native speakers ने जाँची नहीं हैं। अगर आप इनमें से कोई भाषा बोलते हैं, तो [आपकी मदद का स्वागत है](CONTRIBUTING.md#help-wanted)। सबसे आसान तरीक़ा है एक [language review issue](https://github.com/thisiskurubaran/WriteLikeHuman/issues/new?template=language_review.md)।

</details>

## यह क्या नहीं करेगा

WriteLikeHuman बेहतर लिखने में मदद करता है। किसी को दिखावा करने में नहीं।

- आपकी बातें नहीं बदलेगा। नाम, नंबर, तारीख़, रक़म और quotes वैसे ही रहेंगे जैसे आपने लिखे। कुछ साफ़ न हो तो पूछेगा।
- किसी checker को लेकर वादा नहीं करेगा। यह लिखाई को साफ़ और natural बनाता है, बस इतना ही दावा है।
- नकली reviews नहीं लिखेगा, न ही उन चीज़ों के reviews जो आपने इस्तेमाल नहीं कीं।
- Personal statement, visa letter या scholarship के जवाब में ऐसा अनुभव नहीं जोड़ेगा जो हुआ ही नहीं।
- आपके अलावा किसी और की नक़ल नहीं करेगा।

<a name="faq"></a>
## सवाल-जवाब

<details>
<summary><b>क्या यह free है?</b></summary>

<br>

हाँ। WriteLikeHuman MIT license के तहत free और open source है। आपको ऐसा Claude account चाहिए जिसमें skills मिलती हों। ज़्यादा जानकारी [install guide](INSTALL.hi.md) में है।

</details>

<details>
<summary><b>क्या यह मेरे phone पर चलेगा?</b></summary>

<br>

हाँ। एक बार Claude की website या desktop app पर upload कर दीजिए, फिर उसी account से phone की Claude app में इस्तेमाल कीजिए।

</details>

<details>
<summary><b>कहीं मेरा document बिगड़ तो नहीं जाएगा?</b></summary>

<br>

यह शब्द बदलता है, layout नहीं। Fonts, tables, lists और formulas अपनी जगह रहते हैं, और आपको हमेशा नई copy मिलती है, तो असली file को कुछ नहीं होता।

</details>

<details>
<summary><b>यह चला ही नहीं। अब क्या करें?</b></summary>

<br>

Message की शुरुआत "Use WriteLikeHuman to..." से कीजिए। फिर भी न चले, तो **Customize > Skills** में देखिए कि switch on है। बाक़ी उपाय [install guide](INSTALL.md#something-not-working) में हैं।

</details>

## Privacy

आपका text Claude के साथ आपकी अपनी chat में ही रहता है। यह skill आपकी लिखाई कहीं save या send नहीं करता। अगर कभी लगे कि ऐसा हो सकता है, तो [चुपचाप हमें बताइए](SECURITY.md)। पूरी जानकारी [privacy page](https://thisiskurubaran.github.io/WriteLikeHuman/privacy.html) पर है।

<a name="contributing"></a>
## Contribute कीजिए

कोई AI वाली आदत है जो हमसे छूट गई? अपनी भाषा या कोई नई तरह की लिखाई जुड़वानी है? Contributions का स्वागत है। [CONTRIBUTING.md](CONTRIBUTING.md) से शुरू कीजिए और [Code of Conduct](CODE_OF_CONDUCT.md) का पालन कीजिए।

कोई bug मिला? [Issue खोलिए](https://github.com/thisiskurubaran/WriteLikeHuman/issues/new/choose), और अपनी असली files की जगह बनाया हुआ text इस्तेमाल कीजिए।

## License

[MIT License](LICENSE) के तहत जारी। इस्तेमाल कीजिए, बाँटिए, बेहतर बनाइए।
