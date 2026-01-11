# app/agents/nodes/validator.py

from app.mcp.tools import analyze_molecule, check_filters
from app.agents.state import MoleculeState

def validator_node(state: MoleculeState):
    """
    Validator: Su dung RDKit de danh gia cac ung vien.
    """
    # Lay nhung ung vien moi nhat
    new_candidates = [c for c in state["candidates"] if "valid" not in c]

    if not new_candidates:
        return {"logs": ["Validator: Không nhận được ứng viên nào từ Generator."]}
    
    processed_candidates = []
    
    passed_count = 0
    failed_count = 0

    max_v = state['filters'].get('max_violations', 1)
    
    for candidate in new_candidates:
        # Tinh toan chi so hoa hoc
        props = analyze_molecule(candidate["smiles"])

        if props["valid"]:
            # Ap dung bo loc de kiem tra
            result = check_filters(props, state["filters"])
            
            if result['violations'] <= max_v:
                processed_candidates.append(result)
                passed_count += 1
            else: 
                failed_count += 1
        else:
            failed_count += 1

    print("\n--- [VALIDATOR AGENT OUTPUT] ---\n")

    for processed in processed_candidates:
        print(f"Validated: SMILES={processed['smiles']}, Violations={processed['violations']}\n")
    print(f"Validator Summary: Passed={passed_count}, Failed={failed_count}\n")
            
    return {
        "candidates": processed_candidates, 
        "logs": [f"Validator: Kiểm tra xong. Đạt: {passed_count}, Không đạt: {failed_count}."]
    }