>>> from clip import clip
>>> from inspect import signature
>>> sig = signature(clip)
>>> sig
<Signature (text, max_len=80)>
>>> str(sig)
'(text, max_len=80)'
>>> for name, param in sig.parameters.items():
...     print(param.kind, ':', name, '=', param.default)
...
POSITIONAL_OR_KEYWORD : text = <class 'inspect._empty'>
POSITIONAL_OR_KEYWORD : max_len = 80
