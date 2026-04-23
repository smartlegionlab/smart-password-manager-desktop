# Migration Guide: v2.x.x to v3.x.x+

## ⚠️ Breaking Change Notice

**smartpasslib v3.x.x+ is NOT backward compatible with v2.x.x**

Passwords generated with v2.x.x cannot be regenerated using v3.x.x+ due to fundamental changes in the deterministic generation algorithm.

---

## Why the change?

**smartpasslib v3.x.x+ introduces fundamental improvements:**
- **Stronger cryptographic algorithm** — enhanced deterministic generation with better entropy distribution
- **Improved performance** — faster password generation, especially for longer passwords
- **Better cross-platform consistency** — identical results guaranteed across all platforms
- **Extended character set support** — wider range of special characters for stronger passwords
- **Future-proof architecture** — easier updates and security patches

---

## What changed:

- The core password generation algorithm has been completely redesigned
- Passwords created with v2.x.x or earlier **cannot be regenerated** using v3.x.x+
- Old metadata (`passwords.json`) will produce **different passwords** if used with v3.x.x+

---

## What this means for you:

- All passwords created with **v2.x.x or earlier** must be **regenerated** after upgrading
- Old metadata (`passwords.json`) remains readable but will produce **different passwords** if used with v3.x.x+
- You have two options:
  1. **Before upgrading** — manually retrieve and save all passwords from old version
  2. **After upgrading** — re-enter your secret phrases and recreate each entry with correct passwords

---

## Migration Steps

### Before upgrading — follow these steps carefully

#### Step 1: Document your existing passwords

Open your current Smart Password Manager (v2.x.x or earlier)
- For each service, click **Get** and copy the generated password
- Save passwords in a secure temporary location (e.g., encrypted note)

**Alternative method (more secure but manual):**
- Write down for each service: **Service description + Secret phrase + Length**
- After upgrading, you'll manually recreate entries and update passwords in services

#### Step 2: Export old metadata (optional backup)

- Go to **File → Export → Export passwords...**
- Save the JSON file as `passwords_v2_backup.json`

#### Step 3: Upgrade smartpasslib to v3.x.x+

```bash
pip install --upgrade smartpasslib
```

#### Step 4: Migrate your data

- **Option A (recommended)**: Start fresh — delete old `passwords.json` and add entries manually
- **Option B**: Keep metadata but manually verify each password (not recommended — easy to make mistakes)

#### Step 5: Update passwords in all your services

- After regenerating passwords with v3.x.x+, update them in each website/service
- Test login before removing old access

---

## Important Notes

- **No automatic migration** — you must manually regenerate every password
- v2.x.x and v3.x.x+ cannot share the same metadata file
- Keep them completely separate or manually migrate each password
- Always test with non-essential accounts first

---

## Need Help?

- **Issues**: [GitHub Issues](https://github.com/smartlegionlab/smart-password-manager-desktop/issues)
- **Core Library Issues**: [smartpasslib Issues](https://github.com/smartlegionlab/smartpasslib/issues)

