from pytest import mark, approx  # type: ignore

from dialogue import Dialogue  # type: ignore

from calc import evaluate, repl, display, Stack

TOLERANCE = .0001

@mark.parametrize("source, want", [
    ('2', 2),
    ('2 3 +', 5),
    ('5 3 -', 2),
    ('3 5 * 2 +', 17),
    ('2 3 4 5 * * *', 120),
    ('1.1 1.1 1.1 + +', approx(3.3, TOLERANCE)),
    ('100 32 - 5 * 9 /', approx(37.78, TOLERANCE)),
])
def test_evaluate(source, want) -> None:
    stack: Stack = []
    evaluate(source.split(), stack)
    assert want == stack[-1]


@mark.parametrize("value, want", [
    ([], ' →'),
    ([3.], '3.0 →'),
    ([3., 4., 5.], '3.0 │ 4.0 │ 5.0 →'),
])
def test_display(value, want) -> None:
    assert want == display(value)


@mark.parametrize("session", [
    """
    > 3
    3.0 →
    """,
    """
    > 3 5 6
    3.0 │ 5.0 │ 6.0 →
    > *
    3.0 │ 30.0 →
    > -
    -27.0 →
    """,
])
def test_repl(capsys, session) -> None:
    dlg = Dialogue(session)
    repl(dlg.fake_input)
    captured = capsys.readouterr()
    assert dlg.session.strip() == captured.out.strip()
