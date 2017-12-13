# -*- coding: utf-8 -*-
# Copyright (c) 2017, openetech and contributors
# For license information, please see license.txt
from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe import _
from frappe.utils import cstr,dateutils,nowdate
from operator import itemgetter

class GreenLot(Document):
	def autoname(self):
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
		self.name = self.lot

	def validate(self):
		if not self.lot:
			frappe.throw(_("Lot number is not generated. Please contact your admin."))

		veh_ref_cp = []
		for veh_ref in self.vehicle_reference:
			if veh_ref.date > nowdate():
				frappe.throw(_("Date entered cannot be greater than today's date"))
			diff = frappe.utils.date_diff(nowdate(), veh_ref.date)
			print ("hi")
			print (diff)
			if diff > 30 and not self.confirm_days_old:
				frappe.throw(_("Days Old {0} is greater than 30 days. Check Confirm Days Old to confirm.").format(diff))
			date_str = dateutils.parse_date(veh_ref.date)
			year = date_str[2:4]
			month = date_str[5:7]
			day = date_str[8:11]
			veh_ref.vehicle_reference = year + month + day + "." + veh_ref.truck_sequence + veh_ref.species_sequence
			veh_ref_cp.append({
				'vehicle_reference': veh_ref.vehicle_reference,
				'date': veh_ref.date,
				'truck_sequence': veh_ref.truck_sequence,
				'species_sequence': veh_ref.species_sequence
						})

		duplicates = [ref for n, ref in enumerate(veh_ref_cp) if ref in veh_ref_cp[:n]]
		if duplicates:
			frappe.throw(_("Duplicates exist for Date, TT and SS combination"))

		if self.sort_order == "Ascending":
			sort_order = False
		else:
			sort_order = True
		veh_ref_cp = sorted(veh_ref_cp,key=itemgetter('vehicle_reference'),reverse=sort_order)
		self.vehicle_reference = []
		for ref in veh_ref_cp:
			self.append('vehicle_reference',
			{'date': ref["date"],
			'truck_sequence': ref["truck_sequence"],
			'species_sequence': ref["species_sequence"],
			'vehicle_reference': ref["vehicle_reference"]})
