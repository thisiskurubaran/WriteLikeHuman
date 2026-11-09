<!-- Translated from README.md at v0.7.0 -->
<div align="center">

# WriteLikeHuman

**தினமும் எழுதுவது நீங்களே எழுதியது போல இருக்கட்டும்.**

Email, WhatsApp reply, letter, resume, post, நீங்கள் தினமும் பயன்படுத்தும் files எல்லாவற்றுக்கும் ஒரு free Claude skill.

[![Latest release](https://img.shields.io/github/v/release/thisiskurubaran/WriteLikeHuman?label=release&color=2ea44f)](https://github.com/thisiskurubaran/WriteLikeHuman/releases/latest)
[![License: MIT](https://img.shields.io/github/license/thisiskurubaran/WriteLikeHuman?color=blue)](LICENSE)
[![Claude Skill](https://img.shields.io/badge/Claude-Skill-D97757?logo=claude&logoColor=white)](https://support.claude.com/en/articles/12512180-use-skills-in-claude)
[![Works on](https://img.shields.io/badge/works%20on-web%20%7C%20desktop%20%7C%20mobile-6f42c1)](INSTALL.md)
[![No coding needed](https://img.shields.io/badge/coding-not%20needed-success)](INSTALL.md)
[![PRs welcome](https://img.shields.io/badge/PRs-welcome-brightgreen)](CONTRIBUTING.md)

[Install](#install) · [என்ன கேட்கலாம்](#ask) · [Features](#features) · [கேள்வி பதில்](#faq) · [Contribute](#contributing) · [Website](https://thisiskurubaran.github.io/WriteLikeHuman/)

[English](README.md) · [हिंदी](README.hi.md) · தமிழ்

</div>

> இது English [README](README.md)-இன் தமிழ் மொழிபெயர்ப்பு. முதன்மையானது English version தான், அது இதைவிடப் புதியதாக இருக்கலாம். தமிழ் உங்கள் தாய்மொழி என்றால், ஏதாவது சரியில்லாமல் தோன்றினால் திருத்தி அனுப்புங்கள், [எப்படி என்று இங்கே பாருங்கள்](CONTRIBUTING.md#help-wanted).

---

## ஏன் WriteLikeHuman?

Claude-இடம் ஒரு message எழுதச் சொன்னால், அது ஏதோ விளம்பர brochure மாதிரி வருகிறது. "I hope this finds you well." "It's important to note." எல்லா இடத்திலும் நீளமான dash. யாரும் இப்படிப் பேசுவதில்லை.

WriteLikeHuman இதைச் சரிசெய்கிறது. உங்கள் text-ஐ paste செய்யுங்கள் அல்லது file-ஐ இணையுங்கள், "make this sound less robotic" என்று சொல்லுங்கள். அதே விஷயம் எளிமையான, இயல்பான வார்த்தைகளில் திரும்ப வரும். உங்கள் தகவல்கள், எண்கள், formatting எல்லாம் அப்படியே இருக்கும். உங்கள் original file ஒருபோதும் overwrite ஆகாது.

Code பற்றி எதுவும் தெரிய வேண்டியதில்லை. ஒரு photo upload செய்யத் தெரிந்தால், இதையும் install செய்யலாம்.

## வித்தியாசத்தைப் பாருங்கள்

<table>
<tr>
<th width="50%">முன்பு</th>
<th width="50%">பிறகு</th>
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

ஒவ்வொரு பதிலின் முடிவிலும் எளிய வார்த்தைகளில் ஒரு சிறிய குறிப்பு வரும்:

> **What I changed**
> - Removed the stock opening and closing lines.
> - Cut "It's important to note that", which added nothing.
> - Kept the date exactly as it was.

(Text English-இல் இருந்ததால் இந்த example English-இல் இருக்கிறது. நீங்கள் தமிழில் எழுதினால் குறிப்பும் தமிழில் வரும்.)

மேலும் examples: [examples page](https://thisiskurubaran.github.io/WriteLikeHuman/examples.html)-இல் பாருங்கள், அல்லது [before-after.md](write-like-human/examples/before-after.md) படியுங்கள்.

<a name="install"></a>
## இரண்டு நிமிடத்தில் install

| Step | என்ன செய்ய வேண்டும் |
|:---:|---|
| 1 | [Releases page](https://github.com/thisiskurubaran/WriteLikeHuman/releases)-இலிருந்து **`WriteLikeHuman.zip`**-ஐ download செய்யுங்கள். Unzip செய்ய வேண்டாம். |
| 2 | Claude-இல் **Settings > Capabilities** திறந்து **Code execution and file creation**-ஐ on செய்யுங்கள். |
| 3 | **Customize > Skills**-க்குப் போய், **+** அழுத்தி, பிறகு **Upload a skill**, zip-ஐத் தேர்ந்தெடுங்கள். |
| 4 | WriteLikeHuman பக்கத்தில் உள்ள switch on-இல் இருக்கிறதா என்று பாருங்கள். அவ்வளவுதான். |

ஒரே skill, ஒரே upload. உங்கள் account-இல் வந்துவிட்டால், Claude phone app-இலும் வேலை செய்யும்.

Claude Code பயன்படுத்துகிறீர்களா? இதை plugin ஆக install செய்யுங்கள்:

```text
/plugin marketplace add thisiskurubaran/WriteLikeHuman
/plugin install write-like-human@writelikehuman
```

இன்னும் உதவி வேண்டுமா? முழு [install guide](INSTALL.ta.md)-ஐப் பாருங்கள்.

<a name="ask"></a>
## என்ன கேட்கலாம்

சாதாரணமாகப் பேசுங்கள். எந்த command-ஐயும் மனப்பாடம் செய்ய வேண்டாம்.

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

தமிழிலோ Tanglish-இலோ கூடக் கேட்கலாம்:

```text
இந்த email-ஐக் கொஞ்சம் இயல்பா மாத்திக் கொடுங்க
Owner anuppina WhatsApp-ku oru polite reply ezhudhi kudunga
அப்பாவுக்குப் புரியற மாதிரி இதை எளிமையா எழுதுங்க
```

<a name="features"></a>
## Features

### வேலை செய்யும் வழிகள்

| வழி | இப்படிச் சொல்லுங்கள் |
|---|---|
| ஏற்கனவே உள்ள text-ஐ மாற்றி எழுதுவது | "Make this sound natural" |
| முதல் முறையிலேயே சரியாக இருக்கும் புதிய ஒன்றை எழுதுவது | "Write a thank you note to my teacher" |
| எதையும் மாற்றாமல், எது இயல்பாக இல்லை என்று சொல்வது | "Does this sound like AI?" |
| ஒவ்வொரு மாற்றத்தையும் ஒவ்வொன்றாக ஏற்பது அல்லது நிராகரிப்பது | "Show me the changes side by side" |
| ஒரு மாற்றம் ஏன் செய்யப்பட்டது என்று கேட்பது | "Why did you change this line?" |
| இந்தப் பழக்கங்களை நீங்களே கண்டுபிடிக்கக் கற்றுக்கொள்வது | "Teach me why this sounds like AI" |
| யாரோ அனுப்பிய message-ஐப் புரிந்துகொள்வது | "How does this message from my boss sound?" |
| என்ன கேட்பது என்று தெரியவில்லையா? | Text-ஐ paste செய்து "help with this" என்று சொல்லுங்கள், சில சின்ன தேர்வுகள் கிடைக்கும் |

### புதிய files உருவாக்குங்கள்

File கேளுங்கள், file கிடைக்கும். முதல் draft-இலிருந்தே வார்த்தைகள் இயல்பாக இருக்கும். WriteLikeHuman உள்ளடக்கத்தை எழுதுகிறது, Claude தன் file tools மூலம் file-ஐ உருவாக்குகிறது.

| நீங்கள் கேட்பது | உங்களுக்குக் கிடைப்பது |
|---|---|
| "Write my leave letter as a Word file" (அல்லது "என் லீவ் லெட்டரை Word file-ஆ எழுதிக் குடுங்க") | சரியான letter format-இல் ஒரு `.docx`, திறந்து edit செய்யத் தயார் |
| "Make this society notice into a PDF I can print" | print செய்யத் தயாரான ஒரு `.pdf` |
| "Make 5 slides for my team meeting from these notes" | ஒரு `.pptx`, slides-இல் சுருக்கமான text, speaker notes-இல் முழு விவரம் |
| "Fill my company letterhead template with this letter" | உங்கள் template, அதன் தோற்றம் அப்படியே, text மட்டும் நிரப்பப்படும் |
| "Send this Diwali greeting to everyone in my sheet using each name" | ஒவ்வொருவருக்கும் ஒரு draft, எல்லாம் ஒரு file-இல். எதுவும் அனுப்பப்படாது. |
| "Fill this visa form with my details" | PDF அல்லது Word form-இன் நிரப்பிய copy. தெரியாதவை காலியாக விடப்பட்டு பட்டியலிடப்படும் |
| "Put these expenses in a spreadsheet with a notes column" | ஒரு `.xlsx`, நீங்கள் கொடுத்த numbers அப்படியே, totals formulas-ஆக |

### உங்களிடம் உள்ள files-ஐ edit செய்யுங்கள்

| File | உங்களுக்குத் திரும்பக் கிடைப்பது |
|---|---|
| Word (.docx) | அதே fonts, styles, tables, lists. வேண்டுமென்றால் tracked changes, அல்லது ஒவ்வொரு மாற்றத்துக்கும் ஏன் என்று margin-இல் ஒரு சிறிய note. |
| PDF | Edit செய்யக்கூடிய Word copy. Scan செய்த pages அவற்றின் image-இலிருந்து படிக்கப்படும், பெயர்களும் எண்களும் உங்களிடம் உறுதி செய்யப்படும். |
| Google Docs, Claude docs | Claude உங்கள் Google account-உடன் இணைந்திருந்தால் அங்கேயே edit, இல்லையென்றால் paste செய்ய ஒரு சுத்தமான copy. |
| Spreadsheets (.xlsx, .csv, Google Sheets) | Text cells, notes, comments மட்டுமே மாறும். எண்களையும் formulas-ஐயும் தொடாது. Claude உங்கள் Google account-உடன் இணைந்திருந்தால் Google Sheets அங்கேயே edit ஆகும். |
| Slides (.pptx, Google Slides) | Slide text-உம் speaker notes-உம், layout அப்படியே. Google இணைப்பு இருந்தால் Google Slides அங்கேயே edit ஆகும். |
| Text, Markdown (.txt, .md) | Markdown, links, code blocks எல்லாம் இருந்தபடியே. |
| Subtitles (.srt, .vtt) | Captions-இன் வார்த்தைகள் மாறும், timing மாறாது, அதனால் video-வுடன் sync-இல் இருக்கும். |
| OpenDocument, RTF (.odt, .rtf) | Word file ஆக edit செய்யப்படும், எந்த format-இல் திரும்ப வரும் என்றும் சொல்லும். |
| Chat, email screenshots | Screen-இல் தெரிவதை வைத்து reply, யாருடைய phone number-ஐயும் திரும்பச் சொல்லாமல். |
| ஒரே நேரத்தில் பல files | ஒவ்வொரு file-உம் தனியாகச் சரிசெய்யப்படும், ஒன்றின் விவரம் இன்னொன்றில் கலக்காது. |
| Apple Pages, Keynote | Convert செய்து edit செய்யப்படும், அல்லது முதலில் export செய்வதற்கான எளிய steps. |
| Web pages (.html) | கண்ணுக்குத் தெரியும் text மட்டும் மாறும். Tags, links, code அப்படியே இருக்கும். |
| Posters, flyers | மீண்டும் type செய்ய text-இன் சுத்தமான version. Claude image-ஐ நேரடியாக edit செய்ய முடியாது. |
| கையால் எழுதிய notes, whiteboard | Type செய்த text அல்லது Word file. தெளிவாகப் படிக்க முடியாத சொற்கள் ஊகிக்கப்படாமல் குறிக்கப்படும். |
| நீளமான documents (thesis, manual, நீண்ட reports) | ஒவ்வொரு பகுதியாகச் சரிசெய்யப்படும், பெயர்களும் சொற்களும் முழு document-இலும் ஒரே மாதிரி இருக்கும், எதுவும் விடுபடாது. |
| LaTeX (.tex) | Text-இன் வார்த்தைகள் மட்டும் மாறும், commands, maths, citations அப்படியே இருக்கும். |
| நபர்களின் பட்டியல் கொண்ட spreadsheet | ஒவ்வொருவருக்கும் அவர் பெயருடன் ஒரு draft, file-இல் save. எதுவும் அனுப்பப்படாது, உங்களுக்கு ஏற்கனவே தெரிந்தவர்களுக்கு மட்டும். |
| Gmail, Outlook drafts | Claude உங்கள் mail-உடன் இணைந்திருந்தால் அங்கேயே edit. எதுவும் அனுப்பப்படாது. |

ஒவ்வொரு file-உம் `yourfile-humanized` என்ற பெயரில் புதிய copy-ஆக வரும், அதனால் original பத்திரமாக இருக்கும். "a file showing what changed" என்று கேட்டால், ஒவ்வொரு மாற்றமும் குறிக்கப்பட்ட ஒரு Word file-உம் கிடைக்கும்.

<details>
<summary><b>என்னென்ன வகை எழுத்துகள் (43)</b></summary>

<br>

| எழுத்து வகை | எதைக் கவனிக்கும் |
|---|---|
| Emails | சீக்கிரம் அனுப்பும் reply, மரியாதையாக மறுப்பது, follow-up, நன்றி, மன்னிப்பு, ஏதாவது கேட்பது, முழு thread-க்கும் reply, interview-க்குப் பிறகு நன்றி note |
| WhatsApp, SMS | குடும்பம், house owner, delivery ஆட்கள், building group-க்கு reply |
| Formal letters | விடுப்பு, புகார், bank, அரசு அலுவலகம், school letters, Indian format-இல் |
| Resume, cover letter | Buzzwords-க்குப் பதிலாக எளிய வார்த்தைகள், கற்பனைச் சாதனைகள் இல்லை |
| Social posts | LinkedIn, Instagram, X, WhatsApp, Facebook, ஒவ்வொன்றின் limit-க்குள் |
| Bios | Instagram bio, dating profile, website About page |
| Reports | School, office reports, தெளிவாக, உங்கள் வார்த்தைகளிலேயே |
| Meeting notes | கச்சா notes-இலிருந்து படிக்கக்கூடிய minutes |
| Speeches, toasts | கல்யாணம், birthday, farewell, சத்தமாகப் படிக்கும்படி |
| Wishes, cards | பண்டிகை, வாழ்த்து, இரங்கல், கவனமாக எழுதியது |
| Reviews | உங்கள் சொந்த உண்மையான அனுபவம், உங்கள் வார்த்தைகளில் |
| Form answers | Personal statement, visa letter, scholarship பதில்கள், உண்மையாக |
| Voice notes | Speech-to-text transcript-இலிருந்து படிக்கக்கூடிய text |
| Reviews-க்கு reply | Business நடத்துபவர்கள் தங்கள் சார்பில் customer reviews-க்குப் பதில் சொல்வது |
| Listings | Meesho, Etsy, Amazon, Flipkart, OLX, Instagram shop product descriptions, seller கொடுத்த தகவல் மட்டும் |
| அழைப்பிதழ்கள் | கல்யாணம், புதுமனை புகுவிழா, பெயர் சூட்டும் விழா, birthday party |
| கடினமான உரையாடல்கள் | மன்னிப்பு கேட்பது, எல்லை வகுப்பது, குடும்பத்தினரிடம் முடியாது என்று சொல்வது |
| Job posts | எளிய, எல்லோரையும் உள்ளடக்கிய job descriptions |
| Notices, newsletters | Housing society, school, club, office notices |
| Freelance proposals | Upwork, Fiverr, client quotes, கற்பனை அனுபவம் இல்லாமல் |
| Essays | School, college essays, மாணவரின் சொந்த வார்த்தைகளில் மேம்படுத்தியது |
| திருமண biodata | அன்பான, உண்மையான matrimony profile, எதையும் மிகைப்படுத்தாமல் |
| Cold messages | LinkedIn notes, referral கேட்பது, recruiters, clients-க்கு cold emails |
| நிறுவனங்களிடம் புகார் | Online shop, airline, telecom, bank, order number அப்படியே |
| RTI applications | தகவல் அறியும் உரிமை (RTI) மனு, standard Indian format-இல் |
| வாடகை posts | Flat வாடகைக்கு, PG, roommate posts, எல்லோருக்கும் நியாயமான வார்த்தைகளில் |
| School-க்கு messages | Teacher, class group, PTA-க்கு notes |
| இரங்கல் உரை, மரண அறிவிப்பு | எளிய, உண்மையான வார்த்தைகள், உங்கள் சொந்த நினைவுகளிலிருந்து மட்டும் |
| Release notes | Changelogs, app store-இன் "What's new" text |
| அறிவிப்புகள் | நிச்சயதார்த்தம், கல்யாணம், குழந்தை பிறப்பு, நிகழ்ச்சிகள் |
| வாடகை ஒப்பந்தம் | Clauses எளிய வார்த்தைகளில் விளக்கம் அல்லது எழுத்து, அசல் clause அருகிலேயே. இது சட்ட ஆலோசனை அல்ல. |
| Product FAQs | சிறு வணிகங்களுக்கான FAQ pages, நீங்கள் கொடுத்த தகவல்கள் மட்டும் |
| School circulars | School-இலிருந்து பெற்றோருக்கான அறிவிப்புகள், தேதிகளும் fees-உம் அப்படியே |
| Grievance letters | Employer அல்லது HR-க்கு அமைதியான, உண்மைகளுடன் கூடிய புகார் |
| Insurance claims | Claim letters, follow-ups, ஒருபோதும் மிகைப்படுத்தாமல் |
| Payment reminders | மரியாதையான follow-up, invoice notes, தொகையும் due date-உம் அப்படியே |
| Customer support பதில்கள் | சிறு வணிகங்களுக்கான பதில்கள், நீங்கள் ஒப்புக்கொள்ளாத எந்த வாக்குறுதியும் இல்லாமல் |
| Out-of-office, away messages | Auto-replies, WhatsApp Business greetings, email signatures |
| Alt text | Posts, websites, slides-இல் உள்ள படங்களுக்குச் சுருக்கமான விவரம் |
| பேரம் பேசுதல் | சம்பளம், விலை, வாடகை பேச்சு, உங்கள் உண்மையான எண்களும் காரணங்களும் மட்டும் |
| Recommendation letters | பரிந்துரைப்பவர் உண்மையில் பார்த்ததை வைத்து எழுதிய references |
| Video scripts | YouTube, Reels, Shorts-க்கான scripts, பேசுவதற்காக எழுதியவை |
| Work chat | Slack, Teams, Google Chat messages: status update, உதவி கேட்பது, மரியாதையாக மறுப்பது |

</details>

<details>
<summary><b>நீங்கள் கேட்கக்கூடிய மாற்றங்கள்</b></summary>

<br>

| மாற்றம் | இப்படிச் சொல்லுங்கள் |
|---|---|
| Tone | "Friendlier", "more professional", "warmer", "short and direct", "more formal" |
| படிக்கும் நிலை | "Simpler for my mom", "for a 10 year old", "English is their second language" |
| நீளம் | "Cut this to 200 words", "turn these notes into a paragraph" |
| படிக்க எளிதா | "Is this easy to read?" நீண்ட வாக்கியங்கள், கடினமான சொற்கள், தெளிவில்லாத links-ஐச் சுட்டிக்காட்டும் |
| எல்லோரையும் உள்ளடக்கிய சொற்கள் | "Make it gender neutral" (நீங்கள் கேட்டால் மட்டும்) |
| மாற்றக்கூடாத சொற்கள் | "Never change 'FlexiPlan Pro'" என்றால் brand பெயர்கள், சிறப்புச் சொற்கள், செல்லப் பெயர்கள் அப்படியே இருக்கும் |
| எந்த English | "Make it UK English" என்றால் US, UK, Australian, Indian English இடையே மாற்றும். Singapore, Nigerian, Kenyan, Philippine, South African English நீங்கள் எழுதியபடியே இருக்கும் |
| Paste செய்யத் தயார் | ஒவ்வொரு app-இலும் சரியாகத் தெரியும் line breaks, formatting |
| படிக்கும் வயது | "What reading age is this?" என்றால் ஒரு தோராயமான அளவு, நீங்கள் கேட்டால் மட்டும் |
| அனுப்பும் முன் | "Check this before I send it" என்றால்: attachment விடுபட்டது, கிழமையும் தேதியும் பொருந்தாதது, பதில் சொல்லாத கேள்வி, [name] போன்ற placeholders மீதம் இருப்பது |
| ஒரே மாதிரி எழுதுவது | "Check this report for consistency" என்றால் சொற்கள், spelling, எண்கள் எழுதும் முறை பாதியில் மாறிய இடங்களைக் காட்டும் |
| வெளிநாட்டு வாசகர்கள் | "Will this sound okay to my client in Germany?" என்றால் வெளிநாட்டில் எது தவறாகப் படலாம் என்று சொல்லும் |
| இரண்டு நீளம் | "Give me a short and a long version" |
| Speech நேரம் | "How long will this speech take?" என்றால் ஒவ்வொரு பகுதிக்கும் ஆகும் நேரம் |
| Easy Read | "Make this Easy Read" என்றால் ஒவ்வொரு வரியிலும் ஒரே ஒரு விஷயம் உள்ள எளிய version |
| Dyslexia-க்கு எளிதான layout | "Make this Word file dyslexia friendly" என்றால் font, spacing, alignment மாறும், வார்த்தைகள் மாறாது |
| சிக்கலான பதில்கள் | "Reply to my landlord without sounding rude" என்றால் ஒரு பதில், தேவைப்பட்டால் கொஞ்சம் கடுமையான அல்லது மென்மையான tone பரிந்துரை |

</details>

<details>
<summary><b>உங்கள் சொந்தக் குரல்</b></summary>

<br>

நீங்களே எழுதிய சிலவற்றைக் கொடுங்கள், WriteLikeHuman ஒரு சிறிய voice profile உருவாக்கும்: உங்கள் வாக்கியங்கள் எவ்வளவு நீளம், உங்களுக்குப் பிடித்த சொற்கள், message-ஐ எப்படி முடிப்பீர்கள். அதை ஒரு note அல்லது file ஆக வைத்துக்கொண்டு அடுத்த முறை இணையுங்கள். ஒன்றுக்கு மேல் வைத்துக்கொள்ளலாம், உதாரணமாக "work me", "personal me". உங்கள் WhatsApp chat export-இலிருந்தும் உருவாக்கலாம்: உங்கள் messages மட்டுமே எடுத்துக்கொள்ளப்படும், phone numbers, emails, links முதலிலேயே மறைக்கப்படும்.

WhatsApp, Telegram அல்லது Signal chat export-இலிருந்தும் இதை உருவாக்கலாம், உங்கள் சொந்த messages மட்டுமே எடுக்கப்படும். ஒவ்வொரு முறையும் attach செய்யாமல் இருக்க, இதை ஒரு Claude Project-இல் வைத்துக்கொள்ளுங்கள்.

பழைய samples கையில் இல்லையா? மூன்று சிறிய messages போதும், ஒரு starter profile உருவாகும், மேலும் samples கொடுக்கக் கொடுக்க மேம்படும். நீங்கள் எழுதிய Word, PDF, text files-இலிருந்தும் கற்றுக்கொள்ளும். ஒரு team அல்லது சிறு வணிகத்துக்கு, பொதுவான house style வைத்துக்கொள்ளுங்கள்: product பெயர்கள், பயன்படுத்த வேண்டிய, தவிர்க்க வேண்டிய சொற்கள், message-ஐ எப்படி முடிப்பது. அதை இணைத்தால் ஒவ்வொரு message-உம் அதன்படியே இருக்கும்.

</details>

<details>
<summary><b>Developers-க்கு</b></summary>

<br>

WriteLikeHuman உங்கள் code-ஐச் சுற்றியுள்ள வார்த்தைகளை எழுதும். Code-ஐ அது ஒருபோதும் மாற்றாது, coding கேள்விகளையும் எடுத்துக்கொள்ளாது.

| எழுத்து | இப்படிச் சொல்லுங்கள் |
|---|---|
| README files | "Make my README sound less like AI" |
| Commit messages, pull requests | "Write a commit message for this diff" |
| Architecture docs, decision records, folder structure | "Explain the architecture of this project for new joiners" |
| API docs, error messages, button labels, translation files | "Make these error messages friendlier" |
| Code comments, docstrings | "Clean up the comments in this file, don't touch the code" |

Commands, code blocks, config keys, placeholders எல்லாம் அப்படியே இருக்கும். Comments ஒரு script மூலம் மாறும். Code-இல் ஒரு எழுத்து மாறினாலும் அது எதையும் எழுதாது. Claude Code-இல், git repository-க்குள், README மற்றும் docs files-ஐ அங்கேயே edit செய்து, git மூலம் மாற்றங்களை எப்படிப் பார்ப்பது அல்லது திரும்பப் பெறுவது என்று சொல்லும். மற்ற இடங்களில், மற்ற files போலவே, புதிய copy உருவாகும்.

</details>

<details>
<summary><b>மொழிகள்</b></summary>

<br>

| மொழி | என்ன செய்யும் |
|---|---|
| Indian English | லட்சம், கோடி, Indian date format, இயல்பான Indian பேச்சு வழக்கு அப்படியே. வலுக்கட்டாயமான American style இல்லை. |
| Hinglish, Tanglish, Manglish, Benglish, Kanglish, Taglish, மற்ற கலவைகள் | உங்கள் கலவையும் உங்கள் எழுத்துமுறையும் அப்படியே. உங்களை "திருத்தி" pure English ஆக்காது. |
| இந்தி, தமிழ், தெலுங்கு, கன்னடம், மலையாளம், வங்காளம், மராத்தி, குஜராத்தி, பஞ்சாபி, ஒடியா, உருது, அஸ்ஸாமி, நேபாளி, சிங்களம், கொங்கணி, சிந்தி, மைதிலி | புத்தகத்தனமான, இறுக்கமான, அல்லது machine மொழிபெயர்ப்பு போன்ற வார்த்தைகளைச் சரிசெய்யும் |
| Spanish, French, German, Portuguese, Italian, Turkish, Indonesian, Arabic, Japanese, Korean, Chinese, Filipino, Vietnamese, Thai, Swahili | அதே வேலை, ஒவ்வொரு மொழியின் பொதுவான தவறுகளுடன் |
| மொழிபெயர்ப்பு | "Translate this into Tamil" என்றால் உண்மையான தமிழ் போலத் தோன்றும் version கிடைக்கும் |
| எழுத்துமுறை மாற்றம் | "Write this in Tamil script" என்றால் சொற்கள் அதே, எழுத்துமுறை மட்டும் மாறும். தமிழ், இந்தி, தெலுங்கு மற்றும் பிற இந்திய எழுத்துமுறைகளுக்கு |

நீங்கள் கேட்காமல் மொழிபெயர்க்காது. தமிழில் எழுதினால் தமிழில் பதில் வரும்.

மொழி guides-ஐ இன்னும் தாய்மொழியாகப் பேசுபவர்கள் சரிபார்க்கவில்லை. இவற்றில் ஏதாவது ஒரு மொழி உங்களுக்குத் தெரிந்தால், [உங்கள் உதவியை வரவேற்கிறோம்](CONTRIBUTING.md#help-wanted). எளிதான வழி ஒரு [language review issue](https://github.com/thisiskurubaran/WriteLikeHuman/issues/new?template=language_review.md).

</details>

## இது என்ன செய்யாது

WriteLikeHuman நன்றாக எழுத உதவும். யாரும் நடிக்க உதவாது.

- உங்கள் தகவல்களை மாற்றாது. பெயர்கள், எண்கள், தேதிகள், தொகைகள், மேற்கோள்கள் நீங்கள் எழுதியபடியே இருக்கும். ஏதாவது தெளிவில்லை என்றால் கேட்கும்.
- எந்த checker பற்றியும் வாக்குறுதி தராது. எழுத்தைத் தெளிவாகவும் இயல்பாகவும் ஆக்கும், அவ்வளவுதான்.
- போலி reviews எழுதாது, நீங்கள் பயன்படுத்தாதவற்றுக்கும் reviews எழுதாது.
- Personal statement, visa letter, scholarship பதில்களில் நடக்காத அனுபவங்களைச் சேர்க்காது.
- உங்களைத் தவிர வேறு யாரையும் போல எழுதாது.

<a name="faq"></a>
## கேள்வி பதில்

<details>
<summary><b>இது இலவசமா?</b></summary>

<br>

ஆமாம். WriteLikeHuman MIT license-இன் கீழ் இலவசமான open source. Skills கிடைக்கும் ஒரு Claude account வேண்டும். விவரங்களுக்கு [install guide](INSTALL.ta.md)-ஐப் பாருங்கள்.

</details>

<details>
<summary><b>என் phone-இல் வேலை செய்யுமா?</b></summary>

<br>

ஆமாம். Claude website அல்லது desktop app-இல் ஒரு முறை upload செய்யுங்கள், பிறகு அதே account-உடன் phone-இல் உள்ள Claude app-இல் பயன்படுத்துங்கள்.

</details>

<details>
<summary><b>என் document கெட்டுப்போகுமா?</b></summary>

<br>

இது வார்த்தைகளை மாற்றும், layout-ஐ அல்ல. Fonts, tables, lists, formulas அப்படியே இருக்கும். எப்போதும் புதிய copy கிடைக்கும், அதனால் original-க்கு எதுவும் ஆகாது.

</details>

<details>
<summary><b>இது வேலை செய்யவில்லை. இப்போ என்ன செய்வது?</b></summary>

<br>

உங்கள் message-ஐ "Use WriteLikeHuman to..." என்று தொடங்குங்கள். அப்போதும் இல்லையென்றால், **Customize > Skills**-இல் switch on-இல் இருக்கிறதா என்று பாருங்கள். மேலும் தீர்வுகள் [install guide](INSTALL.md#something-not-working)-இல் உள்ளன.

</details>

## Privacy

உங்கள் text Claude-உடனான உங்கள் சொந்த chat-இல் மட்டுமே இருக்கும். இந்த skill உங்கள் எழுத்தை எங்கும் save செய்யாது, அனுப்பாது. அப்படி நடக்கக்கூடும் என்று எப்போதாவது தோன்றினால், [தனிப்பட்ட முறையில் எங்களிடம் சொல்லுங்கள்](SECURITY.md). முழு விவரம் [privacy page](https://thisiskurubaran.github.io/WriteLikeHuman/privacy.html)-இல் உள்ளது.

<a name="contributing"></a>
## பங்களியுங்கள்

நாங்கள் விட்டுப்போன AI பழக்கம் ஏதாவது தெரியுமா? உங்கள் மொழியையோ புதிய எழுத்து வகையையோ சேர்க்க வேண்டுமா? Contributions-ஐ வரவேற்கிறோம். [CONTRIBUTING.md](CONTRIBUTING.md)-இலிருந்து தொடங்குங்கள், [Code of Conduct](CODE_OF_CONDUCT.md)-ஐப் பின்பற்றுங்கள்.

Bug கண்டுபிடித்தீர்களா? [ஒரு issue திறங்கள்](https://github.com/thisiskurubaran/WriteLikeHuman/issues/new/choose). உங்கள் உண்மையான files-க்குப் பதிலாக கற்பனையாக உருவாக்கிய text-ஐப் பயன்படுத்துங்கள்.

## License

[MIT License](LICENSE)-இன் கீழ் வெளியிடப்பட்டது. பயன்படுத்துங்கள், பகிருங்கள், மேம்படுத்துங்கள்.
