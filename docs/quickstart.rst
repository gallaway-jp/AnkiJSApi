.. _quickstart:

Quick Start Guide
=================

Get started with the AnkiDroid JS API for Desktop in 5 minutes!

Step 1: Install the Add-on
---------------------------

See the :ref:`installation` guide for detailed installation instructions.

Quick install via manual installation:

1. Download the latest ``.ankiaddon`` file
2. **Tools → Add-ons → Install from file**
3. Select the file and restart Anki

Step 2: Create Your First Interactive Card
-------------------------------------------

Create a New Note Type
~~~~~~~~~~~~~~~~~~~~~~

1. Go to **Tools → Manage Note Types**
2. Click **Add**
3. Choose **Add: Basic**
4. Name it "Interactive Basic"
5. Click **OK**, then **Close**

Edit the Front Template
~~~~~~~~~~~~~~~~~~~~~~~~

1. Go to **Tools → Manage Note Types**
2. Select "Interactive Basic"
3. Click **Cards...**
4. In the **Front Template**, replace the content with:

.. code-block:: html

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
       document.getElementById('stats').innerHTML = 
           `📚 ${newCards} new | 📖 ${revCards} to review`;
   }

   loadStats();
   </script>

Edit the Back Template
~~~~~~~~~~~~~~~~~~~~~~~

In the **Back Template**:

.. code-block:: html

   {{FrontSide}}

   <hr id="answer">

   <div class="answer">{{Back}}</div>

   <button onclick="markImportant()">🚩 Mark Important</button>
   <button onclick="addTag()">🏷️ Add Tag</button>

   <script>
   async function markImportant() {
       const success = await api.ankiToggleFlag("red");
       if (success) {
           await api.ankiShowToast("Marked as important!");
       }
   }

   async function addTag() {
       await api.ankiAddTagToNote("review-again");
       await api.ankiShowToast("Tag added!");
   }
   </script>

Step 3: Test It Out
--------------------

1. Click **Save** to save the card template
2. Close the card template editor
3. Create a new card using the "Interactive Basic" note type
4. Add some content to Front and Back fields
5. Start reviewing the card

You should now see:

- 📚 Card statistics on the front
- 🔊 A button to speak the front text
- 🚩 A button to flag the card on the back
- 🏷️ A button to add a tag

Next Steps
----------

Explore More Features
~~~~~~~~~~~~~~~~~~~~~~

Try these API functions in your templates:

**Card Information:**

.. code-block:: javascript

   const cardId = await api.ankiGetCardId();
   const reps = await api.ankiGetCardReps();
   const interval = await api.ankiGetCardInterval();

**Card Actions:**

.. code-block:: javascript

   await api.ankiMarkCard();              // Toggle mark
   await api.ankiBuryCard();              // Bury until tomorrow
   await api.ankiSuspendCard();           // Suspend indefinitely

**Text-to-Speech:**

.. code-block:: javascript

   await api.ankiTtsSetLanguage("ja-JP");  // Set language
   await api.ankiTtsSetSpeechRate(1.5);    // Faster speech
   await api.ankiTtsSetPitch(1.2);         // Higher pitch
   await api.ankiTtsSpeak("こんにちは", 0);

**UI Control:**

.. code-block:: javascript

   const nightMode = await api.ankiIsInNightMode();
   if (nightMode) {
       document.body.style.background = "#1e1e1e";
   }

Learn More
~~~~~~~~~~

- :ref:`examples` - More complete card template examples
- :ref:`api-reference` - Full API documentation
- `CONTRIBUTING.md <https://github.com/gallaway-jp/AnkiJSApi/blob/main/CONTRIBUTING.md>`_ - Contribute to the project

Troubleshooting
---------------

API not working
~~~~~~~~~~~~~~~

Make sure you:

1. Initialized the API with ``AnkiDroidJS.init()``
2. Used ``await`` with all API function calls
3. Restarted Anki after installing the add-on

Console errors
~~~~~~~~~~~~~~

1. Enable debug mode in add-on configuration
2. Open **Tools → Debug Console**
3. Look for JavaScript errors
4. Check that all API calls use proper syntax

Need Help?
~~~~~~~~~~

- See :ref:`faq` for common questions
- Check `GitHub Issues <https://github.com/gallaway-jp/AnkiJSApi/issues>`_
- Read the full :ref:`api-reference`
