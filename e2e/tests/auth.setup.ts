import fs from "node:fs";
import path from "node:path";

import { expect, test as setup } from "@playwright/test";

const authFile = "e2e/.auth/user.json";

setup("authenticate", async ({ page }) => {
  fs.mkdirSync(path.dirname(authFile), { recursive: true });

  const loginResponse = await page.request.post("/api/method/login", {
    form: {
      usr: process.env.FRAPPE_USER || "Administrator",
      pwd: process.env.FRAPPE_PASSWORD || "admin",
    },
  });
  expect(loginResponse.ok()).toBeTruthy();

  const userResponse = await page.request.get(
    "/api/method/frappe.auth.get_logged_user"
  );
  expect(userResponse.ok()).toBeTruthy();
  const userData = await userResponse.json();
  expect(userData.message).not.toBe("Guest");

  await page.goto("/app");
  await expect(page).not.toHaveURL(/\/login/);
  await page.context().storageState({ path: authFile });
});
