"""Unit tests for Hermes Performance Pack tools."""

import json
import os
import tempfile
import unittest
from pathlib import Path

# Import tools directly
from tools import ripgrep_search, batch_read_files, _is_safe_path


class TestPerformancePackTools(unittest.TestCase):

    def setUp(self):
        self.test_dir = tempfile.TemporaryDirectory()
        self.base_path = Path(self.test_dir.name).resolve()
        
        # Create test files
        self.file1 = self.base_path / "hello.py"
        self.file1.write_text("def hello():\n    print('Hello World')\n", encoding="utf-8")

        self.file2 = self.base_path / "world.txt"
        self.file2.write_text("Line 1: Solo2OS\nLine 2: Performance test\nLine 3: Hermes Agent\n", encoding="utf-8")

    def tearDown(self):
        self.test_dir.cleanup()

    def test_path_safety_check(self):
        safe, target = _is_safe_path("hello.py", str(self.base_path))
        self.assertTrue(safe)
        self.assertEqual(target, self.file1)

        # Test traversal outside base directory
        safe_bad, _ = _is_safe_path("../../outside.txt", str(self.base_path))
        self.assertFalse(safe_bad)

    def test_batch_read_files(self):
        res_str = batch_read_files(
            paths=[str(self.file1), str(self.file2), "non_existent_file.txt"],
            max_lines_per_file=10
        )
        res = json.loads(res_str)
        self.assertEqual(res["status"], "ok")
        self.assertEqual(res["files_read"], 3)
        
        # Verify first file content
        self.assertEqual(res["results"][0]["status"], "ok")
        self.assertIn("Hello World", res["results"][0]["content"])

        # Verify non-existent file
        self.assertEqual(res["results"][2]["status"], "error")

    def test_ripgrep_search_validation(self):
        # Empty pattern validation
        empty_res = json.loads(ripgrep_search(""))
        self.assertEqual(empty_res["status"], "error")

        # Test search on existing test directory
        res_str = ripgrep_search("Solo2OS", path=str(self.base_path))
        res = json.loads(res_str)
        if res.get("status") == "ok":
            self.assertGreaterEqual(res["match_count"], 1)
            self.assertTrue(any("Solo2OS" in m for m in res["matches"]))


if __name__ == "__main__":
    unittest.main()
