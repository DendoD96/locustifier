import filecmp
import os
import shutil
import unittest

from pydantic import ValidationError

from locustifier.controllers.code_generator import (
    GENERATED_FOLDER,
    CodeGenerator,
)


def are_folders_equal(folder1, folder2):
    def recursion(dcmp):
        if (
            len(dcmp.diff_files) > 0
            or len(dcmp.left_only) > 0
            or len(dcmp.right_only) > 0
        ):
            return False
        res = True
        for sub_dcmp in dcmp.subdirs.values():
            res &= recursion(sub_dcmp)
        return res

    dcmp = filecmp.dircmp(folder1, folder2)
    return recursion(dcmp)


class TestCodeGenerator(unittest.TestCase):
    # Necessary to print multiline test description.
    def shortDescription(self):
        return None

    def setUp(self):
        try:
            shutil.rmtree(GENERATED_FOLDER)
        except FileNotFoundError:
            pass
        except Exception as e:
            print(f"An error occurred while removing the folder: {e}")

    @staticmethod
    def test_code_generation():
        test_spec = "tests/controllers/spec_files/spec.json"
        generator = CodeGenerator(specification_file_path=test_spec)
        generator.generate()
        assert are_folders_equal(
            "tests/controllers/golden_paths/spec/generated", "generated"
        )

    def test_code_generation_error(self):
        test_spec = "tests/controllers/spec_files/spec_error.json"
        generator = CodeGenerator(specification_file_path=test_spec)

        with self.assertRaises(ValidationError):
            generator.generate()

        self.assertFalse(os.path.exists(GENERATED_FOLDER))


if __name__ == "__main__":
    unittest.main()
