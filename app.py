import os
from random import sample

from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path, verbose=True)


# ボットトークンとソケットモードハンドラーを使ってアプリを初期化します
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))


def calc_sample_size(effect_size: float = 0.1) -> int:
    import statsmodels.stats.power as smp

    sample_size = smp.NormalIndPower().solve_power(
        effect_size=effect_size, alpha=0.05, power=0.8, alternative="larger"
    )
    return int(sample_size)


@app.event("app_mention")
def ask_for_introduction(event, say):
    effect_size = float(event["text"].split(" ")[1])
    sample_size = str(calc_sample_size(effect_size=effect_size))

    if effect_size <= 0 or effect_size >= 1.0:
        say(text="評価指標の差は 0 ~ 1 の間にしてね", channel=event["channel"])
    else:
        user_id = event["user"]
        text = f"<@{user_id}>!"
        text += f"ABテスト時の評価指標の差が {effect_size} と仮定すると、"
        text += f"\n必要なサンプルサイズは {sample_size} と推定されます"
        say(text=text, channel=event["channel"])


# アプリを起動します
if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
