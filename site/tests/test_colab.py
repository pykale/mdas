"""Direct Colab copy preservation and setup-cell regression checks."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import unittest
from unittest.mock import patch, MagicMock

ROOT = Path(__file__).resolve().parents[2]
CANCER = ROOT / "notebooks/MDAS/cancer"
spec = importlib.util.spec_from_file_location("mdas_sync_colab", ROOT / "site/sync_colab.py")
sync = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sync)


def setup_source(name):
    return "".join(json.loads((CANCER / f"{name}_colab.ipynb").read_text(encoding="utf-8"))["cells"][1]["source"])


def run_setup(name, *, python=(3, 12), gpu=False, returncode=0, install=None):
    """Run a copy's setup cell with pip, downloads and imports replaced; return the mocks."""
    install = install or MagicMock(return_value=MagicMock(returncode=returncode, stdout="pip out", stderr="pip err"))
    fetch = MagicMock()
    torch = MagicMock(__version__="2.6.0+cpu")
    torch.cuda.is_available.return_value = gpu
    with patch.object(sys, "version_info", python), patch("subprocess.run", install), \
            patch("urllib.request.urlretrieve", fetch), patch("shutil.which", return_value="/usr/bin/nvidia-smi" if gpu else None), \
            patch.dict(sys.modules, {"torch": torch, "kalecancer": MagicMock()}), patch("builtins.print"):
        exec(setup_source(name), {})
    return install, fetch


class DirectColab(unittest.TestCase):
    def test_original_payloads_and_copies(self):
        for name in ("classification_showcase", "survival_showcase"):
            path = f"notebooks/MDAS/cancer/{name}.ipynb"
            authored = subprocess.check_output(["git", "show", f"HEAD:{path}"], cwd=ROOT)
            self.assertEqual((ROOT / path).read_bytes().replace(b"\r\n", b"\n"), authored.replace(b"\r\n", b"\n"))
        for name in sync.NOTEBOOKS:
            original = json.loads((CANCER / f"{name}.ipynb").read_text(encoding="utf-8"))
            direct = json.loads((CANCER / f"{name}_colab.ipynb").read_text(encoding="utf-8"))
            self.assertEqual(direct["cells"][2:], original["cells"])  # includes source, metadata and saved outputs
            self.assertEqual({k: v for k, v in direct.items() if k != "cells"}, {k: v for k, v in original.items() if k != "cells"})
            self.assertIn("Before you start", "".join(direct["cells"][0]["source"]))
            compile(setup_source(name), "setup cell", "exec")
        subprocess.run([sys.executable, str(ROOT / "site/sync_colab.py"), "--check"], check=True)

    def test_page_targets_and_helpers(self):
        spec = importlib.util.spec_from_file_location("mdas_site_conf", ROOT / "site/conf.py")
        conf = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(conf)
        self.assertFalse(conf.html_permalinks)
        for docname, (_, source_path) in conf.NOTEBOOKS.items():
            source = json.loads((ROOT / source_path).read_text(encoding="utf-8"))
            rendered = [json.dumps(source)]
            conf.prepare_notebook(None, docname, rendered)
            intro = json.loads(rendered[0])["cells"][0]["source"]
            target = source_path.replace(".ipynb", "_colab.ipynb")
            self.assertIn(f'href="https://colab.research.google.com/github/pykale/mdas/blob/main/{target}"', intro)
            self.assertTrue((ROOT / target).is_file())
            self.assertNotIn("live-coding-notebook", intro)
            self.assertNotIn('onclick="mdasLaunchInteractive()"', intro)  # Colab is the only route
            name = Path(source_path).stem
            self.assertIn(name, sync.NOTEBOOKS)
            for helper in sync.NOTEBOOKS[name]["helpers"]:
                self.assertTrue((CANCER / helper).is_file())

    def test_unsupported_python_stops_before_installing(self):
        with self.assertRaisesRegex(SystemExit, "Python 3.12"):
            run_setup("hancock_questions", python=(3, 13))
        install = MagicMock()
        with self.assertRaises(SystemExit):
            run_setup("classification_showcase", python=(3, 13), install=install)
        install.assert_not_called()

    def test_installs_cpu_pytorch_and_downloads_each_notebooks_helpers(self):
        for name, config in sync.NOTEBOOKS.items():
            install, fetch = run_setup(name)
            command = install.call_args.args[0]
            self.assertIn(sync.KALECANCER, command)
            self.assertIn("torch==2.6.0+cpu", command)
            self.assertIn("https://download.pytorch.org/whl/cpu", command)
            self.assertEqual([call.args[1] for call in fetch.call_args_list], config["helpers"])
            for call in fetch.call_args_list:
                self.assertEqual(call.args[0], sync.HELPER_URL + call.args[1])

    def test_only_hancock_installs_gpu_pytorch_on_a_gpu_runtime(self):
        install, _ = run_setup("hancock_questions", gpu=True)
        command = install.call_args.args[0]
        self.assertIn("torch==2.6.0", command)
        self.assertNotIn("https://download.pytorch.org/whl/cpu", command)
        install, _ = run_setup("survival_showcase", gpu=True)  # The showcases train on the CPU anyway
        self.assertIn("torch==2.6.0+cpu", install.call_args.args[0])

    def test_failed_installation_stops_and_shows_pip_output(self):
        with self.assertRaisesRegex(SystemExit, "Installation failed"):
            run_setup("survival_showcase", returncode=1)

    def test_buttons_have_white_text_in_all_states_and_accessible_focus(self):
        css = (ROOT / "site/_static/mdas-notebooks.css").read_text(encoding="utf-8")
        for state in (":link", ":visited", ":hover", ":focus-visible", ":active", ":disabled"):
            self.assertIn(".mdas-execution-button" + state, css)
        self.assertGreaterEqual(css.count("color: #FFFFFF !important"), 4)
        self.assertIn("outline: 3px", css)
        self.assertIn("@media (max-width: 480px)", css)
        # WCAG relative luminance: white on each authored blue exceeds 4.5:1.
        for colour in ("0b5ed7", "084bb5", "063b8f", "3d5f90"):
            values = [int(colour[i:i+2], 16) / 255 for i in (0, 2, 4)]
            values = [v / 12.92 if v <= .04045 else ((v + .055) / 1.055) ** 2.4 for v in values]
            lum = sum(v * w for v, w in zip(values, (.2126, .7152, .0722)))
            self.assertGreater(1.05 / (lum + .05), 4.5)


if __name__ == "__main__":
    unittest.main()
