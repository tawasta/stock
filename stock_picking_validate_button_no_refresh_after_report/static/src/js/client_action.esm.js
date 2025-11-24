/** @odoo-module **/

import {_t} from "@web/core/l10n/translation";
import {registry} from "@web/core/registry";
import {sprintf} from "@web/core/utils/strings";

async function doMultiPrint(env, action) {
    /**
    Modified function which is used when validating stock pickings.
    Soft reload is used to avoid reloading a page completely, which
    would remove the filters and sorting that a user has used on a view.
    **/
    for (const report of action.params.reports) {
        if (report.type != "ir.actions.report") {
            env.services.notification.add(
                _t("Incorrect type of action submitted as a report, skipping action"),
                {
                    title: _t("Report Printing Error"),
                }
            );
            continue;
        } else if (report.report_type === "qweb-html") {
            env.services.notification.add(
                sprintf(
                    _t("HTML reports cannot be auto-printed, skipping report: %s"),
                    report.name
                ),
                {
                    title: _t("Report Printing Error"),
                }
            );
            continue;
        }
        // WARNING: potential issue if pdf generation fails, then action_service defaults
        // to HTML and rest of the action chain will break w/potentially never resolving promise
        await env.services.action.doAction({type: "ir.actions.report", ...report});
    }
    if (action.params.anotherAction) {
        return env.services.action.doAction(action.params.anotherAction);
    } else if (action.params.onClose) {
        // Handle special cases such as barcode
        action.params.onClose();
    } else {
        // This is the modified part.
        // Soft refresh used so that the backorder dialog is closed.
        const actionService = env.services.action;
        actionService.doAction({
            type: "ir.actions.client",
            tag: "soft_reload",
        });
    }
}

registry.category("actions").remove("do_multi_print");
registry.category("actions").add("do_multi_print", doMultiPrint);
