.. _examples:

Example Card Templates
======================

This page contains example card templates demonstrating the AnkiDroid JS API features.

Basic Interactive Card
----------------------

A simple card with TTS and statistics.

Front Template
~~~~~~~~~~~~~~

.. code-block:: html

   <div class="question">{{Front}}</div>

   <button onclick="playTTS()">🔊 Speak</button>
   <div id="stats"></div>

   <script>
   const api = AnkiDroidJS.init({ 
       developer: "example@email.com", 
       version: "0.0.3" 
   });

   async function playTTS() {
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

Back Template
~~~~~~~~~~~~~

.. code-block:: html

   {{FrontSide}}

   <hr>

   <div class="answer">{{Back}}</div>

   <button onclick="markDifficult()">🚩 Mark Difficult</button>

   <script>
   async function markDifficult() {
       await api.ankiToggleFlag("red");
       await api.ankiShowToast("Marked as difficult!");
   }
   </script>

Language Learning Card with TTS
--------------------------------

Advanced language learning card with multi-language TTS.

Front Template
~~~~~~~~~~~~~~

.. code-block:: html

   <div class="word">{{Word}}</div>

   <div id="stats"></div>

   <button onclick="playWord()">🔊 Play Word</button>
   <button onclick="playSlowly()">🐌 Play Slowly</button>
   <button onclick="showHint()">💡 Hint</button>

   <div id="hint" style="display: none;">
       {{hint:Pronunciation}}
   </div>

   <script>
   const api = AnkiDroidJS.init({ 
       developer: "language-learner@email.com", 
       version: "0.0.3" 
   });

   async function playWord() {
       await api.ankiTtsSetLanguage("ja-JP");
       await api.ankiTtsSetSpeechRate(1.0);
       await api.ankiTtsSpeak("{{Word}}", 0);
   }

   async function playSlowly() {
       await api.ankiTtsSetLanguage("ja-JP");
       await api.ankiTtsSetSpeechRate(0.6);  // 60% speed
       await api.ankiTtsSpeak("{{Word}}", 0);
   }

   async function showHint() {
       document.getElementById('hint').style.display = 'block';
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

Back Template
~~~~~~~~~~~~~

.. code-block:: html

   {{FrontSide}}

   <hr>

   <div class="meaning">{{Meaning}}</div>
   <div class="example">{{Example}}</div>

   <button onclick="playEnglish()">🔊 English</button>
   <button onclick="addToReview()">📝 Review Again</button>

   <script>
   async function playEnglish() {
       await api.ankiTtsSetLanguage("en-US");
       await api.ankiTtsSpeak("{{Meaning}}", 0);
   }

   async function addToReview() {
       await api.ankiAddTagToNote("needs-review");
       await api.ankiToggleFlag("orange");
       await api.ankiShowToast("Added to review list!");
   }
   </script>

Cloze Card with Progress Tracking
----------------------------------

A cloze deletion card that tracks your progress.

Template
~~~~~~~~

.. code-block:: html

   <div class="cloze">{{cloze:Text}}</div>

   <div id="cardInfo"></div>

   <button onclick="markEasy()">😊 Easy</button>
   <button onclick="markHard()">😓 Hard</button>

   <script>
   const api = AnkiDroidJS.init({ 
       developer: "student@email.com", 
       version: "0.0.3" 
   });

   async function showCardInfo() {
       const cardId = await api.ankiGetCardId();
       const reps = await api.ankiGetCardReps();
       const lapses = await api.ankiGetCardLapses();
       const interval = await api.ankiGetCardInterval();
       const ease = await api.ankiGetCardEase();
       
       document.getElementById('cardInfo').innerHTML = `
           <div>Card #${cardId}</div>
           <div>Reviews: ${reps} | Lapses: ${lapses}</div>
           <div>Interval: ${interval} days | Ease: ${ease}%</div>
       `;
   }

   async function markEasy() {
       await api.ankiToggleFlag("green");
       await api.ankiShowToast("Marked as easy!");
   }

   async function markHard() {
       await api.ankiToggleFlag("red");
       await api.ankiShowToast("Marked as hard!");
   }

   showCardInfo();
   </script>

Night Mode Adaptive Card
-------------------------

A card that adapts its appearance based on Anki's night mode.

Front Template
~~~~~~~~~~~~~~

.. code-block:: html

   <div id="content">
       <div class="question">{{Front}}</div>
   </div>

   <style id="dynamic-style"></style>

   <script>
   const api = AnkiDroidJS.init({ 
       developer: "theme-lover@email.com", 
       version: "0.0.3" 
   });

   async function applyTheme() {
       const isNightMode = await api.ankiIsInNightMode();
       
       const styleElement = document.getElementById('dynamic-style');
       
       if (isNightMode) {
           styleElement.innerHTML = `
               body {
                   background: linear-gradient(135deg, #1e1e1e 0%, #2d2d2d 100%);
                   color: #e0e0e0;
               }
               .question {
                   background: #2d2d2d;
                   border: 2px solid #4a4a4a;
                   padding: 20px;
                   border-radius: 10px;
                   box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
               }
           `;
       } else {
           styleElement.innerHTML = `
               body {
                   background: linear-gradient(135deg, #f5f5f5 0%, #e0e0e0 100%);
                   color: #333;
               }
               .question {
                   background: white;
                   border: 2px solid #ddd;
                   padding: 20px;
                   border-radius: 10px;
                   box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
               }
           `;
       }
   }

   applyTheme();
   </script>

Study Streak Tracker
---------------------

A card that shows your study progress and motivates you.

Front Template
~~~~~~~~~~~~~~

.. code-block:: html

   <div class="question">{{Front}}</div>

   <div id="progress"></div>

   <button onclick="celebrate()">🎉 Celebrate!</button>

   <script>
   const api = AnkiDroidJS.init({ 
       developer: "motivated@email.com", 
       version: "0.0.3" 
   });

   async function showProgress() {
       const newCount = await api.ankiGetNewCardCount();
       const lrnCount = await api.ankiGetLrnCardCount();
       const revCount = await api.ankiGetRevCardCount();
       const eta = await api.ankiGetETA();
       
       const totalRemaining = newCount + lrnCount + revCount;
       const progressPercent = totalRemaining > 0 ? 
           Math.round((1 - totalRemaining / (totalRemaining + 10)) * 100) : 100;
       
       document.getElementById('progress').innerHTML = `
           <div style="margin: 20px 0;">
               <div style="background: #e0e0e0; height: 30px; border-radius: 15px; overflow: hidden;">
                   <div style="background: linear-gradient(90deg, #4CAF50 0%, #8BC34A 100%); 
                               height: 100%; width: ${progressPercent}%; 
                               transition: width 0.5s ease;"></div>
               </div>
               <div style="margin-top: 10px; text-align: center;">
                   ${totalRemaining} cards remaining | ${eta} minutes left
               </div>
           </div>
       `;
   }

   async function celebrate() {
       await api.ankiShowToast("Keep up the great work! 🎉");
       // Add confetti animation here if desired
   }

   showProgress();
   </script>

Interactive Quiz Card
----------------------

A card with multiple choice options using JavaScript.

Front Template
~~~~~~~~~~~~~~

.. code-block:: html

   <div class="question">{{Question}}</div>

   <div id="options"></div>
   <div id="feedback"></div>

   <script>
   const api = AnkiDroidJS.init({ 
       developer: "quiz-master@email.com", 
       version: "0.0.3" 
   });

   const options = [
       "{{Option1}}",
       "{{Option2}}",
       "{{Option3}}",
       "{{Option4}}"
   ];
   const correctAnswer = "{{Answer}}";

   function createOptions() {
       const optionsDiv = document.getElementById('options');
       
       options.forEach((option, index) => {
           if (option.trim()) {  // Only show non-empty options
               const button = document.createElement('button');
               button.textContent = option;
               button.onclick = () => checkAnswer(option, button);
               button.style.display = 'block';
               button.style.margin = '10px 0';
               button.style.padding = '10px 20px';
               button.style.width = '100%';
               optionsDiv.appendChild(button);
           }
       });
   }

   async function checkAnswer(selected, button) {
       const feedback = document.getElementById('feedback');
       
       if (selected === correctAnswer) {
           button.style.background = '#4CAF50';
           button.style.color = 'white';
           feedback.innerHTML = '✅ Correct!';
           await api.ankiToggleFlag("green");
           await api.ankiShowToast("Correct answer!");
       } else {
           button.style.background = '#f44336';
           button.style.color = 'white';
           feedback.innerHTML = '❌ Incorrect. Try again!';
           await api.ankiToggleFlag("red");
       }
   }

   createOptions();
   </script>

Styling Tips
------------

Common CSS for Better Cards
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: html

   <style>
   .card {
       font-family: 'Segoe UI', Arial, sans-serif;
       font-size: 20px;
       text-align: center;
       padding: 20px;
   }

   button {
       background: #2196F3;
       color: white;
       border: none;
       padding: 10px 20px;
       margin: 5px;
       border-radius: 5px;
       cursor: pointer;
       font-size: 16px;
       transition: background 0.3s;
   }

   button:hover {
       background: #1976D2;
   }

   button:active {
       transform: scale(0.95);
   }

   .question {
       font-size: 28px;
       margin-bottom: 20px;
       font-weight: bold;
   }

   .answer {
       font-size: 24px;
       margin-top: 20px;
   }
   </style>

Next Steps
----------

- See :ref:`api-reference` for all available API functions
- Check :ref:`usage` for detailed usage patterns
- Read :ref:`faq` for common questions
