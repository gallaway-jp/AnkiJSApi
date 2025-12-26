.. _installation:

Installation
============

This guide provides detailed instructions for installing the AnkiDroid JS API for Desktop add-on.

Prerequisites
-------------

- Anki Desktop 2.1.50 or higher (recommended: 2.1.60+)
- Python 3.9+ (included with modern Anki versions)
- Windows, macOS, or Linux

Installation Methods
--------------------

Method 1: From AnkiWeb (Coming Soon)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Once published to AnkiWeb:

1. Open Anki Desktop
2. Go to **Tools → Add-ons**
3. Click **Get Add-ons...**
4. Enter the add-on code: ``XXXXXXXXX``
5. Click **OK**
6. Restart Anki

Method 2: Manual Installation from Release
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Download the latest ``.ankiaddon`` file from `GitHub Releases <https://github.com/yourusername/ankidroid-js-api-desktop/releases>`_

2. Open Anki Desktop

3. Go to **Tools → Add-ons**

4. Click **Install from file...**

5. Navigate to and select the downloaded ``.ankiaddon`` file

6. Click **Open**

7. Restart Anki when prompted

Method 3: Install from Source (For Developers)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Windows
^^^^^^^

1. Clone the repository:

   .. code-block:: powershell

      git clone https://github.com/yourusername/ankidroid-js-api-desktop.git
      cd ankidroid-js-api-desktop

2. Create a symbolic link to Anki's add-ons folder:

   .. code-block:: powershell

      mklink /D "%APPDATA%\\Anki2\\addons21\\ankidroid_js_api" "path\\to\\repo\\src\\ankidroid_js_api"

3. Restart Anki

macOS
^^^^^

1. Clone the repository:

   .. code-block:: bash

      git clone https://github.com/yourusername/ankidroid-js-api-desktop.git
      cd ankidroid-js-api-desktop

2. Create a symbolic link:

   .. code-block:: bash

      ln -s "$(pwd)/src/ankidroid_js_api" "$HOME/Library/Application Support/Anki2/addons21/ankidroid_js_api"

3. Restart Anki

Linux
^^^^^

1. Clone the repository:

   .. code-block:: bash

      git clone https://github.com/yourusername/ankidroid-js-api-desktop.git
      cd ankidroid-js-api-desktop

2. Create a symbolic link:

   .. code-block:: bash

      ln -s "$(pwd)/src/ankidroid_js_api" "$HOME/.local/share/Anki2/addons21/ankidroid_js_api"

3. Restart Anki

Verifying Installation
-----------------------

1. Open Anki
2. Go to **Tools → Add-ons**
3. You should see "AnkiDroid JS API for Desktop" in the list
4. The add-on should be checked (enabled)

Configuration
-------------

Accessing Configuration
~~~~~~~~~~~~~~~~~~~~~~~~

1. Go to **Tools → Add-ons**
2. Select "AnkiDroid JS API for Desktop"
3. Click **Config**

Default Configuration
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: json

   {
       "debug_mode": false,
       "log_api_calls": false,
       "tts": {
           "enabled": true
       },
       "ui": {
           "show_toast_notifications": true,
           "toast_duration_ms": 2000
       }
   }

Configuration Options
~~~~~~~~~~~~~~~~~~~~~

**debug_mode** (boolean)
   Enable verbose logging for troubleshooting. Default: ``false``

**log_api_calls** (boolean)
   Log all API function calls. Default: ``false``

**tts.enabled** (boolean)
   Enable text-to-speech functionality. Default: ``true``

**ui.show_toast_notifications** (boolean)
   Show toast notifications when called from API. Default: ``true``

**ui.toast_duration_ms** (integer)
   Duration for toast notifications in milliseconds. Default: ``2000``

Troubleshooting
---------------

Add-on doesn't appear in list
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Make sure you restarted Anki after installation
- Check that the ``.ankiaddon`` file was correctly installed
- Verify Anki version is 2.1.50 or higher

Error on startup
~~~~~~~~~~~~~~~~

1. Go to **Tools → Add-ons → View Add-on Errors**
2. Check for Python errors in the error log
3. Try disabling and re-enabling the add-on
4. If issue persists, report on GitHub with error details

API not working in templates
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Enable debug mode in configuration
2. Check browser console for JavaScript errors
3. Verify API initialization code is correct
4. See :ref:`quickstart` for working examples

Next Steps
----------

- :ref:`quickstart` - Get started in 5 minutes
- :ref:`examples` - Example card templates
- :ref:`api-reference` - Complete API documentation
