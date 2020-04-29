#!/usr/bin/env python
import glob
import re
import os
from datetime import datetime
from pathlib import Path
from shutil import copyfile

import numpy as np
import pandas as pd


def clean_year(x):
    match = re.search(r"\d{4}", str(x))
    if match:
        year = int(match.group())
    else:
        year = 1900
    return year if year <= datetime.now().year else -year


def main():
    dfs = []
    # Mix and add group (style) information
    for excel in glob.glob(os.path.join('tmp/drive', "METADATOS_*.xlsx")):
        df = pd.read_excel(excel)
        df["group"] = excel[:-5].rsplit("_")[-1]
        dfs.append(df)
    metadatos = pd.concat(dfs)
    # Clean date
    metadatos["year"] = metadatos.date.apply(clean_year)
    # Remove rows with no actual files in the folders
    metadatos = metadatos[(
        metadatos.group.apply(Path) / metadatos.filename).apply(
            lambda x: os.path.isfile(f"tmp/drive/{x}.jpg")
    )]
    # Rename columns
    metadatos.rename(columns={"image source": "source"}, inplace=True)
    # Selec only needed solumns
    metadatos = metadatos[
        ["group", "filename", "creator", "title", "source", "year"]
    ]
    metadatos["name"] = metadatos.group.str.lower().str.replace(" ", "_") + "_" + metadatos.filename + ".jpg"
    metadatos["path"] = "tmp/drive/" + metadatos.group + "/" + metadatos.filename + ".jpg"
    metadatos[["path", "name"]].apply(lambda row: copyfile(row.path, "images/" + row["name"]), axis=1)
    # Save to disk
    # metadatos.to_csv(
    #     "metadatos.csv", index=False
    # )
    # Build the new metadata csv
    csv = pd.DataFrame()
    csv["filename"] = metadatos["name"]
    csv["tags"] = metadatos["group"]
    csv["description"] = (
        metadatos["title"].astype(str)
        + " by "
        + metadatos["creator"].astype(str)
    )
    csv["permalink"] = metadatos["source"].fillna("")
    csv["year"] = metadatos["year"]
    csv.to_csv(
        "metadata.csv", index=False, header=False
    )


if __name__ == "__main__":
    main()
