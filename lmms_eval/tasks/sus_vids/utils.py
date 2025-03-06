import os
import sys
import yaml

from copy import deepcopy
from dataclasses import dataclass
from loguru import logger as eval_logger
from pathlib import Path

from sus_vids.models.prompt_settings import PromptSettings
from sus_vids.models.input import VideoInputType, PromptTemplateType
from sus_vids.models.prompt_message import get_prompt_message
from sus_vids.models.prompt_settings import get_prompt_settings_from_registry

with open(Path(__file__).parent / "_sus_vids_common.yaml", "r") as f:
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


def get_video_path(doc):
  video_path = os.path.join(cache_dir, doc["example_id"] + ".mp4")

  if not os.path.exists(video_path):
    sys.exit(f"video path:{video_path} does not exist, please check")

  return video_path


def sus_vids_doc_to_visual(doc, lmms_eval_specific_kwargs=None):
  video_path = get_video_path(doc)

  print(video_path)

  return [video_path]

def sus_vids_doc_to_text(doc, lmms_eval_specific_kwargs=None):
  if lmms_eval_specific_kwargs is None:
    lmms_eval_specific_kwargs = {}

  video_path = get_video_path(doc)

  if 'prompt_settings' in lmms_eval_specific_kwargs:
    prompt_settings = get_prompt_settings_from_registry(lmms_eval_specific_kwargs['prompt_settings'])
  else:
    prompt_settings = get_prompt_settings_from_registry('90-frames-only-frames')

  return get_prompt_message(
    video_path,
    input_type=VideoInputType.FramesWithTranscript,
    template_type=PromptTemplateType.GeneralDescription,
    prompt_settings=prompt_settings,
    template_extra_kwargs={
      "TRANSCRIPT": doc["transcript_srt"]
    }
  )
