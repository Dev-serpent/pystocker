import re
def clean_numeric(s):
    if s is None:
        return None
    s = str(s).replace(',', '').strip()
    s = re.sub(r'[^0-9.-]', '', s)
    try:
        return float(s)
    except:
        return None
