import os
import hashlib
import shutil
import time

import gradio as gr
# import time
from datetime import datetime, timedelta
from pytz import timezone
# import docker
from zipfile import ZipFile



from transcribe import transcribe
from whisperx.utils import LANGUAGES

session_id = 1
task_number = 1
file_list = []
# ui_srt_file_path = ''
ui_file_path = ''
ui_start_time = ''
app_path = os.path.dirname(os.path.realpath(__file__))
# gr.set_static_paths(paths=[str(os.path.join(app_path, 'upload'))])


def calculate_md5(file_name, block_size=4096):
    hasher = hashlib.md5()
    with open(file_name, 'rb', encoding="utf-8") as file:
        for chunk in iter(lambda: file.read(block_size), b''):
            hasher.update(chunk)
    return hasher.hexdigest()


def move_file(source_path, destination_path):
    try:
        shutil.move(source_path, destination_path)
        print(f"File moved successfully to {destination_path}")
    except Exception as e:
        # Handle the case where the move operation fails
        print(f"Error occurred while moving the file: {e}")


def map_language(language):
    return None if language == "auto" else find_language_code(language)


def find_language_code(language):
    for key, value in LANGUAGES.items():
        if language == value:
            print('key:', key)
            return key


def create_dir_if_not_exist(dir):
    if not os.path.exists(os.path.join(app_path, dir)):
        os.makedirs(os.path.join(app_path, dir))


def write_content(srt_path, content):
    file_name, file_ext = os.path.splitext(srt_path)
    if file_ext != '.srt':
        srt_path = os.path.join(app_path, 'subs', f'{file_name}.srt')
    f = open(srt_path, "w", encoding="utf-8")
    if content:
        f.write(content)
    else:
        f.write('1\n00:00:00,000 --> 00:00:00,001\nnull')
    f.close()
    print('srt_path:', srt_path)
    print('subs have written')

# def table_info(evt: gr.SelectData):
#     return evt

def edit_content(file_path, start_time):
    # global ui_srt_file_path
    global ui_file_path
    global ui_start_time
    # file_name, file_ext = os.path.splitext(srt_path)
    # if file_ext != '.srt':
    #     srt_path = os.path.join('/app/subs', f'{file_name}.srt')
    file_name, file_ext = os.path.splitext(file_path)
    srt_path = os.path.join(app_path, 'subs', f'{file_name}.srt')
    try:
        with open(srt_path, "r", encoding="utf-8") as srt_content:
            # ui_srt_file_path = srt_path
            ui_file_path = file_path
            ui_start_time = start_time
            return ui_file_path, ui_start_time, srt_content.read()
    except Exception:
        raise gr.Error("Srt file not found")



def close_update_srt(ui_content, old_srt_file_list):
    # global ui_srt_file_path
    global ui_file_path
    global ui_start_time
    print('old srt_file_list', old_srt_file_list)
    file_name, file_ext = os.path.splitext(ui_file_path)
    # if file_ext != '.srt':
    srt_path = os.path.join(app_path, 'subs', f'{os.path.basename(file_name)}.srt')
    # srt_path = ui_srt_file_path
    srt_file_list = [os.path.join(app_path, 'subs', os.path.basename(srt_file)) for srt_file in old_srt_file_list]
    if ui_content:
        try:
            with open(srt_path, "w", encoding="utf-8") as srt_content:
                srt_content.write(ui_content)
        except Exception:
            raise gr.Error("Srt file cannot be written")
    else:
        with open(srt_path, "w", encoding="utf-8") as srt_content:
            srt_content.write('1\n00:00:00,000 --> 00:00:00,001\nnull')

    print('srt_path:', srt_path)
    print('subs have written')
    print('new srt_file_list', srt_file_list)
    return ui_file_path, ui_start_time, ui_content, srt_file_list

def update_ui():
    pass

    # zip_name = f'SUB_ID_{session_id:02d}_Task_{task_number:04d}.zip'
    # myzip = ZipFile(zip_name, "w")
    # try:
    #     myzip.write(srt_path)
    #     print('ZIP was updated')
    # except Exception:
    #     print('ZIP updating ERROR')
    # finally:
    #     myzip.close()
    #     print('updating_zip_name:', os.path.abspath(zip_name))

