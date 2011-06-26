registry = dict(version=0)
def bind():
    from cPickle import loads as _loads
    _attrs_4362662736 = _loads('(dp1\n.')
    _lookup_attr = _loads('cchameleon.core.codegen\nlookup_attr\np1\n.')
    _init_scope = _loads('cchameleon.core.utils\necontext\np1\n.')
    _attrs_4362662288 = _loads('(dp1\n.')
    _attrs_4343414864 = _loads('(dp1\n.')
    _attrs_4362662480 = _loads('(dp1\n.')
    _attrs_4378660752 = _loads('(dp1\n.')
    _attrs_4378657360 = _loads('(dp1\n.')
    _attrs_4343415056 = _loads('(dp1\n.')
    _init_stream = _loads('cchameleon.core.generation\ninitialize_stream\np1\n.')
    _attrs_4378659024 = _loads('(dp1\n.')
    _attrs_4362662352 = _loads('(dp1\nVhref\np2\nVstatic/default.css\np3\nsVrel\np4\nVstylesheet\np5\nsVtype\np6\nVtext/css\np7\ns.')
    _init_default = _loads('cchameleon.core.generation\ninitialize_default\np1\n.')
    _attrs_4362662096 = _loads('(dp1\nVid\np2\nVmain\np3\ns.')
    _init_tal = _loads('cchameleon.core.generation\ninitialize_tal\np1\n.')
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
        attrs = _attrs_4343415056
        _write(u'<html>\n  ')
        attrs = _attrs_4343414864
        u'success'
        _write(u'<head>\n    ')
        _tmp1 = econtext['success']
        if _tmp1:
            pass
            attrs = _attrs_4362662736
            _write(u'<title>Your search has been confirmed</title>')
        u'not success'
        _write(u'\n    ')
        _tmp1 = not econtext['success']
        if _tmp1:
            pass
            attrs = _attrs_4362662480
            _write(u'<title>Could not confirm your search</title>')
        _write(u'\n    ')
        attrs = _attrs_4362662352
        _write(u'<link rel="stylesheet" type="text/css" href="static/default.css" />\n  </head>\n  ')
        attrs = _attrs_4362662288
        _write(u'<body>\n    ')
        attrs = _attrs_4362662096
        _write(u'<div id="main">\n    ')
        attrs = _attrs_4378657360
        u'success'
        _write(u'<h1>bmi bargains</h1>\n    ')
        _tmp1 = econtext['success']
        if _tmp1:
            pass
            attrs = _attrs_4378659024
            _write(u'<p>Your search has been confirmed</p>')
        u'not success'
        _write(u'\n    ')
        _tmp1 = not econtext['success']
        if _tmp1:
            pass
            attrs = _attrs_4378660752
            _write(u'<p>Could not confirm your search</p>')
        _write(u'\n    </div>\n  </body>\n</html>')
        return _out.getvalue()
    return render

__filename__ = u'/Users/mitch/Documents/Projects/bmibargins/bmibargains/bmibargains/templates/confirm_search.pt'
registry[(None, True, '1488bdb950901f8f258549439ef6661a49aae984')] = bind()
