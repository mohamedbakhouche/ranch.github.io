import os
import pytest

from ranch import ranchecker


class TestRanchecker:
    def test_create_archive(self):
        r = ranchecker.Ranchecker()
        g_licenseUsername = os.environ.get("g_licenseUsername")
        g_licensePassword = os.environ.get("g_licensePassword")
        res = r.create_archive(
            software_commandline="C:\\Maxon\\C4D2023\\Commandline.exe",
            g_licenseUsername=g_licenseUsername,
            g_licensePassword=g_licensePassword,
            scene_destination="C:\\Users\\mohbakh\\Pictures\\car\\sdk.c4d",
        )
        assert res == "C:\\Users\\mohbakh\\Pictures\\car\\sdk.vuc"
