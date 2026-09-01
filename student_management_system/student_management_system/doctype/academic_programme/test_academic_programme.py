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


class IntegrationTestAcademicProgramme(IntegrationTestCase):
	def test_programme_is_required(self):
		programme = frappe.get_doc(
			{
				"doctype": "Academic Programme",
				"name": f"Missing Programme {uuid4().hex}",
			}
		)

		with self.assertRaises(frappe.MandatoryError):
			programme.insert()

	def test_active_defaults_to_disabled(self):
		programme_name = f"Test Programme {uuid4().hex}"
		programme = frappe.get_doc(
			{
				"doctype": "Academic Programme",
				"name": programme_name,
				"programme": programme_name,
			}
		).insert(ignore_links=True)

		self.assertEqual(programme.active, 0)
