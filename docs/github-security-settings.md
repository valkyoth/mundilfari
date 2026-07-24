# GitHub Security Settings

GitHub CodeQL default setup is required for the public repository.

This project intentionally does not add an advanced CodeQL workflow because
default and advanced setups must not upload duplicate analysis for the same
repository configuration.

Before a release tag:

1. Open repository settings.
2. Go to Code security.
3. Confirm CodeQL analysis default setup is active for the default branch.
4. Confirm the latest analysis completed successfully for the release commit.
5. Confirm secret scanning and private vulnerability reporting are enabled
   where the repository plan supports them.
6. Record the review in the permanent pentest report.
