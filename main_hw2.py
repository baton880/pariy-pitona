import pandas as pd
from flask import Flask, request

#py main_hw2.py
#http://127.0.0.1:1337/names
#http://127.0.0.1:1337/hw-01/mean_score
#http://127.0.0.1:1337/mean_score?hw_name=hw-01&group_id=25137
#http://127.0.0.1:1337/mark?student_id=1
#http://127.0.0.1:1337/course_table?hw_name=hw-01&group_id=25137


app = Flask(__name__)
app.json.ensure_ascii = False
app.url_map.strict_slashes = False

FILES = {
    "hw-01": "data/hw-01.csv",
    "hw-02": "data/hw-02.csv",
}


def read_table(file_name: str) -> pd.DataFrame:
    df = pd.read_csv(file_name)
    df = df.dropna(axis=1, how="all")
    df = df.rename(columns={
        "ФИ": "name",
        "Имя": "name",
        "Группа": "group_id",
        "Ссылка на MR": "mr_link",
        "Баллы": "score",
    })

    df = df[["name", "group_id", "mr_link", "score"]]
    df["name"] = df["name"].fillna("").astype(str).str.strip()
    df = df[df["name"] != ""]
    df["group_id"] = df["group_id"].astype(str).str.extract("(\\d+)")[0].astype(int)
    df["mr_link"] = df["mr_link"].fillna("").astype(str)
    df["score"] = pd.to_numeric(df["score"], errors="coerce").fillna(0)
    return df


hw1 = read_table(FILES["hw-01"])
hw2 = read_table(FILES["hw-02"])
all_names = sorted(set(hw1["name"]) | set(hw2["name"]))
student_ids = {}
for i, name in enumerate(all_names, start=1):
    student_ids[name] = i

hw1["student_id"] = hw1["name"].map(student_ids)
hw2["student_id"] = hw2["name"].map(student_ids)
TABLES = {
    "hw-01": hw1[["student_id", "name", "group_id", "mr_link", "score"]],
    "hw-02": hw2[["student_id", "name", "group_id", "mr_link", "score"]],
}


def get_table(hw_name: str) -> pd.DataFrame | None:
    if hw_name not in TABLES:
        return None
    return TABLES[hw_name]


def avg(series: pd.Series) -> float:
    if len(series) == 0:
        return 0
    return round(series.mean(), 2)


def get_mark(score: float) -> int:
    if score >= 50:
        return 5
    if score >= 30:
        return 4
    if score >= 1:
        return 3
    return 2


@app.route("/names")
def names() -> dict:
    return {"names": all_names}


@app.route("/<hw_name>/mean_score")
def mean_score_for_hw(hw_name: str) -> dict | tuple[dict, int]:
    df = get_table(hw_name)
    if df is None:
        return {"error": "unknown homework"}, 404
    return {"hw_name": hw_name, "mean_score": avg(df["score"])}


@app.route("/<hw_name>/<int:group_id>/mean_score")
def mean_score_for_group(hw_name: str, group_id: int) -> dict | tuple[dict, int]:
    df = get_table(hw_name)
    if df is None:
        return {"error": "unknown homework"}, 404

    group_df = df[df["group_id"] == group_id]
    return {"hw_name": hw_name, "group_id": group_id, "mean_score": avg(group_df["score"])}


@app.route("/mean_score")
def mean_score_query() -> dict | tuple[dict, int]:
    hw_name = request.args.get("hw_name")
    group_id = request.args.get("group_id", type=int)

    if hw_name is None or group_id is None:
        return {"error": "write hw_name and group_id"}, 400
    df = get_table(hw_name)
    if df is None:
        return {"error": "unknown homework"}, 404

    group_df = df[df["group_id"] == group_id]
    return {"hw_name": hw_name, "group_id": group_id, "mean_score": avg(group_df["score"])}


@app.route("/mark")
def mark() -> dict | tuple[dict, int]:
    student_id = request.args.get("student_id", type=int)
    group_id = request.args.get("group_id", type=int)
    if student_id is None and group_id is None:
        return {"error": "write student_id or group_id"}, 400

    all_scores = pd.concat([TABLES["hw-01"], TABLES["hw-02"]])
    total_scores = all_scores.groupby("student_id").agg({
        "name": "first",
        "group_id": "first",
        "score": "sum",
    }).reset_index()

    if student_id is not None:
        student = total_scores[total_scores["student_id"] == student_id]
        if len(student) == 0:
            return {"error": "student not found"}, 404

        score = student.iloc[0]["score"]
        return {
            "student_id": student_id,
            "name": student.iloc[0]["name"],
            "total_score": score,
            "mark": get_mark(score),
        }

    group = total_scores[total_scores["group_id"] == group_id].copy()
    group["mark"] = group["score"].apply(get_mark)
    return {"group_id": group_id, "mean_mark": avg(group["mark"])}


@app.route("/course_table")
def course_table() -> str | tuple[dict, int]:
    hw_name = request.args.get("hw_name")
    group_id = request.args.get("group_id", type=int)

    if hw_name is None:
        return {"error": "write hw_name"}, 400

    df = get_table(hw_name)
    if df is None:
        return {"error": "unknown homework"}, 404

    df = df.copy()
    if group_id is not None:
        df = df[df["group_id"] == group_id]

    df["mr_link"] = df["mr_link"].apply(lambda link: f'<a href="{link}">link</a>' if link else "")
    html = df.to_html(index=False, escape=False)
    return "<html><head><meta charset='utf-8'></head><body>" + html + "</body></html>"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=1337)
