# app/mcp/tools.py

from typing import Dict, Any
from rdkit import Chem
from rdkit.Chem import Descriptors, QED

def analyze_molecule(smiles: str) -> Dict[str, Any]:
    # Phan tich ma SMILES va tra ve chi so hoa hoc
    mol = Chem.MolFromSmiles(smiles)
    if not mol:
        return {"valid": False, "smiles": smiles}
    
    # Tinh toan cac chi so hoa hoc
    properties = {
        "valid": True,
        "smiles": Chem.MolToSmiles(mol),
        "mw": Descriptors.MolWt(mol),               # Molecular Weight
        "logp": Descriptors.MolLogP(mol),           # cLogP
        "hbd": Descriptors.NumHDonors(mol),         # H-Bond Donors
        "hba": Descriptors.NumHAcceptors(mol),      # H-Bond Acceptors
        "tpsa": Descriptors.TPSA(mol),              # Polar Surface Area
        "rotb": Descriptors.NumRotatableBonds(mol), # Rotatable Bonds
        "qed": QED.qed(mol)                         # QED score
    }
    return properties

def check_filters(props: Dict[str, Any], filters: Dict[str, Any]) -> Dict[str, Any]:
    # Su dung bo loc de danh gia phu hop cua phan tu hoa hoc
    violations = 0  # So loi vi pham
    if props["mw"] > filters.get("mw", 500): violations += 1
    if props["logp"] > filters.get("logp", 5): violations += 1
    if props["hbd"] > filters.get("hbd", 5): violations += 1
    if props["hba"] > filters.get("hba", 10): violations += 1
    if props["tpsa"] > filters.get("tpsa", 140): violations += 1
    
    props["violations"] = violations
    # Cong thuc: QED - 0.1 * violations
    props["score"] = props["qed"] - (0.1 * violations)
    return props