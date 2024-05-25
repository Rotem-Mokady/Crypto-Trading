import os
import pandas as pd

from typing import Dict, Union, Any, List


class Processor:

    def __init__(self):

        self.dir = 'logs'
        self.file_Type = 'txt'
        self.log_type = "INFO"

        self.exported_filename = "logs_data.xlsx"

    def _line_generator(self, line: str) -> Union[Dict[str, Any], None]:
        parts = line.strip().split(' - ')

        if len(parts) != 4:
            return
        if parts[1] != self.log_type:
            return

        trading_time, _ = parts[0].split(',')
        candle_time, action_type = parts[2], parts[3]

        return {"trading_time": trading_time, "candle_time": candle_time, "action_type": action_type}

    def _lines_generator(self, lines: List[str]) -> pd.DataFrame:
        rows = []

        for line in lines:
            data = self._line_generator(line)

            if data:
                rows.append(data)

        return pd.DataFrame(rows)

    def _file_generator(self, filename: str) -> Union[pd.DataFrame, None]:
        if not filename.endswith(f'.{self.log_type}'):  # Process only .txt files
            return

        file_path = os.path.join(self.dir, filename)
        with open(file_path, 'r') as file:
            lines = file.readlines()

        df = self._lines_generator(lines=lines)
        return df

    def _run(self) -> pd.DataFrame:
        files = os.listdir(self.dir)
        files_data = []

        # Iterate over each file in the directory
        for filename in files:
            file_data = self._file_generator(filename)

            if file_data:
                files_data.append(file_data)

        df = pd.concat(files_data, ignore_index=True)
        return df

    def run(self) -> None:
        final_df = self._run()
        final_df.to_excel(self.exported_filename)
