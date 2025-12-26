.. _usage:

Usage Guide
===========

This guide covers how to use the AnkiDroid JS API in your card templates.

API Initialization
------------------

Every card template that uses the API must initialize it first:

.. code-block:: javascript

   const api = AnkiDroidJS.init({ 
       developer: "your-email@example.com", 
       version: "0.0.3" 
   });

The ``developer`` field should be your email, and ``version`` should match the add-on version you're using.

Making API Calls
----------------

All API functions are asynchronous and return Promises. Always use ``await`` or ``.then()``:

.. code-block:: javascript

   // Using await (recommended)
   async function getCardInfo() {
       const cardId = await api.ankiGetCardId();
       const reps = await api.ankiGetCardReps();
       console.log(`Card ${cardId} reviewed ${reps} times`);
   }

   // Using .then()
   api.ankiGetCardId().then(cardId => {
       console.log(`Card ID: ${cardId}`);
   });

Common Patterns
---------------

Displaying Card Statistics
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: javascript

   async function showStats() {
       const newCount = await api.ankiGetNewCardCount();
       const lrnCount = await api.ankiGetLrnCardCount();
       const revCount = await api.ankiGetRevCardCount();
       const eta = await api.ankiGetETA();
       
       document.getElementById('stats').innerHTML = `
           <div>📚 New: ${newCount}</div>
           <div>📖 Learning: ${lrnCount}</div>
           <div>✅ Review: ${revCount}</div>
           <div>⏱️ ETA: ${eta} minutes</div>
       `;
   }

Interactive Buttons
~~~~~~~~~~~~~~~~~~~

.. code-block:: html

   <button onclick="handleClick()">Do Something</button>

   <script>
   async function handleClick() {
       const success = await api.ankiMarkCard();
       if (success) {
           await api.ankiShowToast("Card marked!");
       }
   }
   </script>

Night Mode Styling
~~~~~~~~~~~~~~~~~~

.. code-block:: javascript

   async function applyTheme() {
       const isNightMode = await api.ankiIsInNightMode();
       
       if (isNightMode) {
           document.body.style.backgroundColor = "#1e1e1e";
           document.body.style.color = "#e0e0e0";
       } else {
           document.body.style.backgroundColor = "#ffffff";
           document.body.style.color = "#000000";
       }
   }
   
   applyTheme();

Text-to-Speech
~~~~~~~~~~~~~~

.. code-block:: javascript

   async function speakText(text, language = "en-US") {
       // Set language
       await api.ankiTtsSetLanguage(language);
       
       // Optional: adjust speech rate and pitch
       await api.ankiTtsSetSpeechRate(1.0);  // 1.0 is normal speed
       await api.ankiTtsSetPitch(1.0);       // 1.0 is normal pitch
       
       // Speak the text
       await api.ankiTtsSpeak(text, 0);  // 0 = replace current speech
   }

Error Handling
--------------

Always handle potential errors:

.. code-block:: javascript

   async function safeApiCall() {
       try {
           const result = await api.ankiGetCardId();
           if (result === 0) {
               console.log("No card available");
               return;
           }
           console.log(`Card ID: ${result}`);
       } catch (error) {
           console.error("API call failed:", error);
       }
   }

Default Return Values
~~~~~~~~~~~~~~~~~~~~~

When an API call fails, it returns a safe default:

- Number functions return ``0``
- Boolean functions return ``false``
- String functions return ``""`` (empty string)
- Array functions return ``[]`` (empty array)

Best Practices
--------------

1. **Initialize once per template**
   
   Don't initialize the API multiple times in the same template.

2. **Use async/await**
   
   It's cleaner and easier to read than promise chains.

3. **Check return values**
   
   API functions return ``0``, ``false``, or ``""`` when unsuccessful.

4. **Enable debug mode during development**
   
   Go to Tools → Add-ons → Config and set ``debug_mode: true``.

5. **Use the browser console**
   
   Open Tools → Debug Console to see ``console.log()`` output and errors.

6. **Test on all platforms**
   
   If you plan to use your templates on AnkiDroid, test there too.

Advanced Usage
--------------

Conditional API Usage
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: javascript

   // Check if API is available (for templates that work without it)
   if (typeof AnkiDroidJS !== 'undefined') {
       const api = AnkiDroidJS.init({ 
           developer: "your-email@example.com", 
           version: "0.0.3" 
       });
       
       // Use API features
       await api.ankiShowToast("API available!");
   } else {
       console.log("API not available on this platform");
   }

Combining Multiple Operations
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: javascript

   async function studyHelper() {
       // Get card info
       const cardType = await api.ankiGetCardType();
       const interval = await api.ankiGetCardInterval();
       
       // Take action based on info
       if (cardType === 0) {  // New card
           await api.ankiToggleFlag("blue");
           await api.ankiShowToast("New card - marked blue");
       } else if (interval > 30) {  // Mature card
           await api.ankiToggleFlag("green");
           await api.ankiShowToast("Mature card!");
       }
   }

Debugging Tips
--------------

Enable Debug Logging
~~~~~~~~~~~~~~~~~~~~

1. Go to **Tools → Add-ons**
2. Select "AnkiDroid JS API for Desktop"
3. Click **Config**
4. Set ``"debug_mode": true`` and ``"log_api_calls": true``
5. Restart Anki

View Debug Output
~~~~~~~~~~~~~~~~~

- **Python side**: Check Anki's console (startup terminal)
- **JavaScript side**: Open **Tools → Debug Console**

Common Issues
~~~~~~~~~~~~~

**API functions return 0/false**
   This usually means no card is currently being reviewed or the operation failed.

**"AnkiDroidJS is not defined" error**
   The add-on isn't installed or enabled. Check Tools → Add-ons.

**TTS doesn't work**
   Check that TTS is enabled in configuration and that your system has TTS voices installed.

Next Steps
----------

- See :ref:`examples` for complete card template examples
- Check :ref:`api-reference` for all available functions
- Read :ref:`faq` for common questions
