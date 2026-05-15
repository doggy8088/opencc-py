import subprocess
import sys
import tempfile
from pathlib import Path


def main() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        input_path = Path(temp_dir) / "input.txt"
        output_path = Path(temp_dir) / "output.txt"

        input_path.write_text("默认用户界面支持数据库和网络请求。", encoding="utf-8")

        subprocess.run(
            [
                sys.executable,
                "-m",
                "opencc_py.cli",
                str(input_path),
                "cn",
                "tw2",
                "-o",
                str(output_path),
            ],
            check=True,
        )

        print(output_path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
