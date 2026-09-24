import os
import sys
import urllib.request
import json

class MobileLangV3:
    def __init__(self):
        self.variables = {}

    def execute(self, code_text):
        lines = code_text.strip().split("\n")
        i = 0
        while i < len(lines):
            line = lines[i].strip()

            if not line or line.startswith("#"):
                i += 1
                continue

            if line.startswith("set "):
                parts = line[4:].split("=", 1)
                if len(parts) == 2:
                    var_name = parts[0].strip()
                    val_expr = parts[1].strip()
                    self.variables[var_name] = self.evaluate(val_expr)

            elif line.startswith("print "):
                val_to_print = line[6:].strip()
                print(">>", self.evaluate(val_to_print))

            elif line.startswith("if "):
                condition_expr = line[3:].strip()
                condition_result = self.eval_condition(condition_expr)

                if_body = []
                i += 1
                while i < len(lines) and (lines[i].startswith("    ") or lines[i].startswith("\t")):
                    if_body.append(lines[i].strip())
                    i += 1

                if condition_result:
                    sub = MobileLangV3()
                    sub.variables = self.variables.copy()
                    sub.execute("\n".join(if_body))
                continue

            elif " times" in line and line.startswith("loop "):
                count_str = line.replace("loop", "").replace("times", "").strip()
                count = int(self.evaluate(count_str))

                loop_body = []
                i += 1
                while i < len(lines) and (lines[i].startswith("    ") or lines[i].startswith("\t")):
                    loop_body.append(lines[i].strip())
                    i += 1

                for _ in range(count):
                    sub = MobileLangV3()
                    sub.variables = self.variables.copy()
                    sub.execute("\n".join(loop_body))
                continue

            elif line.startswith("notify "):
                msg = self.evaluate(line[7:].strip())
                print(f"📱 [NOTIFICATION]: {msg}")

            elif line.startswith("vibrate "):
                ms = self.evaluate(line[8:].strip())
                print(f"📳 [VIBRATION]: {ms}ms")

            elif line.startswith("flash "):
                mode = line[6:].strip()
                print(f"🔦 [FLASHLIGHT]: {mode}")

            elif line.startswith("get "):
                parts = line[4:].strip().split(" as ")
                url = self.evaluate(parts[0].strip())
                var_to_save = parts[1].strip() if len(parts) > 1 else None

                print(f"🌐 [FETCHING API]: {url}")
                try:
                    req = urllib.request.urlopen(url)
                    data = req.read().decode('utf-8')
                    try:
                        res_json = json.loads(data)
                        if var_to_save:
                            self.variables[var_to_save] = res_json
                    except:
                        if var_to_save:
                            self.variables[var_to_save] = data
                except Exception as e:
                    print(f"❌ Error fetching URL: {e}")

            i += 1

    def evaluate(self, expr):
        expr = expr.strip()
        if (expr.startswith('"') and expr.endswith('"')) or (expr.startswith("'") and expr.endswith("'")):
            return expr[1:-1]
        for var_name, var_val in self.variables.items():
            expr = expr.replace(var_name, str(var_val))
        try:
            return eval(expr)
        except:
            return expr

    def eval_condition(self, expr):
        for var_name, var_val in self.variables.items():
            expr = expr.replace(var_name, str(var_val))
        try:
            return bool(eval(expr))
        except:
            return False

if __name__ == "__main__":
    engine = MobileLangV3()
    if len(sys.argv) > 1:
        filepath = sys.argv[1]
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                code = f.read()
            print(f"🚀 Running Mobile Script: {filepath}...\n")
            engine.execute(code)
        else:
            print(f"❌ Error: File '{filepath}' မတွေ့ရှိပါ")
    else:
        print("💡 အသုံးပုံ: python main.py <script_name.mbl>")
