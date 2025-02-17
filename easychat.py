import os
import json
from openai import OpenAI

class AIPromptGenerator:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "prompt": ("STRING", {"multiline": True}),
                "system_prompt": ("STRING", {
                    "multiline": True,
                    "default": "你好，我是 Flux 提示生成器，Flux 提示生成助手：专注于为 Flux 模型生成高质量图像输出而创作详细、创意提示的专家，你发给我你想作的图的构想，我不会给你我的想法，也不会重复你的话，不会向你提问，我会输出高质量的提示词，并且要求作出来的图是高清8K图，我只会将内容直接以英文提示词回复你，不会有多余的话语！"
                }),
            },
            "optional": {
                "temperature": ("FLOAT", {
                    "default": 1.0,
                    "min": 0.0,
                    "max": 2.0,
                    "step": 0.1,
                    "tooltip": "创造性（越大越有创意，越小越严谨）"
                }),
                "max_tokens": ("INT", {
                    "default": 2048,
                    "min": 1,
                    "max": 4096,
                    "step": 1,
                    "tooltip": "最大输出长度"
                }),
                "top_p": ("FLOAT", {
                    "default": 1.0,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.1,
                    "tooltip": "采样范围（影响回答的多样性）"
                }),
                "frequency_penalty": ("FLOAT", {
                    "default": 0.0,
                    "min": -2.0,
                    "max": 2.0,
                    "step": 0.1,
                    "tooltip": "用词重复度（越大越不爱重复用词）"
                }),
                "presence_penalty": ("FLOAT", {
                    "default": 0.0,
                    "min": -2.0,
                    "max": 2.0,
                    "step": 0.1,
                    "tooltip": "话题重复度（越大越容易换新话题）"
                }),
                "stop_sequence": ("STRING", {
                    "default": "",
                    "multiline": False,
                    "tooltip": "停止标记（AI看到这个词就停止回答）"
                }),
                "base_url": ("STRING", {
                    "default": "https://api.deepseek.com",
                    "multiline": False,
                    "tooltip": "API地址"
                }),
                "api_key": ("STRING", {
                    "default": "",
                    "multiline": False,
                    "tooltip": "APIKey"
                }),
                "model_name": ("STRING", {
                    "default": "deepseek-v3",
                    "multiline": False,
                    "tooltip": "模型名称"
                }),
            }
        }
    
    RETURN_TYPES = ("STRING",)
    FUNCTION = "execute"
    CATEGORY = "EasyAI"

    @classmethod
    def get_icon(cls):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        icon_path = os.path.join(dir_path, "deepseek_icon.svg")
        if os.path.exists(icon_path):
            with open(icon_path, "r") as f:
                return f.read()
        return None

    def execute(self, prompt, system_prompt="You are a professional assistant for writing flux prompt words", 
                temperature=1.0, max_tokens=2048, top_p=1.0,
                frequency_penalty=0.0, presence_penalty=0.0, 
                stop_sequence="",base_url = "https://api.deepseek.com" , api_key="",model_name="deepseek-v3"):
        if not api_key:
            return ("Error: Please configure your API key in config.json",)
            
        try:
            client = OpenAI(
                api_key=api_key,
                base_url=base_url
            )
            
            # 构建请求参数
            params = {
                "model": model_name ,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt},
                ],
                "temperature": temperature, 
                "max_tokens": max_tokens,
                "top_p": top_p,
                "frequency_penalty": frequency_penalty,
                "presence_penalty": presence_penalty,
                "stream": False,
                "response_format": {"type": "text"}
            }
            
            # 如果提供了stop_sequence，添加到参数中
            if stop_sequence:
                params["stop"] = [stop_sequence]
            
            response = client.chat.completions.create(**params)
            
            return (response.choices[0].message.content,)
        except Exception as e:
            return (f"Error: {str(e)}",)
