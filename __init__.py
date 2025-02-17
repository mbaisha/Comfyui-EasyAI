from .easychat import AIPromptGenerator

# 在模块级别定义这些映射
NODE_CLASS_MAPPINGS = {
    "AIPromptGenerator": AIPromptGenerator
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "AIPromptGenerator": "AI Prompt Generator"
}

# 确保这些变量可以被ComfyUI导入
__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS'] 
