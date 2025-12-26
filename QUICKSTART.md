# Quick Start Guide

Get started with the AnkiDroid JS API for Desktop in 5 minutes!

## Step 1: Install the Add-on

### Option A: Manual Installation (Recommended for now)

1. Download the latest release from [GitHub Releases](https://github.com/gallaway-jp/AnkiJSApi/releases)
2. Open Anki Desktop
3. Go to **Tools → Add-ons → Install from file**
4. Select the downloaded `.ankiaddon` file
5. Restart Anki

### Option B: From Source (for developers)

```bash
git clone https://github.com/gallaway-jp/AnkiJSApi.git
cd AnkiJSApi

# Windows
mklink /D "%APPDATA%\Anki2\addons21\ankidroid_js_api" "src\ankidroid_js_api"

# macOS/Linux
ln -s "$(pwd)/src/ankidroid_js_api" "$HOME/.local/share/Anki2/addons21/ankidroid_js_api"
```

Then restart Anki.

## Step 2: Create Your First Interactive Card

### 2.1 Create a New Note Type

1. Go to **Tools → Manage Note Types**
2. Click **Add**
3. Choose **Add: Basic**
4. Name it "Interactive Basic"
5. Click **OK**, then **Close**

### 2.2 Edit the Front Template

1. Go to **Tools → Manage Note Types**
2. Select "Interactive Basic"
3. Click **Cards...**
4. In the **Front Template**, replace the content with:

```html
<div class="question">{{Front}}</div>

<button onclick="speakQuestion()">🔊 Speak</button>

<div id="stats"></div>

<script>
const api = AnkiDroidJS.init({ 
    developer: "your-email@example.com", 
    version: "0.0.3" 
});

async function speakQuestion() {
    await api.ankiTtsSpeak("{{Front}}", 0);
}

async function loadStats() {
    const newCards = await api.ankiGetNewCardCount();
    const revCards = await api.ankiGetRevCardCount();
    const eta = await api.ankiGetETA();
    
    document.getElementById('stats').innerHTML = 
        `📚 ${newCards} new | 📖 ${revCards} review | ⏱️ ${eta} min`;
}

loadStats();
</script>
```

### 2.3 Edit the Back Template

In the **Back Template**, replace with:

```html
{{FrontSide}}

<hr id="answer">

<div class="answer">{{Back}}</div>

<button onclick="markDifficult()">🚩 Mark Difficult</button>
<button onclick="markEasy()">✅ Mark Easy</button>

<script>
async function markDifficult() {
    await api.ankiToggleFlag("red");
    await api.ankiShowToast("Marked as difficult!");
}

async function markEasy() {
    await api.ankiToggleFlag("green");
    await api.ankiShowToast("Marked as easy!");
}
</script>
```

### 2.4 Add Some Styling

In the **Styling** section, add:

```css
.card {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    font-size: 20px;
    text-align: center;
    padding: 20px;
}

button {
    margin: 10px 5px;
    padding: 10px 20px;
    font-size: 16px;
    border: none;
    border-radius: 5px;
    background-color: #0066cc;
    color: white;
    cursor: pointer;
}

button:hover {
    background-color: #0052a3;
}

#stats {
    margin: 15px 0;
    padding: 10px;
    background-color: #f0f0f0;
    border-radius: 5px;
    font-size: 14px;
}

.question, .answer {
    font-size: 24px;
    margin: 20px 0;
}
```

Click **Save**.

## Step 3: Create a Test Card

1. Click **Add** (or press 'A')
2. Select the "Interactive Basic" note type
3. In the **Front** field, type: `What is the capital of France?`
4. In the **Back** field, type: `Paris`
5. Click **Add**

## Step 4: Test Your Card

1. Go to your deck
2. Click **Study Now**
3. You should see:
   - The question
   - A speaker button (click it to hear TTS)
   - Stats showing new/review cards and time remaining
4. Click **Show Answer**
5. You'll see:
   - The answer
   - Buttons to flag the card as difficult or easy
   - Toast notifications when you click them

## Common API Functions

### Card Information

```javascript
// Get card counts
const newCards = await api.ankiGetNewCardCount();
const reviewCards = await api.ankiGetRevCardCount();
const learningCards = await api.ankiGetLrnCardCount();

// Get current card info
const cardId = await api.ankiGetCardId();
const reps = await api.ankiGetCardReps();
const lapses = await api.ankiGetCardLapses();
const interval = await api.ankiGetCardInterval();
```

### Card Actions

```javascript
// Mark/flag cards
await api.ankiMarkCard();
await api.ankiToggleFlag("red");  // red, orange, green, blue, pink, turquoise, purple

// Manage cards
await api.ankiBuryCard();
await api.ankiSuspendCard();
await api.ankiResetProgress();

// Set due date (in days from today)
await api.ankiSetCardDue(7);
```

### Text-to-Speech

```javascript
// Basic TTS
await api.ankiTtsSpeak("Hello world", 0);

// Customize voice
await api.ankiTtsSetLanguage("ja-JP");
await api.ankiTtsSetSpeechRate(0.8);  // slower
await api.ankiTtsSetPitch(1.2);  // higher pitch

// Control playback
const isSpeaking = await api.ankiTtsIsSpeaking();
await api.ankiTtsStop();
```

### UI Control

```javascript
// Show messages
await api.ankiShowToast("Hello!", true);  // short duration
await api.ankiShowToast("Important message", false);  // long duration

// Check theme
const isNightMode = await api.ankiIsInNightMode();
if (isNightMode) {
    document.body.style.backgroundColor = '#1e1e1e';
}
```

### Tag Management

```javascript
// Get tags
const tagsJson = await api.ankiGetNoteTags();
const tags = JSON.parse(tagsJson);

// Set tags (replaces all tags)
await api.ankiSetNoteTags(["vocabulary", "lesson-1", "important"]);
```

## Next Steps

- **Explore Examples**: Check out [EXAMPLES.md](docs/EXAMPLES.md) for more templates
- **API Reference**: See [TEMPLATE_API_REFERENCE.md](TEMPLATE_API_REFERENCE.md) for all available functions
- **Troubleshooting**: Read the [FAQ](docs/FAQ.md) if you encounter issues
- **Advanced Usage**: Read [CONTRIBUTING.md](CONTRIBUTING.md) to extend the add-on

## Tips

1. **Always use `await`** with API functions (they return Promises)
2. **Initialize the API** in every card template where you use it
3. **Test on all platforms** if you sync cards between Desktop and AnkiDroid
4. **Check the console** (Tools → Debug Console) for errors
5. **Enable debug mode** in the add-on config to see detailed logs

## Get Help

- 📖 [Full Documentation](README.md)
- 💡 [FAQ](docs/FAQ.md)
- 🐛 [Report Issues](https://github.com/gallaway-jp/AnkiJSApi/issues)
- 🤝 [Contribute](CONTRIBUTING.md)

Happy learning! 🎉