#
# def create_zip(table_data):
#     print('table_data:', table_data)
#     srt_list = []
#     if table_data:
#         for i in range(len(table_data)):
#             file_path = table_data[i][0]
#             file_name, file_ext = os.path.splitext(file_path)
#             srt_file_path = os.path.join("subs", f"{os.path.basename(file_name)}.srt")
#             srt_list.append(srt_file_path)
#     zip_name = f'SUB_ID_{session_id:02d}_Task_{task_number:04d}.zip'
#     myzip = ZipFile(zip_name, "w")
#     try:
#         [myzip.write(srt) for srt in srt_list]
#         print('ZIP archive created')
#     except Exception:
#         print('ZIP archive ERROR')
#     finally:
#         myzip.close()
#     print('abs_zip_name:', os.path.abspath(zip_name))
#     return zip_name

# def create_zip(srt_list):
#     # sub_zip = os.path.join('')
#     zip_name = f'SUB_ID_{session_id:02d}_Task_{task_number:04d}.zip'
#     myzip = ZipFile(zip_name, "w")
#     try:
#         [myzip.write(srt) for srt in srt_list]
#         print('ZIP archive created')
#     except Exception:
#         print('ZIP archive ERROR')
#     finally:
#         myzip.close()
#         print('creating_zip_name:', os.path.abspath(zip_name))
#     return zip_name
#
# def update_zip(srt_path):
#     # sub_zip = os.path.join('')
#     zip_name = f'SUB_ID_{session_id:02d}_Task_{task_number:04d}.zip'
#     myzip = ZipFile(zip_name, "w")
#     try:
#         myzip.write(srt_path)
#         print('ZIP was updated')
#     except Exception:
#         print('ZIP updating ERROR')
#     finally:
#         myzip.close()
#         print('updating_zip_name:', os.path.abspath(zip_name))
#     return zip_name

def zip_name(text):
    return f'SUB_ID_{session_id:02d}_Task_{task_number:04d}.zip'

def load_vid(file_list, evt: gr.SelectData):
    print('evt.row_value', evt.row_value)
    file = evt.row_value[0]
    start_time = evt.row_value[2]
    file_name, file_ext = os.path.splitext(file)
    # file_path = os.path.join(app_path, 'upload', f'{file_name}{file_ext}')
    srt_path = os.path.join(app_path, 'subs', f'{file_name}.srt')
    for temp_file in file_list:
        # print('file_list:', file_list)
        if file in temp_file:
            file_path = temp_file
            print('video_file_path:', file_path)
    with open(srt_path, 'r', encoding="utf-8") as text:
        sub_text = text.read()
    return [file, start_time, sub_text, (file_path, srt_path)]

def logs(log_name, text, time=True):
    tz = timezone('Europe/Moscow')
    with open(log_name, "a", encoding="utf-8") as file:
        if time:
            time = datetime.now(tz).strftime('%d-%m-%Y_%H-%M-%S')
        else:
            time = ''
        print(time, text, file=file, sep='')


# def task_number():
#     log_list = os.listdir()
#     fact_task_list = []
#     for file in log_list:
#         if file.startswith('LOG'):
#             fact_task = os.path.splitext(file)[0].split('Task_')[1]
#             fact_task_list.append(int(fact_task))
#     print(fact_task_list)
#     if fact_task_list:
#         task = max(fact_task_list) + 1
#     else:
#         task = 1
#     return f'{task:04d}'



