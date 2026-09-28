import re
from datetime import datetime, timedelta

from flask import render_template

from ..models import agreement as model_agreement
from ..models import sample as model_sample
from ..models import client as model_client
from ..models import warehouse as model_warehouse
from .market import get_market_data

_DATE_RE = re.compile(r'\b(\d{1,2}/\d{1,2}/(?:\d{4}|\d{2}))\b')


def _parse_date(raw):
    for fmt in ('%d/%m/%Y', '%d/%m/%y'):
        try:
            return datetime.strptime(raw, fmt).date()
        except ValueError:
            continue
    return None


def index():
    clients = {c['id']: c['nome'] for c in model_client.get_all()}
    warehouses = {w['id']: w['nome'] for w in model_warehouse.get_all()}

    today = datetime.today().date()
    cutoff = today + timedelta(days=15)

    upcoming = []
    for ag in model_agreement.get_all():
        m = _DATE_RE.search(ag.get('cond_venda', '') or '') or _DATE_RE.search(ag.get('modalidade', '') or '')
        if not m:
            continue
        d = _parse_date(m.group(1))
        if d is None:
            continue
        if today <= d <= cutoff:
            upcoming.append({
                'id': ag.get('id'),
                'date': d,
                'comprador': clients.get(ag.get('comprador', ''), '—'),
                'quantidade': ag.get('quantidade', '—'),
                'retirada': warehouses.get(ag.get('retirada', ''), '—'),
            })
    upcoming.sort(key=lambda x: x['date'])
    upcoming = upcoming[:10]

    def _num(s):
        raw = (s.get('num_amostra') or '').split('/')[0]
        try:
            return int(raw)
        except ValueError:
            return 0

    all_samples = model_sample.get_all()
    all_samples.sort(key=_num, reverse=True)
    recent_samples = [
        {
            'numero': s.get('num_amostra', '—'),
            'vendedor': clients.get(s.get('client', ''), '—'),
            'tipo': (s.get('type') or '—').capitalize(),
            'sacas': s.get('quantidade', '—'),
        }
        for s in all_samples[:10]
    ]

    try:
        market = get_market_data()
    except Exception as e:
        print(f"Market data error: {e}")
        market = {'kc': [], 'usd_brl': None, 'usd_brl_change': None, 'usd_brl_change_pct': None, 'updated_at': '—'}

    return render_template('app/index.html', upcoming=upcoming, recent_samples=recent_samples, market=market)
