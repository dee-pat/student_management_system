# Student Management System agent guidance

The parent `../../AGENTS.md` contains the shared Frappe bench and framework
rules. This file adds only the conventions for this app. Read both files before
changing the app.

## Working agreement

- Inspect the current worktree and nearby implementation before editing. Keep
  unrelated user changes intact.
- Keep app-specific skills under `.agents/skills/`. The installed skills are
  `frappe-app-dev`, `code-style`, `writing-for-agents`, `playwright`, and
  `caveman`.
- Use Caveman communication by default: terse, technically complete, and free
  of filler. Use normal detail when the user requests it or when security,
  irreversible actions, or complex sequencing requires extra clarity.
- Match verification to the change and report the exact commands and exit
  results. A check that was not run is not a passing check.
- Keep comments short and explain why a non-obvious choice exists. Prefer a
  small, direct change over a new abstraction.

## App baseline and structure

- This is a custom Frappe Framework v16 app. Use the Frappe v16.31.0-compatible
  API and Python 3.14 environment described by the app and bench metadata.
  ERPNext is not an app dependency; add it only for an explicit requirement.
- The bench root is two levels above this app. The interactive site is
  `student_management_system.localhost`; use a separate test site for tests.
- The outer Python package is `student_management_system/`. The Frappe module
  package is `student_management_system/student_management_system/`.
  DocTypes live below
  `student_management_system/student_management_system/doctype/`.
- This app currently uses Frappe Desk forms and has no Vue `frontend/` app.
  Keep DocType controllers focused and put genuinely shared server logic in a
  deliberate utility module.
- Read `pyproject.toml`, `.pre-commit-config.yaml`, `hooks.py`, the relevant
  DocType JSON/controller/client script, and its tests before extending a
  feature. Use absolute imports that match the actual package tree.

## Student DocType conventions

- The Student metadata is
  `student_management_system/student_management_system/doctype/student/student.json`.
  Its controller, client script, and integration test sit beside it.
- `Gender` is a required `Select` with the options `Male` and `Female` and is
  placed in the left form column. `Date of Birth` is a `Date` field. Preserve
  these fieldnames and option values in server, client, import, and test code.
- `Full Name` is read-only in the DocType and its light-green Desk styling is
  implemented in `student.js`. If the display behavior changes, update the
  client script and cover the user-visible result with a focused UI check.
- Client-side required flags improve Desk feedback; server-side validation and
  permissions remain authoritative for API, import, and background-job writes.
- Data backfills and other transformations must be idempotent patches under
  `student_management_system/patches/`, registered in `patches.txt`, and
  verified on a test site. Schema-only DocType changes use normal Frappe
  migration.

## Frappe implementation workflow

- Use bare `bench` from the bench root and pass `--site <site>` to site-scoped
  commands. Do not create a second app or hand-create DocType directories.
- After DocType metadata or patch changes, run
  `bench --site <site> migrate`. After Desk/client changes, clear the relevant
  cache and build assets when the change requires it.
- Use Frappe ORM or Query Builder for application data access. Keep raw SQL
  isolated to a justified framework or migration boundary, with values bound
  through Frappe APIs.
- Keep durable state and validation server-authoritative. Do not rely on a
  client-only check for gender, permissions, or any future business rule.
- When a backend field is surfaced in a Desk or other frontend, update the
  corresponding UI contract and tests in the same change.

## Playwright UI tests — Wiki is the reference

- For committed browser tests, use the newer `frappe/wiki` repository's current
  Playwright conventions rather than Bond Management's Cypress conventions.
  Treat `https://github.com/frappe/wiki/blob/develop/playwright.config.ts` as
  the primary reference and re-check it when the Wiki setup changes.
- Keep tests under `e2e/tests/` and use `@playwright/test`. Mirror the Wiki
  setup-project pattern: `auth.setup.ts` creates `e2e/.auth/user.json`, the
  Chromium project depends on setup, and the suite runs sequentially with one
  worker because Frappe state is shared.
- Configure `BASE_URL` explicitly for the target site. Supply login values via
  `FRAPPE_USER` and `FRAPPE_PASSWORD`; keep credentials and generated auth
  state out of the repository. Use a dedicated test site for state-changing
  E2E flows.
- Follow the Wiki naming split: normal tests use `*.test.ts`; mobile tests use
  `*.mobile.spec.ts` only when a mobile viewport is part of the requirement.
  Prefer role, label, and visible-text locators, and wait on observable UI
  state rather than fixed sleeps or internal implementation details.
- If package scripts are added, preserve the Wiki names `test:e2e`,
  `test:e2e:ui`, `test:e2e:headed`, and `test:e2e:debug`. Start the backend with
  `bench start`, install the required browser outside the repository, and run
  the focused spec before the full suite.
- Use `.agents/skills/playwright` for exploratory browser control and artifact
  capture. For committed test specs, the Wiki `@playwright/test` pattern above
  takes precedence.

## Verification

- Python changes: run the focused Frappe test module, then
  `bench --site <test-site> run-tests --app student_management_system` when
  the change affects shared behavior.
- DocType or migration changes: migrate the test site first, then run the
  affected test module and the app suite. Confirm both fresh-install and
  migrate paths when installation behavior changes.
- JavaScript changes: run the configured ESLint/Prettier checks and
  `node --check` on the changed plain JavaScript files. JSON metadata must pass
  the configured JSON check.
- Playwright changes: run the focused `npx playwright test <spec>` (or the
  matching `yarn test:e2e` script), then the full E2E command when shared setup
  or navigation changes.
- For documentation or agent-guidance-only changes, run `git diff --check` and
  validate the changed file paths and links. Do not claim application tests
  passed unless they were actually executed.

## References

- Shared bench rules: `../../AGENTS.md`
- Frappe workflow skill: `.agents/skills/frappe-app-dev/SKILL.md`
- Code style: `.agents/skills/code-style/SKILL.md`
- Agent-document writing: `.agents/skills/writing-for-agents/SKILL.md`
- Browser automation: `.agents/skills/playwright/SKILL.md`
- Terse communication mode: `.agents/skills/caveman/SKILL.md`
- Local app-pattern reference: `../bond_management/AGENTS.md` (financial
  rules in that file do not apply to this app)
- [Frappe v16.31.0](https://github.com/frappe/frappe/tree/v16.31.0)
- [ERPNext](https://github.com/frappe/erpnext)
- [Frappe Wiki](https://github.com/frappe/wiki)
- [Wiki agent guidance](https://github.com/frappe/wiki/blob/develop/CLAUDE.md)
