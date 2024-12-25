import whisperx
import gc
import torch
import io
from whisperx.utils import WriteSRT
import os
import re


def add_word(new_result_aligned, dict_num, i, seq_words):
    try:

        new_result_aligned['segments'][dict_num]['words'].append({})
        if len(new_result_aligned['segments'][dict_num]['words']) > 0:
            word_list_num = len(new_result_aligned['segments'][dict_num]['words']) - 1
        else:
            word_list_num = 0
        new_result_aligned['segments'][dict_num]['words'][word_list_num]['word'] = seq_words[i]['word']
        new_result_aligned['segments'][dict_num]['words'][word_list_num]['start'] = seq_words[i]['start']
        new_result_aligned['segments'][dict_num]['words'][word_list_num]['end'] = seq_words[i]['end']
        new_result_aligned['segments'][dict_num]['words'][word_list_num]['score'] = seq_words[i]['score']
    except Exception:
        pass
    new_result_aligned['word_segments'].append({})
    if len(new_result_aligned['word_segments']) > 0:
        word_seg_count = len(new_result_aligned['word_segments']) - 1
    else:
        word_seg_count = 0
    try:
        new_result_aligned['word_segments'][word_seg_count]['word'] = seq_words[i]['word']
        new_result_aligned['word_segments'][word_seg_count]['start'] = seq_words[i]['start']
        new_result_aligned['word_segments'][word_seg_count]['end'] = seq_words[i]['end']
        new_result_aligned['word_segments'][word_seg_count]['score'] = seq_words[i]['score']
    except Exception:
        pass

def check_text(aligned):
    new_result_aligned = {'segments': [], 'word_segments': [], 'language': ''}
    segments = aligned['segments']
    word_segments = aligned['word_segments']
    language = aligned['language']

    for num, seq in enumerate(segments):
        seq_start = seq['start']
        seq_end = seq['end']
        seq_text = seq['text']
        seq_words = seq['words']
        if seq_end - seq_start > 0.5:
            if not 'Тикабон' in seq_text and not latin(seq_text) > 3:
                new_result_aligned['segments'].append({})

                if len(new_result_aligned['segments']) > 0:
                    dict_num = len(new_result_aligned['segments']) - 1
                else:
                    dict_num = 0

                new_result_aligned['segments'][dict_num] = {'start': '', 'end': '', 'text': '', 'words': []}
                new_result_aligned['segments'][dict_num]['start'] = seq_start
                new_result_aligned['segments'][dict_num]['end'] = seq_end
                new_result_aligned['segments'][dict_num]['words'] = []
                text = []
                for i in range(len(seq_words)):
                    # new_result_aligned['segments'][num]['words'][i] = {'word': '', 'start': '', 'end': '', 'score': ''}
                    seq_dict_word = seq_words[i]['word']
                    if len(seq_dict_word) > 30:
                        seq_dict_word = seq_dict_word[:30]
                    if i <= 3:
                        add_word(new_result_aligned, dict_num, i, seq_words)
                        text.append(seq_dict_word)
                    elif seq_dict_word == seq_words[i - 3]['word'] or seq_dict_word == seq_words[i - 2]['word'] or seq_dict_word == seq_words[i - 1]['word']:
                        # new_result_aligned['segments'][num]['words'].append({})
                        # dict_word[i] = ''
                        print('repeated', seq_words[i])
                        # end_i = seq_words[i]['end']
                        # seq_words[i - 1]['end'] = end_i
                        if len(new_result_aligned['segments'][dict_num]['words']) > 0:
                            word_list_num = len(new_result_aligned['segments'][dict_num]['words']) - 1
                        else:
                            word_list_num = 0

                        if len(new_result_aligned['word_segments']) > 0:
                            word_seg_count = len(new_result_aligned['word_segments']) - 1
                        else:
                            word_seg_count = 0
                        try:
                            new_result_aligned['segments'][dict_num]['words'][word_list_num]['end'] = seq_words[i]['end']
                            print("timecode_1 changed")
                            new_result_aligned['word_segments'][word_seg_count]['end'] = seq_words[i]['end']
                            print("timecode_2 changed")
                        except Exception:
                            print("timecode didn't change")
                            pass
                        # seq_words[i]['word'] = ''
                        # word_segments[num]['word'] = ''
                        # dict_word['word'] = ''
                    else:
                        add_word(new_result_aligned, dict_num, i, seq_words)
                        text.append(seq_dict_word)
                new_result_aligned['segments'][dict_num]['text'] = ' '.join(text)
            else:
                print("exclusion")
                # segments[num] = ''
                # seq['text'] = ''
                # for dict_word in dict_words:
                #     print('dict_word deleted', dict_word)
                #     dict_word['word'] = ''
    new_result_aligned['language'] = language
    print('new_result_aligned', new_result_aligned)
    return new_result_aligned

def latin(text):
    print('latin_text', text)
    return len(re.findall(r'\w+[A-Za-z]', text))

def transcribe(model, language, audio_file):
    device = get_device()
    device = 'cpu'
    batch_size = get_batch_size(device)
    compute_type = get_compute_type(device)

    # 1. Transcribe with original whisper (batched)
    # progress(0, desc="Performing transcription")
    model_transcribe = whisperx.load_model(
        model,
        device,
        compute_type=compute_type,
        language=language,
        threads=10,
        asr_options={'length_penalty': 2,
                     'repetition_penalty': 1,
                     "no_repeat_ngram_size": 2}
    )
    audio = whisperx.load_audio(audio_file)
    result_transcribed = model_transcribe.transcribe(
        audio,
        batch_size=batch_size,
        language=language,
        print_progress=True
    )
    print(result_transcribed["segments"]) # before alignment
    # print('audio_file', audio_file[:-4])
    # with open(f'{audio_file[:-4]}_result_transcribed.txt', 'w', encoding="utf-8") as file:
    #     file.write(str(result_transcribed["segments"]))
    #
    # for result in result_transcribed["segments"]:
    #     if not 'Субтитры подготовил DimaTorzok' in result['text']:
    #         result['text'] = check_text(result['text'])
    #     else:
    #         result['text'] = ''
    #
    # print('result_check:', result_transcribed["segments"])  # before alignment, after checking
    # print('audio_file', audio_file[:-4])
    # with open(f'{audio_file[:-4]}_result_check.txt', 'w', encoding="utf-8") as file:
    #     file.write(str(result_transcribed["segments"]))

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
    print('result_aligned_seg', result_aligned["segments"]) # after alignment
    print('result_aligned', result_aligned)

    with open(f'{audio_file[:-4]}_result_aligned.txt', 'w', encoding="utf-8") as file:
        file.write(str(result_aligned))
    unload_model(model_align)

    result_aligned = check_text(result_aligned)

    with open(f'{audio_file[:-4]}_result_checked.txt', 'w', encoding="utf-8") as file:
        file.write(str(result_aligned))
    unload_model(model_align)

    with io.StringIO() as buffer:
        writesrt = WriteSRT(".")
        print('final_result_aligned', result_aligned)
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
