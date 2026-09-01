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


class IntegrationTestAdmissionEnquiry(IntegrationTestCase):
	def test_required_fields_are_enforced(self):
		enquiry = frappe.get_doc({"doctype": "Admission Enquiry"})

		with self.assertRaises(frappe.MandatoryError):
			enquiry.insert()

	def test_creates_enquiry_for_an_academic_programme(self):
		programme_name = f"Test Programme {uuid4().hex}"
		programme = frappe.get_doc(
			{
				"doctype": "Academic Programme",
				"name": programme_name,
				"programme": programme_name,
			}
		).insert(ignore_links=True)

		enquiry = frappe.get_doc(
			{
				"doctype": "Admission Enquiry",
				"student_name": "Grace Hopper",
				"guardian_name": "Annie Hopper",
				"programme": programme.name,
				"dob": "1906-12-09",
				"email": "grace@example.com",
			}
		).insert()

		self.assertTrue(enquiry.name.startswith("AE-"))
		self.assertEqual(enquiry.programme, programme.name)
		self.assertEqual(enquiry.dob, "1906-12-09")
