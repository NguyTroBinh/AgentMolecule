# app/core/celery_app.py

from celery import Celery
from app.core.config import settings
from app.agents.graph import molecule_app
from app.db.session import SessionLocal 
from app.db.models import MoleculeRun, MoleculeResult

celery_app = Celery(
    'tasks',
    broker = settings.REDIS_URL,
    backend = settings.REDIS_URL,
)

@celery_app.task(name='run_molecule_discovery')
def run_molecule_discovery_task(run_id: str, objective: str, seeds: list, filters: dict):
    """ Tac vu chay LangGraph bat dong bo """
    # Khoi tao trang thai ban dau cho LangGraph
    initial_state = {
        'objectives': objective,
        'seeds': seeds,
        'filters': filters,
        'current_round': 1,
        'max_rounds': filters.get("max_rounds", 3),
        'candidates': [],
        'logs': [f"Hệ thống: Bắt đầu lượt chạy {run_id}"],
        'top_candidates': [],
        'status': 'running',
    }

    # Thuc thi do thi: Planner -> Generator -> Validator -> Ranker
    final_result = molecule_app.invoke(initial_state)

    # Cap nhat ket qua vao co so du lieu
    with SessionLocal() as session:
        run = session.get(MoleculeRun, run_id)
        if run:
            run.status = 'COMPLETED'
            run.logs = final_result['logs']
            session.add(run)

            # Luu ket qua ung vien hang dau
            for candidate in final_result["top_candidates"]:
                mol = MoleculeResult(run_id=run_id, **candidate)
                session.add(mol)
            session.commit()