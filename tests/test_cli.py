import contextlib
import io
import tempfile
import unittest
from pathlib import Path

from opencc_py.cli import main


class CliTests(unittest.TestCase):
    def test_cli_prints_to_stdout_by_default(self):
        with tempfile.TemporaryDirectory() as tmp:
            input_path = Path(tmp) / "input.txt"
            input_path.write_text("汉语", encoding="utf-8")
            stdout = io.StringIO()

            with contextlib.redirect_stdout(stdout):
                exit_code = main([str(input_path), "cn", "tw2"])

        self.assertEqual(exit_code, 0)
        self.assertEqual(stdout.getvalue(), "漢語\n")

    def test_cli_writes_output_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            input_path = Path(tmp) / "input.txt"
            output_path = Path(tmp) / "output.txt"
            input_path.write_text("汉语", encoding="utf-8")

            exit_code = main([str(input_path), "cn", "tw2", "--output", str(output_path)])

            self.assertEqual(exit_code, 0)
            self.assertEqual(input_path.read_text(encoding="utf-8"), "汉语")
            self.assertEqual(output_path.read_text(encoding="utf-8"), "漢語")

    def test_cli_writes_in_place(self):
        with tempfile.TemporaryDirectory() as tmp:
            input_path = Path(tmp) / "input.txt"
            input_path.write_text("汉语", encoding="utf-8")

            exit_code = main([str(input_path), "cn", "tw2", "--in-place"])

            self.assertEqual(exit_code, 0)
            self.assertEqual(input_path.read_text(encoding="utf-8"), "漢語")

    def test_cli_reports_conversion_errors(self):
        with tempfile.TemporaryDirectory() as tmp:
            input_path = Path(tmp) / "input.txt"
            input_path.write_text("汉语", encoding="utf-8")
            stderr = io.StringIO()

            with contextlib.redirect_stderr(stderr):
                exit_code = main([str(input_path), "missing", "tw2"])

        self.assertEqual(exit_code, 1)
        self.assertIn("Unknown locale `missing`", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
