import os
from llama_index.llms.openai import OpenAI
from llama_index.core.indices.struct_store import JSONQueryEngine
from llama_index.readers.json import JSONReader

def vector(insights):
    # https://llamahub.ai/l/readers/llama-index-readers-json?from=readers
    reader = JSONReader(levels_back=1, collapse_length=100, ensure_ascii=False)
    documents = reader.load_data('path_to_your_json_file.json')

    return insights
