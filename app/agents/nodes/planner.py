# app/agents/nodes/planner.py

import re
import json
from langchain_groq import ChatGroq
from app.core.config import settings
from app.agents.state import MoleculeState

# Khoi tao model Llama3 70B cho Planner Agent
model = ChatGroq(
    api_key = settings.GROQ_API_KEY,
    model_name = settings.PLANNER_MODEL,
)

def planner_node(state: MoleculeState):
    """
    Planner Agent: Khoi tao so vong, so ung vien moi vong, cac rang buoc, ...
    """
    objective = state['objectives']

    # Prompt yeu cau LLM phan tich muc tieu va thiet lap ke hoach
    prompt = f"""
    Bạn là một chuyên gia lập kế hoạch AI trong dược phẩm.
    Mục tiêu khoa học: {objective}
    
    Nhiệm vụ: Hãy thiết lập thông số kỹ thuật cho hệ thống Multi-Agent.
    
    Trả về định dạng JSON duy nhất gồm:
    - max_rounds (int: từ 1 đến 3)
    - candidates_per_round (int: từ 20 đến 50)
    - strategy (string: nhận xét ngắn gọn về hướng tiếp cận)
    
    Lưu ý quan trọng: Chỉ trả về JSON, không giải thích gì thêm.
    """

    # Goi LLM de tao ke hoach
    response = model.invoke(prompt)
    content = response.content

    print(f"\n--- [PLANNER AGENT] ---\nĐang phân tích mục tiêu và thiết lập kế hoạch...\n")
    print(f"\n--- [PLANNER AGENT OUTPUT] ---\n{content}\n------------------------\n")

    try:
        match = re.search(r'\{.*\}', content, re.DOTALL)
        plan = json.loads(match.group()) if match else {"max_rounds": 3, "candidates_per_round": 50}
        
        return {
            "current_round": 1,
            "max_rounds": plan.get("max_rounds", 3),
            "logs": [f"Planner: Chiến lược thiết lập - {plan.get('strategy', 'Mặc định')}. Chạy {plan['max_rounds']} vòng."]
        }
    except Exception as e:
        return {
            "current_round": 1,
            "max_rounds": 3,
            "logs": [f"Planner Error: Lỗi phân tích kế hoạch ({str(e)}). Sử dụng cấu hình mặc định."]
        }