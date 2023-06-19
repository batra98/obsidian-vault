import io
import os
import sys
from xxlimited import new
import pandas as pd
import json
import pandoc
from sqlalchemy import table


def change_ext(filename: str, new_ext: str):
    pre, ext = os.path.splitext(filename)

    return f"{pre}.{new_ext}"


file_name = sys.argv[1]


with open(file_name, "r") as f:
    data = json.load(f)


df = pd.DataFrame(data=data)
df = df.drop(columns="pluginVersion")
df = df.drop(labels="filterRules")
df = df.drop(labels="columns")
df = df.drop(labels="bodyRows")
df = df.drop(labels="footerRows")
df = df.drop(labels="headerRows")

headerCells = df["model"]["headerCells"]
footerCells = df["model"]["footerCells"]
bodyCells = df["model"]["bodyCells"]

headerCells = pd.DataFrame(data=headerCells)
headerCells = headerCells.sort_values(by=["rowId", "columnId"])
headerCells = headerCells.drop(columns=["id", "columnId", "rowId"])

columns = len(headerCells)
headerCells = headerCells.transpose()


footerCells = pd.DataFrame(data=footerCells)
footerCells = footerCells.sort_values(by=["rowId", "columnId"])
footerCells = footerCells.drop(columns=["id", "columnId", "rowId"])

bodyCells = pd.DataFrame(data=bodyCells)
bodyCells = bodyCells.sort_values(by=["rowId", "columnId"])
bodyCells = bodyCells.drop(
    columns=["id", "columnId", "rowId", "dateTime", "tagIds"],
)

total_cells = bodyCells.values.size
rows = total_cells // columns

bodyCells = pd.DataFrame(bodyCells.values.reshape(rows, columns))


bodyCells.columns = headerCells.values[0]


file_name = change_ext(filename=file_name, new_ext="md")
os.makedirs("tables", exist_ok=True)
with open(f"tables/{file_name}", "w") as f:
    bodyCells.to_markdown(f)
