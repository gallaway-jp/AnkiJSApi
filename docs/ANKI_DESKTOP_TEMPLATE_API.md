# Anki Card Template API Documentation

This document provides comprehensive documentation for the APIs available in Anki card templates on desktop.

## Table of Contents

- [Template Syntax](#template-syntax)
- [Built-in Filters](#built-in-filters)
- [Special Template Fields](#special-template-fields)
- [JavaScript API](#javascript-api)
- [Python Hooks](#python-hooks)
- [Security Considerations](#security-considerations)

---

## Template Syntax

Anki uses a Mustache-like template syntax with double curly braces.

### Basic Field Reference

```html
{{FieldName}}
```

**Example:**
```html
<!-- Front Template -->
{{Front}}
<hr>
{{Image}}

<!-- Back Template -->
{{FrontSide}}
<hr>
{{Back}}
```

### Filters

Filters modify field content using colon syntax:

```html
{{filter:FieldName}}
{{filter1:filter2:FieldName}}
```

---

## Built-in Filters

### Text Filters

#### `text` - Strip HTML

Removes all HTML tags, leaving only plain text.

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

#### `plain` - Alias for text

Same as `text` filter.

---

### Furigana Filters

For Japanese text with furigana notation.

#### `furigana` - Convert to Ruby Tags

Converts furigana notation to HTML ruby tags.

**Syntax:**
```html
{{furigana:FieldName}}
```

**Example:**
```html
{{furigana:Expression}}
```

**Input:** `漢字[かんじ]`  
**Output:** `<ruby><rb>漢字</rb><rt>かんじ</rt></ruby>`

---

#### `kana` - Show Only Reading

Extracts only the kana/reading portion.

**Syntax:**
```html
{{kana:FieldName}}
```

**Example:**
```html
{{kana:Expression}}
```

**Input:** `漢字[かんじ] 勉強[べんきょう]`  
**Output:** `かんじべんきょう`

---

#### `kanji` - Show Only Kanji

Extracts only the kanji/base text portion.

**Syntax:**
```html
{{kanji:FieldName}}
```

**Example:**
```html
{{kanji:Expression}}
```

**Input:** `漢字[かんじ] 勉強[べんきょう]`  
**Output:** `漢字勉強`

---

### Cloze Filters

For cloze deletion note types.

#### `cloze` - Render Cloze Deletions

Shows cloze deletions with `[...]` on question side and revealed on answer side.

**Syntax:**
```html
{{cloze:Text}}
```

**Example:**
```html
<!-- Question Template -->
{{cloze:Text}}

<!-- Answer Template -->
{{cloze:Text}}
```

**Input:** `{{c1::Paris}} is the capital of {{c2::France}}`  

**Card 1 Question:** `[...] is the capital of France`  
**Card 1 Answer:** `Paris is the capital of France`

**Card 2 Question:** `Paris is the capital of [...]`  
**Card 2 Answer:** `Paris is the capital of France`

---

#### `cloze-only` - Show Only Cloze Content

Shows only the cloze deletion for the current card.

**Syntax:**
```html
{{cloze-only:Text}}
```

**Example:**
```html
{{cloze-only:Text}}
```

**Input:** `{{c1::Paris}} is the capital of {{c2::France}}`  

**Card 1:** `Paris`  
**Card 2:** `France`

---

### Type Answer Filter

#### `type` - Type Answer Input

Creates an input field for typing the answer.

**Syntax:**
```html
{{type:FieldName}}
```

**Example:**
```html
<!-- Question Template -->
{{Front}}
{{type:Back}}

<!-- Answer Template -->
{{Front}}
<hr>
{{type:Back}}
{{Back}}
```

**Usage with Cloze:**
```html
{{type:cloze:Text}}
```

**Non-case sensitive variant:**
```html
{{type:nc:FieldName}}
```

---

### Hint Filter

#### `hint` - Collapsible Hint

Creates a clickable hint that reveals the content when clicked.

**Syntax:**
```html
{{hint:FieldName}}
```

**Example:**
```html
{{Front}}
{{hint:ExtraInfo}}
```

**Rendered HTML:**
```html
<a class=hint href="#"
onclick="this.style.display='none';
document.getElementById('hint...').style.display='block';
return false;">
ExtraInfo</a>
<div id="hint..." class=hint style="display: none">
[Content of ExtraInfo field]
</div>
```

---

### Text-to-Speech Filter

#### `tts` - Text-to-Speech Tag

Marks text for text-to-speech playback.

**Syntax:**
```html
{{tts lang=LANGUAGE:FieldName}}
```

**Example:**
```html
{{tts lang=en_US:Front}}
{{tts lang=ja_JP:Expression}}
{{tts lang=fr_FR voices=Apple_Amelie,Microsoft_Hortense:French}}
```

**Generated Tag:**
```
[anki:tts lang=en_US]text content[/anki:tts]
```

**Available voices** can be listed in Tools → Preferences → Text to Speech

---

### Case Filters

#### `upper` - Uppercase

Converts text to uppercase.

**Syntax:**
```html
{{upper:FieldName}}
```

**Example:**
```html
{{upper:Front}}
```

**Input:** `hello world`  
**Output:** `HELLO WORLD`

---

#### `lower` - Lowercase

Converts text to lowercase.

**Syntax:**
```html
{{lower:FieldName}}
```

**Example:**
```html
{{lower:Front}}
```

**Input:** `HELLO WORLD`  
**Output:** `hello world`

---

### Combining Filters

Multiple filters can be chained together:

**Example:**
```html
{{text:cloze:Text}}
{{kana:hint:Reading}}
```

Filters are applied left-to-right.

---

## Special Template Fields

These special fields provide metadata about the card/note.

### `{{Tags}}`

Displays the note's tags.

**Example:**
```html
<div class="tags">{{Tags}}</div>
```

**Output:** `tag1 tag2 tag3`

---

### `{{Type}}`

Displays the note type name.

**Example:**
```html
<div class="notetype">{{Type}}</div>
```

**Output:** `Basic` or `Cloze` etc.

---

### `{{Deck}}`

Displays the full deck name including parent decks.

**Example:**
```html
<div class="deck">{{Deck}}</div>
```

**Output:** `Languages::Japanese::Vocabulary`

---

### `{{Subdeck}}`

Displays only the current deck name (without parents).

**Example:**
```html
<div class="subdeck">{{Subdeck}}</div>
```

**Output:** `Vocabulary` (from `Languages::Japanese::Vocabulary`)

---

### `{{Card}}`

Displays the card template name.

**Example:**
```html
<div class="template">{{Card}}</div>
```

**Output:** `Card 1` or `Forward` etc.

---

### `{{CardFlag}}`

Displays the card's flag status.

**Example:**
```html
<div class="flag">{{CardFlag}}</div>
```

**Output:** `flag1`, `flag2`, `flag3`, `flag4`, or empty string if no flag

---

### `{{FrontSide}}`

On the back of the card, contains the fully rendered question side HTML.

**Example:**
```html
<!-- Back Template -->
{{FrontSide}}
<hr id="answer">
{{Back}}
```

**Note:** Only available on the answer/back template.

---

## JavaScript API

Card templates can include JavaScript with certain APIs available.

### Global Variables

#### `ankiPlatform`

Identifies the platform running Anki.

**Type:** `string`  
**Values:** `"desktop"`, `"mobile"`, or `"ankidroid"`

**Example:**
```javascript
if (typeof ankiPlatform !== "undefined") {
    if (ankiPlatform === "desktop") {
        // Desktop-specific code
        console.log("Running on Anki Desktop");
    } else if (ankiPlatform === "mobile") {
        // AnkiMobile-specific code
        console.log("Running on AnkiMobile");
    }
}
```

---

### `globalThis.anki` Object

The `anki` object is available on `globalThis` (or `window`) and provides various APIs.

#### `anki.mutateNextCardStates`

Allows modifying the scheduling states before answering a card (advanced usage).

**Type:** `function`

**Example:**
```javascript
// This is an advanced API - use with caution
if (globalThis.anki && globalThis.anki.mutateNextCardStates) {
    // Modify card scheduling
}
```

---

#### `anki.imageOcclusion`

API for image occlusion features (if using image occlusion note type).

**Properties:**
- `setup()` - Setup image occlusion on the card

**Example:**
```javascript
if (globalThis.anki && globalThis.anki.imageOcclusion) {
    globalThis.anki.imageOcclusion.setup({
        // configuration options
    });
}
```

---

### Reviewer Hooks

Custom JavaScript can hook into the card review lifecycle.

#### `onUpdateHook`

Array of callbacks executed when a card is shown, before MathJax rendering.

**Type:** `Array<() => void | Promise<void>>`

**Example:**
```javascript
<script>
// Access the reviewer module
const reviewer = require("anki/reviewer");

reviewer.onUpdateHook.push(function() {
    console.log("Card is being updated");
    
    // Manipulate the DOM before MathJax
    const qa = document.getElementById("qa");
    // ... your code
});
</script>
```

---

#### `onShownHook`

Array of callbacks executed after images are loaded and MathJax is rendered.

**Type:** `Array<() => void | Promise<void>>`

**Example:**
```javascript
<script>
const reviewer = require("anki/reviewer");

reviewer.onShownHook.push(function() {
    console.log("Card fully shown");
    
    // Safe to manipulate rendered content
    // Images and MathJax are ready
    
    // Example: Auto-scroll to specific element
    const element = document.querySelector(".myclass");
    if (element) {
        element.scrollIntoView({ behavior: "smooth" });
    }
});
</script>
```

---

### DOM Manipulation

Standard DOM APIs are available:

**Example:**
```javascript
<script>
// Wait for DOM to be ready
document.addEventListener('DOMContentLoaded', function() {
    // Add a class to the body
    document.body.classList.add('custom-styling');
    
    // Modify elements
    const front = document.getElementById('front');
    if (front) {
        front.style.fontSize = '24px';
    }
    
    // Add event listeners
    document.querySelectorAll('.clickable').forEach(function(elem) {
        elem.addEventListener('click', function() {
            this.classList.toggle('active');
        });
    });
});
</script>
```

---

### Available Libraries

#### jQuery

jQuery is available in the reviewer (though direct DOM APIs are preferred).

**Example:**
```javascript
<script>
// jQuery is available as $ or jQuery
$(document).ready(function() {
    $('.answer').hide();
    $('.reveal').on('click', function() {
        $('.answer').slideDown();
    });
});
</script>
```

---

#### MathJax

MathJax is available for mathematical notation rendering.

**Example:**
```javascript
<script>
// Wait for MathJax to be ready
MathJax.startup.promise.then(function() {
    console.log("MathJax is ready");
    
    // Manually typeset new content
    const element = document.getElementById('new-math');
    MathJax.typesetPromise([element]).then(function() {
        console.log("New math typeset");
    });
});
</script>
```

---

### Limitations

⚠️ **Important Security Restrictions:**

1. **No Network Requests** - `fetch()`, `XMLHttpRequest`, and similar APIs are blocked
2. **No External Resources** - Cannot load external scripts or resources
3. **Sandboxed Environment** - Limited access to system resources
4. **No Persistent Storage** - `localStorage` and `sessionStorage` may not work reliably
5. **No File Access** - Cannot read/write files from the filesystem

**Example of what NOT to do:**
```javascript
// ❌ This will NOT work - network requests are blocked
fetch('https://api.example.com/data')
    .then(response => response.json())
    .then(data => console.log(data));

// ❌ This will NOT work - localStorage is unreliable
localStorage.setItem('key', 'value');
```

---

## Python Hooks

Add-on developers can extend template rendering using Python hooks.

### `hooks.field_filter`

Allows custom filters to be defined.

**Type:** `(field_text: str, field_name: str, filter_name: str, ctx: TemplateRenderContext) -> str`

**Example:**
```python
from anki import hooks
from anki.template import TemplateRenderContext

def my_custom_filter(
    field_text: str,
    field_name: str,
    filter_name: str,
    ctx: TemplateRenderContext
) -> str:
    """Custom filter that reverses text."""
    if filter_name == "reverse":
        return field_text[::-1]
    elif filter_name == "shout":
        return field_text.upper() + "!!!"
    
    # Return unchanged if not our filter
    return field_text

# Register the filter
hooks.field_filter.append(my_custom_filter)
```

**Usage in Template:**
```html
{{reverse:Front}}
{{shout:Back}}
```

**Input:** `Hello World`  
**With `reverse`:** `dlroW olleH`  
**With `shout`:** `HELLO WORLD!!!`

---

### `hooks.card_did_render`

Modifies the final rendered output after all filters are applied.

**Type:** `(output: TemplateRenderOutput, ctx: TemplateRenderContext) -> None`

**Example:**
```python
from anki import hooks
from anki.template import TemplateRenderOutput, TemplateRenderContext

def modify_rendered_card(
    output: TemplateRenderOutput,
    ctx: TemplateRenderContext
) -> None:
    """Add a watermark to all cards."""
    
    watermark = '<div class="watermark">Study Hard!</div>'
    
    # Modify question
    output.question_text += watermark
    
    # Modify answer  
    output.answer_text += watermark
    
    # Access card/note information
    card = ctx.card()
    note = ctx.note()
    
    # Conditional modification
    if "important" in note.tags:
        output.question_text = (
            '<div class="important-marker">⚠️</div>' 
            + output.question_text
        )

# Register the hook
hooks.card_did_render.append(modify_rendered_card)
```

---

### TemplateRenderContext API

The `TemplateRenderContext` object provides access to card/note data.

**Properties:**

- **`ctx.col()`** - Returns the `Collection` object
- **`ctx.card()`** - Returns the `Card` being rendered
- **`ctx.note()`** - Returns the `Note` 
- **`ctx.note_type()`** - Returns the note type dictionary
- **`ctx.fields()`** - Returns field dictionary (legacy)
- **`ctx.question_side`** - Boolean, `True` if rendering question
- **`ctx.extra_state`** - Dictionary for storing custom state between hooks

**Example:**
```python
from anki import hooks

def my_filter(field_text, field_name, filter_name, ctx):
    if filter_name == "cardinfo":
        # Access card information
        card = ctx.card()
        note = ctx.note()
        
        info = f"""
        <div class="card-info">
            <p>Card ID: {card.id}</p>
            <p>Note ID: {note.id}</p>
            <p>Deck: {ctx.col().decks.name(card.did)}</p>
            <p>Tags: {' '.join(note.tags)}</p>
        </div>
        """
        return info
    
    return field_text

hooks.field_filter.append(my_filter)
```

**Template Usage:**
```html
{{cardinfo:Front}}
```

---

### Legacy Hooks

For backward compatibility, legacy hooks are still supported.

**Example:**
```python
from anki import hooks

def legacy_filter(field_text, field_name, filter_name, ctx):
    if filter_name == "myfilter":
        return field_text.upper()
    return field_text

# Legacy method
hooks.addHook('fmod_myfilter', legacy_filter)
```

---

## Security Considerations

### JavaScript Security

From the SECURITY.md file:

> Anki allows users and shared deck authors to augment their card designs with Javascript. This is used frequently, so disabling Javascript by default would likely break a lot of the shared decks out there.

**Key Points:**

1. **Limited Interface** - The desktop version has a limited interface between JavaScript and parts of Anki outside the webview
2. **No Arbitrary Code Execution** - Arbitrary code execution outside the webview should not be possible
3. **Separate Domain** - AnkiWeb study interface runs on `ankiuser.net` domain to isolate JavaScript
4. **Content Filtering** - JavaScript is filtered on the main AnkiWeb site

### Best Practices

1. **Avoid External Resources** - Don't try to load external scripts or data
2. **Don't Store Sensitive Data** - JavaScript in templates is visible to anyone with the deck
3. **Test Thoroughly** - Test templates across different Anki versions and platforms
4. **Use Add-ons for Complex Logic** - For advanced features, create an add-on instead
5. **Validate User Input** - If using type-answer fields, validate the input

### Trusted Content Only

⚠️ **Warning:** Only use templates from trusted sources. Malicious JavaScript in templates could:
- Exfiltrate card content if combined with vulnerabilities
- Create phishing interfaces
- Interfere with the review process

---

## Complete Template Examples

### Example 1: Basic Card with Hint

```html
<!-- Front Template -->
<div class="question">
    {{Front}}
</div>

<div class="hint-section">
    {{hint:Hint}}
</div>

<!-- Back Template -->
{{FrontSide}}

<hr id="answer">

<div class="answer">
    {{Back}}
</div>

<!-- Styling -->
<style>
.card {
    font-family: arial;
    font-size: 20px;
    text-align: center;
    color: black;
    background-color: white;
}

.hint-section {
    margin-top: 20px;
    font-size: 14px;
}
</style>
```

---

### Example 2: Japanese Card with Furigana

```html
<!-- Front Template -->
<div class="japanese">
    {{furigana:Expression}}
</div>

<!-- Back Template -->
{{FrontSide}}

<hr id="answer">

<div class="reading">
    {{kana:Expression}}
</div>

<div class="meaning">
    {{Meaning}}
</div>

<div class="audio">
    {{Audio}}
</div>

<!-- Styling -->
<style>
.japanese {
    font-size: 40px;
    font-family: "Yu Mincho", "Hiragino Mincho Pro", serif;
}

.reading {
    font-size: 20px;
    color: #666;
    margin: 10px 0;
}

.meaning {
    font-size: 24px;
    margin-top: 20px;
}

ruby rt {
    font-size: 0.6em;
}
</style>
```

---

### Example 3: Cloze with Type Answer

```html
<!-- Front Template -->
{{cloze:Text}}

{{type:cloze:Text}}

<!-- Back Template -->
{{cloze:Text}}

{{type:cloze:Text}}

<div class="extra">
    {{Extra}}
</div>

<!-- Styling -->
<style>
.card {
    font-family: arial;
    font-size: 20px;
    text-align: center;
}

.cloze {
    font-weight: bold;
    color: blue;
}

#typeans {
    font-size: 20px;
    padding: 5px;
    margin: 10px 0;
}
</style>
```

---

### Example 4: Card with JavaScript Enhancements

```html
<!-- Front Template -->
<div id="question">
    {{Front}}
</div>

<!-- Back Template -->
{{FrontSide}}

<hr id="answer">

<div id="answer-content" style="display: none;">
    {{Back}}
</div>

<button id="reveal-btn">Show Answer</button>

<script>
// Platform detection
if (typeof ankiPlatform !== "undefined") {
    document.body.classList.add('platform-' + ankiPlatform);
}

// Reveal answer with animation
document.getElementById('reveal-btn').addEventListener('click', function() {
    const answer = document.getElementById('answer-content');
    answer.style.display = 'block';
    answer.style.opacity = '0';
    
    let opacity = 0;
    const timer = setInterval(function() {
        opacity += 0.1;
        answer.style.opacity = opacity;
        if (opacity >= 1) {
            clearInterval(timer);
        }
    }, 50);
    
    this.style.display = 'none';
});

// Add class after DOM loads
document.addEventListener('DOMContentLoaded', function() {
    document.body.classList.add('template-loaded');
});
</script>

<!-- Styling -->
<style>
.card {
    font-family: arial;
    font-size: 20px;
    text-align: center;
}

#reveal-btn {
    margin: 20px auto;
    padding: 10px 20px;
    font-size: 16px;
    background: #0066cc;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
}

#reveal-btn:hover {
    background: #0052a3;
}

#answer-content {
    margin-top: 20px;
    padding: 20px;
    background: #f0f0f0;
    border-radius: 5px;
}
</style>
```

---

### Example 5: Multi-Platform Optimized Card

```html
<!-- Front Template -->
<div class="question-container">
    {{Front}}
</div>

{{#Image}}
<div class="image-container">
    {{Image}}
</div>
{{/Image}}

<!-- Back Template -->
{{FrontSide}}

<hr id="answer">

<div class="answer-container">
    {{Back}}
</div>

<script>
// Detect and adapt to platform
(function() {
    const platform = typeof ankiPlatform !== "undefined" ? ankiPlatform : "unknown";
    document.documentElement.setAttribute('data-platform', platform);
    
    // Mobile-specific adjustments
    if (platform === "mobile" || platform === "ankidroid") {
        document.body.classList.add('is-mobile');
        
        // Larger tap targets on mobile
        const style = document.createElement('style');
        style.textContent = `
            .card { font-size: 18px; }
            button { min-height: 44px; }
        `;
        document.head.appendChild(style);
    }
    
    // Desktop-specific features
    if (platform === "desktop") {
        document.body.classList.add('is-desktop');
        
        // Keyboard shortcuts
        document.addEventListener('keydown', function(e) {
            if (e.key === 'h') {
                // Toggle hints or custom behavior
                const hints = document.querySelectorAll('.hint');
                hints.forEach(h => h.classList.toggle('visible'));
            }
        });
    }
})();
</script>

<!-- Styling -->
<style>
.card {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    font-size: 20px;
    text-align: center;
    padding: 20px;
}

.image-container {
    margin: 20px 0;
}

.image-container img {
    max-width: 100%;
    height: auto;
}

/* Mobile optimizations */
.is-mobile .card {
    padding: 15px;
    font-size: 18px;
}

/* Desktop optimizations */
.is-desktop .card {
    max-width: 800px;
    margin: 0 auto;
}

/* Platform-specific styles */
[data-platform="desktop"] .question-container {
    min-height: 100px;
}

[data-platform="mobile"] .answer-container,
[data-platform="ankidroid"] .answer-container {
    padding: 10px;
}
</style>
```

---

## Additional Resources

- **Official Manual**: [Anki Manual - Templates](https://docs.ankiweb.net/templates/intro.html)
- **Add-on Development**: See `pylib/anki/hooks.py` for all available hooks
- **Template Rendering**: See `rslib/src/template_filters.rs` for filter implementation
- **Security Policy**: See `SECURITY.md` for security considerations

## Version Information

This documentation is based on the Anki codebase as of December 2025. APIs and features may change in future versions.

For the most up-to-date information, consult the official Anki documentation and source code.
