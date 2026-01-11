# app/agents/nodes/generator.py

import json
import re
from langchain_groq import ChatGroq
from app.core.config import settings
from app.agents.state import MoleculeState

# Khoi tao model Llama3 70B cho Generator Agent
model = ChatGroq(
    api_key = settings.GROQ_API_KEY,
    model_name = settings.GENERATOR_MODEL,
)

def generator_node(state: MoleculeState):
    """
    Generator Agent: Tao cac phan tu ung vien duoi dang ma SMILES tu mot hoac nhieu phan tu ban dau (seeds)
    """

    objective = state['objectives']
    seeds = state['seeds']

    # Prompt yeu cau LLM tao moi phan tu duoi dang SMILES
    prompt = f"""
    [SYSTEM: ROLE]
    Bạn là một Công cụ tạo cấu trúc hóa học (SMILES Generator). 
    KHÔNG PHẢI là trợ lý lập trình. KHÔNG được viết code Python. 

    [TASK]
    Dựa trên các SMILES mồi: {seeds}
    Và mục tiêu: {objective}
    - Hãy tạo ra 20-50 phân tử SMILES mới có tiềm năng. ĐƠN GIẢN (dưới 15 nguyên tử).
    - Carbon (C) chỉ có tối đa 4 hóa trị. KHÔNG tạo Carbon 5 hóa trị.
    - Đảm bảo mọi vòng (ring) đều được đóng đúng số (VD: c1ccccc1).
    - KHÔNG viết số dư thừa ở cuối chuỗi.
    - Cấu trúc ĐƠN GIẢN, ưu tiên các nhóm chức cơ bản (OH, NH2, COOH).
    
    [OUTPUT FORMAT - BẮT BUỘC]
    Chỉ trả về duy nhất một mảng JSON chứa các chuỗi SMILES.
    Ví dụ: ["CCO", "c1ccccc1", "CC(=O)O"]
    KHÔNG giải thích. KHÔNG viết ```python. KHÔNG nói lời chào.
    """

    # Goi LLM de tao phan tu moi
    response = model.invoke(prompt)
    content = response.content

    new_candidates = []

    print(f"\n--- [GENERATOR AGENT] ---\nĐang tạo các phân tử ứng viên mới dựa trên các phân tử ban đầu...\n")
    print(f"\n--- [GENERATOR AGENT OUTPUT] ---\n{content[:200]}...\n------------------------\n")

    try:
        match = re.search(r'\[.*\]', content, re.DOTALL)

        if match:
            smiles_list = json.loads(match.group())
        else:
            smiles_list = re.findall(r'[A-Za-z0-9@\(\)\+=\-\[\]#/\\]+', content)
        
        new_candidates = [{"smiles": s, "round": state["current_round"]} for s in smiles_list[:50]]

        return {
            "candidates": new_candidates,
            "logs": [f"Generator: Đã đề xuất {len(new_candidates)} ứng viên mới."]
        }
    except Exception as e:
        return {"logs": [f"Generator Error: Không thể parse SMILES - {str(e)}"]}