import whisperx
import gc
import torch
import io
from whisperx.utils import WriteSRT
import os
import re

def check_text(text):
    words = text.split()
    res = ['']
    if not latin(text)>3:
        for i, w in enumerate(words):
            if len(w) > 30:
                w = w[:30]
            if i < 3:
                res.append(w)
            elif w != words[i - 3] or w != words[i - 2] or w != words[i - 1]:
                res.append(w)
    return ' '.join(res)

def latin(text):
    return len(re.findall(r'\w+[A-Za-z]', text))

def transcribe(model, language, audio_file):
    device = get_device()
    batch_size = get_batch_size(device)
    compute_type = get_compute_type(device)

    # 1. Transcribe with original whisper (batched)
    # progress(0, desc="Performing transcription")
    model_transcribe = whisperx.load_model(
        model,
        device,
        compute_type=compute_type,
        language=language,
        threads=6
    )
    audio = whisperx.load_audio(audio_file)
    result_transcribed = model_transcribe.transcribe(
        audio,
        batch_size=batch_size,
        language=language,
        print_progress=True
    )
    print(result_transcribed["segments"]) # before alignment
    print('audio_file', audio_file[:-4])
    with open(f'{audio_file[:-4]}_result_transcribed.txt', 'w') as file:
        file.write(str(result_transcribed["segments"]))

    for result in result_transcribed["segments"]:
        if not 'Субтитры подготовил DimaTorzok' in result['text']:
            result['text'] = check_text(result['text'])
        else:
            result['text'] = ''

    print('result_check:', result_transcribed["segments"])  # before alignment, after checking
    print('audio_file', audio_file[:-4])
    with open(f'{audio_file[:-4]}_result_check.txt', 'w') as file:
        file.write(str(result_transcribed["segments"]))

    unload_model(model_transcribe)

    # 2. Align whisper output
    # progress(0.9, desc="Performing alignment")
    model_align, metadata = whisperx.load_align_model(
        language_code=result_transcribed["language"],
        device=device
    )
    result_aligned = whisperx.align(
        result_transcribed["segments"],
        model_align,
        metadata,
        audio,
        device,
        return_char_alignments=False
    )
    result_aligned["language"] = result_transcribed["language"]
    print(result_aligned["segments"]) # after alignment
    with open(f'{audio_file[:-4]}_result_aligned.txt', 'w') as file:
        file.write(str(result_aligned["segments"]))
    unload_model(model_align)

    with io.StringIO() as buffer:
        writesrt = WriteSRT(".")
        writesrt.write_result(
            result_aligned,
            buffer,
            {
                "max_line_width": None,
                "max_line_count": 2,
                "highlight_words": False,
                "preserve_segments": True
            }
        )

        # Now buffer.getvalue() contains the entire SRT content
        srt_content = buffer.getvalue()
    return srt_content

def get_device():
    return "cuda" if torch.cuda.is_available() else "cpu"

def get_batch_size(device):
    if device == "cuda":
        props = torch.cuda.get_device_properties(device)
        total_memory_gb = props.total_memory / (1024 ** 3)
        if total_memory_gb < 4:
            return 4
        if total_memory_gb < 6:
            return 8
        return 16
    else:
        return 2

def get_compute_type(device):
    return "float16" if device == "cuda" else "int8"

def unload_model(model):
    gc.collect()
    torch.cuda.empty_cache()
    del model
