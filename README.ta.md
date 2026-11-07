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

[Install](#install) · [என்ன கேட்கலாம்](#ask) · [Features](#features) · [கேள்வி பதில்](#faq) · [Contribute](#contributing)

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

மேலும் examples: [before-after.md](write-like-human/examples/before-after.md)

<a name="install"></a>
## இரண்டு நிமிடத்தில் install

| Step | என்ன செய்ய வேண்டும் |
|:---:|---|
| 1 | [Releases page](https://github.com/thisiskurubaran/WriteLikeHuman/releases)-இலிருந்து **`WriteLikeHuman.zip`**-ஐ download செய்யுங்கள். Unzip செய்ய வேண்டாம். |
| 2 | Claude-இல் **Settings > Capabilities** திறந்து **Code execution and file creation**-ஐ on செய்யுங்கள். |
| 3 | **Customize > Skills**-க்குப் போய், **+** அழுத்தி, பிறகு **Upload a skill**, zip-ஐத் தேர்ந்தெடுங்கள். |
| 4 | WriteLikeHuman பக்கத்தில் உள்ள switch on-இல் இருக்கிறதா என்று பாருங்கள். அவ்வளவுதான். |

ஒரே skill, ஒரே upload. உங்கள் account-இல் வந்துவிட்டால், Claude phone app-இலும் வேலை செய்யும்.

இன்னும் உதவி வேண்டுமா, அல்லது Claude Code பயன்படுத்துகிறீர்களா? முழு [install guide](INSTALL.ta.md)-ஐப் பாருங்கள்.

<a name="ask"></a>
## என்ன கேட்கலாம்

சாதாரணமாகப் பேசுங்கள். எந்த command-ஐயும் மனப்பாடம் செய்ய வேண்டாம்.

```text
Make this email sound less robotic
Humanize this Word file
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

### வேலை செய்ய நான்கு வழிகள்

| வழி | இப்படிச் சொல்லுங்கள் |
|---|---|
| ஏற்கனவே உள்ள text-ஐ மாற்றி எழுதுவது | "Make this sound natural" |
| முதல் முறையிலேயே சரியாக இருக்கும் புதிய ஒன்றை எழுதுவது | "Write a thank you note to my teacher" |
| எதையும் மாற்றாமல், எது இயல்பாக இல்லை என்று சொல்வது | "Does this sound like AI?" |
| ஒவ்வொரு மாற்றத்தையும் ஒவ்வொன்றாக ஏற்பது அல்லது நிராகரிப்பது | "Show me the changes side by side" |

### உங்கள் files, அப்படியே

| File | உங்களுக்குத் திரும்பக் கிடைப்பது |
|---|---|
| Word (.docx) | அதே fonts, styles, tables, lists. வேண்டுமென்றால் tracked changes-உம். |
| PDF | Edit செய்யக்கூடிய Word copy. ஏதாவது page scan செய்த image என்றால் அதையும் சொல்லும். |
| Google Docs, Claude docs | Claude உங்கள் Google account-உடன் இணைந்திருந்தால் அங்கேயே edit, இல்லையென்றால் paste செய்ய ஒரு சுத்தமான copy. |
| Spreadsheets (.xlsx, .csv, Google Sheets) | Text cells, notes, comments மட்டுமே மாறும். எண்களையும் formulas-ஐயும் தொடாது. |
| Slides (.pptx, Google Slides) | Slide text-உம் speaker notes-உம், layout அப்படியே. |
| Text, Markdown (.txt, .md) | Markdown, links, code blocks எல்லாம் இருந்தபடியே. |
| Subtitles (.srt, .vtt) | Captions-இன் வார்த்தைகள் மாறும், timing மாறாது, அதனால் video-வுடன் sync-இல் இருக்கும். |
| OpenDocument, RTF (.odt, .rtf) | Word file ஆக edit செய்யப்படும், எந்த format-இல் திரும்ப வரும் என்றும் சொல்லும். |
| Chat, email screenshots | Screen-இல் தெரிவதை வைத்து reply, யாருடைய phone number-ஐயும் திரும்பச் சொல்லாமல். |
| ஒரே நேரத்தில் பல files | ஒவ்வொரு file-உம் தனியாகச் சரிசெய்யப்படும், ஒன்றின் விவரம் இன்னொன்றில் கலக்காது. |

ஒவ்வொரு file-உம் `yourfile-humanized` என்ற பெயரில் புதிய copy-ஆக வரும், அதனால் original பத்திரமாக இருக்கும். "a file showing what changed" என்று கேட்டால், ஒவ்வொரு மாற்றமும் குறிக்கப்பட்ட ஒரு Word file-உம் கிடைக்கும்.

<details>
<summary><b>என்னென்ன வகை எழுத்துகள் (21)</b></summary>

<br>

| எழுத்து வகை | எதைக் கவனிக்கும் |
|---|---|
| Emails | சீக்கிரம் அனுப்பும் reply, மரியாதையாக மறுப்பது, follow-up, நன்றி, மன்னிப்பு, ஏதாவது கேட்பது, முழு thread-க்கும் reply |
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
| எந்த English | "Make it UK English" என்றால் US, UK, Australian, Indian spelling, dates இடையே மாற்றும் |
| Paste செய்யத் தயார் | ஒவ்வொரு app-இலும் சரியாகத் தெரியும் line breaks, formatting |
| படிக்கும் வயது | "What reading age is this?" என்றால் ஒரு தோராயமான அளவு, நீங்கள் கேட்டால் மட்டும் |

</details>

<details>
<summary><b>உங்கள் சொந்தக் குரல்</b></summary>

<br>

நீங்களே எழுதிய சிலவற்றைக் கொடுங்கள், WriteLikeHuman ஒரு சிறிய voice profile உருவாக்கும்: உங்கள் வாக்கியங்கள் எவ்வளவு நீளம், உங்களுக்குப் பிடித்த சொற்கள், message-ஐ எப்படி முடிப்பீர்கள். அதை ஒரு note அல்லது file ஆக வைத்துக்கொண்டு அடுத்த முறை இணையுங்கள். ஒன்றுக்கு மேல் வைத்துக்கொள்ளலாம், உதாரணமாக "work me", "personal me". உங்கள் WhatsApp chat export-இலிருந்தும் உருவாக்கலாம்: உங்கள் messages மட்டுமே எடுத்துக்கொள்ளப்படும், phone numbers, emails, links முதலிலேயே மறைக்கப்படும்.

</details>

<details>
<summary><b>மொழிகள்</b></summary>

<br>

| மொழி | என்ன செய்யும் |
|---|---|
| Indian English | லட்சம், கோடி, Indian date format, இயல்பான Indian பேச்சு வழக்கு அப்படியே. வலுக்கட்டாயமான American style இல்லை. |
| Hinglish, Tanglish, Manglish, Benglish, Kanglish, மற்ற கலவைகள் | உங்கள் கலவையும் உங்கள் எழுத்துமுறையும் அப்படியே. உங்களை "திருத்தி" pure English ஆக்காது. |
| இந்தி, தமிழ், தெலுங்கு, கன்னடம், மலையாளம், வங்காளம், மராத்தி, குஜராத்தி, பஞ்சாபி, ஒடியா, உருது, அஸ்ஸாமி | புத்தகத்தனமான, இறுக்கமான, அல்லது machine மொழிபெயர்ப்பு போன்ற வார்த்தைகளைச் சரிசெய்யும் |
| Spanish, French, German, Portuguese, Indonesian, Arabic, Japanese | அதே வேலை, ஒவ்வொரு மொழியின் பொதுவான தவறுகளுடன் |
| மொழிபெயர்ப்பு | "Translate this into Tamil" என்றால் உண்மையான தமிழ் போலத் தோன்றும் version கிடைக்கும் |

நீங்கள் கேட்காமல் மொழிபெயர்க்காது. தமிழில் எழுதினால் தமிழில் பதில் வரும்.

மொழி guides-ஐ இன்னும் தாய்மொழியாகப் பேசுபவர்கள் சரிபார்க்கவில்லை. இவற்றில் ஏதாவது ஒரு மொழி உங்களுக்குத் தெரிந்தால், [உங்கள் உதவியை வரவேற்கிறோம்](CONTRIBUTING.md#help-wanted).

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

உங்கள் text Claude-உடனான உங்கள் சொந்த chat-இல் மட்டுமே இருக்கும். இந்த skill உங்கள் எழுத்தை எங்கும் save செய்யாது, அனுப்பாது. அப்படி நடக்கக்கூடும் என்று எப்போதாவது தோன்றினால், [தனிப்பட்ட முறையில் எங்களிடம் சொல்லுங்கள்](SECURITY.md).

<a name="contributing"></a>
## பங்களியுங்கள்

நாங்கள் விட்டுப்போன AI பழக்கம் ஏதாவது தெரியுமா? உங்கள் மொழியையோ புதிய எழுத்து வகையையோ சேர்க்க வேண்டுமா? Contributions-ஐ வரவேற்கிறோம். [CONTRIBUTING.md](CONTRIBUTING.md)-இலிருந்து தொடங்குங்கள், [Code of Conduct](CODE_OF_CONDUCT.md)-ஐப் பின்பற்றுங்கள்.

Bug கண்டுபிடித்தீர்களா? [ஒரு issue திறங்கள்](https://github.com/thisiskurubaran/WriteLikeHuman/issues/new/choose). உங்கள் உண்மையான files-க்குப் பதிலாக கற்பனையாக உருவாக்கிய text-ஐப் பயன்படுத்துங்கள்.

## License

[MIT License](LICENSE)-இன் கீழ் வெளியிடப்பட்டது. பயன்படுத்துங்கள், பகிருங்கள், மேம்படுத்துங்கள்.
