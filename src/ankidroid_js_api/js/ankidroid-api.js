/**
 * AnkiDroid JS API for Desktop
 * 
 * This script provides a JavaScript API compatible with AnkiDroid's AnkiDroidJS API,
 * enabling advanced interactive card templates on Anki Desktop.
 * 
 * @version 0.0.4
 * @license MIT
 */

(function() {
    'use strict';
    
    // Platform identifier
    if (typeof ankiPlatform === 'undefined') {
        window.ankiPlatform = 'desktop';
    }
    
    // Callback registry for async pycmd responses
    var _callbacks = {};
    var _callbackId = 0;
    
    /**
     * Global callback handler that Python will call
     */
    window._ankidroidJsCallback = function(callbackId, result) {
        console.log('AnkiDroidJS: Callback', callbackId, 'received:', result);
        
        var callback = _callbacks[callbackId];
        if (callback) {
            if (result.success) {
                callback.resolve({ success: true, value: result.result });
            } else {
                callback.resolve({ success: false, error: result.error });
            }
            delete _callbacks[callbackId];
        }
    };
    
    /**
     * Call a Python function via pycmd with callback support
     * @param {string} functionName - Name of the Python function
     * @param {Object} args - Arguments to pass to the function
     * @returns {Promise} Promise that resolves with {success: true, value: result}
     */
    function callPython(functionName, args) {
        return new Promise(function(resolve, reject) {
            var callbackId = _callbackId++;
            
            // Store the callback
            _callbacks[callbackId] = { resolve: resolve, reject: reject };
            
            // Build the command with callback ID
            var argsJson = args ? JSON.stringify(args) : '{}';
            var cmd = 'ankidroidjs:' + callbackId + ':' + functionName + ':' + argsJson;
            
            console.log('AnkiDroidJS: Calling', functionName, 'with callback', callbackId);
            
            // Use pycmd to call Python (fire and forget - response comes via callback)
            if (typeof pycmd !== 'undefined') {
                pycmd(cmd);
            } else {
                console.error('AnkiDroidJS: pycmd is not available');
                resolve({ success: false, error: 'pycmd is not available' });
                delete _callbacks[callbackId];
                return;
            }
            
            // Timeout after 5 seconds
            setTimeout(function() {
                if (_callbacks[callbackId]) {
                    delete _callbacks[callbackId];
                    reject(new Error('Timeout calling ' + functionName));
                }
            }, 5000);
        });
    }
    
    
    /**
     * Create the API object with all available methods
     * @returns {Object} API object
     */
    function createAPI() {
        return {
            // Card Information APIs
            ankiGetNewCardCount: function() {
                return callPython('ankiGetNewCardCount');
            },
            
            ankiGetLrnCardCount: function() {
                return callPython('ankiGetLrnCardCount');
            },
            
            ankiGetRevCardCount: function() {
                return callPython('ankiGetRevCardCount');
            },
            
            ankiGetETA: function() {
                return callPython('ankiGetETA');
            },
            
            ankiGetCardMark: function() {
                return callPython('ankiGetCardMark');
            },
            
            ankiGetCardFlag: function() {
                return callPython('ankiGetCardFlag');
            },
            
            ankiGetCardLeft: function() {
                return callPython('ankiGetCardLeft');
            },
            
            ankiGetNextTime1: function() {
                return callPython('ankiGetNextTime1');
            },
            
            ankiGetNextTime2: function() {
                return callPython('ankiGetNextTime2');
            },
            
            ankiGetNextTime3: function() {
                return callPython('ankiGetNextTime3');
            },
            
            ankiGetNextTime4: function() {
                return callPython('ankiGetNextTime4');
            },
            
            ankiGetCardReps: function() {
                return callPython('ankiGetCardReps');
            },
            
            ankiGetCardInterval: function() {
                return callPython('ankiGetCardInterval');
            },
            
            ankiGetCardFactor: function() {
                return callPython('ankiGetCardFactor');
            },
            
            ankiGetCardMod: function() {
                return callPython('ankiGetCardMod');
            },
            
            ankiGetCardId: function() {
                return callPython('ankiGetCardId');
            },
            
            ankiGetCardNid: function() {
                return callPython('ankiGetCardNid');
            },
            
            ankiGetCardType: function() {
                return callPython('ankiGetCardType');
            },
            
            ankiGetCardDid: function() {
                return callPython('ankiGetCardDid');
            },
            
            ankiGetCardQueue: function() {
                return callPython('ankiGetCardQueue');
            },
            
            ankiGetCardLapses: function() {
                return callPython('ankiGetCardLapses');
            },
            
            ankiGetCardDue: function() {
                return callPython('ankiGetCardDue');
            },
            
            ankiGetDeckName: function() {
                return callPython('ankiGetDeckName');
            },
            
            // Card Action APIs
            ankiMarkCard: function() {
                return callPython('ankiMarkCard');
            },
            
            ankiToggleFlag: function(flagColor) {
                return callPython('ankiToggleFlag', { flag_color: flagColor });
            },
            
            ankiBuryCard: function() {
                return callPython('ankiBuryCard');
            },
            
            ankiBuryNote: function() {
                return callPython('ankiBuryNote');
            },
            
            ankiSuspendCard: function() {
                return callPython('ankiSuspendCard');
            },
            
            ankiSuspendNote: function() {
                return callPython('ankiSuspendNote');
            },
            
            ankiResetProgress: function() {
                return callPython('ankiResetProgress');
            },
            
            ankiSearchCard: function(query) {
                return callPython('ankiSearchCard', { query: query });
            },
            
            ankiSetCardDue: function(days) {
                return callPython('ankiSetCardDue', { days: days });
            },
            
            // Reviewer Control APIs
            ankiGetDebugInfo: function() {
                return callPython('ankiGetDebugInfo');
            },
            
            ankiIsDisplayingAnswer: function() {
                return callPython('ankiIsDisplayingAnswer');
            },
            
            ankiShowAnswer: function() {
                return callPython('ankiShowAnswer');
            },
            
            ankiAnswerEase1: function() {
                return callPython('ankiAnswerEase1');
            },
            
            ankiAnswerEase2: function() {
                return callPython('ankiAnswerEase2');
            },
            
            ankiAnswerEase3: function() {
                return callPython('ankiAnswerEase3');
            },
            
            ankiAnswerEase4: function() {
                return callPython('ankiAnswerEase4');
            },
            
            // Alternative names for compatibility
            buttonAnswerEase1: function() {
                return callPython('buttonAnswerEase1');
            },
            
            buttonAnswerEase2: function() {
                return callPython('buttonAnswerEase2');
            },
            
            buttonAnswerEase3: function() {
                return callPython('buttonAnswerEase3');
            },
            
            buttonAnswerEase4: function() {
                return callPython('buttonAnswerEase4');
            },
            
            // Text-to-Speech APIs
            ankiTtsSpeak: function(text, queueMode) {
                queueMode = queueMode !== undefined ? queueMode : 0;
                return callPython('ankiTtsSpeak', { text: text, queue_mode: queueMode });
            },
            
            ankiTtsSetLanguage: function(languageCode) {
                return callPython('ankiTtsSetLanguage', { language_code: languageCode });
            },
            
            ankiTtsSetPitch: function(pitch) {
                return callPython('ankiTtsSetPitch', { pitch: pitch });
            },
            
            ankiTtsSetSpeechRate: function(rate) {
                return callPython('ankiTtsSetSpeechRate', { rate: rate });
            },
            
            ankiTtsIsSpeaking: function() {
                return callPython('ankiTtsIsSpeaking');
            },
            
            ankiTtsStop: function() {
                return callPython('ankiTtsStop');
            },
            
            ankiTtsFieldModifierIsAvailable: function() {
                return callPython('ankiTtsFieldModifierIsAvailable');
            },
            
            // UI Control APIs
            ankiIsInFullscreen: function() {
                return callPython('ankiIsInFullscreen');
            },
            
            ankiIsTopbarShown: function() {
                return callPython('ankiIsTopbarShown');
            },
            
            ankiIsInNightMode: function() {
                return callPython('ankiIsInNightMode');
            },
            
            ankiEnableHorizontalScrollbar: function(enabled) {
                return callPython('ankiEnableHorizontalScrollbar', { enabled: enabled });
            },
            
            ankiEnableVerticalScrollbar: function(enabled) {
                return callPython('ankiEnableVerticalScrollbar', { enabled: enabled });
            },
            
            ankiShowNavigationDrawer: function() {
                return callPython('ankiShowNavigationDrawer');
            },
            
            ankiShowOptionsMenu: function() {
                return callPython('ankiShowOptionsMenu');
            },
            
            ankiShowToast: function(text, shortLength) {
                shortLength = shortLength !== undefined ? shortLength : true;
                return callPython('ankiShowToast', { text: text, short_length: shortLength });
            },
            
            // Tag Management APIs
            ankiSetNoteTags: function(tags) {
                return callPython('ankiSetNoteTags', { tags: tags });
            },
            
            ankiGetNoteTags: function() {
                return callPython('ankiGetNoteTags');
            },
            
            ankiAddTagToNote: function(tag) {
                return callPython('ankiAddTagToNote', { tag: tag });
            },
            
            // Utility APIs
            ankiIsActiveNetworkMetered: function() {
                return callPython('ankiIsActiveNetworkMetered');
            },
            
            // Deprecated/Stub APIs (for compatibility)
            ankiSearchCardWithCallback: function(query) {
                console.warn('ankiSearchCardWithCallback is not fully supported on desktop');
                return this.ankiSearchCard(query);
            },
            
            ankiSttSetLanguage: function(languageCode) {
                console.warn('Speech-to-text is not supported on desktop');
                return Promise.resolve(false);
            },
            
            ankiSttStart: function() {
                console.warn('Speech-to-text is not supported on desktop');
                return Promise.resolve(false);
            },
            
            ankiSttStop: function() {
                console.warn('Speech-to-text is not supported on desktop');
                return Promise.resolve(false);
            },
            
            ankiAddTagToCard: function() {
                console.warn('ankiAddTagToCard is deprecated, use ankiSetNoteTags instead');
                return Promise.resolve({ success: false, value: false });
            }
        };
    }
    
    /**
     * AnkiDroidJS Constructor
     * Supports both `new AnkiDroidJS(contract)` and `AnkiDroidJS.init(contract)` patterns
     * @param {Object} contract - API contract with version and developer info
     * @constructor
     */
    window.AnkiDroidJS = function(contract) {
        // Support constructor pattern
        if (!(this instanceof window.AnkiDroidJS)) {
            return new window.AnkiDroidJS(contract);
        }
        
        // Validate contract
        if (!contract || !contract.developer) {
            console.error('AnkiDroidJS: Developer contact information required');
            throw new Error('AnkiDroidJS: Developer contact required in contract');
        }
        
        if (contract.version && contract.version !== '0.0.3') {
            console.warn('AnkiDroidJS: Version mismatch. Expected 0.0.3, got ' + contract.version);
        }
        
        // Log initialization
        console.log('AnkiDroidJS initialized for developer: ' + contract.developer);
        
        // Copy all API methods to this instance
        var api = createAPI();
        for (var key in api) {
            if (api.hasOwnProperty(key)) {
                this[key] = api[key];
            }
        }
        
        return this;
    };
    
    // Also support the old init pattern
    window.AnkiDroidJS.init = function(contract) {
        return new window.AnkiDroidJS(contract);
    };
    
    // Expose common button functions globally for template compatibility
    // This allows templates to call buttonAnswerEase3() directly
    window.buttonAnswerEase1 = function() {
        if (window.api && window.api.buttonAnswerEase1) {
            return window.api.buttonAnswerEase1();
        }
        return callPython('buttonAnswerEase1');
    };
    
    window.buttonAnswerEase2 = function() {
        if (window.api && window.api.buttonAnswerEase2) {
            return window.api.buttonAnswerEase2();
        }
        return callPython('buttonAnswerEase2');
    };
    
    window.buttonAnswerEase3 = function() {
        if (window.api && window.api.buttonAnswerEase3) {
            return window.api.buttonAnswerEase3();
        }
        return callPython('buttonAnswerEase3');
    };
    
    window.buttonAnswerEase4 = function() {
        if (window.api && window.api.buttonAnswerEase4) {
            return window.api.buttonAnswerEase4();
        }
        return callPython('buttonAnswerEase4');
    };
    
    // Also expose showAnswer() for template compatibility
    // Store the original if it exists
    var _originalShowAnswer = window.showAnswer;
    
    window.showAnswer = function() {
        // Call Python synchronously without waiting for callback
        // This is needed because the page will reload and callbacks won't work
        // Use callback ID -1 which will be ignored by our callback handler
        if (typeof pycmd !== 'undefined') {
            pycmd('ankidroidjs:-1:ankiShowAnswer:{}');
        } else if (_originalShowAnswer) {
            _originalShowAnswer();
        }
    };
    
})();