from io import BytesIO
from openpyxl import Workbook

from app.domains.exports.schema import ShiftExportRow


class ExcelExporter:

    @staticmethod
    def export(rows: list[ShiftExportRow]) -> bytes:
        """
        Excelファイルを生成してbytesで返す
        """

        wb = Workbook()
        ws = wb.active
        ws.title = "Shift Export"

        # ヘッダー
        ws.append([
            "日付",
            "シフトID",
            "ユーザーID",
            "名前",
            "自動割当",
            "確定",
            "必要人数",
        ])

        # データ
        for r in rows:
            ws.append([
                r.date,
                r.slot_id,
                r.user_id,
                r.user_name,
                r.is_auto,
                r.is_confirmed,
                r.required_staff_count,
            ])

        buffer = BytesIO()
        wb.save(buffer)
        buffer.seek(0)

        return buffer.getvalue()