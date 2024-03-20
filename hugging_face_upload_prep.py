# %%
import json
from pathlib import Path
import pandas as pd

PARAGRAPH_START_IDENTIFIER = "# Paragraph"
#%%

def assert_huggingface_correct():
    # d = json.load(Path('parsed_data.json').open())
    # japan = d['data'][12]
    # love = d['data'][14]
    # love['paragraphs'][5]
    # japan['paragraphs'][2]
    from datasets import load_dataset

    dataset = load_dataset("onestop_qa", split="train")
    for r in dataset:
        if not (r["a_span"][0] > r["d_span"][1] or r["a_span"][1] < r["d_span"][0]):
            print(r, "\n")
        if len(r["a_span"]) == 4 and not (
            r["a_span"][2] > r["d_span"][1] or r["a_span"][3] < r["d_span"][0]
        ):
            print(r, "\n")
        if len(r["d_span"]) == 4 and not (
            r["a_span"][0] > r["d_span"][3] or r["a_span"][1] < r["d_span"][2]
        ):
            print(r, "\n")


def convert_raw_text_to_json(base_path: Path, raw_text_path: Path, save_name: str):
    """
    Parse each text in raw_text_path and dump to json

    :return: None
    """
    text_path = base_path / raw_text_path

    data = []
    for path in text_path.iterdir():
        print(f"parsing {path}")
        parsed_text = _parse_raw_text(text_path=path)
        data.append(
            {"title": parsed_text["title"],
             "article_id": parsed_text["article_id"],
             "paragraphs": parsed_text["text_blocks"]}
        )

    save_path = base_path / save_name
    print(f"saving to {save_path}")
    with save_path.open(mode="w") as f:
        json.dump({"data": data}, f, indent=4)

    # To load the parsed_data:
    text_data = json.load(save_path.open(mode="r"))
    assert data == text_data["data"], "Saving/loading data failed!"


def _parse_paragraph(raw_paragraph_text: str, level: str) -> dict:
    start_identifier = f"{level}: "
    assert raw_paragraph_text.startswith(start_identifier), "incorrect level"
    raw_paragraph_text = raw_paragraph_text.removeprefix(start_identifier)
    a1_span = []
    a2_span = []
    a3_span = []
    d1_span = []
    d2_span = []
    d3_span = []
    for ind, word in enumerate(raw_paragraph_text.split()):
        # a spans
        if "<A1>" in word:
            a1_span.append(ind)
        if "</A1>" in word:
            a1_span.append(ind)

        if "<A2>" in word:
            a2_span.append(ind)
        if "</A2>" in word:
            a2_span.append(ind)

        if "<A3>" in word:
            a3_span.append(ind)
        if "</A3>" in word:
            a3_span.append(ind)

        # d spans
        if "<D1>" in word:
            d1_span.append(ind)
        if "</D1>" in word:
            d1_span.append(ind)

        if "<D2>" in word:
            d2_span.append(ind)
        if "</D2>" in word:
            d2_span.append(ind)

        if "<D3>" in word:
            d3_span.append(ind)
        if "</D3>" in word:
            d3_span.append(ind)

    clean_text = (
        raw_paragraph_text.replace("<A1>", "")
        .replace("</A1>", "")
        .replace("<A2>", "")
        .replace("</A2>", "")
        .replace("<A3>", "")
        .replace("</A3>", "")
        .replace("<D1>", "")
        .replace("</D1>", "")
        .replace("<D2>", "")
        .replace("</D2>", "")
        .replace("<D3>", "")
        .replace("</D3>", "")
    )
    for span in [a1_span, a2_span, a3_span, d1_span, d2_span, d3_span]:
        assert len(span) % 2 == 0, "incorrect span creation"
    return {
        "context": clean_text,
        "a_spans": [a1_span, a2_span, a3_span],
        "d_spans": [d1_span, d2_span, d3_span],
    }


def _parse_answer(line: str, letter: str):
    start_identifier = f"{letter}: "
    assert line.startswith(start_identifier), "incorrect answer format"
    line = line.removeprefix(start_identifier)
    return line


def _parse_raw_text(text_path: Path) -> dict:
    article_mappings = get_article_mappings()
    text: list[str] = []
    with open(text_path, "rb") as f:
        for line in f:
            clean_line = line.decode().strip()
            if clean_line:
                text.append(clean_line)
    title = text[1]
    article_id = article_mappings[title]
    print(f"parsing {title} with id {article_id}")
    parsed_text = {"title": title,
                   "article_id": article_id, 
                   "text_blocks": []}
    text_block = {}
    paragraph_id = 1
    for ind, line in enumerate(text):
        
        if line == PARAGRAPH_START_IDENTIFIER:
            if text_block:
                references = [qa["references"] for qa in text_block["qas"]]
                counts = {i: references.count(i) for i in references}

                # Define the mapping based on the counts
                mapping = {i: 1 if counts[i] == 2 else 0 for i in counts}

                # Use list comprehension to convert the list
                converted_references = [mapping[i] for i in references]
                for i, qa in enumerate(text_block['qas']):
                    qa['cs_has_two_questions'] = converted_references[i]
                parsed_text["text_blocks"].append(text_block)
            text_block = {
                "Adv": _parse_paragraph(text[ind + 1], "Adv"),
                "Int": _parse_paragraph(text[ind + 2], "Int"),
                "Ele": _parse_paragraph(text[ind + 3], "Ele"),
                "paragraph_id": paragraph_id,
                "qas": [],
            }
            paragraph_id += 1
            q_ind = 0

        elif line.startswith("Q"):
            assert line.startswith(("Q: ", "Q1: ", "Q2: ")), "incorrect question format"
            qa = {
                "question": line.removeprefix("Q: ")
                .removeprefix("Q1: ")
                .removeprefix("Q2: "),
                "references": int(line[1]) - 1 if line[1] != ":" else q_ind,
                "answers": [
                    _parse_answer(text[ind + 1], "a"),
                    _parse_answer(text[ind + 2], "b"),
                    _parse_answer(text[ind + 3], "c"),
                    _parse_answer(text[ind + 4], "d"),
                ],
                'q_ind': q_ind
            }
            q_ind += 1
            text_block["qas"].append(qa)
    if text_block:
        parsed_text["text_blocks"].append(text_block)
    return parsed_text


def get_article_mappings():
    data = pd.read_csv("all_dat_files_merged.tsv", sep="\t")
    # keep only unique article_id and article_title and batch
    data = data[["article_id", "article_title", "batch"]].drop_duplicates()
    data["unique_article_id"] = (
        data["batch"].astype(str) + "_" + data["article_id"].astype(str)
    )
    data.drop(columns=["article_id", "batch"], inplace=True)
    # replace ’ with '
    data["article_title"] = data["article_title"].str.replace("'", "’")
    article_mappings = data.set_index("article_title").to_dict()["unique_article_id"]
    return article_mappings


if __name__ == "__main__":
    convert_raw_text_to_json(
        base_path=Path("."),
        raw_text_path=Path("annotations") / "annotated_articles",
        save_name="onestop_qa.json",
    )
    # assert_huggingface_correct()


# %%

# %%

# %%
def get_article_data(article_id: str):
    import json
    from pathlib import Path
    text_data = json.load(Path('onestop_qa/onestop_qa.json').open(mode="r"))

    for article in text_data['data']:
        if article['article_id'] == article_id:
            return article
    raise ValueError(f'Article id {article_id} not found')