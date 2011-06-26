registry = dict(version=0)
def bind():
    from cPickle import loads as _loads
    _lookup_attr = _loads('cchameleon.core.codegen\nlookup_attr\np1\n.')
    _init_scope = _loads('cchameleon.core.utils\necontext\np1\n.')
    _re_amp = _loads("cre\n_compile\np1\n(S'&(?!([A-Za-z]+|#[0-9]+);)'\np2\nI0\ntRp3\n.")
    _attrs_4349833552 = _loads('(dp1\nVID\np2\nV${guid}\np3\ns.')
    _init_stream = _loads('cchameleon.core.generation\ninitialize_stream\np1\n.')
    _attrs_4349808336 = _loads('(dp1\n.')
    _init_default = _loads('cchameleon.core.generation\ninitialize_default\np1\n.')
    _attrs_4349808528 = _loads('(dp1\n.')
    _init_tal = _loads('cchameleon.core.generation\ninitialize_tal\np1\n.')
    _attrs_4349833360 = _loads('(dp1\n.')
    def render(econtext, rcontext=None):
        macros = econtext.get('macros')
        _translate = econtext.get('_translate')
        _slots = econtext.get('_slots')
        target_language = econtext.get('target_language')
        u'_init_stream()'
        (_out, _write, ) = _init_stream()
        u'_init_tal()'
        (_attributes, repeat, ) = _init_tal()
        u'_init_default()'
        _default = _init_default()
        u'None'
        default = None
        u'None'
        _domain = None
        _write(u'<?xml version="1.0" encoding="utf-8" standalone="no" ?>\n')
        attrs = _attrs_4349808336
        _write(u'<ARC_RouteListRQ>\n  ')
        attrs = _attrs_4349808528
        _write(u'<POS>\n    ')
        attrs = _attrs_4349833360
        _write(u'<Source>\n      ')
        attrs = _attrs_4349833552
        "join(value('guid'),)"
        _write(u'<RequestorID')
        _tmp1 = econtext['guid']
        if (_tmp1 is _default):
            _tmp1 = u'${guid}'
        if ((_tmp1 is not None) and (_tmp1 is not False)):
            if (_tmp1.__class__ not in (str, unicode, int, float, )):
                _tmp1 = unicode(_translate(_tmp1, domain=_domain, mapping=None, target_language=target_language, default=None))
            else:
                if not isinstance(_tmp1, unicode):
                    _tmp1 = str(_tmp1)
            if ('&' in _tmp1):
                if (';' in _tmp1):
                    _tmp1 = _re_amp.sub('&amp;', _tmp1)
                else:
                    _tmp1 = _tmp1.replace('&', '&amp;')
            if ('<' in _tmp1):
                _tmp1 = _tmp1.replace('<', '&lt;')
            if ('>' in _tmp1):
                _tmp1 = _tmp1.replace('>', '&gt;')
            if ('"' in _tmp1):
                _tmp1 = _tmp1.replace('"', '&quot;')
            _write(((' ID="' + _tmp1) + '"'))
        _write(u' />\n    </Source>\n  </POS>\n</ARC_RouteListRQ>')
        return _out.getvalue()
    return render

__filename__ = '/Users/mitch/Documents/Projects/bmibargins/bmibargains/bmibargains/templates/GetRoutesRequest.pt'
registry[(None, True, '1488bdb950901f8f258549439ef6661a49aae984')] = bind()