def process_file(model, language, file_list):
    if not file_list:
        return "Please choose files before submitting."
    file_name = 'Preparing...'
    global task_number
    create_dir_if_not_exist("upload")
    create_dir_if_not_exist("subs")
    create_dir_if_not_exist("logs")
    task_number += 1

    tz = timezone('Europe/Moscow')
    start_time_frm = datetime.now(tz).strftime('%d-%m-%Y_%H-%M-%S')

    log_name = f'{app_path}/logs/LOG_{start_time_frm}_ID_{session_id:02d}_Task_{task_number:04d}.log'
    logs(log_name, f"\n{'-' * 50}\nQueue:")
    [logs(log_name, os.path.basename(file), False) for file in file_list]
    logs(log_name, f'started with settings: {model}/{language}', False)
    logs(log_name, '-' * 20, False)
    table_data = []
    srt_list = []
    srt_content = ''
    # srt_table = []
    execution_time = '00:00:00'
    total_start_time = datetime.now(tz)
    for temp_file in file_list:
        logs(log_name, os.path.basename(temp_file), False)
        logs(log_name, " - Transcription started")
        status = 'In progress...'
        print('temp_file:', temp_file)
        print('abspath_temp_file:', os.path.abspath(temp_file))
        start_time = datetime.now(tz)
        # start_time_frm = datetime.now(tz).strftime('%d-%m-%Y_%H-%M-%S')
        start_time_frm = datetime.now(tz).strftime('%H-%M-%S')
        print(start_time_frm)
        if not temp_file or not os.path.exists(temp_file):
            # raise gr.Error("This should fail!")
            return "Please upload a file before submitting."
        print('language_map:', language)
        lang = map_language(language)
        print('language:', lang)
        print('model:', model)

        file_path, file_extension = os.path.splitext(temp_file)
        print('file_path:', file_path)
        # md5_hash = calculate_md5(temp_file)
        # print('md5_hash:', md5_hash)
        # output_file = os.path.join(app_path, "upload", os.path.basename(temp_file))
        # print('abs_output_file:', os.path.abspath(output_file))
        # move_file(temp_file, output_file)
        file_name = os.path.basename(temp_file)
        # print('output_file:', output_file)
        # srt_content = transcribe(model, lang, temp_file)
        try:
            srt_content = transcribe(model, lang, temp_file)
            # srt_table = open("F_12.Years.a.Slave_2013_CENZ_1080p25_H264_10Mbps.srt", 'r').read()
            # srt_table = [[t] for t in srt_content.read().split('\n')]
            # print('srt_table:', srt_table)
            status = 'Done'
            output_file_srt = os.path.join(app_path, "subs", f"{os.path.basename(file_path)}.srt")
            srt_list.append(output_file_srt)
            print(srt_list)
            print('abspath_output_file_srt:', os.path.abspath(output_file_srt))
            write_content(output_file_srt, srt_content)
            # move_file(output_file_srt, os.path.splitext(output_file)[0]+'.srt')
            print('srt file created')
            logs(log_name, " - Srt file created")
            end_time = datetime.now(tz)
            execution_time = str(end_time - start_time).split(".")[0]

            file_data = [file_name, status, start_time_frm, execution_time]
            table_data.append(file_data)
            logs(log_name, " - Transcription finished")
            logs(log_name, " - Alignment started")
        except Exception as e:
            status = 'Error'
            print(e)
            print(datetime.now(tz), '- !!!Transcription failed!!!')
            file_data = [file_name, status, execution_time]
            table_data.append(file_data)
            logs(log_name, " - !!!Transcription failed!!!")
            logs(log_name, os.path.basename(temp_file), False)
            logs(log_name, '-' * 50, False)

        # sub_zip = create_zip(srt_list)
        logs(log_name, " - Alignment finished")
        # sub_zip = create_zip()
        # logs(log_name, f" - {sub_zip} created")
        logs(log_name, f'Execution_time: {execution_time}', False)
        logs(log_name, temp_file, False)
        logs(log_name, '-' * 60, False)
        yield file_name, start_time_frm, srt_content, table_data, srt_list
    # sub_zip = create_zip(srt_list)
    # sub_zip = create_zip()
    total_time = str(datetime.now(tz) - total_start_time).split(".")[0]
    logs(log_name, f'Total_time: {total_time}', False)
    logs(log_name, '-' * 60, False)
    yield file_name, start_time_frm, srt_content, table_data, srt_list

def collapse_accord(file_list):
    if file_list:
        return {gr_set_accord: gr.Accordion(open=False),
                gr_in_list_accord: gr.Accordion(open=False),
                gr_out_file_list: gr.Files(visible=True),
                gr_out_table: gr.Dataframe(visible=True)}
    else:
        return gr_set_accord, gr_in_list_accord, gr_out_file_list, gr_out_table


def visible_vid_sub():
    return {gr_vid: gr.Video(visible=True),
            gr_sub_text: gr.Code(visible=True),
            gr_edit_sub_text: gr.Code(visible=False),
            gr_edit_btn: gr.Button(visible=True)}

