from django import template
from django.utils.safestring import SafeUnicode
from django.conf import settings

register=template.Library()

@register.filter()
def currency(value):
    symbol = getattr(settings, 'CURRENCY_SYMBOL', '$')
    thousand_sep = getattr(settings, 'THOUSAND_SEPARATOR', ',')
    decimal_sep = getattr(settings, 'DECIMAL_SEPARATOR', '.')

    intstr = str(int(value))
    f = lambda x, n, acc=[]: f(x[:-n], n, [(x[-n:])]+acc) if x else acc
    intpart = thousand_sep.join(f(intstr, 3))
    return "%s%s%s%s" % (symbol, intpart, decimal_sep, ("%0.2f" % value)[-2:])

currency.is_safe = True