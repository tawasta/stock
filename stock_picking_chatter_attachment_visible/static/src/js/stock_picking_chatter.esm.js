/** @odoo-module **/

import {Chatter} from "@mail/core/web/chatter";
import {patch} from "@web/core/utils/patch";

// Lisätään toiminallaisuus chatteriin
patch(Chatter.prototype, {
    setup() {
        super.setup();

        // Tallennetaan nykyinen arvo
        let currentVal = this.state.isAttachmentBoxOpened;

        // Toiminnallisuus getteriin ja setteriin isAttachmentBoxOpened muuttujalle.
        Object.defineProperty(this.state, "isAttachmentBoxOpened", {
            configurable: true,
            enumerable: true,
            get: () => {
                // Jos malli on stock.picking -> liitteiden pitäisi olla aina näkyvissä
                if (this.props && this.props.threadModel === "stock.picking") {
                    return true;
                }
                // Muuten palautetaan alkuperäinen arvo
                return currentVal;
            },
            set: (newVal) => {
                // Jos recordi on stock.picking -> liitteet aina auki
                if (this.props && this.props.threadModel === "stock.picking") {
                    currentVal = true;
                } else {
                    // Käyttäjä painoi paper clip iconia, jolloin arvo muuttui,
                    // eikä olla stock.picking recordilla. Palautetaan muutunut arvo.
                    currentVal = newVal;
                }
                return currentVal;
            },
        });
    },
});
