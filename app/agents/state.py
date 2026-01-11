# app/agents/state.py

from typing import Annotated, List, Dict, Any, Union
from typing_extensions import TypedDict
import operator

class MoleculeState(TypedDict):
    # Input
    objectives: str             # Muc tieu thiet ke
    seeds: List[str]            # Cac SMILES ban dau
    filters: Dict[str, Any]     # Cac bo loc

    current_round: int          # Vong hien tai
    max_rounds: int             # So vong toi da

    candidates: Annotated[List[Dict[str, Any]], operator.add] 
    logs: Annotated[List[str], operator.add]

    # Output
    top_candidates: List[Dict[str, Any]]  # Cac ung vien hang dau
    status: str
    