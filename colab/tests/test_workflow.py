"""External workflow regression tests; run with python -m unittest discover -s colab/tests."""
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("mdas_environment", ROOT / "colab/environment.py")
environment = importlib.util.module_from_spec(spec)
spec.loader.exec_module(environment)


class Preparation(unittest.TestCase):
    def test_unsupported_python_fails_before_install_or_environment_creation(self):
        with patch.object(environment.sys, "version_info", (3, 13)), patch.object(environment.subprocess, "run") as run:
            with self.assertRaisesRegex(RuntimeError, "does not change the Python version"):
                environment.prepare()
            run.assert_not_called()

    def test_repeat_preparation_reuses_matching_installation_but_checks_it(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / ".binder").mkdir()
            (root / "colab").mkdir()
            (root / ".binder/requirements.txt").write_text("research-lock", encoding="utf-8")
            (root / "colab/requirements.txt").write_text("runner-lock", encoding="utf-8")
            env = root / ".venv/colab"
            python = environment.environment_python(env)
            python.parent.mkdir(parents=True)
            python.touch()
            marker = env / ".mdas-lock.json"
            fingerprint = hashlib.sha256(b"research-lock\nrunner-lock").hexdigest()
            marker.write_text(json.dumps({"lock": fingerprint}), encoding="utf-8")
            with patch.object(environment, "ROOT", root), patch.object(environment, "ENV", env), \
                 patch.object(environment, "environment_python", return_value=python), \
                 patch.object(environment.sys, "version_info", (3, 12)), \
                 patch.object(environment.subprocess, "run") as run:
                self.assertEqual(environment.prepare(), python)
                self.assertEqual(run.call_count, 2)  # pip check and actual imports, no install
                self.assertEqual(run.call_args_list[0].args[0][-1], "check")

    def test_four_scientific_notebooks_match_the_authored_git_payloads(self):
        import subprocess
        for name in ("classification", "survival", "classification_blank", "survival_blank"):
            path = f"notebooks/MDAS/cancer/{name}.ipynb"
            authored = subprocess.check_output(["git", "show", f"HEAD:{path}"], cwd=ROOT)
            self.assertEqual((ROOT / path).read_bytes().replace(b"\r\n", b"\n"), authored.replace(b"\r\n", b"\n"), path)

    def test_separate_notebook_and_requirements_validate(self):
        notebook = json.loads((ROOT / "colab/prepare_colab.ipynb").read_text(encoding="utf-8"))
        for cell in notebook["cells"]:
            if cell["cell_type"] == "code":
                compile("".join(cell["source"]), "preparation cell", "exec")
        requirements = (ROOT / "colab/requirements.txt").read_text(encoding="utf-8")
        self.assertIn("-r ../.binder/requirements.txt", requirements)
        self.assertNotIn("ignore-requires-python", requirements)
        self.assertNotIn("no-deps", requirements)


if __name__ == "__main__":
    unittest.main()
