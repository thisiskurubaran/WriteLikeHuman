# WriteLikeHuman-ஐ install செய்வது

> இது English [INSTALL guide](INSTALL.md)-இன் தமிழ் மொழிபெயர்ப்பு. முதன்மையானது English version தான், அது இதைவிடப் புதியதாக இருக்கலாம். தமிழ் உங்கள் தாய்மொழி என்றால், ஏதாவது சரியில்லாமல் தோன்றினால் திருத்தி அனுப்புங்கள், [எப்படி என்று இங்கே பாருங்கள்](CONTRIBUTING.md#help-wanted).

இதுவரை Claude-இல் எதையும் install செய்யாதவர்களுக்கான guide இது. சுமார் இரண்டு நிமிடம் ஆகும். ஒரே ஒரு முறை செய்தால் போதும்.

Claude app-இன் buttons, menus எல்லாம் English-இல் இருக்கும். அதனால் அவற்றின் பெயர்களை இங்கேயும் English-இலேயே எழுதியிருக்கிறோம், screen-இல் அதையே தேடலாம்.

## என்ன தேவை

- ஒரு Claude account. Skills, Free, Pro, Max, Ultra, Team, Enterprise plans-இல் வேலை செய்யும்.
- முதல் step-க்கு ஒரு computer. Skill-ஐ Claude website அல்லது desktop app-இல் upload செய்ய வேண்டும். அதன் பிறகு phone-இலும் பயன்படுத்தலாம்.
- `WriteLikeHuman.zip` file. இது [Releases page](https://github.com/thisiskurubaran/WriteLikeHuman/releases)-இல் கிடைக்கும்.

Skill என்பது, தேவைப்படும்போது Claude படிக்கும் சில சிறிய வழிமுறைகளின் தொகுப்பு. WriteLikeHuman ஒரே ஒரு skill. ஒரு zip-ஐ install செய்தால் எல்லாமே அதில் அடங்கும்.

## Step 1: Zip-ஐ download செய்யுங்கள்

1. [Releases page](https://github.com/thisiskurubaran/WriteLikeHuman/releases)-ஐத் திறங்கள்.
2. மேலே உள்ள புதிய release-ஐப் பாருங்கள்.
3. **Assets** கீழே உள்ள `WriteLikeHuman.zip`-ஐ click செய்யுங்கள்.
4. File-ஐ அப்படியே விடுங்கள். Unzip செய்ய வேண்டாம்.

## Step 2: Claude-இல் file creation-ஐ on செய்யுங்கள்

Skills வேலை செய்ய Claude-இன் "code execution" setting on-இல் இருக்க வேண்டும். இந்த setting இருந்தால்தான் Claude உங்களுக்காக files உருவாக்கவும் edit செய்யவும் முடியும்.

1. [claude.ai](https://claude.ai)-க்குப் போங்கள் அல்லது Claude desktop app-ஐத் திறங்கள்.
2. கீழே இடது மூலையில் உங்கள் பெயர் அல்லது initials-ஐ click செய்யுங்கள்.
3. **Settings**-ஐ click செய்யுங்கள்.
4. **Capabilities**-ஐ click செய்யுங்கள்.
5. **Code execution and file creation**-ஐத் தேடுங்கள். புதிய versions-இல் இதன் பெயர் **Create and edit files** என்று இருக்கலாம்.
6. அதை on செய்யுங்கள்.

Team அல்லது Enterprise plan என்றால், உங்கள் organization owner முதலில் எல்லோருக்கும் இதை on செய்ய வேண்டியிருக்கலாம். Setting கிடைக்கவில்லை என்றால் அவர்களிடம் கேளுங்கள்.

## Step 3: Skill-ஐ upload செய்யுங்கள்

1. Claude-இல் **Customize**-க்குப் போய், பிறகு **Skills**-க்குப் போங்கள்.
2. **+** button-ஐ click செய்யுங்கள்.
3. **+ Create skill**-ஐ click செய்யுங்கள்.
4. **Upload a skill**-ஐ click செய்யுங்கள்.
5. நீங்கள் download செய்த `WriteLikeHuman.zip`-ஐத் தேர்ந்தெடுங்கள்.
6. முடியும் வரை காத்திருங்கள். இப்போது WriteLikeHuman உங்கள் skills பட்டியலில் தெரியும்.
7. அதன் பக்கத்தில் உள்ள switch on-இல் இருக்கிறதா என்று உறுதிசெய்யுங்கள்.

அவ்வளவுதான். ஒரு புதிய chat தொடங்கி முயற்சி செய்யுங்கள்.

## Phone-இல் பயன்படுத்துவது

1. முதலில் website அல்லது desktop app-இல் skill-ஐ upload செய்யுங்கள் (மேலே உள்ள step 1 முதல் 3 வரை).
2. Phone-இல் Claude app-ஐத் திறந்து அதே account-இல் sign in செய்யுங்கள்.
3. புதிய chat தொடங்கி ஏதாவது கேளுங்கள், உதாரணமாக "Make this message sound less robotic".

Skills உங்கள் account-உடன் இணைந்தவை, அதனால் phone app-இலும் அவையே வேலை செய்யும். Phone-இல் வேலை செய்யவில்லை என்றால், அதே account-இல் sign in செய்திருக்கிறீர்களா என்று பார்த்து, website-இல் மீண்டும் முயற்சி செய்யுங்கள்.

## Claude Code-இல் பயன்படுத்துவது

இந்தப் பகுதி Claude Code பயன்படுத்துபவர்களுக்கு மட்டும், அதாவது terminal-இல் ஓடும் Claude version. பெரும்பாலானவர்கள் இதைத் தவிர்க்கலாம்.

1. `WriteLikeHuman.zip`-ஐ download செய்து unzip செய்யுங்கள்.
2. `write-like-human` folder-ஐ `~/.claude/skills/`-க்குள் copy செய்யுங்கள் (folder இல்லையென்றால் உருவாக்குங்கள்).
3. Claude Code-ஐத் தொடங்குங்கள். Skill தானாகவே load ஆகும்.

கடைசியில் உங்களிடம் `~/.claude/skills/write-like-human/SKILL.md` இருக்க வேண்டும்.

## எப்படிப் பயன்படுத்துவது

உங்கள் வார்த்தைகளிலேயே கேளுங்கள். சிறப்பு commands எதுவும் தேவையில்லை. இவற்றை முயற்சி செய்யுங்கள்:

- "Make this email sound less robotic"
- "Humanize this Word file" (பிறகு file-ஐ இணையுங்கள்)
- "Does this sound like AI?"
- "Write a farewell speech for my manager"
- "Reply to this WhatsApp from my landlord"
- "Make this simpler for my dad"
- "Show me each change so I can approve it"

தமிழிலோ Tanglish-இலோ கூட வேலை செய்யும், உதாரணமாக "இந்த message-ஐக் கொஞ்சம் இயல்பா மாத்துங்க" அல்லது "Manager-ku leave kekka oru email ezhudhunga".

முதலில் உங்கள் text திரும்ப வரும், பிறகு என்ன மாறியது, ஏன் என்று ஒரு சிறிய பட்டியல். File அனுப்பினால், பெயரின் முடிவில் `-humanized` என்று உள்ள புதிய copy கிடைக்கும். உங்கள் original file அப்படியே இருக்கும்.

## ஏதாவது வேலை செய்யவில்லையா?

**Upload fail ஆகிறது.**
பொதுவாக இதன் அர்த்தம், zip-ஐத் திறந்து கையால் மீண்டும் zip செய்திருக்கிறீர்கள் என்பது. Zip-க்குள் `write-like-human` folder இருக்க வேண்டும், அதற்குள் உள்ள தனித்தனி files அல்ல. [Releases page](https://github.com/thisiskurubaran/WriteLikeHuman/releases)-இலிருந்து புதிய copy-ஐ download செய்து, unzip செய்யாமல் upload செய்யுங்கள். நீங்களே zip உருவாக்கினால், folder-ஐயே zip செய்யுங்கள், அதற்குள் உள்ளவற்றை அல்ல.

**Upload button தெரியவில்லை.**
Step 2-ஐ மீண்டும் பாருங்கள். Code execution and file creation on-இல் இருக்க வேண்டும். அலுவலக account என்றால், உங்கள் organization skills-ஐ off செய்திருக்கலாம். உங்கள் admin-இடம் கேளுங்கள்.

**Claude skill-ஐப் பயன்படுத்தவில்லை.**
உங்கள் message-இல் அதன் பெயரைச் சொல்லுங்கள், உதாரணமாக: "Use WriteLikeHuman to make this sound more natural." **Customize > Skills**-இல் அதன் பக்கத்தில் உள்ள switch on-இல் இருக்கிறதா என்றும் பாருங்கள்.

**File மிகப் பெரியதாக இருக்கிறது.**
மிகப் பெரிய files upload ஆகாமல் போகலாம் அல்லது நீண்ட நேரம் எடுக்கலாம். ஒரு நேரத்தில் ஒரு chapter அல்லது சில pages அனுப்புங்கள், அல்லது text-ஐ நேரடியாக chat-இல் paste செய்யுங்கள்.

**மாற்றக்கூடாத ஒன்றை மாற்றிவிட்டது.**
GitHub-இல் ஒரு issue திறந்து எங்களிடம் சொல்லுங்கள். என்ன நடந்தது என்பதைக் கற்பனையாக உருவாக்கிய text வைத்து விளக்குங்கள். உங்கள் உண்மையான தனிப்பட்ட files-ஐ இணைக்க வேண்டாம்.
