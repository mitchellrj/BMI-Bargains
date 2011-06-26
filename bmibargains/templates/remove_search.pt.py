registry = dict(version=0)
def bind():
    from cPickle import loads as _loads
    _attrs_4354601488 = _loads('(dp1\n.')
    _lookup_attr = _loads('cchameleon.core.codegen\nlookup_attr\np1\n.')
    _init_scope = _loads('cchameleon.core.utils\necontext\np1\n.')
    _attrs_4354604944 = _loads('(dp1\n.')
    _attrs_4354601680 = _loads('(dp1\n.')
    _init_stream = _loads('cchameleon.core.generation\ninitialize_stream\np1\n.')
    _attrs_4354604560 = _loads('(dp1\n.')
    _attrs_4354604816 = _loads('(dp1\n.')
    _init_default = _loads('cchameleon.core.generation\ninitialize_default\np1\n.')
    _attrs_4354601744 = _loads('(dp1\n.')
    _init_tal = _loads('cchameleon.core.generation\ninitialize_tal\np1\n.')
    _attrs_4354604304 = _loads('(dp1\n.')
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
        attrs = _attrs_4354604304
        _write(u'<html>\n  ')
        attrs = _attrs_4354604560
        u'success'
        _write(u'<head>\n    ')
        _tmp1 = econtext['success']
        if _tmp1:
            pass
            attrs = _attrs_4354604944
            _write(u'<title>Successfully removed search</title>')
        u'not success'
        _write(u'\n    ')
        _tmp1 = not econtext['success']
        if _tmp1:
            pass
            attrs = _attrs_4354601488
            _write(u'<title>Failed to remove search</title>')
        _write(u'\n  </head>\n  ')
        attrs = _attrs_4354604816
        u'success'
        _write(u'<body>\n    ')
        _tmp1 = econtext['success']
        if _tmp1:
            pass
            attrs = _attrs_4354601680
            _write(u'<p>Successfully removed search</p>')
        u'not success'
        _write(u'\n    ')
        _tmp1 = not econtext['success']
        if _tmp1:
            pass
            attrs = _attrs_4354601744
            _write(u'<p>Failed to remove search</p>')
        _write(u'\n  </body>\n</html>')
        return _out.getvalue()
    return render

__filename__ = u'/Users/mitch/Documents/Projects/bmibargins/bmibargains/bmibargains/templates/remove_search.pt'
registry[(None, True, '1488bdb950901f8f258549439ef6661a49aae984')] = bind()
