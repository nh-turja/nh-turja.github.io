# Validation — September 25, 2026

- Built eight primary pages using Python 3.11 and the standard library.
- Checked all 12 generated HTML pages (including four legacy redirects):
  138 local file and fragment references resolved successfully.
- Tested all eight primary pages in Chrome at 1440 px, 390 px, and 320 px widths:
  no horizontal overflow and no WCAG 2 A/AA or WCAG 2.1 AA violations reported
  by axe-core across the 24 combinations. Automated testing does not establish
  full accessibility conformance.
- Exercised all five primary navigation links and current-page indicators,
  keyboard skip-to-content behavior, and citation disclosure.
- Checked that the homepage remains readable with JavaScript disabled.
- Reviewed desktop/mobile screenshots and the first page of the generated CV.
- Generated a tagged, three-page A4 CV PDF with the current affiliation,
  location, upcoming appointment, publications, and selected projects.
- Homepage HTML, CSS, portrait, and favicon total 40,078 bytes before transfer
  compression; no JavaScript or remote font requests are needed.
- Thirteen public links returned HTTP 200. LinkedIn returned 999 and requires
  manual verification; see `link-audit.json` and `content-review.md`.
- `git diff --check` passed.

The preview is local; no production deployment was performed.

Follow-up: hardware security emphasis, the prominent University of Delaware
affiliation, and the confirmed August 2026 PhD start date were rebuilt and
rechecked; browser previews and the CV PDF were refreshed.
