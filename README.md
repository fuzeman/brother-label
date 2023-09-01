# brother-label

Brother label printer interface for QL and PT series printers.

**API is currently being re-worked and should not be considered stable.**

Fork of https://github.com/pklaus/brother_ql and https://github.com/matmair/brother_ql-inventree with many
improvements and features planned, including:

- Better support for device-specific label specifications (e.g. QL vs PT)
- Support for new devices (PT-E550W)
- Removed redudant legacy/compatibility code
- ...

## Devices

| Device           | Status       |
| ---------------- | ------------ |
| QL-500           | Supported    |
| QL-550           | Supported    |
| QL-560           | Supported    |
| QL-570           | Supported    |
| QL-580N          | Supported    |
| QL-600           | Supported    |
| QL-650TD         | Supported    |
| QL-700           | Supported    |
| QL-710W          | Supported    |
| QL-720NW         | Supported    |
| QL-800           | Supported    |
| QL-810W          | Supported    |
| QL-820NWB        | Supported    |
| QL-1050          | Supported    |
| QL-1060N         | Supported    |
| QL-1100          | Supported    |
| QL-1100NWB       | Supported    |
| QL-1115NWB       | Supported    |
| PT-P750W         | Supported    |
| PT-P900W         | Supported    |
| PT-P950NW        | Supported    |
| PT-E550W         | ✔️ Verified |

 - **Supported:** Device is supported, but no verification has been received.
 - **Verified:** Device is supported, and verified by a user.

## Labels

### Continuous / Endless

| Type             | QL     | QL-10  | QL-11  | PT    | PT-E  |
| ---------------- | ------ | ------ | ------ | ----- | ------ |
| 6                | ❌    | ❌    | ❌    | ❌    | ✔️    |
| 9                | ❌    | ❌    | ❌    | ❌    | ✔️    |
| 12               | ✔️    | ✔️    | ✔️    | ✔️    | ✔️    |
| 18               | ✔️    | ✔️    | ✔️    | ✔️    | ✔️    |
| 24               | ❌    | ❌    | ❌    | ✔️    | ✔️    |
| 29               | ✔️    | ✔️    | ✔️    | ❌    | ❌    |
| 36               | ❌    | ❌    | ❌    | ✔️    | ✔️    |
| 38               | ✔️    | ✔️    | ✔️    | ❌    | ❌    |
| 50               | ✔️    | ✔️    | ✔️    | ❌    | ❌    |
| 54               | ✔️    | ✔️    | ✔️    | ❌    | ❌    |
| 62               | ✔️    | ✔️    | ✔️    | ❌    | ❌    |
| 62red            | ✔️    | ✔️    | ✔️    | ❌    | ❌    |
| 102              | ❌    | ✔️    | ❌    | ❌    | ❌    |
| 103              | ❌    | ❌    | ✔️    | ❌    | ❌    |
| 104              | ❌    | ✔️    | ❌    | ❌    | ❌    |

### Die-Cut

| Type             | QL     | QL-10  | QL-11 |
| ---------------- | ------ | ------ | ----- |
| 17x54            | ✔️    | ✔️    | ✔️    |
| 17x87            | ✔️    | ✔️    | ✔️    |
| 23x23            | ✔️    | ✔️    | ✔️    |
| 29x42            | ✔️    | ✔️    | ✔️    |
| 29x90            | ✔️    | ✔️    | ✔️    |
| 39x90            | ✔️    | ✔️    | ✔️    |
| 39x48            | ✔️    | ✔️    | ✔️    |
| 52x29            | ✔️    | ✔️    | ✔️    |
| 54x29            | ✔️    | ✔️    | ✔️    |
| 60x86            | ✔️    | ✔️    | ✔️    |
| 62x29            | ✔️    | ✔️    | ✔️    |
| 62x100           | ✔️    | ✔️    | ✔️    |
| 102x51           | ❌    | ✔️    | ❌    |
| 102x152          | ❌    | ✔️    | ❌    |
| 103x164          | ❌    | ❌    | ✔️    |

### Round Die-Cut

| Type             | QL     | QL-10  | QL-11  |
| ---------------- | ------ | ------ | ------ |
| d12              | ✔️    | ✔️    | ✔️    |
| d24              | ✔️    | ✔️    | ✔️    |
| d58              | ✔️    | ✔️    | ✔️    |

## Backends

| Backend       | Type | Linux | Mac OS | Windows |
| ------------- | ---- | ----- | ------ | ------- |
| network       | TCP  | ✔️   | ✔️     | ✔️     |
| linux\_kernel | USB  | ✔️   | ❌     | ❌     |
| py_usb        | USB  | ✔️   | ✔️     | ✔️     |
