import os
import re

folder_path = "."  # Current folder

for filename in os.listdir(folder_path):
    if filename.endswith(".xml") and not filename.startswith("Cleaned_"):
        file_path = os.path.join(folder_path, filename)
        
        # Tally XML encoding read cheyyunnu
        try:
            with open(file_path, "r", encoding="utf-16") as f:
                content = f.read()
            enc = "utf-16"
        except UnicodeError:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            enc = "utf-8"

        # 1. Voucher Header-ile REMOTEID, VCHKEY enniva ozhivakkunnu
        content = re.sub(r'\s+REMOTEID=(?:"[^"]*"|\'[^\']*\')', '', content, flags=re.IGNORECASE)
        content = re.sub(r'\s+VCHKEY=(?:"[^"]*"|\'[^\']*\')', '', content, flags=re.IGNORECASE)

        # 2. Vouchers-inte ullile GUID, MASTERID, ALTERID, VOUCHERKEY, VOUCHERRETAINKEY enniva ozhivakkunnu
        def clean_voucher_block(match):
            vch = match.group(0)
            vch = re.sub(r'<GUID\b[^>]*>.*?</GUID>\s*', '', vch, flags=re.DOTALL | re.IGNORECASE)
            vch = re.sub(r'<GUID\b[^>]*/>\s*', '', vch, flags=re.IGNORECASE)
            vch = re.sub(r'<MASTERID\b[^>]*>.*?</MASTERID>\s*', '', vch, flags=re.DOTALL | re.IGNORECASE)
            vch = re.sub(r'<MASTERID\b[^>]*/>\s*', '', vch, flags=re.IGNORECASE)
            vch = re.sub(r'<ALTERID\b[^>]*>.*?</ALTERID>\s*', '', vch, flags=re.DOTALL | re.IGNORECASE)
            vch = re.sub(r'<ALTERID\b[^>]*/>\s*', '', vch, flags=re.IGNORECASE)
            vch = re.sub(r'<VOUCHERKEY\b[^>]*>.*?</VOUCHERKEY>\s*', '', vch, flags=re.DOTALL | re.IGNORECASE)
            vch = re.sub(r'<VOUCHERKEY\b[^>]*/>\s*', '', vch, flags=re.IGNORECASE)
            vch = re.sub(r'<VOUCHERRETAINKEY\b[^>]*>.*?</VOUCHERRETAINKEY>\s*', '', vch, flags=re.DOTALL | re.IGNORECASE)
            vch = re.sub(r'<VOUCHERRETAINKEY\b[^>]*/>\s*', '', vch, flags=re.IGNORECASE)
            return vch

        content = re.sub(r'<VOUCHER\b.*?</VOUCHER>', clean_voucher_block, content, flags=re.DOTALL | re.IGNORECASE)

        # 3. OPENINGBALANCE tag-ukal ozhivakkunnu
        content = re.sub(r'<OPENINGBALANCE\b[^>]*>.*?</OPENINGBALANCE>\s*', '', content, flags=re.DOTALL | re.IGNORECASE)
        content = re.sub(r'<OPENINGBALANCE\b[^>]*/>\s*', '', content, flags=re.IGNORECASE)

        # 4. Puthiya file aayi save cheyyunnu
        new_file_path = os.path.join(folder_path, "Cleaned_" + filename)
        with open(new_file_path, "w", encoding=enc) as f:
            f.write(content)
            
        print(f"Success: Cleaned_{filename} ready!")