def visible_edit_sub_text():
    return {gr_file_name: gr.Textbox(visible=False),
            gr_edit_file_name: gr.Textbox(visible=True),
            gr_start_time: gr.Textbox(visible=False),
            gr_edit_start_time: gr.Textbox(visible=True),
            gr_sub_text: gr.Code(visible=False),
            gr_edit_sub_text: gr.Code(visible=True),
            gr_edit_btn: gr.Button(visible=False),
            gr_save_btn: gr.Button(visible=True),
            gr_cancel_btn: gr.Button(visible=True)}

def unvisible_edit_sub_text():
    return {gr_file_name: gr.Textbox(visible=True),
            gr_edit_file_name: gr.Textbox(visible=False),
            gr_start_time: gr.Textbox(visible=True),
            gr_edit_start_time: gr.Textbox(visible=False),
            gr_sub_text: gr.Code(visible=True),
            gr_edit_sub_text: gr.Code(visible=False),
            gr_edit_btn: gr.Button(visible=True),
            gr_save_btn: gr.Button(visible=False),
            gr_cancel_btn: gr.Button(visible=False)}

def exit_fn():
    global session_id
    session_id += 1
    # file_dir = os.path.join(app_path, "upload")
    # if file_list:
    #     for file in file_list:
    #         try:
    #             os.remove(file)
    #             print('Cache deleted successfully')
    #         except Exception:
    #             print('ERROR! Cache did not delete')
    # gr.Blocks.unload()
    # print('Blocks unloaded')

