from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse, Response
from sqlalchemy.orm import Session
from io import BytesIO, StringIO

from app.db.session import get_db
from app.domains.exports.service import ShiftExportService
from app.domains.exports.csv_exporter import CSVExporter
from app.domains.exports.excel_exporter import ExcelExporter


router = APIRouter(prefix="/exports", tags=["exports"])


@router.get("/shifts/csv")
async def export_shifts_csv(db: Session = Depends(get_db)):
    rows = await ShiftExportService.build_export_rows(db)

    csv_text = CSVExporter.export(rows)

    return Response(
        content=csv_text,
        media_type="text/csv",
        headers={
            "Content-Disposition": "attachment; filename=shifts.csv"
        },
    )


@router.get("/shifts/excel")
async def export_shifts_excel(db: Session = Depends(get_db)):
    rows = await ShiftExportService.build_export_rows(db)

    excel_bytes = ExcelExporter.export(rows)

    buffer = BytesIO(excel_bytes)

    return StreamingResponse(
        buffer,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={
            "Content-Disposition": "attachment; filename=shifts.xlsx"
        },
    )