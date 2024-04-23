import torch
from diffusers import AnimateDiffPipeline, MotionAdapter, EulerDiscreteScheduler
from diffusers.utils import export_to_gif
from huggingface_hub import hf_hub_download
from safetensors.torch import load_file
import numpy as np

device = "cuda"
dtype = torch.float16

step = 4  # Options: [1,2,4,8]
repo = "ByteDance/AnimateDiff-Lightning"
ckpt = f"animatediff_lightning_{step}step_diffusers.safetensors"
base = "emilianJR/epiCRealism"  # Choose to your favorite base model.

adapter = MotionAdapter().to(device, dtype)
adapter.load_state_dict(load_file(hf_hub_download(repo ,ckpt), device=device))
pipe = AnimateDiffPipeline.from_pretrained(base, motion_adapter=adapter, torch_dtype=dtype).to(device)
pipe.scheduler = EulerDiscreteScheduler.from_config(pipe.scheduler.config, timestep_spacing="trailing", beta_schedule="linear")

def text_to_video(sentences,audio, fps=5, num_inference_steps=80):
    sample_rate = 22050
    aud_length = len(audio[0])/sample_rate
    frames_rate = round(fps*aud_length)
    torch.cuda.empty_cache()
    vid_model = pipe(sentences[0], guidance_scale=1.0, num_inference_steps=num_inference_steps, num_frames=frames_rate)
    vid = vid_model.frames[0]
    del vid_model
    for ind in range(1,len(sentences)):
        aud_length = len(audio[ind])/sample_rate
        frames_rate = round(fps*aud_length)

        pipe_model = pipe(sentences[ind], guidance_scale=1.0, num_inference_steps=num_inference_steps, num_frames=frames_rate)
        video_frames = pipe_model.frames[0]
        del pipe_model
        vid=np.concatenate((vid,video_frames))
        del video_frames
    return vid