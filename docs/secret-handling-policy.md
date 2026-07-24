# Mundilfari Secret Handling Policy

Future NTS cookies, exporter keys, TLS credentials, signing keys,
timestamp-authority keys, and privileged-helper credentials are
secret-bearing. GNSS authentication keys and trust stores belong to Navheim;
the companion receives only bounded authentication state and provenance.

Rules:

- no `Copy`;
- no revealing `Debug`;
- no ordinary `Clone` without review;
- controlled exposure with the narrowest lifetime;
- no secret bytes in errors, logs, panic text, metrics, packet dumps, or test
  output;
- no automatic serialization;
- constant-time comparison where secret-dependent;
- explicit clearing through an admitted implementation where meaningful;
- bounded retention and rotation;
- no fallback entropy from time, PID, address, or deterministic test RNG;
- hard failure when required cryptographic entropy is unavailable.

Memory clearing cannot guarantee removal of historical copies, compiler
spills, registers, swap, core dumps, or privileged reads. Documentation must
state residual guarantees precisely.
