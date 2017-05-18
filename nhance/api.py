from __future__ import unicode_literals
import frappe
from frappe.utils import cint, flt, cstr, comma_or, getdate
from frappe import _, throw, msgprint
from frappe.model.mapper import get_mapped_doc


@frappe.whitelist()
def make_proposal_stage(source_name, target_doc=None):

	target_doc = get_mapped_doc("Opportunity", source_name, {
		"Opportunity": {
			"doctype": "Proposal Stage",
			"field_map": {
				"name": "reference_name"
			 }
		}
		
	}, target_doc, set_missing_values)

	return target_doc

@frappe.whitelist()
def make_interactions(source_name, target_doc=None):
	
	target_doc = get_mapped_doc("Opportunity", source_name, {
		"Opportunity": {
			"doctype": "Interactions",
			"field_map": {
				"name": "reference_document",
				"doctype": "reference_doctype"
				}
		}
		
	}, target_doc, set_missing_values)

	return target_doc

@frappe.whitelist()
def make_interactions_quot(source_name, target_doc=None):
	src_name = "Quotation"
	target_doc = get_mapped_doc("Quotation", source_name, {
		"Quotation": {
			"doctype": "Interactions",
			"field_map": {
				"name": "reference_document",
				"doctype": "reference_doctype"
				}
		}
		
	}, target_doc, set_missing_values)

	return target_doc


@frappe.whitelist()
def set_proposal_stage_values(opportunity):

        
	max_closing_date = frappe.db.sql("""select max(closing_date) from `tabProposal Stage` where reference_name=%s""",
				(opportunity))
				
        sc_rec = frappe.db.sql("""select value, closing_date, stage, opportunity_purpose, buying_status, support_needed, competition_status
		from `tabProposal Stage`
		where reference_name=%s and closing_date = %s""",
		(opportunity, max_closing_date))
        return sc_rec

def set_missing_values(source, target_doc):
	target_doc.run_method("set_missing_values")
	target_doc.run_method("calculate_taxes_and_totals")
