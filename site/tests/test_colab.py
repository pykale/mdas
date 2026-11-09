"""Direct Colab copy preservation, bootstrap and runtime-safety regression checks."""
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch, MagicMock

ROOT = Path(__file__).resolve().parents[2]
CANCER = ROOT / "notebooks/MDAS/cancer"
spec = importlib.util.spec_from_file_location("mdas_colab_setup", CANCER / "colab_setup.py")
setup = importlib.util.module_from_spec(spec)
spec.loader.exec_module(setup)


class DirectColab(unittest.TestCase):
    def test_original_payloads_and_copies(self):
        for name in ("classification", "survival", "classification_blank", "survival_blank", "classification_showcase"):
            path = f"notebooks/MDAS/cancer/{name}.ipynb"
            authored = subprocess.check_output(["git", "show", f"HEAD:{path}"], cwd=ROOT)
            self.assertEqual((ROOT / path).read_bytes().replace(b"\r\n", b"\n"), authored.replace(b"\r\n", b"\n"))
        for name in ("classification", "survival", "classification_showcase", "survival_showcase"):
            original = json.loads((CANCER / f"{name}.ipynb").read_text(encoding="utf-8"))
            direct = json.loads((CANCER / f"{name}_colab.ipynb").read_text(encoding="utf-8"))
            self.assertEqual(direct["cells"][2:], original["cells"])  # includes source, metadata and saved outputs
            self.assertEqual({k: v for k, v in direct.items() if k != "cells"}, {k: v for k, v in original.items() if k != "cells"})
            self.assertIn("Google Colab Environment Setup", "".join(direct["cells"][0]["source"]))
            compile("".join(direct["cells"][1]["source"]), "setup cell", "exec")
        subprocess.run([sys.executable, str(ROOT / "site/sync_colab.py"), "--check"], check=True)

    def test_showcase_bootstrap_and_page_targets(self):
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
            self.assertNotIn("(live-coding-notebook)=", intro)
            if "_showcase" in source_path:
                self.assertNotIn("Binder unavailable", intro)
                self.assertIn('onclick="mdasLaunchInteractive()"', intro)
                bootstrap = "".join(json.loads((ROOT / target).read_text(encoding="utf-8"))["cells"][1]["source"])
                for helper in ("synthetic_showcase_data.py", "synthetic_data_generation.py"):
                    digest = hashlib.sha256((CANCER / helper).read_bytes().replace(b"\r\n", b"\n")).hexdigest()
                    self.assertIn(digest, bootstrap)
                    self.assertIn(helper, bootstrap)
                self.assertIn("showcase=True", bootstrap)

    def test_unsupported_python_does_not_install_or_download(self):
        with patch.object(setup.sys, "version_info", (3, 13)), patch.object(setup.subprocess, "run") as install, patch.object(setup, "urlopen") as fetch:
            with self.assertRaisesRegex(RuntimeError, "2026.07"):
                setup.prepare()
            install.assert_not_called()
            fetch.assert_not_called()

    def test_already_imported_different_binary_libraries_require_restart(self):
        with self.assertRaisesRegex(RuntimeError, "Restart session"):
            setup._check_loaded({"torch": "2.11.0", "numpy": "2.0.2"}, {"torch": "2.6.0+cpu", "numpy": "2.0.2"})
        setup._check_loaded({"torch": "2.6.0+cpu"}, {"torch": "2.6.0+cpu"})

    def test_previously_loaded_hub_requires_restart_after_downgrade(self):
        hub = MagicMock(__version__="2.3.0")
        with patch.dict(sys.modules, {"huggingface_hub": hub}):
            before = setup._loaded_versions()
        self.assertEqual(before["huggingface-hub"], "2.3.0")
        with self.assertRaisesRegex(RuntimeError, "huggingface-hub.*Restart session"):
            setup._check_loaded(before, {"huggingface-hub": "1.33.0"})
        setup._check_loaded({"huggingface-hub": "1.33.0"}, {"huggingface-hub": "1.33.0"})

    def test_colab_transformers_hub_requirement_is_checked_before_imports(self):
        def version(name):
            return "5.13.1" if name == "transformers" else hub_version
        with patch.object(setup.metadata, "requires", return_value=["huggingface-hub>=1.5.0,<2.0"]), \
             patch.object(setup.metadata, "version", side_effect=version):
            hub_version = "1.33.0"
            setup._check_transformers_hub()
            hub_version = "2.3.0"
            with self.assertRaisesRegex(RuntimeError, "Transformers 5.13.1.*Hub 2.3.0"):
                setup._check_transformers_hub()
        with patch.object(setup.metadata, "requires", side_effect=setup.metadata.PackageNotFoundError):
            setup._check_transformers_hub()  # Optional Transformers stays optional.

    def test_correct_alpha_version_from_wrong_git_commit_is_not_reused(self):
        with patch.object(setup.metadata, "version", return_value="2.0.2"), patch.object(setup.metadata, "distribution") as dist:
            dist.return_value.read_text.return_value = json.dumps({"vcs_info": {"commit_id": "wrong"}})
            self.assertFalse(setup._matches({"numpy": "2.0.2"}))
            dist.return_value.read_text.return_value = json.dumps({"vcs_info": {"commit_id": setup.CANCER_REF}})
            self.assertTrue(setup._matches({"numpy": "2.0.2"}))

    def test_companion_download_is_verified_cached_and_does_not_overwrite_existing_source(self):
        contents = (CANCER / "synthetic_data_generation.py").read_bytes().replace(b"\r\n", b"\n")
        self.assertEqual(hashlib.sha256(contents).hexdigest(), setup.DATA_SHA256)
        with tempfile.TemporaryDirectory() as tmp, patch.object(setup, "urlopen") as fetch:
            directory = Path(tmp)
            fetch.return_value.__enter__.return_value.read.return_value = contents
            setup._ensure_helper(directory)
            setup._ensure_helper(directory)
            fetch.assert_called_once()
            self.assertEqual((directory / "synthetic_data_generation.py").read_bytes(), contents)
        with tempfile.TemporaryDirectory() as tmp, patch.object(setup, "urlopen") as fetch:
            fetch.return_value.__enter__.return_value.read.return_value = b"bad download"
            with self.assertRaisesRegex(RuntimeError, "checksum"):
                setup._ensure_helper(Path(tmp))
            self.assertFalse((Path(tmp) / "synthetic_data_generation.py").exists())

    def test_fresh_bootstrap_downloads_verified_support_and_reuses_cache(self):
        bootstrap = "".join(json.loads((CANCER / "classification_showcase_colab.ipynb").read_text(encoding="utf-8"))["cells"][1]["source"])
        contents = {name: (CANCER / name).read_bytes().replace(b"\r\n", b"\n") for name in ("colab_setup.py", "colab-requirements.txt", "synthetic_data_generation.py", "synthetic_showcase_data.py")}
        prepare = MagicMock()
        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp) / "notebooks/MDAS/cancer"
            code = bootstrap.replace('/content/mdas-cancer/notebooks/MDAS/cancer', directory.as_posix())
            def response(request, **kwargs):
                item = MagicMock()
                # Exercise Windows CRLF downloads/caches against LF GitHub hashes.
                item.__enter__.return_value.read.return_value = contents[request.full_url.rsplit("/", 1)[-1]].replace(b"\n", b"\r\n")
                return item
            with patch("pathlib.Path.cwd", return_value=Path(tmp)), patch.object(sys, "version_info", (3, 12)), \
                 patch("urllib.request.urlopen", side_effect=response) as fetch, patch("runpy.run_path", return_value={"prepare": prepare}):
                exec(code, {})
                (directory / "colab_setup.py").write_bytes(contents["colab_setup.py"].replace(b"\n", b"\r\n"))
                exec(code, {})
                self.assertEqual(fetch.call_count, 4)
                self.assertEqual(prepare.call_count, 2)
                prepare.assert_called_with(directory, showcase=True)
                self.assertEqual((directory / "colab_setup.py").read_bytes().replace(b"\r\n", b"\n"), contents["colab_setup.py"])

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
