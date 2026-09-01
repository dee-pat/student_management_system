# Copyright (c) 2026, Deepak Patel and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class Student(Document):
	def validate(self):
		self.full_name = " ".join(filter(None, [self.first_name, self.last_name]))
