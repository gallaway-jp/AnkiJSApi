.. _faq:

Frequently Asked Questions
===========================

General Questions
-----------------

What is this add-on?
~~~~~~~~~~~~~~~~~~~~

This add-on brings AnkiDroid's powerful JavaScript template API to Anki Desktop, allowing you to create interactive card templates with features like TTS, card statistics, tag management, and more.

Is this compatible with AnkiDroid?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Yes! Card templates using this API will work on both Anki Desktop (with this add-on) and AnkiDroid. The API is designed to match AnkiDroid's implementation.

Will my templates work on AnkiMobile?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Some features may not work on AnkiMobile as it has different API support. We recommend testing on all platforms you plan to use.

Installation & Setup
--------------------

How do I know if the add-on is installed correctly?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Go to **Tools → Add-ons**
2. Look for "AnkiDroid JS API for Desktop" in the list
3. It should be checked (enabled)

The add-on shows an error on startup
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Check that you're using Anki 2.1.50 or higher
2. Go to **Tools → Add-ons → View Add-on Errors** for details
3. Try reinstalling the add-on
4. Report the error on GitHub if it persists

Usage Questions
---------------

How do I use the API in my card templates?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Add this JavaScript to your card template:

.. code-block:: html

   <script>
   const api = AnkiDroidJS.init({ 
       developer: "your-email@example.com", 
       version: "0.0.3" 
   });

   // Now use the API
   async function myFunction() {
       const cardId = await api.ankiGetCardId();
       console.log(cardId);
   }
   </script>

Do I need to include the API in every card?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Yes, you need to initialize the API in each card template where you want to use it. The initialization is lightweight.

Can I use the API on the front and back of a card?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Yes! You can initialize and use the API on both sides. When using ``{{FrontSide}}`` on the back, the front's JavaScript will also be included.

Why do all API functions return Promises?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The API functions are asynchronous because they communicate with Python. Always use ``await`` or ``.then()``:

.. code-block:: javascript

   // Good ✓
   const count = await api.ankiGetNewCardCount();

   // Also good ✓
   api.ankiGetNewCardCount().then(count => {
       console.log(count);
   });

   // Bad ✗ - won't work
   const count = api.ankiGetNewCardCount(); // This is a Promise, not a number

How do I debug my templates?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Enable debug mode in add-on configuration
2. Open the debug console: **Tools → Debug Console**
3. Use ``console.log()`` in your JavaScript
4. Check for errors in the console

Features
--------

Does TTS work offline?
~~~~~~~~~~~~~~~~~~~~~~

Yes! The add-on uses your system's built-in TTS, which works offline.

What languages does TTS support?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

It depends on your system:

- **Windows**: Voices installed in Windows settings
- **macOS**: Voices in System Preferences
- **Linux**: Depends on espeak/festival voices

Can I customize TTS voice?
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Currently, the system's default voice is used. You can adjust:

- Speech rate: ``api.ankiTtsSetSpeechRate(1.5)``
- Pitch: ``api.ankiTtsSetPitch(1.2)``
- Language: ``api.ankiTtsSetLanguage("en-US")``

Does speech-to-text (STT) work?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

No, STT is not currently supported on desktop. These API functions return ``false``:

- ``ankiSttSetLanguage()``
- ``ankiSttStart()``
- ``ankiSttStop()``

Can I search for cards from a template?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Yes! Use ``api.ankiSearchCard("tag:difficult")`` to open the browser with a search query.

Performance
-----------

Will this slow down my reviews?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

No, the add-on is designed to be lightweight. The JavaScript API bridge adds minimal overhead.

Should I avoid certain API calls?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

All API calls are reasonably fast, but if you're calling many in rapid succession, consider:

- Caching results instead of re-querying
- Using ``Promise.all()`` for parallel calls
- Avoiding API calls in tight loops

How many API calls can I make per card?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

There's no hard limit, but be reasonable. Dozens of calls per card should be fine; hundreds might cause lag.

Compatibility
-------------

What versions of Anki are supported?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Anki Desktop 2.1.50 and higher.

Will this work with Anki 2.0?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

No, this add-on requires Anki 2.1.50+.

Does this work with other add-ons?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Generally yes, but there could be conflicts with add-ons that:

- Modify the reviewer's JavaScript
- Hook into card rendering
- Change how pycmd works

Report conflicts on GitHub.

Can I use this with image occlusion?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Yes, the API works with all note types including image occlusion.

Troubleshooting
---------------

API functions return ``undefined`` or ``null``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Common causes:

1. Forgot to ``await`` the Promise:

   .. code-block:: javascript

      // Wrong ✗
      const id = api.ankiGetCardId();
      
      // Right ✓
      const id = await api.ankiGetCardId();

2. No card is currently displayed (e.g., on the deck browser)
3. API not initialized properly

Toast notifications don't appear
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Check that toasts are enabled in configuration
2. Verify the add-on is enabled
3. Try with ``shortLength = false`` for longer display

TTS doesn't speak
~~~~~~~~~~~~~~~~~

1. Verify TTS is enabled in configuration
2. Check system TTS is working:

   - **Windows**: Try ``PowerShell > Add-Type -AssemblyName System.Speech; (New-Object System.Speech.Synthesis.SpeechSynthesizer).Speak("test")``
   - **macOS**: Try ``say "test"`` in Terminal
   - **Linux**: Try ``espeak "test"`` or ``echo "test" | festival --tts``

3. Check the text isn't empty

Changes to configuration don't take effect
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Restart Anki after changing configuration.

Card templates work on AnkiDroid but not Desktop
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Verify the add-on is installed and enabled
2. Check for JavaScript errors in the debug console
3. Ensure you're using API version "0.0.3"

Advanced Usage
--------------

Can I call Python directly from templates?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The add-on provides a bridge via ``pycmd``, but it's recommended to use the provided API functions rather than creating custom calls.

Can I extend the API with custom functions?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Yes! You can:

1. Fork the repository
2. Add your custom functions to a new Python module
3. Register them in ``api_bridge.py``
4. Add JavaScript wrappers in ``ankidroid-api.js``

See :ref:`contributing` for details.

How do I contribute to this project?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

See :ref:`contributing` for guidelines on:

- Setting up development environment
- Adding new features
- Submitting pull requests
- Testing and code style

Still Need Help?
----------------

- Check the :ref:`installation` guide
- Review :ref:`examples`
- Read the :ref:`api-reference`
- Open an issue on `GitHub <https://github.com/RisingOrange/anki-smart-templates>`_
