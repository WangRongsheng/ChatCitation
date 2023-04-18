import gradio as gr
from scholarly import scholarly
import openai

def process(key, choice, artitle, trans):
    openai.api_key = str(key)
    
    results = []
    if choice=='单个生成':
        search_query = scholarly.search_pubs(str(artitle))
        pub = next(search_query)
        bib = scholarly.bibtex(pub)
        
        if trans=='bib':
            results.append(bib)
        else:
            prompt = "请把以下bib格式转为"+str(trans)+"格式："+str(bib)
            completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
            )
            results.append(completion.choices[0].message)
     if choice=='批量生成':
        m_artitle = artitle.split('\n')
        for i in range(len(m_artitle)):
            if trans=='bib':
                results.append(bib)
            else:
                prompt = "请把以下bib格式转为"+str(trans)+"格式："+str(bib)
                completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ]
                )
                results.append(completion.choices[0].message+'\n')
    
    return results

# 标题
title = "ChatCitation"
# 描述
description = '''<div align='left'>
论文引用
</div>
'''

input_c = [
        gradio.inputs.Textbox(label="输入OpenAI的API-key",
                          default="",
                          type='password'),
        gradio.inputs.Radio(choices=["单个生成", "批量生成"],
                        default="单个生成",
                        label="题目生成(默认单个生成)"),
        gradio.inputs.Textbox(
                        label="输入论文标题(如果为批量则每行一个标题)",
                        default="Transfer learning based plant diseases detection using ResNet50"),
        gradio.inputs.Dropdown(
                        choices=["AMA", "MLA", "APA", "GB/T 7714", "bib"],
                        label="转化的格式(默认bib)",
                        default="APA"),
        ]

demo = gr.Interface(fn=process, 
                    inputs=input_c,
                    outputs="text",
                    title=title,
                    description=description)
demo.launch()