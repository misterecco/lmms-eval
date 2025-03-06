import os
import sys
import yaml
from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path

PROMPT = "Describe the video content in detail."

with open(Path(__file__).parent / "sus_vids.yaml", "r") as f:
    raw_data = f.readlines()
    safe_data = []
    for i, line in enumerate(raw_data):
        # remove function definition since yaml load cannot handle it
        if "!function" not in line:
            safe_data.append(line)

    config = yaml.safe_load("".join(safe_data))

HF_HOME = os.environ["HF_HOME"]
cache_dir = config["dataset_kwargs"]["cache_dir"]
cache_dir = os.path.join(HF_HOME, cache_dir, "videos")


# @dataclass
# class Example:
#     """An example loaded from sus-vids, stored as jsonl in the repo."""

#     example_id: str
#     prompt: str
#     transcript_plain: str
#     transcript_srt: str
#     reference: str
#     media_filename: str

#     # The fields below are not stored in the dataset, but are populated by this script.
#     generation: Optional[str] = None
#     score: Optional[int] = None
#     evaluator_explanation: Optional[str] = None


def sus_vids_doc_to_visual(doc, lmms_eval_specific_kwargs=None):
  video_path = os.path.join(cache_dir, doc["example_id"] + ".mp4")

  if not os.path.exists(video_path):
    sys.exit(f"video path:{video_path} does not exist, please check")

  return [video_path]

def sus_vids_doc_to_text(doc, lmms_eval_specific_kwargs=None):
    # if lmms_eval_specific_kwargs is None:
    #     lmms_eval_specific_kwargs = {}
    # post_prompt = ""
    # post_prompt += lmms_eval_specific_kwargs["perception_and_comprehension_prompt"]
    # question = doc["prompts"]
    # parsed_options = parse_options(doc["options"])
    # question += "\n" + parsed_options

    return PROMPT
