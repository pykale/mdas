"""Integration checks for the actual external worker; requires its prepared Python 3.12 environment."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("mdas_runner", ROOT / "colab/run_notebooks.py")
runner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)


class Worker(unittest.TestCase):
    def test_failed_cell_stops_execution_and_preserves_source(self):
        import nbformat
        from nbclient.exceptions import CellExecutionError
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "notebooks/MDAS/cancer/classification.ipynb"
            source.parent.mkdir(parents=True)
            notebook = nbformat.v4.new_notebook(cells=[
                nbformat.v4.new_code_cell("from pathlib import Path; assert Path.cwd().name == 'cancer'"),
                nbformat.v4.new_code_cell("raise ValueError('intentional regression-test failure')"),
                nbformat.v4.new_code_cell("raise AssertionError('must never run')"),
            ])
            nbformat.write(notebook, source)
            before = source.read_bytes()
            (root / "outputs").mkdir()
            (root / "outputs/classification.html").write_text("stale success", encoding="utf-8")
            with self.assertRaises(CellExecutionError):
                runner.execute("classification", root, root / "outputs", 30)
            self.assertEqual(source.read_bytes(), before)
            self.assertFalse((root / "outputs/classification.html").exists())
            result = json.loads((root / "outputs/classification.execution.json").read_text(encoding="utf-8"))
            self.assertEqual(result["status"], "failed")
            self.assertTrue(result["source_unchanged"])
            executed = nbformat.read(root / "outputs/classification.executed.ipynb", as_version=4)
            self.assertIsNone(executed.cells[-1].execution_count)


if __name__ == "__main__":
    unittest.main()
