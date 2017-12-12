# -*- coding: utf-8 -*-
# Copyright (c) 2017, openetech and contributors
# For license information, please see license.txt
from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe import _
from frappe.utils import cstr

class GreenLot(Document):
	def validate(self):
		def update_lot_no():
			last_series_no = frappe.db.sql("""select year,last_series_used from `tabLot Series`
								where active = 1""")
			if last_series_no:
				year = last_series_no[0][0]
				last_no = last_series_no[0][1]
				new_no = last_no + 1
				str_len_new_series_no = len(cstr(new_no))
				if str_len_new_series_no < 3:
					no_of_leading_zeroes = 3 - str_len_new_series_no
					str_new_series_no = cstr(new_no)
					if no_of_leading_zeroes == 2:
						str_new_series_no = "00"+ str_new_series_no
					elif no_of_leading_zeroes == 1:
						str_new_series_no = "0"+ str_new_series_no
					lot_no = "L" + year + str_new_series_no
					self.lot = lot_no
					doc_lot_series = frappe.get_doc("Lot Series",year)
					doc_lot_series.last_series_used = new_no
					doc_lot_series.save()
				elif str_len_new_series_no == 3:
					lot_no = "L" + year + str_new_series_no
					self.lot = lot_no
					doc_lot_series = frappe.get_doc("Lot Series",year)
					doc_lot_series.last_series_used = new_no
					doc_lot_series.save()
				elif str_len_new_series_no > 0:
					frappe.throw(_("Lot number is not generated. Please contact your admin."))

		if self.lot:
			lot_check = frappe.db.sql("""select name from `tabGreen Lot` where lot = %s""",self.lot)
			if lot_check:
				name = lot_check[0][0]
				if self.name == name:
					pass
				else:
					frappe.throw(_("Lot ID {0} already exists").format(self.lot))
		else:
			update_lot_no()

		if not self.lot:
			frappe.throw(_("Lot number is not generated. Please contact your admin."))

	def on_submit(self):
		pass

