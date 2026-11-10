# 📋 CHANGELOG — Tally XML Cleaner

All notable changes, bug fixes, architectural modifications, and updates to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to Semantic Versioning.

---

## [Unreleased]
### Planned / Future Roadmap
- [ ] Dedicated Web Worker pipeline to prevent browser UI freezing on 100MB+ files.
- [ ] Desktop `.exe` packaging using Tauri or Python PySide/Tkinter.
- [ ] Voucher filter option (e.g., Export/Import only Sales, Purchase, Receipt, or Payment).
- [ ] Date-range filter within XML.

---

## [1.2.0] - 2026-10-13
### 🐛 Critical Bug Fix: Stock Item "Primary Batch" Quantity Error
#### Problem:
Tally Prime failed with fatal import error:
```
Line 1004: No QUANTITY given for 'Primary Batch' of 'Cane Jaggery 30kg'!
Line 4462: No QUANTITY given for 'Primary Batch' of 'J Goldd 50kg'!
```
#### Root Cause:
Stock items in Tally XML store opening balances inside both top-level `<OPENINGBALANCE>` and nested `<BATCHALLOCATIONS.LIST>`. When previous versions stripped `<OPENINGBALANCE>` alone, the `<BATCHALLOCATIONS.LIST>` remained with `BATCHNAME='Primary Batch'`, `OPENINGVALUE`, and `OPENINGRATE`, but **no quantity**, leading Tally to abort the import.
#### Solution:
- Completely cleaned `<OPENINGVALUE>` and `<OPENINGRATE>`.
- Replaced populated batch lists inside `<STOCKITEM>` with an empty `<BATCHALLOCATIONS.LIST>      </BATCHALLOCATIONS.LIST>` block.
- Updated both `index.html` (JS) and `gemini-code-1791868496368.py` (Python).

---

## [1.1.0] - 2026-10-13
### 🚀 Added: Company Name Lock Stripping
- Added stripping of `<SVCURRENTCOMPANY>...</SVCURRENTCOMPANY>`.
- Allows XML files exported from a specifically named company (e.g. `FATHIMA TRADERS - May`) to be seamlessly imported into any destination company without name conflict errors.

---

## [1.0.0] - 2026-10-12
### 🎉 Initial Release
- **100% Client-Side Web Tool (`index.html`)**: Single-page modern responsive dark-mode UI with drag-and-drop.
- **UTF-16LE & UTF-8 Encoding Auto-Detection**: Uses `TextDecoder` and `encodeUtf16LE` with BOM (`0xFF 0xFE`) preservation.
- **Duplicate Identifier Stripping**:
  - Cleans `<GUID>`, `<MASTERID>`, `<ALTERID>`, `<VOUCHERKEY>`, `<VOUCHERRETAINKEY>`.
  - Cleans `<VOUCHER>` header attributes: `REMOTEID` and `VCHKEY`.
- **Opening Balance Toggle**: Optional stripping of party ledger `<OPENINGBALANCE>`.
- **Python CLI Companion**: `gemini-code-1791868496368.py` for automated local directory cleaning.
