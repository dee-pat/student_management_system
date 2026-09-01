import { defineConfig, devices } from "@playwright/test";

const authFile = "e2e/.auth/user.json";

export default defineConfig({
	testDir: "./e2e/tests",
	fullyParallel: false,
	forbidOnly: Boolean(process.env.CI),
	retries: process.env.CI ? 2 : 0,
	workers: 1,
	reporter: process.env.CI ? [["github"], ["blob"]] : "html",
	timeout: 60_000,
	expect: {
		timeout: 10_000,
	},
	use: {
		baseURL: process.env.BASE_URL || "http://student_management_system.test:8000",
		trace: "on-first-retry",
		video: "retain-on-failure",
		screenshot: "only-on-failure",
		actionTimeout: 15_000,
		navigationTimeout: 30_000,
	},
	projects: [
		{
			name: "setup",
			testMatch: /auth\.setup\.ts/,
		},
		{
			name: "chromium",
			use: {
				...devices["Desktop Chrome"],
				storageState: authFile,
			},
			testIgnore: /auth\.setup\.ts/,
			dependencies: ["setup"],
		},
	],
});
