# app/api/v1/endpoints.py

from fastapi import APIRouter, HTTPException, BackgroundTasks
from uuid import uuid4
from app.db.models import MoleculeResult, MoleculeRun
from app.db.session import SessionLocal
from app.core.celery_app import run_molecule_discovery_task

router = APIRouter()

@router.post('/runs')
async def start_run(objective: str, seeds: list[str], filters: dict):
    """ API bat dau mot luot chay moi """
    run_id = str(uuid4())

    # Tao ban ghi RUN trong DB voi trang thai PENDING
    with SessionLocal() as session:
        new_run = MoleculeRun(id = run_id, objective = objective, filters = filters)
        session.add(new_run)
        session.commit()

    # Day vao hang doi Celery de thuc thi bat dong bo
    run_molecule_discovery_task.delay(run_id, objective, seeds, filters)

    return {'run_id': run_id, 'message': 'Lượt chạy đã được bắt đầu thành công.'}

@router.get('/runs/{run_id}/status')
async def get_status(run_id: str):
    """ Kiem tra trang thai cua mot luot chay """

    with SessionLocal() as session:
        run = session.get(MoleculeRun, run_id)

        if not run:
            raise HTTPException(status_code=404, detail="Không tìm thấy Run ID.")
        return {'status': run.status, 'current_round': run.current_round}
    
@router.get('/runs/{run_id}/results')
async def get_results(run_id: str):
    """ Lay danh sach cac phan tu tot nhat cua mot luot chay """

    with SessionLocal() as session:
        results = session.query(MoleculeResult).filter(MoleculeResult.run_id == run_id).all()
        return results