# WriteLikeHuman install करना

> यह English [INSTALL guide](INSTALL.md) का हिंदी अनुवाद है। असली version English वाला है, और वह इससे नया हो सकता है। अगर आपकी भाषा हिंदी है और कुछ अटपटा लगे, तो सुधार भेजिए, [यहाँ देखें कैसे](CONTRIBUTING.md#help-wanted)।

यह guide उन लोगों के लिए है जिन्होंने Claude में पहले कभी कुछ install नहीं किया। लगभग दो मिनट लगते हैं। और यह सिर्फ़ एक बार करना है।

Claude app के buttons और menu English में होते हैं, इसलिए उनके नाम यहाँ भी English में ही लिखे हैं, ताकि आप screen पर वही ढूँढ सकें।

## क्या चाहिए

- एक Claude account. Skills Free, Pro, Max, Ultra, Team और Enterprise plans पर चलती हैं।
- पहले step के लिए एक computer. Skill को Claude की website या desktop app पर upload करते हैं। उसके बाद phone पर भी इस्तेमाल कर सकते हैं।
- `WriteLikeHuman.zip` file. यह [Releases page](https://github.com/thisiskurubaran/WriteLikeHuman/releases) से मिलेगी।

Skill कुछ छोटे निर्देशों का एक set है, जिसे Claude ज़रूरत पड़ने पर पढ़ता है। WriteLikeHuman एक ही skill है। एक zip install कीजिए और सब कुछ उसमें आ जाता है।

## Step 1: Zip download कीजिए

1. [Releases page](https://github.com/thisiskurubaran/WriteLikeHuman/releases) खोलिए।
2. सबसे ऊपर सबसे नया release देखिए।
3. **Assets** के नीचे `WriteLikeHuman.zip` पर click कीजिए।
4. File को वैसे ही रहने दीजिए। उसे unzip मत कीजिए।

## Step 2: Claude में file creation चालू कीजिए

Skills के लिए Claude की "code execution" setting चालू होनी चाहिए। इसी setting से Claude आपके लिए files बना और edit कर पाता है।

1. [claude.ai](https://claude.ai) पर जाइए या Claude desktop app खोलिए।
2. नीचे बाएँ कोने में अपने नाम या initials पर click कीजिए।
3. **Settings** पर click कीजिए।
4. **Capabilities** पर click कीजिए।
5. **Code execution and file creation** ढूँढिए। नए versions में इसका नाम **Create and edit files** हो सकता है।
6. इसे चालू कर दीजिए।

Team या Enterprise plan पर हो सकता है कि आपकी organization के owner को पहले सबके लिए इसे चालू करना पड़े। Setting न मिले तो उनसे पूछिए।

## Step 3: Skill upload कीजिए

1. Claude में **Customize** पर जाइए, फिर **Skills** पर।
2. **+** button पर click कीजिए।
3. **+ Create skill** पर click कीजिए।
4. **Upload a skill** पर click कीजिए।
5. जो `WriteLikeHuman.zip` download की थी, उसे चुनिए।
6. पूरा होने तक रुकिए। अब WriteLikeHuman आपकी skills की list में दिखेगा।
7. पक्का कर लीजिए कि उसके आगे वाला switch on है।

बस इतना ही। नई chat शुरू कीजिए और आज़माइए।

## Phone पर इस्तेमाल

1. पहले website या desktop app पर skill upload कीजिए (ऊपर के step 1 से 3)।
2. Phone पर Claude app खोलिए और उसी account से sign in कीजिए।
3. नई chat शुरू कीजिए और कुछ माँगिए, जैसे "Make this message sound less robotic"।

Skills आपके account से जुड़ी होती हैं, इसलिए phone app में भी वही चलती हैं। अगर phone पर काम न करे, तो देखिए कि आप उसी account से sign in हैं, फिर website पर दोबारा कोशिश कीजिए।

## Claude Code में इस्तेमाल

यह हिस्सा सिर्फ़ उनके लिए है जो Claude Code इस्तेमाल करते हैं, यानी Claude का वह version जो terminal में चलता है। ज़्यादातर लोग इसे छोड़ सकते हैं।

1. `WriteLikeHuman.zip` download करके unzip कीजिए।
2. `write-like-human` folder को `~/.claude/skills/` में copy कीजिए (folder न हो तो बना लीजिए)।
3. Claude Code चालू कीजिए। Skill अपने आप load हो जाएगी।

आख़िर में आपके पास `~/.claude/skills/write-like-human/SKILL.md` होना चाहिए।

## इस्तेमाल कैसे करें

बस अपने शब्दों में पूछिए। कोई ख़ास command नहीं चाहिए। कुछ चीज़ें आज़माइए:

- "Make this email sound less robotic"
- "Humanize this Word file" (फिर file लगाइए)
- "Does this sound like AI?"
- "Write a farewell speech for my manager"
- "Reply to this WhatsApp from my landlord"
- "Make this simpler for my dad"
- "Show me each change so I can approve it"

हिंदी या Hinglish में भी चलेगा, जैसे "यह message थोड़ा natural बना दो" या "Boss ko leave ke liye email likh do"।

पहले आपको आपका text वापस मिलता है, फिर एक छोटी list कि क्या बदला और क्यों। File भेजेंगे तो नई copy मिलेगी जिसके नाम के आख़िर में `-humanized` होगा। आपकी असली file वैसी ही रहती है।

## कुछ काम नहीं कर रहा?

**Upload fail हो रहा है।**
आमतौर पर इसका मतलब है कि zip को खोलकर हाथ से दोबारा zip किया गया है। Zip के अंदर `write-like-human` folder होना चाहिए, उसके अंदर की अलग-अलग files नहीं। [Releases page](https://github.com/thisiskurubaran/WriteLikeHuman/releases) से नई copy download कीजिए और बिना unzip किए upload कीजिए। अगर zip आपने ख़ुद बनाई है, तो folder को zip कीजिए, उसके अंदर की files को नहीं।

**Upload वाला button नहीं दिख रहा।**
Step 2 दोबारा देखिए। Code execution and file creation चालू होनी चाहिए। Office वाले account पर हो सकता है आपकी organization ने skills बंद रखी हों। अपने admin से पूछिए।

**Claude skill इस्तेमाल नहीं कर रहा।**
Message में उसका नाम लिखिए, जैसे: "Use WriteLikeHuman to make this sound more natural." यह भी देखिए कि **Customize > Skills** में उसके आगे वाला switch on है।

**File बहुत बड़ी है।**
बहुत बड़ी files upload होने में fail हो सकती हैं या बहुत समय ले सकती हैं। एक बार में एक chapter या कुछ pages भेजिए, या text सीधे chat में paste कर दीजिए।

**कुछ ऐसा बदल दिया जो नहीं बदलना था।**
GitHub पर issue खोलकर हमें बताइए। जो हुआ उसे बनाए हुए text से समझाइए। अपनी असली personal files मत लगाइए।
