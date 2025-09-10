# pystocker

Lightweight open-source stock data fetching and analysis library for Indian stocks (Moneycontrol-focused).

## Files included
- pystocker/ (package)
- setup.py
- requirements.txt

## Quick install (local)
```bash
pip install -r requirements.txt
python setup.py develop
```

## Example
```python
import pystocker as ps
df = ps.getAllData('RELIANCE')
print(ps.getDod('2024-05-25', 'RELIANCE'))
ps.plotStock(df, columns=['Close'])
```
