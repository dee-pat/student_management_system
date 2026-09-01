import { expect, test } from "@playwright/test";

const green100 = "rgb(228, 245, 233)";

test.describe("Student Desk form", () => {
	test("creates a student and styles the read-only full name", async ({ page }) => {
		const suffix = Date.now().toString();

		await page.goto(`/app/student/new-student-${suffix}`);
		await expect(page.getByLabel("First Name")).toBeVisible();

		await page.getByLabel("First Name").fill("Playwright");
		await page.getByLabel("Last Name").fill(`Student ${suffix}`);
		await page.getByLabel("Gender").selectOption({ label: "Female" });
		await page.getByLabel("Date of Birth").fill("2004-06-15");
		await page.getByRole("button", { name: "Save", exact: true }).click();

		await expect(page).toHaveURL(/\/app\/student\/(?!new-student-)[^/?#]+/);
		await expect(page.getByLabel("Gender")).toHaveValue("Female");

		const fullNameSurface = page
			.locator(
				'[data-fieldname="full_name"] input:visible, [data-fieldname="full_name"] .control-value:visible',
			)
			.first();
		await expect(fullNameSurface).toBeVisible();
		await expect(fullNameSurface).toHaveCSS("background-color", green100);
	});

	test("shows gender as mandatory before saving", async ({ page }) => {
		const suffix = Date.now().toString();

		await page.goto(`/app/student/new-student-mandatory-${suffix}`);
		await page.getByLabel("First Name").fill("Required");
		await page.getByLabel("Last Name").fill(`Gender ${suffix}`);
		await page.getByRole("button", { name: "Save", exact: true }).click();

		await expect(page.getByText("Missing Fields", { exact: true })).toBeVisible();
		await expect(page.getByText("Gender is required.", { exact: true })).toBeVisible();
	});
});
