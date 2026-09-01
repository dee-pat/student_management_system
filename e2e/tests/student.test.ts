import { expect, test } from "@playwright/test";

const green100 = "rgb(228, 245, 233)";

test.describe("Student Desk form", () => {
  test("creates a student and styles the read-only full name", async ({
    page,
  }) => {
    const suffix = Date.now().toString();

    await page.goto(`/desk/student/new-student-${suffix}`);
    const firstName = page.locator('[data-fieldname="first_name"] input');
    const lastName = page.locator('[data-fieldname="last_name"] input');
    const gender = page.locator('[data-fieldname="gender"] select');
    const dateOfBirth = page.locator('[data-fieldname="date_of_birth"] input');

    await expect(firstName).toBeVisible();

    await firstName.fill("Playwright");
    await lastName.fill(`Student ${suffix}`);
    await gender.selectOption({ label: "Female" });
    await dateOfBirth.fill("06-15-2004");
    await dateOfBirth.press("Tab");
    await page.getByRole("button", { name: "Save", exact: true }).click();

    await expect(page).toHaveURL(/\/desk\/student\/(?!new-student-)[^/?#]+/);
    await expect(gender).toHaveValue("Female");

    const fullNameSurface = page
      .locator(
        '[data-fieldname="full_name"] input:visible, [data-fieldname="full_name"] .control-value:visible'
      )
      .first();
    await expect(fullNameSurface).toBeVisible();
    await expect(fullNameSurface).toHaveCSS("background-color", green100);
  });

  test("shows gender as mandatory in Desk", async ({ page }) => {
    const suffix = Date.now().toString();

    await page.goto(`/desk/student/new-student-mandatory-${suffix}`);

    await expect(
      page.locator('[data-fieldname="gender"] .control-label')
    ).toHaveClass(/reqd/);
  });
});
