# brother-label

Python package for the raster language protocol of the Brother QL series label printers

Fork of https://github.com/pklaus/brother_ql and https://github.com/matmair/brother_ql-inventree with many
improvements and features planned, including:

- Better support for device-specific label specifications (e.g. QL vs PTouch)
- Support for new devices (PT-E550W)
- Removed redudant legacy/compatibility code
- ...

## Devices

| Device           | Status                      |
| ---------------- | --------------------------- |
| QL-500           | Supported                   |
| QL-550           | Supported                   |
| QL-560           | Supported                   |
| QL-570           | Supported                   |
| QL-580N          | Supported                   |
| QL-600           | Supported                   |
| QL-650TD         | Supported                   |
| QL-700           | Supported                   |
| QL-710W          | Supported                   |
| QL-720NW         | Supported                   |
| QL-800           | Supported                   |
| QL-810W          | Supported                   |
| QL-820NWB        | Supported                   |
| QL-1050          | Supported                   |
| QL-1060N         | Supported                   |
| QL-1100          | Supported                   |
| QL-1100NWB       | Supported                   |
| QL-1115NWB       | Supported                   |
| PT-P750W         | Supported                   |
| PT-P900W         | Supported                   |
| PT-P950NW        | Supported                   |
| PT-E550W         | :heavy_check_mark: Verified |

 - **Supported:** Device is supported, but no verification has been received.
 - **Verified:** Device is supported, and verified by a user.

## Backends

| Backend       | Type | Linux              | Mac OS             | Windows            |
| ------------- | ---- | ------------------ | ------------------ | ------------------ |
| network       | TCP  | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |
| linux\_kernel | USB  | :heavy_check_mark: | :x:                | :x:                |
| py_usb        | USB  | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |
