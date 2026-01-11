# app/agents/nodes/ranker.py

from langchain_groq import ChatGroq
from app.core.config import settings
from app.agents.state import MoleculeState

# Khoi tao model Llama3 70B cho Ranker Agent
model = ChatGroq(
    api_key = settings.GROQ_API_KEY,
    model_name = settings.RANKER_MODEL,
)

def ranker_node(state: MoleculeState):
    """
    Ranker Agent: Lua chon cac ung vien hang dau va chuan bi ket qua
    """

    candidates = state['candidates']
    objective = state['objectives']
    valid_candidates = [c for c in candidates if c.get('valid')]

    print(f"\n--- [RANKER AGENT] ---\nĐang xếp hạng {len(valid_candidates)} ứng viên...\n")

    if not valid_candidates:
        return {
            "status": "failed",
            "logs": ["Ranker: Không tìm thấy ứng viên hợp lệ nào để xếp hạng."]
        }
    
    # Sap xep cac ung vien theo chi so giam dan
    sorted_candidates = sorted(valid_candidates, key=lambda x: x['score'], reverse=True)

    # Lay Top K ung vien tot nhat (K = 5)
    top_k = sorted_candidates[:5] 

    # Goi LLM de tao bao cao ket qua
    best_molecule = top_k[0]
    prompt = f"""
    Dựa trên mục tiêu: {objective}
    Phân tử tốt nhất hiện tại có các chỉ số: 
    QED: {best_molecule['qed']}, MW: {best_molecule['mw']}, LogP: {best_molecule['logp']}, HBD: {best_molecule['hbd']}, HBA: {best_molecule['hba']}, TPSA: {best_molecule['tpsa']}, Vi phạm: {best_molecule['violations']}.
    Hãy viết một câu nhận xét chuyên môn ngắn gọn về phân tử này.
    """

    analysis = model.invoke(prompt).content

    print(f"\n--- [RANKER AGENT OUTPUT] ---\nPhân tử có score cao nhất là: {best_molecule['smiles']}\nNhận xét: {analysis}\n------------------------\n")

    # Quyet dinh trang thai tiep theo
    new_status = 'compelete' if state['current_round'] >= state['max_rounds'] else 'running'

    if new_status == 'compelete':
        print(f"\n--- [SYSTEM] ---\nĐã đạt số vòng tối đa. Kết thúc quá trình.\n")
    else:
        print(f"\n--- [SYSTEM] ---\nTiếp tục sang vòng {state['current_round'] + 1}\n")

    return {
        "top_candidates": top_k,
        "status": new_status,
        "current_round": state["current_round"] + 1, 
        "logs": [f"Ranker: Đã chọn Top {len(top_k)} ứng viên. Nhận xét: {analysis}."]
    }
    