from frappe import _

def get_data():
	return [
		{	"module_name": "ccl",
			"label": _("Setup"),
			"icon": "icon-star",
			"items": [
				{	"type": "doctype",
					"name": "Grade",
					"label": "Grade"
				},
				{	"type": "doctype",
					"name": "Species",
					"label": "Species"
				},
				{	"type": "doctype",
					"name": "Thickness",
					"label": "Thickness"
				},
				{	"type": "doctype",
					"name": "Lot Series",
					"label": "Lot Series "
				}
			]
		},
		{	"module_name": "ccl",
			"label": _("Transactions"),
			"icon": "icon-star",
			"items": [
				{	"type": "doctype",
					"name": "Green Lot",
					"label": "Green Lot",
				}
			]
		}
]