# app/agents/graph.py

from langgraph.graph import StateGraph, END
from app.agents.nodes.planner import planner_node
from app.agents.nodes.validator import validator_node
from app.agents.nodes.ranker import ranker_node
from app.agents.nodes.generator import generator_node
from app.agents.state import MoleculeState

def create_molecule_graph():
    # Khoi tao do thi trang thai
    workflow = StateGraph(MoleculeState)

    # Them cac nut vao do thi
    workflow.add_node("planner", planner_node)
    workflow.add_node("validator", validator_node)
    workflow.add_node("ranker", ranker_node)
    workflow.add_node("generator", generator_node)

    # Thiet lap cac canh giua cac nut
    workflow.set_entry_point("planner")
    workflow.add_edge("planner", "generator")
    workflow.add_edge("generator", "validator")
    workflow.add_edge("validator", "ranker")

    # Them logic vong lap: Neu status == 'running', quay lai generator thuc hien vong lap tiep theo, nguoc lai ket thuc
    workflow.add_conditional_edges(
        'ranker',
        lambda state: 'continue' if state['status'] == 'running' else 'end',
        {
            'continue': 'generator',
            'end': END
        }
    )

    return workflow.compile()

molecule_app = create_molecule_graph()