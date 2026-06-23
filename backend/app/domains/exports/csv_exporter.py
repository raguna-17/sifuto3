import csv
from io import StringIO

from app.domains.exports.schema import ShiftExportRow


class CSVExporter:

    @staticmethod
    def export(rows: list[ShiftExportRow]) -> str:
        """
        CSV文字列を生成
        """

        output = StringIO()
        writer = csv.writer(output)

        # ヘッダー
        writer.writerow([
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
            writer.writerow([
                r.date,
                r.slot_id,
                r.user_id,
                r.user_name,
                r.is_auto,
                r.is_confirmed,
                r.required_staff_count,
            ])

        return output.getvalue()