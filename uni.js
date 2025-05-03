// ==UserScript==
// @name         update+no-copy
// @namespace    http://tampermonkey.net/
// @version      0.1
// @description  .
// @author       YandexGPT
// @match        *://*/*
// @grant        none
// @run-at       document-start
// ==/UserScript==

(function() {

    window.addEventListener('load', function() {
        'use strict';

        setInterval(function () {
            var paragraphs = document.getElementsByTagName("p");

            for (var i = 0; i < paragraphs.length; i++) {
                // Change the user-select property value to "auto", allowing text selection
                paragraphs[i].style.userSelect = "auto";
            }

            var forms = document.getElementsByTagName('form');

            for (var c = 0; c < forms.length; c++) {
                var form = forms[c];
                if (form.hasAttribute('oncopy') || form.hasAttribute('oncut')) {
                    form.removeAttribute('oncopy');
                    form.removeAttribute('oncut');
                }
            }

         })();
    }, 2000);

})();