with gr.Blocks(
        title='Subtitle Transcription',
        delete_cache=(86400, 86400),
        css='''footer {visibility: hidden} 
        h1 {text-align: center;
        display:block;
        }''') as main_window:
    gr.Markdown('# TLTV Subtitle Transcription')
    # gr.Markdown('Upload your audio or video file')
    with gr.Row():
        # gr.DownloadButton(label="Download Processed File"),
        with gr.Column(scale=1, min_width=300):
            with gr.Accordion('Select settings') as gr_set_accord:
                gr_mode_set = gr.Dropdown(
                    ["medium", "large-v2", "large-v3"],
                    value="large-v2",
                    multiselect=False,
                    label="Whisper Model"
                )
                gr_lang_set = gr.Dropdown(
                    ["auto"] + list(LANGUAGES.values()),
                    value="russian",
                    multiselect=False,
                    label="Language"
                )
            with gr.Accordion('File list') as gr_in_list_accord:
                gr_inp_vid = gr.Files(
                    type="filepath",
                    file_types=["audio", "video"],
                    label="Upload your files",
                    file_count="multiple"
                )
            with gr.Row():
                gr_start_btn = gr.Button(value='Start', variant='primary')
                gr_stop_btn = gr.Button(value='Stop', variant='stop')

            gr_vid = gr.Video(visible=False,
                              autoplay=True,
                              height=410,
                              show_download_button=False)
            # with gr.Accordion(label='LOG list:', visible=False) as gr_out_accord:
            gr_out_table = gr.Dataframe(visible=False,
                                        interactive=False,
                                        type="array",
                                        headers=['File', 'Status', 'Start time', 'Total time'],
                                        column_widths=[105, 20, 30, 25],
                                        max_height=275)





        with gr.Column(scale=1, min_width=300):
            gr_file_name = gr.Textbox(label="Running file name:",
                                      interactive=False)
            gr_edit_file_name = gr.Textbox(label="Running file name:",
                                           interactive=False,
                                           visible=False)
            gr_start_time = gr.Textbox(label="Start time:",
                                       interactive=False)
            gr_edit_start_time = gr.Textbox(label="Start time:",
                                            interactive=False,
                                            visible=False)
            # gr_sub_text = gr.Textbox(label="Subtitle text:",
            #                          lines=4,
            #                          max_lines=25,
            #                          interactive=True)

            # gr_sub_text = gr.Dataframe(max_height=300,
            #                            wrap=True,
            #                            interactive=True)
            gr_sub_text = gr.Code(
                visible=False,
                label="Subtitle text:",
                # wrap_lines=True,
                max_lines=30,
                interactive=False,
                container=False)
            # [[t] for t in text.split('\n')]
            # gr.Textbox(label="Execution Time"),
            gr_edit_sub_text = gr.Code(
                visible=False,
                label="Subtitle text:",
                # wrap_lines=True,
                max_lines=30,
                interactive=True,
                container=False)
            with gr.Row():
                gr_edit_btn = gr.Button(value='edit', size='sm', visible=False)
                gr_save_btn = gr.Button(value='save', size='sm', visible=False)
                gr_cancel_btn = gr.Button(value='cancel', size='sm', visible=False)
            gr_out_file_list = gr.Files(label='Download list',
                                        interactive=False,
                                        # type="binary",
                                        visible=False)


            # with gr.Row():
            #     gr_down_sub = gr.DownloadButton(label="Download SUB")
            #     gr_down_log = gr.DownloadButton(label="Download LOG")

    main_inputs = [gr_mode_set, gr_lang_set, gr_inp_vid]
    main_outputs = [gr_file_name, gr_start_time, gr_sub_text, gr_out_table, gr_out_file_list]

    main_process = gr_start_btn.click(fn=process_file, inputs=main_inputs, outputs=main_outputs, concurrency_limit=3)
    gr_start_btn.click(fn=collapse_accord, inputs=gr_inp_vid, outputs=[gr_set_accord, gr_in_list_accord, gr_out_file_list, gr_out_table])

    gr_stop_btn.click(fn=None, inputs=main_inputs, outputs=main_outputs, cancels=[main_process])
    gr_out_table.select(fn=load_vid, inputs=gr_inp_vid, outputs=[gr_file_name, gr_start_time, gr_sub_text, gr_vid], show_progress="hidden")
    gr_out_table.select(fn=visible_vid_sub, outputs=[gr_vid, gr_sub_text, gr_edit_sub_text, gr_edit_btn])
    # gr_sub_text.change(fn=edit_content, inputs=[gr_file_name, gr_sub_text, gr_out_file_list], outputs=gr_out_file_list)

    # gr_sub_text.focus(edit_content, inputs=gr_file_name, outputs=gr_edit_sub_text)
    # gr_sub_text.focus(visible_edit_sub_text, outputs=[gr_sub_text, gr_edit_sub_text])

    gr_edit_btn.click(edit_content, inputs=[gr_file_name, gr_start_time], outputs=[gr_edit_file_name, gr_edit_start_time, gr_edit_sub_text])
    gr_edit_btn.click(visible_edit_sub_text, outputs=[gr_file_name, gr_start_time, gr_edit_file_name, gr_edit_start_time, gr_sub_text, gr_edit_sub_text, gr_edit_btn, gr_save_btn, gr_cancel_btn])
    gr_save_btn.click(close_update_srt, inputs=[gr_edit_sub_text, gr_out_file_list], outputs=[gr_file_name, gr_start_time, gr_sub_text, gr_out_file_list])
    gr_save_btn.click(unvisible_edit_sub_text, outputs=[gr_file_name, gr_start_time, gr_edit_file_name, gr_edit_start_time, gr_sub_text, gr_edit_sub_text, gr_edit_btn, gr_save_btn, gr_cancel_btn])
    gr_cancel_btn.click(unvisible_edit_sub_text, outputs=[gr_file_name, gr_start_time, gr_edit_file_name, gr_edit_start_time, gr_sub_text, gr_edit_sub_text, gr_edit_btn, gr_save_btn, gr_cancel_btn])
    # gr_out_file_list.change(fn=None, outputs=gr_out_file_list)
    # gr_down_sub.click(fn=zip_name, inputs=gr_sub_text, outputs=gr_down_sub, preprocess=False)
    main_window.unload(fn=exit_fn)
    # gr.Interface(
    #     fn=process_file,
    #     clear_btn=None,
    #     submit_btn='Start',
    #     inputs=inputs,
    #     outputs=outputs,
    #     title="WhisperX Subtitle Transcription",
    #     description="Upload your audio or video file.",
    #     allow_flagging="never",
    #     css="footer {visibility: hidden}"
    # )
favicon_path=os.path.join(app_path, "FAVICON_TLTV_256x256.ico")
allowed_paths = [os.path.join(app_path, 'subs'), os.path.join(app_path, 'logs')]
if __name__ == "__main__":
    main_window.queue()
    main_window.launch(server_name="0.0.0.0", server_port=7860, allowed_paths=allowed_paths, favicon_path=favicon_path)
