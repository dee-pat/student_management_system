# Copyright (c) 2026, Deepak Patel and Contributors
# See license.txt

from uuid import uuid4

import frappe
from frappe.tests import IntegrationTestCase

# On IntegrationTestCase, the doctype test records and all
# link-field test record dependencies are recursively loaded
# Use these module variables to add/remove to/from that list
EXTRA_TEST_RECORD_DEPENDENCIES = []  # eg. ["User"]
IGNORE_TEST_RECORD_DEPENDENCIES = []  # eg. ["User"]


class IntegrationTestFeeRecord(IntegrationTestCase):
	def test_required_fields_are_enforced(self):
		fee_record = frappe.get_doc({"doctype": "Fee Record"})

		with self.assertRaises(frappe.MandatoryError):
			fee_record.insert()

	def test_fee_record_can_be_submitted_for_a_student(self):
		programme_name = f"Test Programme {uuid4().hex}"
		programme = frappe.get_doc(
			{
				"doctype": "Academic Programme",
				"name": programme_name,
				"programme": programme_name,
			}
		).insert(ignore_links=True)
		student = frappe.get_doc(
			{
				"doctype": "Student",
				"first_name": "Katherine",
				"last_name": "Johnson",
				"gender": "Female",
			}
		).insert()

		fee_record = frappe.get_doc(
			{
				"doctype": "Fee Record",
				"student": student.name,
				"amount": 1250,
				"programme": programme.name,
				"paid_on": "2026-02-01",
			}
		).insert()
		fee_record.submit()

		self.assertEqual(fee_record.docstatus, 1)
		self.assertEqual(frappe.db.get_value("Fee Record", fee_record.name, "docstatus"), 1)
