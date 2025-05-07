[![License: AGPL v3](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)
[![Pipeline Status](https://gitlab.com/tawasta/odoo/stock/badges/17.0-dev/pipeline.svg)](https://gitlab.com/tawasta/odoo/stock/-/pipelines/)

Stock
=====
Stock Addons for Odoo.

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[stock_auditlog_rules](stock_auditlog_rules/) | 17.0.1.0.0 |  | Adds audit log rules for stock.warehouse and stock.location
[stock_batch_transfer_carrier_and_tracking_ref](stock_batch_transfer_carrier_and_tracking_ref/) | 17.0.1.1.1 |  | Adds Carrier and Tracking reference to batch transfer
[stock_batch_transfer_contact_and_delivery_address](stock_batch_transfer_contact_and_delivery_address/) | 17.0.1.0.0 |  | Adds a default delivery address and contact to batch transfer
[stock_disable_invoice_shipping_on_delivery](stock_disable_invoice_shipping_on_delivery/) | 17.0.1.0.0 |  | Disable picking auto-generated delivery SO lines
[stock_dispatch_note_report_template](stock_dispatch_note_report_template/) | 17.0.1.0.1 |  | Adds weights, dates and clickable print is shown as 'Dispatch Note'
[stock_hide_packing_buttons](stock_hide_packing_buttons/) | 17.0.1.0.0 |  | Hides "put in pack" buttons
[stock_inventory_adjustment_domain_company](stock_inventory_adjustment_domain_company/) | 17.0.1.0.1 |  | Show stock locations without company in inventory adjustments
[stock_inventory_include_exhausted](stock_inventory_include_exhausted/) | 17.0.1.0.0 |  | Option to automatically add rows for exhausted products when doing inventory
[stock_inventory_quantity_history_stock_inventory_link](stock_inventory_quantity_history_stock_inventory_link/) | 17.0.1.0.1 |  | Show the new qty fields also in list view provided by the another OCA inventory module
[stock_location_analytic_account](stock_location_analytic_account/) | 17.0.1.0.1 |  | Integrate stock location with analytic account
[stock_location_auditlog_rules](stock_location_auditlog_rules/) | 17.0.1.0.0 |  | Adds audit log rules for stock.warehouse and stock.location
[stock_location_excess_mark](stock_location_excess_mark/) | 17.0.1.1.0 |  | Select a stock location and mark it as of excess type
[stock_move_carrier_in_view_and_filter](stock_move_carrier_in_view_and_filter/) | 17.0.1.0.1 |  | Carrier info added to stock move list view and as a filter
[stock_move_pivot_disable_count_as_default](stock_move_pivot_disable_count_as_default/) | 17.0.1.0.0 |  | Disables the Count variable as default on stock move pivot.
[stock_move_pivot_report_sh_product_tag](stock_move_pivot_report_sh_product_tag/) | 17.0.1.0.0 |  | Group by SH product tags in Stock Move pivot view
[stock_move_recompute_state_scheduled](stock_move_recompute_state_scheduled/) | 17.0.1.0.0 |  | Scheduled action to recompute stock move statuses
[stock_move_recompute_volume_scheduled](stock_move_recompute_volume_scheduled/) | 17.0.1.0.0 |  | Scheduled action to recompute stock move volumes
[stock_move_search](stock_move_search/) | 17.0.1.0.0 |  | Additional Search options for Stock Move
[stock_package_sticker](stock_package_sticker/) | 17.0.1.1.0 |  | Print Package sticker from pickings
[stock_picking_bypass_reservation](stock_picking_bypass_reservation/) | 17.0.1.0.1 |  | Stock Picking Bypass Reservation
[stock_picking_carrier_info_form_header](stock_picking_carrier_info_form_header/) | 17.0.1.0.1 |  | Reposition Carrier info on picking form
[stock_picking_chatter_attachment_visible](stock_picking_chatter_attachment_visible/) | 17.0.1.0.0 |  | Attachments are visible on pickings
[stock_picking_comment](stock_picking_comment/) | 17.0.1.1.4 |  | External comment for stock picking Delivery Slip and Picking Operations
[stock_picking_country_group_text](stock_picking_country_group_text/) | 17.0.1.0.0 |  | Get stock picking reports' text from country groups setting
[stock_picking_create_manufacturing_order_from_move](stock_picking_create_manufacturing_order_from_move/) | 17.0.1.0.0 |  | Create Manufacturing order from stock picking move
[stock_picking_customer_reference](stock_picking_customer_reference/) | 17.0.1.0.1 |  | Stock Picking Customer Reference
[stock_picking_dispatch_fields](stock_picking_dispatch_fields/) | 17.0.1.0.0 |  | Add different fields to picking for Dispatch Note
[stock_picking_dropshipping_move_description_from_product_name](stock_picking_dropshipping_move_description_from_product_name/) | 17.0.1.0.0 |  | Do not use product's 'description' field as move description
[stock_picking_internal_transfer_domain_internal_location](stock_picking_internal_transfer_domain_internal_location/) | 17.0.1.0.0 |  | Use Internal location as domain for Internal transfers
[stock_picking_move_lines_partner](stock_picking_move_lines_partner/) | 17.0.1.0.0 |  | Stock Picking Move Lines Partner
[stock_picking_operations_show_name](stock_picking_operations_show_name/) | 17.0.1.0.0 |  | Show name field on Stock Picking operations
[stock_picking_override_values](stock_picking_override_values/) | 17.0.1.0.0 |  | Allow overriding new picking values with system parameters
[stock_picking_printed](stock_picking_printed/) | 17.0.1.0.0 |  | Mark stock pickings as printed and log date after printing picking list
[stock_picking_process_as_sudo](stock_picking_process_as_sudo/) | 17.0.1.1.1 |  | Process Stock Pickings as Admin user
[stock_picking_purchase_related_sale_order_customer](stock_picking_purchase_related_sale_order_customer/) | 17.0.1.0.0 |  | Get Sale Order Partner to Stock Picking from Purchase Order
[stock_picking_receipt_set_all_moves_done](stock_picking_receipt_set_all_moves_done/) | 17.0.1.0.1 |  | Use button to set all moves as done on receipt
[stock_picking_reinvoice](stock_picking_reinvoice/) | 17.0.1.0.1 |  | Allow making invoices from stock pickings
[stock_picking_reserve_chosen_moves](stock_picking_reserve_chosen_moves/) | 17.0.1.0.0 |  | Select manually the moves to be reserved on deliveries
[stock_picking_sale_order_id](stock_picking_sale_order_id/) | 17.0.1.0.1 |  | Get Sale Order to Stock Picking from Purchase Order
[stock_picking_sort_by_print_and_scheduled_date](stock_picking_sort_by_print_and_scheduled_date/) | 17.0.1.0.0 |  | Stock Picking sort by printed and Scheduled Date
[stock_picking_source_document_link](stock_picking_source_document_link/) | 17.0.1.0.0 |  | Add link to source document
[stock_picking_tree_date_deadline_as_date](stock_picking_tree_date_deadline_as_date/) | 17.0.1.0.0 |  | Show date deadline as date in stock picking tree
[stock_picking_tree_date_done](stock_picking_tree_date_done/) | 17.0.1.0.0 |  | Stock Picking date done in tree view
[stock_picking_tree_effective_date](stock_picking_tree_effective_date/) | 17.0.1.0.1 |  | Adds effective date from Sale Order to picking list view
[stock_picking_tree_scheduled_date_as_date](stock_picking_tree_scheduled_date_as_date/) | 17.0.1.0.0 |  | Show scheduled date as date in stock picking tree
[stock_picking_view_vendor_product](stock_picking_view_vendor_product/) | 17.0.1.0.0 |  | Vendor Product Name and Code are added to Picking form view
[stock_picking_volume_in_tree_and_prints](stock_picking_volume_in_tree_and_prints/) | 17.0.1.0.0 |  | Picking's Volume is shown in list view and picking prints
[stock_product_qty_available_unreserved](stock_product_qty_available_unreserved/) | 17.0.1.0.1 |  | Add unreserved available (on hand - reserved)
[stock_quant_list_view_increased_limit](stock_quant_list_view_increased_limit/) | 17.0.1.0.0 |  | Increase the number of shown lines to 300
[stock_report_add_description_to_picking](stock_report_add_description_to_picking/) | 17.0.1.0.1 |  | Adds Description column to picking report
[stock_report_carrier_transportation_mode](stock_report_carrier_transportation_mode/) | 17.0.1.0.0 |  | Delivery slip Carrier – Mode of transportation
[stock_report_code_as_name_stock_picking](stock_report_code_as_name_stock_picking/) | 17.0.1.0.0 |  | Replace Product name with product code
[stock_report_customer_address](stock_report_customer_address/) | 17.0.1.0.0 |  | Stock Report Customer Address
[stock_report_customer_reference](stock_report_customer_reference/) | 17.0.1.0.1 |  | Stock Report Customer Reference
[stock_report_customer_reference_under_address](stock_report_customer_reference_under_address/) | 17.0.1.0.2 |  | Customer Reference under address
[stock_report_date_done](stock_report_date_done/) | 17.0.1.0.1 |  | Stock Picking Report Date of Transfer
[stock_report_element_sizes](stock_report_element_sizes/) | 17.0.1.0.3 |  | Stock Report element size changes
[stock_report_enable_translation_by_partner](stock_report_enable_translation_by_partner/) | 17.0.1.0.0 |  | Use the language set for Delivery Address in Picking Operations PDF print
[stock_report_invoice_and_delivery_address](stock_report_invoice_and_delivery_address/) | 17.0.1.1.0 |  | Adds Invoice and Delivery addresses to delivery slip
[stock_report_kit_quantity](stock_report_kit_quantity/) | 17.0.1.0.0 |  | Show ordered and delivered quantity of kits in Delivery slip
[stock_report_label_product_barcode](stock_report_label_product_barcode/) | 17.0.1.0.0 |  | Print Product Labels with barcodes
[stock_report_label_product_ean_code](stock_report_label_product_ean_code/) | 17.0.1.0.0 |  | Print Product Labels with EAN codes
[stock_report_our_reference](stock_report_our_reference/) | 17.0.1.0.2 |  | Stock Picking and Delivery Slip Report Our Reference
[stock_report_picking_customer_address](stock_report_picking_customer_address/) | 17.0.1.0.0 |  | Stock Report picking Customer Address details
[stock_report_picking_header_shrink](stock_report_picking_header_shrink/) | 17.0.1.0.0 |  | Decrease font size of stock picking print header section
[stock_report_picking_hide_footer](stock_report_picking_hide_footer/) | 17.0.1.0.0 |  | Hide footer on Picking Operations
[stock_report_picking_product_receipt_description](stock_report_picking_product_receipt_description/) | 17.0.1.0.0 |  | Show 'Description for receipts' text on Picking list
[stock_report_picking_vendor_product](stock_report_picking_vendor_product/) | 17.0.1.1.1 |  | Vendor Product name and code for Picking list
[stock_report_picking_warning_text](stock_report_picking_warning_text/) | 17.0.1.0.0 |  | Show warning on picking list printout instead of a form popup
[stock_report_product_customer_code](stock_report_product_customer_code/) | 17.0.2.0.1 |  | Place Product Customer code to picking print
[stock_report_quantity_decimals](stock_report_quantity_decimals/) | 17.0.1.0.3 |  | Modifications to Stock Reports' decimal precision
[stock_report_scheduled_date_as_date_only](stock_report_scheduled_date_as_date_only/) | 17.0.1.0.1 |  | Stock Picking and Delivery Slip Report Scheduled Date as Date only
[stock_report_set_company_as_sale_order_company](stock_report_set_company_as_sale_order_company/) | 17.0.1.0.0 |  | Show related sale order's company on prints instead of the default picking company
[stock_report_show_only_ordered_qty](stock_report_show_only_ordered_qty/) | 17.0.1.0.0 |  | Show only the ordered quantity in delivery slip as 'Quantity'
[stock_report_title](stock_report_title/) | 17.0.1.3.3 |  | Stock Picking and Delivery Slip Report Title
[stock_report_week_of_shipment](stock_report_week_of_shipment/) | 17.0.1.0.0 |  | Add week of shipment to Picking report
[stock_report_year_of_shipment](stock_report_year_of_shipment/) | 17.0.1.0.0 |  | Add year of shipment to delivery slip
[stock_see_product_forecasted_with_sudo](stock_see_product_forecasted_with_sudo/) | 17.0.1.0.0 |  | Form the Product Forecast Report with sudo rights
[stock_valuation_layer_archive](stock_valuation_layer_archive/) | 17.0.1.0.0 |  | Allows archiving inventory valuation records

[//]: # (end addons)
