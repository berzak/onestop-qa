import json
from pathlib import Path


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
            {"title": parsed_text["title"], "paragraphs": parsed_text["text_blocks"]}
        )

    save_path = base_path / save_name
    print(f"saving to {save_path}")
    with save_path.open(mode="w") as f:
        json.dump({"data": data}, f)

    # To load the parsed_data:
    text_data = json.load(save_path.open(mode="r"))
    assert data == text_data["data"], "Saving/loading data failed!"


def _parse_paragraph(raw_paragraph_text: str) -> dict:
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


def _parse_raw_text(text_path: Path) -> dict:
    text = []
    with open(text_path, "rb") as f:
        for line in f:
            clean_line = line.decode().strip("\r\n")
            if clean_line:
                text.append(clean_line)

    parsed_text = {"title": text[1], "text_blocks": []}
    text_block = {}
    for ind, line in enumerate(text):
        if line == "# Paragraph":
            if text_block:
                parsed_text["text_blocks"].append(text_block)
            text_block = {
                "Adv": _parse_paragraph(text[ind + 1].strip("Adv: ")),
                "Int": _parse_paragraph(text[ind + 2].strip("Int: ")),
                "Ele": _parse_paragraph(text[ind + 3].strip("Ele: ")),
                "qas": [],
            }

        elif line.startswith("Q"):
            qa = {
                "question": line.lstrip("Q12: "),
                "references": int(line[1]) - 1 if line[1] != ":" else -1,
                "answers": [
                    text[ind + 1].strip("a: "),
                    text[ind + 2].strip("b: "),
                    text[ind + 3].strip("c: "),
                    text[ind + 4].strip("d: "),
                ],
            }
            text_block["qas"].append(qa)
    if text_block:
        parsed_text["text_blocks"].append(text_block)
    return parsed_text


if __name__ == "__main__":
    convert_raw_text_to_json(
        base_path=Path("."),
        raw_text_path=Path("annotations") / "annotated_articles",
        save_name="parsed_data.json",
    )
    #assert_huggingface_correct()
