import flet as ft
from fractions import Fraction
import math


def eval_expr(expr: str) -> str:
    # 「^」をべき乗の「**」に置換
    expr = expr.replace("^", "**")
    # 数式に pi, e, 三角関数, sqrt などの特殊記号が含まれている場合は math モジュールを利用して評価
    if any(token in expr for token in ['pi', 'e', 'sin', 'cos', 'tan', 'log', 'sqrt']):
        safe_dict = {
            "pi": math.pi,
            "e": math.e,
            "sin": math.sin,
            "cos": math.cos,
            "tan": math.tan,
            "sqrt": math.sqrt,
            "log": math.log,
            "log10": math.log10
        }
        try:
            result = eval(expr, {"__builtins__": {}}, safe_dict)
            return str(round(result, 12))
        except Exception:
            return "Error"
    else:
        try:
            result = eval(expr, {"__builtins__": {}}, {})
            frac = Fraction(str(result))
            if frac.denominator == 1:
                return str(frac.numerator)
            else:
                return f"{frac.numerator}/{frac.denominator}"
        except Exception:
            return "Error"


def main(page: ft.Page):
    page.title = "Enhanced Calculator"

    # 上部に計算式と結果を表示するためのテキストウィジェットを作成
    expression_display = ft.Text(value="", size=24, color="grey", text_align=ft.TextAlign.RIGHT)
    result_display = ft.Text(value="0", size=40, text_align=ft.TextAlign.RIGHT)

    # 入力中の式を保持する変数
    expr = ""

    # 式と結果を更新する関数
    def update_display():
        expression_display.value = expr
        result_display.value = expr if expr else "0"
        page.update()

    # ボタン押下時のイベントハンドラ
    def button_click(e):
        nonlocal expr
        text = e.control.data

        if text == "AC":
            expr = ""
        elif text == "DEL":
            expr = expr[:-1]
        elif text == "=":
            try:
                result_display.value = eval_expr(expr)
                expression_display.value = expr + " ="
                expr = result_display.value  # 結果を次の計算式として使用
            except Exception:
                result_display.value = "Error"
        else:
            expr += text

        update_display()

    # キーボード入力イベントハンドラ
    def on_keyboard_event(e: ft.KeyboardEvent):
        nonlocal expr

        key_map = {
            "Enter": "=",
            "Backspace": "DEL",
            "Escape": "AC",
        }

        if e.key == "(" or e.key == ")":
            key_input = e.key
        elif e.shift and e.key == "8":
            key_input = "("
        elif e.shift and e.key == "9":
            key_input = ")"
        else:
            key_input = key_map.get(e.key, e.key)  # 特殊キー以外はそのまま使用

        if key_input in ["AC", "DEL", "="] or key_input.isdigit() or key_input in "+-*/().^":
            if key_input == "=":
                try:
                    result_display.value = eval_expr(expr)
                    expression_display.value = expr + " ="
                    expr = result_display.value  # 結果を次の計算式として使用
                except Exception:
                    result_display.value = "Error"
            elif key_input == "DEL":
                expr = expr[:-1]
            elif key_input == "AC":
                expr = ""
            else:
                expr += key_input

            update_display()

    # ボタンレイアウト（行ごとにリストで定義）
    button_rows = [
        ["AC", "DEL", "(", ")"],
        ["7", "8", "9", "/"],
        ["4", "5", "6", "*"],
        ["1", "2", "3", "-"],
        ["0", ".", "^", "+"]
    ]

    # 各行のボタンウィジェットを作成
    button_controls = []
    for row in button_rows:
        cols = []
        for b in row:
            btn = ft.ElevatedButton(text=b, data=b, on_click=button_click, expand=True)
            cols.append(btn)
        button_controls.append(ft.Row(controls=cols, spacing=10))

    # 「=」ボタンは1行分として中央に配置
    equals_button = ft.ElevatedButton(text="=", data="=", on_click=button_click, expand=True)
    equals_row = ft.Row(controls=[equals_button], spacing=10)

    # 上部の表示部分とボタン群をレイアウト
    page.add(
        ft.Column(
            [
                ft.Container(content=expression_display, alignment=ft.alignment.top_right),
                ft.Container(content=result_display, alignment=ft.alignment.top_right),
                ft.Divider(height=1),
                *button_controls,
                equals_row
            ],
            spacing=10,
            expand=True
        )
    )

    # ページ全体でキーボードイベントを監視するよう設定
    page.on_keyboard_event = on_keyboard_event


ft.app(target=main)
