# Parameter Pollution / Unexpected Input Handling — Survey `select1` Abuse

## Vulnerability:
The survey endpoint accepts multiple values for the `select1` form parameter and fails to properly validate or normalize them. By supplying an unexpected extra value (or multiple values) for `select1`, the application returned the challenge flag. This is a server-side input-handling flaw (parameter pollution / unexpected input handling) that leads to sensitive data disclosure.

## Weakness:
- Server trusts and directly processes multiple values for the same parameter without normalization.
- No allowlist or strict validation of acceptable `select1` values.
- Business logic assumes a single value but does not enforce it, enabling edge cases.
- Inadequate output filtering or access control for responses triggered by unusual input combinations.
- Missing tests for multipart/form-data / repeated parameters and unusual input shapes.

## Exploitation:
1. Submitted the survey form normally to observe baseline behavior.
2. Intercepted the request (proxy / repeater) and modified the `select1` parameter to include an extra value (e.g., `select1=value1&select1=EXTRA` or `select1[]=value1&select1[]=EXTRA` depending on how the app parses repeated params).
3. Replayed the request. The server processed the unexpected additional `select1` value and responded with the flag.
4. The behavior indicates the server either:
   - concatenates values and uses the combined value to select a special code path, or
   - treats the extra value as a trigger for an alternative branch that exposes sensitive data.
5. Evidence: the response body contained the flag when the extra `select1` value was present. (Store sanitized request/response evidence in `Resources/`.)

## How to Fix:
- **Normalize input**: server-side, reject repeated occurrences of parameters that must be single-valued. Choose clear semantics (first value, last value, or reject) and enforce it.
- **Strict validation / allowlist**: accept only expected values for `select1`. Validate against a server-side allowlist and reject unknown values with `400` or `422`.
- **Sanitize and canonicalize** all inputs before using them in logic decisions.
- **Harden business logic** to require explicit authorization checks for any code path that can reveal sensitive data; do not allow data exposure based purely on input shape.
- **Add unit/integration tests** for uncommon input shapes (repeated params, arrays, very long inputs, unexpected encodings).
- **Log and monitor** unusual parameter shapes and repeated-parameter attempts, and alert on anomalous patterns.
- **Fail closed**: prefer rejecting unexpected inputs rather than attempting to process them in a permissive way.
