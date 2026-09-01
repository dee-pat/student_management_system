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


class IntegrationTestStudent(IntegrationTestCase):
	def test_gender_is_required(self):
		student = frappe.get_doc(
			{
				"doctype": "Student",
				"first_name": f"Missing Gender {uuid4().hex}",
			}
		)

		with self.assertRaises(frappe.MandatoryError):
			student.insert()

	def test_rejects_unsupported_gender(self):
		student = frappe.get_doc(
			{
				"doctype": "Student",
				"first_name": f"Invalid Gender {uuid4().hex}",
				"gender": "Other",
			}
		)

		with self.assertRaises(frappe.ValidationError):
			student.insert()

	def test_saves_student_with_supported_gender_and_enrollment(self):
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
				"first_name": "Ada",
				"last_name": "Lovelace",
				"gender": "Female",
				"date_of_birth": "1815-12-10",
				"table_oldt": [
					{
						"doctype": "Student Course Enrollment",
						"programme": programme.name,
						"date_of_enrollment": "2026-01-15",
						"credit": "3",
					}
				],
			}
		).insert()

		self.assertIsNotNone(student.name)
		self.assertEqual(student.gender, "Female")
		self.assertEqual(student.date_of_birth.isoformat(), "1815-12-10")
		self.assertEqual(student.table_oldt[0].programme, programme.name)

	def test_student_field_contract(self):
		meta = frappe.get_meta("Student")
		gender = meta.get_field("gender")

		self.assertEqual(gender.fieldtype, "Select")
		self.assertTrue(gender.reqd)
		self.assertEqual(gender.options, "Male\nFemale")
		self.assertTrue(meta.get_field("full_name").read_only)
