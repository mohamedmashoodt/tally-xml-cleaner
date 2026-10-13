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
        content = re.sub(r' REMOTEID="[^"]*"', '', content)
        content = re.sub(r' VCHKEY="[^"]*"', '', content)

        # 2. Vouchers-inte ullile GUID, MASTERID, ALTERID, VOUCHERKEY enniva ozhivakkunnu
        def clean_voucher_block(match):
            vch = match.group(0)
            vch = re.sub(r'<GUID>.*?</GUID>\s*', '', vch)
            vch = re.sub(r'<MASTERID>.*?</MASTERID>\s*', '', vch)
            vch = re.sub(r'<ALTERID>.*?</ALTERID>\s*', '', vch)
            vch = re.sub(r'<VOUCHERKEY>.*?</VOUCHERKEY>\s*', '', vch)
            vch = re.sub(r'<VOUCHERRETAINKEY>.*?</VOUCHERRETAINKEY>\s*', '', vch)
            return vch

        content = re.sub(r'<VOUCHER\b.*?</VOUCHER>', clean_voucher_block, content, flags=re.DOTALL)

        # 3. OPENINGBALANCE tag-ukal ozhivakkunnu
        content = re.sub(r'<OPENINGBALANCE>.*?</OPENINGBALANCE>\s*', '', content)

        # 4. Puthiya file aayi save cheyyunnu
        new_file_path = os.path.join(folder_path, "Cleaned_" + filename)
        with open(new_file_path, "w", encoding=enc) as f:
            f.write(content)
            
        print(f"Success: Cleaned_{filename} ready!")