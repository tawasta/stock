from odoo import api, models, _


class StockMoveCreateManufacturingOrder(models.TransientModel):

    _name = 'stock.move.create.manufacturing.order'

    @api.multi
    def create_manufacturing_orders(self):
        picking_ids = self.env['stock.picking'].browse(
            self.env.context.get('active_ids', []))

        created_mos    = []
        validated_mos  = []
        ignored_draft  = []
        ignored_done   = []
        ignored_cancel = []
        deliv_message  = ''
        mo_message     = ''

        for picking in picking_ids:
            if picking.state == 'draft':
                ignored_draft.append(picking.name)
            elif picking.state == 'done':
                ignored_done.append(picking.name)
            elif picking.state == 'cancel':
                ignored_cancel.append(picking.name)
            else:
                # Check availability of picking moves
                picking.action_assign()
                for move in picking.move_lines:
                    if move.has_bom and move.state not in \
                            ('draft', 'cancel', 'assigned', 'done') \
                            and move.mo_to_complete:
                        if not move.manufacturing_order_id:
                            mo = move.create_manufacturing_order()
                            created_mos.append(mo.name)
                        move.validate_manufacturing_order()
                        validated_mos.append(
                                move.manufacturing_order_id.name)

        deliv_message = "{}{}{}".format(
            _("These deliveries were ignored because they are in Draft state: \
            \n%s\n\n") % '\n'.join(ignored_draft) if ignored_draft else '',
            _("These deliveries were ignored because they are in Done state: \
            \n%s\n\n") % '\n'.join(ignored_done) if ignored_done else '',
            _("These deliveries were ignored because they are in Cancelled " \
            "state: \n%s\n\n") % '\n'.join(ignored_cancel) \
            if ignored_cancel else '',
        )

        no_mos = "Nothing could be manufactured from the selected Deliveries."

        mo_message = "{}{}".format(
            "The following Manufacturing Orders were created:\
            \n%s\n\n" % '\n'.join(created_mos) if created_mos else '',
            "The following Manufacturing Orders were validated:\
            \n%s\n\n" % '\n'.join(validated_mos) if validated_mos else '',
        ) or no_mos

        message = self.env['stock.move.create.manufacturing.order.message'].\
            create({
                'delivery_message': deliv_message,
                'mo_message': mo_message
            })

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'stock.move.create.manufacturing.order.message',
            'view_type': 'form',
            'view_mode': 'form',
            'res_id': message.id,
            'target': 'new',
        }
