# AnkiDroid Card Template API Reference

This document provides comprehensive documentation for all APIs available in AnkiDroid card templates. Card templates support two main approaches:

1. **Template Syntax** - Double curly brace `{{...}}` notation for field replacement and filters
2. **JavaScript API** - `AnkiDroidJS` API for dynamic card behavior and interactions

---

## Table of Contents

- [Template Syntax (Mustache-like)](#template-syntax-mustache-like)
  - [Basic Field Replacement](#basic-field-replacement)
  - [Conditional Sections](#conditional-sections)
  - [Built-in Filters](#built-in-filters)
  - [Special Variables](#special-variables)
  - [Filter Chaining](#filter-chaining)
- [JavaScript API (AnkiDroidJS)](#javascript-api-ankidroidjs)
  - [Initialization](#initialization)
  - [Card Information APIs](#card-information-apis)
  - [Card Action APIs](#card-action-apis)
  - [Reviewer Control APIs](#reviewer-control-apis)
  - [Text-to-Speech APIs](#text-to-speech-apis)
  - [Speech-to-Text APIs](#speech-to-text-apis)
  - [UI Control APIs](#ui-control-apis)
  - [Tag Management APIs](#tag-management-apis)
  - [Other APIs](#other-apis)

---

## Template Syntax (Mustache-like)

AnkiDroid uses a Mustache-like template syntax for rendering card content. Templates are processed server-side by the Rust backend and support various filters and replacements.

### Basic Field Replacement

Replace field content with the value from your note.

#### Syntax
```html
{{FieldName}}
```

#### Example
```html
<!-- Front Template -->
<div class="question">{{Front}}</div>

<!-- Back Template -->
<div class="answer">{{Back}}</div>
```

**Result:** If the note has a "Front" field with value "Hello", it will render as:
```html
<div class="question">Hello</div>
```

---

### Conditional Sections

Show or hide content based on whether a field is empty or not.

#### Positive Conditional - Show if field has content

**Syntax:**
```html
{{#FieldName}}
  Content to show if field is not empty
{{/FieldName}}
```

**Example:**
```html
{{#Pronunciation}}
  <div class="pronunciation">[{{Pronunciation}}]</div>
{{/Pronunciation}}
```

**Result:** The div will only appear if the "Pronunciation" field has content.

#### Negative Conditional - Show if field is empty

**Syntax:**
```html
{{^FieldName}}
  Content to show if field is empty
{{/FieldName}}
```

**Example:**
```html
{{^Image}}
  <p>No image available</p>
{{/Image}}
```

**Result:** The paragraph will only appear if the "Image" field is empty.

---

### Built-in Filters

Filters modify field content before displaying. Apply filters using the colon `:` separator.

#### `text:` - Strip HTML Tags

Removes all HTML formatting, leaving only plain text.

**Syntax:**
```html
{{text:FieldName}}
```

**Example:**
```html
{{text:Front}}
```

**Input:** `<b>Hello</b> <i>World</i>`  
**Output:** `Hello World`

---

#### `type:` - Type-in-the-answer Box

Creates an input field for typing answers. Commonly used for testing recall.

**Syntax:**
```html
{{type:FieldName}}
```

**Example:**
```html
<!-- Front Template -->
<p>What is the capital of France?</p>
{{type:Answer}}

<!-- Back Template -->
{{FrontSide}}
<hr id=answer>
<p>{{Answer}}</p>
```

**Result:** On the front, shows a text input. On the back, compares typed answer with the actual answer and highlights differences.

---

#### `cloze:` - Process Cloze Deletions

Handles cloze deletion cards (fill-in-the-blank style).

**Syntax:**
```html
{{cloze:FieldName}}
```

**Example:**
```html
<!-- Template -->
{{cloze:Text}}

<!-- Note content -->
Text field: "{{c1::Paris}} is the capital of {{c2::France}}"
```

**Result Card 1:** `[...] is the capital of France`  
**Result Card 2:** `Paris is the capital of [...]`

**Note:** Cloze deletions use `{{c1::text}}`, `{{c2::text}}`, etc. in the field content.

---

#### `type:cloze:` - Type Answer for Cloze

Combines type-answer with cloze deletions.

**Syntax:**
```html
{{type:cloze:FieldName}}
```

**Example:**
```html
<!-- Front Template -->
{{type:cloze:Text}}

<!-- Note content -->
Text: "The speed of light is {{c1::299,792,458}} m/s"
```

**Result:** Shows a type-in box where you must type "299,792,458".

---

#### `hint:` - Collapsible Hint

Shows content as a collapsible hint that can be revealed.

**Syntax:**
```html
{{hint:FieldName}}
```

**Example:**
```html
{{hint:ExtraInfo}}
```

**Result:** Creates a clickable "Show Hint" link that reveals the field content when clicked.

---

#### `furigana:` - Extract Furigana Reading

Extracts furigana (pronunciation guide) from Japanese text.

**Syntax:**
```html
{{furigana:FieldName}}
```

**Example:**
```html
{{furigana:Expression}}
```

**Input:** `漢字[かんじ]`  
**Output:** ` かんじ`

---

#### `kanji:` - Extract Kanji Only

Removes furigana, keeping only the kanji characters.

**Syntax:**
```html
{{kanji:FieldName}}
```

**Example:**
```html
{{kanji:Expression}}
```

**Input:** `漢字[かんじ]`  
**Output:** `漢字`

---

#### `kana:` - Extract Kana Only

Extracts only kana (hiragana/katakana) from Japanese text.

**Syntax:**
```html
{{kana:FieldName}}
```

**Example:**
```html
{{kana:Reading}}
```

---

#### `tts` - Text-to-Speech (Limited Support)

Marks text for text-to-speech playback. 

**Syntax:**
```html
{{tts:FieldName}}
{{tts-voices:}}
```

**Note:** Current AnkiDroid implementation has limited support. Use the JavaScript TTS API for full functionality.

---

### Special Variables

Special variables provide metadata about the card and its context.

#### `{{FrontSide}}` - Include Front Template

On the back of the card, inserts the fully-rendered front template.

**Syntax:**
```html
{{FrontSide}}
```

**Example:**
```html
<!-- Back Template -->
{{FrontSide}}
<hr id=answer>
<div class="answer">{{Back}}</div>
```

**Result:** The back shows everything from the front, followed by a divider and the answer.

**Important:** `{{FrontSide}}` on the front template returns an empty string.

---

#### `{{Tags}}` - Note Tags

Displays all tags associated with the note.

**Syntax:**
```html
{{Tags}}
```

**Example:**
```html
<div class="tags">{{Tags}}</div>
```

**Result:** If note has tags "vocab grammar", displays: `vocab grammar`

---

#### `{{Type}}` - Card Type/Template Name

The name of the card template.

**Syntax:**
```html
{{Type}}
```

---

#### `{{Deck}}` - Full Deck Name

The complete deck path.

**Syntax:**
```html
{{Deck}}
```

**Example Output:** `Spanish::Verbs::Irregular`

---

#### `{{Subdeck}}` - Subdeck Name

Only the subdeck portion of the deck name.

**Syntax:**
```html
{{Subdeck}}
```

**Example:** For deck "Spanish::Verbs::Irregular", returns: `Irregular`

---

#### `{{Card}}` - Card Template Name

The name of the current card template.

**Syntax:**
```html
{{Card}}
```

---

#### Cloze Numbers `{{c1}}`, `{{c2}}`, etc.

In cloze deletion templates, represents the cloze number.

**Syntax:**
```html
{{c1}}
```

---

### Filter Chaining

Apply multiple filters in sequence by chaining them with colons.

**Syntax:**
```html
{{filter1:filter2:filter3:FieldName}}
```

**Example:**
```html
{{text:cloze:Text}}
```

**Result:** First applies cloze deletion processing, then strips HTML tags.

**Example:**
```html
{{kanji:furigana:Expression}}
```

**Processing Order:** 
1. Extract furigana from Expression field
2. Then extract only kanji from the result

---

## JavaScript API (AnkiDroidJS)

The AnkiDroidJS API provides JavaScript functions for dynamic card behavior, accessing card data, controlling the reviewer, and more.

### Initialization

Before using any API functions, you must initialize the API with your contact information.

#### `AnkiDroidJS.init()`

**Syntax:**
```javascript
const api = AnkiDroidJS.init({ 
    developer: "your-contact-info", 
    version: "0.0.3" 
});
```

**Parameters:**
- `developer` (string, required): Your contact information (email or website) for tracking purposes
- `version` (string, required): API version, must be `"0.0.3"`

**Example:**
```javascript
const api = AnkiDroidJS.init({ 
    developer: "email@example.com", 
    version: "0.0.3" 
});

// Now you can use API functions
const cardId = await api.ankiGetCardId();
```

**Important Notes:**
- The API requires initialization to track add-on developers
- Current API version is `0.0.3`
- Minimum supported version is `0.0.3`
- Using older or newer versions may result in compatibility warnings

---

### Card Information APIs

Retrieve information about the current card, its properties, and review statistics.

#### `ankiGetNewCardCount()`

Get the count of new cards remaining in the deck.

**Returns:** `Promise<number>` - Number of new cards

**Example:**
```javascript
const newCards = await api.ankiGetNewCardCount();
console.log(`${newCards} new cards remaining`);
```

---

#### `ankiGetLrnCardCount()`

Get the count of learning cards (cards currently in the learning queue).

**Returns:** `Promise<number>` - Number of learning cards

**Example:**
```javascript
const learningCards = await api.ankiGetLrnCardCount();
console.log(`${learningCards} cards in learning`);
```

---

#### `ankiGetRevCardCount()`

Get the count of review cards due today.

**Returns:** `Promise<number>` - Number of review cards

**Example:**
```javascript
const reviewCards = await api.ankiGetRevCardCount();
console.log(`${reviewCards} cards due for review`);
```

---

#### `ankiGetETA()`

Get the estimated time (in minutes) to complete remaining reviews.

**Returns:** `Promise<number>` - Estimated time in minutes

**Example:**
```javascript
const eta = await api.ankiGetETA();
console.log(`Estimated ${eta} minutes remaining`);
```

---

#### `ankiGetCardMark()`

Check if the current card is marked.

**Returns:** `Promise<boolean>` - `true` if card is marked, `false` otherwise

**Example:**
```javascript
const isMarked = await api.ankiGetCardMark();
if (isMarked) {
    console.log("This card is marked for review");
}
```

---

#### `ankiGetCardFlag()`

Get the flag color of the current card.

**Returns:** `Promise<number>` - Flag value (0 = no flag, 1-7 = different colors)

**Flag Values:**
- `0` - No flag
- `1` - Red
- `2` - Orange
- `3` - Green
- `4` - Blue
- `5` - Pink
- `6` - Turquoise
- `7` - Purple

**Example:**
```javascript
const flag = await api.ankiGetCardFlag();
const flagNames = ['None', 'Red', 'Orange', 'Green', 'Blue', 'Pink', 'Turquoise', 'Purple'];
console.log(`Card flag: ${flagNames[flag]}`);
```

---

#### `ankiGetNextTime1()` / `ankiGetNextTime2()` / `ankiGetNextTime3()` / `ankiGetNextTime4()`

Get the next review interval for each answer button (Again/Hard/Good/Easy).

**Returns:** `Promise<string>` - Formatted interval string (e.g., "10m", "2d", "1.5mo")

**Example:**
```javascript
const time1 = await api.ankiGetNextTime1(); // Again
const time2 = await api.ankiGetNextTime2(); // Hard
const time3 = await api.ankiGetNextTime3(); // Good
const time4 = await api.ankiGetNextTime4(); // Easy

console.log(`Again: ${time1}, Hard: ${time2}, Good: ${time3}, Easy: ${time4}`);
```

---

#### `ankiGetCardReps()`

Get the number of times the card has been reviewed.

**Returns:** `Promise<number>` - Review count

**Example:**
```javascript
const reps = await api.ankiGetCardReps();
console.log(`Reviewed ${reps} times`);
```

---

#### `ankiGetCardInterval()`

Get the current interval of the card in days.

**Returns:** `Promise<number>` - Interval in days

**Example:**
```javascript
const interval = await api.ankiGetCardInterval();
console.log(`Current interval: ${interval} days`);
```

---

#### `ankiGetCardFactor()`

Get the ease factor of the card (as a percentage multiplied by 10).

**Returns:** `Promise<number>` - Ease factor (e.g., 2500 = 250%)

**Example:**
```javascript
const factor = await api.ankiGetCardFactor();
console.log(`Ease: ${factor / 10}%`);
```

---

#### `ankiGetCardMod()`

Get the modification timestamp of the card.

**Returns:** `Promise<number>` - Unix timestamp (seconds)

**Example:**
```javascript
const mod = await api.ankiGetCardMod();
const modDate = new Date(mod * 1000);
console.log(`Last modified: ${modDate.toLocaleString()}`);
```

---

#### `ankiGetCardId()`

Get the unique ID of the current card.

**Returns:** `Promise<number>` - Card ID

**Example:**
```javascript
const cardId = await api.ankiGetCardId();
console.log(`Card ID: ${cardId}`);
```

---

#### `ankiGetCardNid()`

Get the note ID associated with the current card.

**Returns:** `Promise<number>` - Note ID

**Example:**
```javascript
const noteId = await api.ankiGetCardNid();
console.log(`Note ID: ${noteId}`);
```

---

#### `ankiGetCardType()`

Get the card type (new/learning/review).

**Returns:** `Promise<number>` - Type code (0=new, 1=learning, 2=review, 3=relearning)

**Example:**
```javascript
const type = await api.ankiGetCardType();
const typeNames = ['New', 'Learning', 'Review', 'Relearning'];
console.log(`Card type: ${typeNames[type]}`);
```

---

#### `ankiGetCardDid()`

Get the deck ID containing the current card.

**Returns:** `Promise<number>` - Deck ID

**Example:**
```javascript
const deckId = await api.ankiGetCardDid();
console.log(`Deck ID: ${deckId}`);
```

---

#### `ankiGetCardQueue()`

Get the queue the card is currently in.

**Returns:** `Promise<number>` - Queue code

**Example:**
```javascript
const queue = await api.ankiGetCardQueue();
console.log(`Queue: ${queue}`);
```

---

#### `ankiGetCardLapses()`

Get the number of times the card has been forgotten (lapsed).

**Returns:** `Promise<number>` - Lapse count

**Example:**
```javascript
const lapses = await api.ankiGetCardLapses();
console.log(`Lapsed ${lapses} times`);
```

---

#### `ankiGetCardDue()`

Get the due date of the card.

**Returns:** `Promise<number>` - Due value (interpretation depends on queue)

**Example:**
```javascript
const due = await api.ankiGetCardDue();
console.log(`Due: ${due}`);
```

---

#### `ankiGetDeckName()`

Get the name of the current deck (basename only, not full path).

**Returns:** `Promise<string>` - Deck name

**Example:**
```javascript
const deckName = await api.ankiGetDeckName();
console.log(`Current deck: ${deckName}`);
```

---

### Card Action APIs

Perform actions on cards such as marking, flagging, burying, suspending, and more.

#### `ankiMarkCard()`

Toggle the mark status of the current card.

**Returns:** `Promise<boolean>` - `true` if successful

**Example:**
```javascript
await api.ankiMarkCard();
console.log("Card mark toggled");
```

---

#### `ankiToggleFlag(flagColor)`

Toggle a flag on the current card.

**Parameters:**
- `flagColor` (string): One of: `"none"`, `"red"`, `"orange"`, `"green"`, `"blue"`, `"pink"`, `"turquoise"`, `"purple"`

**Returns:** `Promise<boolean>` - `true` if successful

**Example:**
```javascript
// Set red flag
await api.ankiToggleFlag("red");

// Remove flag
await api.ankiToggleFlag("none");
```

---

#### `ankiBuryCard()`

Bury the current card (hide it until the next day).

**Returns:** `Promise<boolean>` - `true` if successful

**Example:**
```javascript
await api.ankiBuryCard();
console.log("Card buried");
```

---

#### `ankiBuryNote()`

Bury all cards from the current note.

**Returns:** `Promise<boolean>` - `true` if successful

**Example:**
```javascript
await api.ankiBuryNote();
console.log("All cards from this note buried");
```

---

#### `ankiSuspendCard()`

Suspend the current card (prevent it from appearing in reviews).

**Returns:** `Promise<boolean>` - `true` if successful

**Example:**
```javascript
await api.ankiSuspendCard();
console.log("Card suspended");
```

---

#### `ankiSuspendNote()`

Suspend all cards from the current note.

**Returns:** `Promise<boolean>` - `true` if successful

**Example:**
```javascript
await api.ankiSuspendNote();
console.log("All cards from this note suspended");
```

---

#### `ankiAddTagToCard()`

**DEPRECATED** - Opens the tag dialog for adding tags to the card. Use `ankiSetNoteTags()` instead.

**Returns:** `Promise<boolean>` - `true` if successful

**Example:**
```javascript
// Opens tag dialog
await api.ankiAddTagToCard();
```

---

#### `ankiResetProgress()`

Reset the review progress of the current card (as if it were new).

**Returns:** `Promise<boolean>` - `true` if successful

**Example:**
```javascript
await api.ankiResetProgress();
console.log("Card progress reset");
```

---

#### `ankiSearchCard(query)`

Search for cards and open the Card Browser with results.

**Parameters:**
- `query` (string): Search query (uses Anki search syntax)

**Returns:** `Promise<boolean>` - `true` if successful

**Example:**
```javascript
// Search for cards with tag "difficult"
await api.ankiSearchCard("tag:difficult");

// Search for cards in current deck
await api.ankiSearchCard("deck:current");
```

---

#### `ankiSearchCardWithCallback(query)`

Search for cards and receive results in a callback function.

**Parameters:**
- `query` (string): Search query

**Callback:** Results are returned via `ankiSearchCard()` JavaScript function

**Example:**
```javascript
// Define callback function to receive results
function ankiSearchCard(jsonResults) {
    const results = JSON.parse(jsonResults);
    results.forEach(card => {
        console.log(`Card ID: ${card.cardId}`);
        console.log(`Note ID: ${card.noteId}`);
        console.log(`Fields:`, card.fieldsData);
    });
}

// Trigger search
await api.ankiSearchCardWithCallback("tag:review");
```

---

#### `ankiSetCardDue(days)`

Set the due date of the current card.

**Parameters:**
- `days` (number): Number of days from today (0-9999)

**Returns:** `Promise<boolean>` - `true` if successful

**Example:**
```javascript
// Review this card in 7 days
await api.ankiSetCardDue(7);

// Review today
await api.ankiSetCardDue(0);
```

---

### Reviewer Control APIs

Control the card reviewer interface and answer cards programmatically.

#### `ankiIsDisplayingAnswer()`

Check if the answer side is currently displayed.

**Returns:** `Promise<boolean>` - `true` if showing answer, `false` if showing question

**Example:**
```javascript
const showingAnswer = await api.ankiIsDisplayingAnswer();
if (showingAnswer) {
    console.log("Showing answer side");
} else {
    console.log("Showing question side");
}
```

---

#### `ankiShowAnswer()`

Flip the card to show the answer.

**Returns:** `Promise<boolean>` - `true` if successful

**Example:**
```javascript
await api.ankiShowAnswer();
```

---

#### `ankiAnswerEase1()` / `ankiAnswerEase2()` / `ankiAnswerEase3()` / `ankiAnswerEase4()`

Answer the card with a specific ease button.

- `ankiAnswerEase1()` - Answer "Again" (failed)
- `ankiAnswerEase2()` - Answer "Hard"
- `ankiAnswerEase3()` - Answer "Good"
- `ankiAnswerEase4()` - Answer "Easy"

**Returns:** `Promise<boolean>` - `true` if successful

**Example:**
```javascript
// Answer "Good"
await api.ankiAnswerEase3();

// Create custom answer buttons
document.getElementById('againBtn').onclick = () => api.ankiAnswerEase1();
document.getElementById('hardBtn').onclick = () => api.ankiAnswerEase2();
document.getElementById('goodBtn').onclick = () => api.ankiAnswerEase3();
document.getElementById('easyBtn').onclick = () => api.ankiAnswerEase4();
```

---

### Text-to-Speech APIs

Control text-to-speech functionality for audio playback of card content.

#### `ankiTtsSpeak(text, queueMode)`

Speak text using text-to-speech.

**Parameters:**
- `text` (string): Text to speak
- `queueMode` (number, optional, default=0): Queue mode
  - `0` - QUEUE_FLUSH: Stop current speech and speak immediately
  - `1` - QUEUE_ADD: Add to queue after current speech

**Returns:** `Promise<boolean>` - `true` if successful

**Example:**
```javascript
// Speak immediately
await api.ankiTtsSpeak("Hello world", 0);

// Add to queue
await api.ankiTtsSpeak("This is the second sentence", 1);

// Speak field content
const front = document.querySelector('.front').textContent;
await api.ankiTtsSpeak(front);
```

---

#### `ankiTtsSetLanguage(languageCode)`

Set the TTS language.

**Parameters:**
- `languageCode` (string): Language code (e.g., "en-US", "es-ES", "ja-JP")

**Returns:** `Promise<boolean>` - `true` if successful

**Example:**
```javascript
await api.ankiTtsSetLanguage("ja-JP");
await api.ankiTtsSpeak("こんにちは");
```

---

#### `ankiTtsSetPitch(pitch)`

Set the TTS pitch.

**Parameters:**
- `pitch` (number): Pitch value (typically 0.5 to 2.0, default 1.0)

**Returns:** `Promise<boolean>` - `true` if successful

**Example:**
```javascript
// Higher pitch
await api.ankiTtsSetPitch(1.5);

// Lower pitch
await api.ankiTtsSetPitch(0.7);
```

---

#### `ankiTtsSetSpeechRate(rate)`

Set the TTS speech rate.

**Parameters:**
- `rate` (number): Speech rate (typically 0.5 to 2.0, default 1.0)

**Returns:** `Promise<boolean>` - `true` if successful

**Example:**
```javascript
// Faster speech
await api.ankiTtsSetSpeechRate(1.5);

// Slower speech
await api.ankiTtsSetSpeechRate(0.7);
```

---

#### `ankiTtsIsSpeaking()`

Check if TTS is currently speaking.

**Returns:** `Promise<boolean>` - `true` if speaking, `false` otherwise

**Example:**
```javascript
const isSpeaking = await api.ankiTtsIsSpeaking();
if (isSpeaking) {
    console.log("TTS is currently speaking");
}
```

---

#### `ankiTtsStop()`

Stop TTS playback.

**Returns:** `Promise<boolean>` - `true` if successful

**Example:**
```javascript
await api.ankiTtsStop();
```

---

#### `ankiTtsFieldModifierIsAvailable()`

Check if `{{tts}}` field modifier is available.

**Returns:** `Promise<boolean>` - Currently always returns `false`

**Note:** This feature is not yet fully supported in AnkiDroid.

**Example:**
```javascript
const isAvailable = await api.ankiTtsFieldModifierIsAvailable();
console.log(`TTS field modifier available: ${isAvailable}`);
```

---

### Speech-to-Text APIs

Control speech recognition for voice input.

#### `ankiSttSetLanguage(languageCode)`

Set the speech recognition language.

**Parameters:**
- `languageCode` (string): Language code (e.g., "en-US", "es-ES")

**Returns:** `Promise<boolean>` - `true` if successful

**Example:**
```javascript
await api.ankiSttSetLanguage("en-US");
```

---

#### `ankiSttStart()`

Start speech recognition. Results are delivered to the `ankiSttResult()` callback.

**Returns:** `Promise<boolean>` - `true` if started successfully

**Callback:** Results are sent to `ankiSttResult(jsonResult)` function

**Example:**
```javascript
// Define callback to receive results
function ankiSttResult(jsonResult) {
    const result = JSON.parse(jsonResult);
    if (result.success) {
        const transcriptions = JSON.parse(result.value);
        console.log("Recognized:", transcriptions[0]);
    } else {
        console.error("Recognition error:", result.value);
    }
}

// Start listening
document.getElementById('micBtn').onclick = async () => {
    await api.ankiSttStart();
};
```

---

#### `ankiSttStop()`

Stop speech recognition.

**Returns:** `Promise<boolean>` - `true` if successful

**Example:**
```javascript
await api.ankiSttStop();
```

---

### UI Control APIs

Control the AnkiDroid user interface and display elements.

#### `ankiIsInFullscreen()`

Check if the reviewer is in fullscreen mode.

**Returns:** `Promise<boolean>` - `true` if fullscreen, `false` otherwise

**Example:**
```javascript
const isFullscreen = await api.ankiIsInFullscreen();
console.log(`Fullscreen: ${isFullscreen}`);
```

---

#### `ankiIsTopbarShown()`

Check if the top bar is currently shown.

**Returns:** `Promise<boolean>` - `true` if topbar is shown

**Example:**
```javascript
const topbarShown = await api.ankiIsTopbarShown();
console.log(`Topbar visible: ${topbarShown}`);
```

---

#### `ankiIsInNightMode()`

Check if night mode is currently active.

**Returns:** `Promise<boolean>` - `true` if in night mode

**Example:**
```javascript
const isNightMode = await api.ankiIsInNightMode();
if (isNightMode) {
    document.body.classList.add('night-mode');
} else {
    document.body.classList.add('day-mode');
}
```

---

#### `ankiEnableHorizontalScrollbar(enabled)`

Enable or disable the horizontal scrollbar.

**Parameters:**
- `enabled` (boolean): `true` to enable, `false` to disable

**Returns:** `Promise<boolean>` - `true` if successful

**Example:**
```javascript
// Enable horizontal scrolling for wide content
await api.ankiEnableHorizontalScrollbar(true);

// Disable horizontal scrolling
await api.ankiEnableHorizontalScrollbar(false);
```

---

#### `ankiEnableVerticalScrollbar(enabled)`

Enable or disable the vertical scrollbar.

**Parameters:**
- `enabled` (boolean): `true` to enable, `false` to disable

**Returns:** `Promise<boolean>` - `true` if successful

**Example:**
```javascript
// Enable vertical scrolling
await api.ankiEnableVerticalScrollbar(true);

// Disable vertical scrolling
await api.ankiEnableVerticalScrollbar(false);
```

---

#### `ankiShowNavigationDrawer()`

Open the navigation drawer.

**Returns:** `Promise<boolean>` - `true` if successful

**Example:**
```javascript
await api.ankiShowNavigationDrawer();
```

---

#### `ankiShowOptionsMenu()`

Open the options menu.

**Returns:** `Promise<boolean>` - `true` if successful

**Example:**
```javascript
await api.ankiShowOptionsMenu();
```

---

#### `ankiShowToast(text, shortLength)`

Display a toast message.

**Parameters:**
- `text` (string): Message to display
- `shortLength` (boolean, optional, default=true): `true` for short duration, `false` for long duration

**Returns:** `Promise<boolean>` - `true` if successful

**Example:**
```javascript
// Short toast
await api.ankiShowToast("Card marked!", true);

// Long toast
await api.ankiShowToast("Important message", false);
```

---

### Tag Management APIs

Manage tags associated with notes.

#### `ankiAddTagToNote(noteId, tag)` 

**DEPRECATED** - Use `ankiSetNoteTags()` instead.

Add a tag to a specific note.

**Parameters:**
- `noteId` (number): Note ID
- `tag` (string): Tag to add

**Returns:** `Promise<boolean>` - `true` if successful

**Example:**
```javascript
const noteId = await api.ankiGetCardNid();
await api.ankiAddTagToNote(noteId, "important");
```

---

#### `ankiSetNoteTags(tags)`

Set the tags for the current note (replaces all existing tags).

**Parameters:**
- `tags` (Array<string>): Array of tag names

**Returns:** `Promise<boolean>` - `true` if successful

**Important:**
- Spaces in tags are automatically converted to underscores
- Tags are automatically trimmed

**Example:**
```javascript
// Set multiple tags
await api.ankiSetNoteTags(["vocabulary", "lesson-1", "important"]);

// Remove all tags
await api.ankiSetNoteTags([]);

// Spaces are converted to underscores
await api.ankiSetNoteTags(["multi word"]); // Becomes "multi_word"
```

---

#### `ankiGetNoteTags()`

Get all tags from the current note.

**Returns:** `Promise<string>` - JSON string containing array of tags

**Example:**
```javascript
const tagsJson = await api.ankiGetNoteTags();
const tags = JSON.parse(tagsJson);
console.log("Current tags:", tags);
// Output: ["vocabulary", "lesson-1"]
```

---

### Other APIs

Miscellaneous utility functions.

#### `ankiIsActiveNetworkMetered()`

Check if the active network connection is metered (limited data).

**Returns:** `Promise<boolean>` - `true` if metered, `false` otherwise

**Example:**
```javascript
const isMetered = await api.ankiIsActiveNetworkMetered();
if (isMetered) {
    console.log("Warning: Using metered connection");
    // Skip downloading large media files
} else {
    // Safe to download
}
```

---

## Complete Examples

### Example 1: Basic Card Template with Conditional Content

```html
<!-- Front Template -->
<div class="word">{{Word}}</div>

{{#Pronunciation}}
  <div class="pronunciation">[{{Pronunciation}}]</div>
{{/Pronunciation}}

{{#Image}}
  <img src="{{Image}}">
{{/Image}}

<!-- Back Template -->
{{FrontSide}}

<hr id=answer>

<div class="definition">{{Definition}}</div>

{{#Example}}
  <div class="example">
    <strong>Example:</strong><br>
    {{Example}}
  </div>
{{/Example}}

{{#Notes}}
  <div class="notes">
    {{hint:Notes}}
  </div>
{{/Notes}}
```

---

### Example 2: Interactive Card with JavaScript

```html
<!-- Front Template -->
<div id="question">{{Question}}</div>

<button onclick="showHint()">Show Hint</button>
<div id="hint" style="display: none;"></div>

<script>
const api = AnkiDroidJS.init({ 
    developer: "email@example.com", 
    version: "0.0.3" 
});

async function showHint() {
    const hint = "{{Hint}}";
    document.getElementById('hint').innerHTML = hint;
    document.getElementById('hint').style.display = 'block';
    
    await api.ankiShowToast("Hint revealed");
}
</script>

<!-- Back Template -->
{{FrontSide}}

<hr id=answer>

<div class="answer">{{Answer}}</div>

<button onclick="markDifficult()">Mark as Difficult</button>

<script>
async function markDifficult() {
    await api.ankiToggleFlag("red");
    await api.ankiSetNoteTags(["difficult", "review"]);
    await api.ankiShowToast("Marked as difficult");
}
</script>
```

---

### Example 3: TTS-Enabled Language Learning Card

```html
<!-- Front Template -->
<div class="japanese">{{Expression}}</div>

<button onclick="playAudio()">🔊 Play</button>

<script>
const api = AnkiDroidJS.init({ 
    developer: "language-learner@example.com", 
    version: "0.0.3" 
});

async function playAudio() {
    await api.ankiTtsSetLanguage("ja-JP");
    await api.ankiTtsSetSpeechRate(0.8); // Slower for learning
    
    const text = "{{kanji:Expression}}";
    await api.ankiTtsSpeak(text);
}
</script>

<!-- Back Template -->
{{FrontSide}}

<hr id=answer>

<div class="reading">{{furigana:Expression}}</div>
<div class="meaning">{{Meaning}}</div>

<button onclick="playEnglish()">🔊 English</button>

<script>
async function playEnglish() {
    await api.ankiTtsSetLanguage("en-US");
    await api.ankiTtsSpeak("{{Meaning}}");
}
</script>
```

---

### Example 4: Cloze Deletion with Type-Answer

```html
<!-- Front Template -->
{{type:cloze:Text}}

<!-- Back Template -->
{{cloze:Text}}

<hr id=answer>

{{#Extra}}
  <div class="extra">{{Extra}}</div>
{{/Extra}}

<!-- Styling -->
<style>
.cloze {
    font-weight: bold;
    color: blue;
}
</style>
```

---

### Example 5: Statistics Display Card

```html
<!-- Front Template -->
<div class="question">{{Front}}</div>

<div id="stats"></div>

<script>
const api = AnkiDroidJS.init({ 
    developer: "stats-user@example.com", 
    version: "0.0.3" 
});

async function loadStats() {
    const newCards = await api.ankiGetNewCardCount();
    const lrnCards = await api.ankiGetLrnCardCount();
    const revCards = await api.ankiGetRevCardCount();
    const eta = await api.ankiGetETA();
    
    const reps = await api.ankiGetCardReps();
    const lapses = await api.ankiGetCardLapses();
    const interval = await api.ankiGetCardInterval();
    
    document.getElementById('stats').innerHTML = `
        <div class="deck-stats">
            <strong>Deck:</strong> ${newCards} new, ${lrnCards} learning, ${revCards} review<br>
            <strong>ETA:</strong> ${eta} min
        </div>
        <div class="card-stats">
            <strong>This card:</strong> ${reps} reviews, ${lapses} lapses, ${interval}d interval
        </div>
    `;
}

loadStats();
</script>

<!-- Back Template -->
{{FrontSide}}

<hr id=answer>

<div class="answer">{{Back}}</div>
```

---

### Example 6: Card Search and Navigation

```html
<!-- Template with Search -->
<div class="content">{{Front}}</div>

<button onclick="searchRelated()">Find Related Cards</button>

<div id="results"></div>

<script>
const api = AnkiDroidJS.init({ 
    developer: "search-user@example.com", 
    version: "0.0.3" 
});

// Define callback for search results
function ankiSearchCard(jsonResults) {
    const results = JSON.parse(jsonResults);
    let html = `<div class="search-results"><strong>Found ${results.length} cards:</strong><ul>`;
    
    results.slice(0, 5).forEach(card => {
        const fields = card.fieldsData;
        html += `<li>${Object.values(fields)[0]}</li>`;
    });
    
    html += '</ul></div>';
    document.getElementById('results').innerHTML = html;
}

async function searchRelated() {
    const tags = JSON.parse(await api.ankiGetNoteTags());
    if (tags.length > 0) {
        await api.ankiSearchCardWithCallback(`tag:${tags[0]}`);
    }
}
</script>
```

---

### Example 7: Progressive Difficulty Card

```html
<!-- Front Template -->
<div class="question">{{Question}}</div>

<div id="difficulty-hint"></div>

<script>
const api = AnkiDroidJS.init({ 
    developer: "adaptive-learning@example.com", 
    version: "0.0.3" 
});

async function checkDifficulty() {
    const lapses = await api.ankiGetCardLapses();
    const reps = await api.ankiGetCardReps();
    
    if (lapses > 2) {
        document.getElementById('difficulty-hint').innerHTML = 
            '<div class="hint-box">💡 This card has been difficult. Take your time!</div>';
        
        // Auto-show a hint after 5 seconds
        setTimeout(() => {
            document.getElementById('difficulty-hint').innerHTML += 
                '<div class="auto-hint">{{hint:Hint}}</div>';
        }, 5000);
    }
}

checkDifficulty();
</script>

<!-- Back Template -->
{{FrontSide}}

<hr id=answer>

<div class="answer">{{Answer}}</div>

<button onclick="resetIfNeeded()">Reset Progress</button>

<script>
async function resetIfNeeded() {
    const lapses = await api.ankiGetCardLapses();
    if (lapses > 5) {
        if (confirm('This card has many lapses. Reset progress?')) {
            await api.ankiResetProgress();
            await api.ankiShowToast("Card progress reset", false);
        }
    }
}
</script>
```

---

## API Version Compatibility

### Current Version: 0.0.3

**Required for initialization:**
```javascript
const api = AnkiDroidJS.init({ 
    developer: "your-contact", 
    version: "0.0.3" 
});
```

### Version Requirements

- **Current API Version:** `0.0.3`
- **Minimum Supported Version:** `0.0.3`

### Version Warnings

If your card template uses an outdated version, AnkiDroid will display a warning message with your developer contact information, prompting you to update the API version.

**Version Check Behavior:**
- ✅ **Exact match** (`0.0.3`): Full functionality
- ⚠️ **Lower version** (e.g., `0.0.2`): Warning shown, limited functionality
- ❌ **Higher version** (e.g., `0.0.4`): Error shown, API may not work

---

## Error Codes

When JavaScript API calls fail, the following error codes may be displayed:

| Code | Constant | Description |
|------|----------|-------------|
| -1 | ANKI_JS_ERROR_CODE_ERROR | General error |
| 0 | ANKI_JS_ERROR_CODE_DEFAULT | Default/no error |
| 1 | ANKI_JS_ERROR_CODE_MARK_CARD | Mark card operation failed |
| 2 | ANKI_JS_ERROR_CODE_FLAG_CARD | Flag card operation failed |
| 3 | ANKI_JS_ERROR_CODE_BURY_CARD | Bury card operation failed |
| 4 | ANKI_JS_ERROR_CODE_SUSPEND_CARD | Suspend card operation failed |
| 5 | ANKI_JS_ERROR_CODE_BURT_NOTE | Bury note operation failed |
| 6 | ANKI_JS_ERROR_CODE_SUSPEND_NOTE | Suspend note operation failed |
| 7 | ANKI_JS_ERROR_CODE_SET_DUE | Set due date operation failed |
| 8 | ANKI_JS_ERROR_CODE_SEARCH_CARD | Card search operation failed |

---

## Best Practices

### Template Syntax

1. **Use Conditionals for Optional Fields**
   ```html
   {{#OptionalField}}
     <div>{{OptionalField}}</div>
   {{/OptionalField}}
   ```

2. **Chain Filters Logically**
   ```html
   {{text:cloze:Field}}  <!-- Process cloze first, then strip HTML -->
   ```

3. **Use `{{FrontSide}}` for Consistency**
   ```html
   <!-- Back Template -->
   {{FrontSide}}
   <hr id=answer>
   {{Answer}}
   ```

### JavaScript API

1. **Always Initialize the API**
   ```javascript
   const api = AnkiDroidJS.init({ 
       developer: "your-contact-info", 
       version: "0.0.3" 
   });
   ```

2. **Handle Async Operations Properly**
   ```javascript
   async function myFunction() {
       const cardId = await api.ankiGetCardId();
       // Use cardId
   }
   ```

3. **Check Night Mode for Adaptive Styling**
   ```javascript
   const isNightMode = await api.ankiIsInNightMode();
   if (isNightMode) {
       document.body.style.backgroundColor = '#1e1e1e';
   }
   ```

4. **Be Mindful of Metered Connections**
   ```javascript
   const isMetered = await api.ankiIsActiveNetworkMetered();
   if (!isMetered) {
       // Download large media
   }
   ```

5. **Provide User Feedback**
   ```javascript
   await api.ankiMarkCard();
   await api.ankiShowToast("Card marked!");
   ```

---

## Resources

- **AnkiDroid Wiki:** https://github.com/ankidroid/Anki-Android/wiki
- **Anki Manual (Template Reference):** https://docs.ankiweb.net/templates/intro.html
- **Source Code:**
  - JavaScript API: `AnkiDroid/src/main/assets/scripts/js-api.js`
  - API Implementation: `AnkiDroid/src/main/java/com/ichi2/anki/AnkiDroidJsAPI.kt`
  - Template Filters: `libanki/src/main/java/com/ichi2/anki/libanki/template/TemplateFilters.kt`

---

## Contributing

If you encounter issues or have suggestions for improving this documentation, please contribute to the AnkiDroid project on GitHub.

---

**Document Version:** 1.0  
**Last Updated:** December 26, 2025  
**AnkiDroid API Version:** 0.0.3
