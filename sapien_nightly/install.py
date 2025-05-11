import os
import pathlib
import platform
import subprocess
import sys

HOME = pathlib.Path.home()

VULKAN_SDK_DOWNLOAD_URL = "https://sdk.lunarg.com/sdk/download/1.3.290.0/mac/vulkansdk-macos-1.3.290.0.dmg"

VULKAN_SDK_APPLICATION = pathlib.Path("/Applications/vulkanCapsViewer.app")

VULKAN_SDK = HOME / "VulkanSDK" / "1.3.290.0" / "macOS"

VULKAN_SDK_ENVIRONMENT_VARIABLES = f"""
# >>> SAPIEN Nightly Release initialize >>>
export VULKAN_SDK={VULKAN_SDK}

export PATH=$VULKAN_SDK/bin:$PATH
export VK_ICD_FILENAMES=$VULKAN_SDK/share/vulkan/icd.d/MoltenVK_icd.json
export VK_LAYER_PATH=$VULKAN_SDK/share/vulkan/explicit_layer.d
export DYLD_LIBRARY_PATH=$VULKAN_SDK/lib:$DYLD_LIBRARY_PATH
# <<< SAPIEN Nightly Release initialize <<<
"""


def error(message):
    """Print an error message in red."""
    print(f"\033[31m  ERROR: {message}\033[0m")


def warn(message):
    """Print a warning message in yellow."""
    print(f"\033[33m  WARNING: {message}\033[0m")


def info(message):
    """Print an informational message in green."""
    print(f"\033[32m  INFO: {message}\033[0m")


def install():
    """Install SAPIEN Nightly Release."""
    if platform.system() != "Darwin":
        error("Only macOS is supported.")
        sys.exit(1)

    if sys.version_info.major != 3:
        error("Only Python 3 is supported.")
        sys.exit(1)

    if sys.version_info.minor < 10:
        error("Python 3.10 or higher are required.")
        sys.exit(1)

    if not VULKAN_SDK_APPLICATION.exists():
        error(
            f"Please download the Vulkan SDK installer from the link {VULKAN_SDK_DOWNLOAD_URL}, "
            f"and open the installer installing the Vulkan SDK first."
        )
        sys.exit(1)

    shell = os.environ.get("SHELL", "")
    if "zsh" in shell:
        rc_file = HOME / ".zshrc"
    elif "bash" in shell:
        rc_file = HOME / ".bash_profile"
    else:
        rc_file = None
        warn(
            "Please add the Vulkan SDK environment variables for SAPIEN Nightly Release to your shell startup file manually."
        )

    if rc_file is not None:
        # TODO: improve the logic to check if the environment variables are already set
        if os.environ.get("VULKAN_SDK", None) is None:
            with open(rc_file, mode="a") as f:
                f.write(VULKAN_SDK_ENVIRONMENT_VARIABLES)

            info(
                f"Vulkan SDK environment variables for SAPIEN Nightly Release are added to {rc_file}."
            )

            if not VULKAN_SDK.exists():
                warn(
                    f"Vulkan SDK is not found at the default directory {VULKAN_SDK.parent}, "
                    f"please customize the Vulkan SDK path manually in {rc_file}."
                )

            info(f"Please restart your terminal or run: source {rc_file}.")

    version_tag = f"cp{sys.version_info.major}{sys.version_info.minor}"

    wheel_url = (
        f"https://github.com/haosulab/SAPIEN/releases/download/nightly/"
        f"sapien-3.0.0.dev20250303+291f6a77-{version_tag}-{version_tag}-macosx_12_0_universal2.whl"
    )

    info(f"Installing SAPIEN Nightly Release using the wheel {wheel_url}")

    try:
        subprocess.check_call(["uv", "pip", "install", wheel_url])
    except subprocess.CalledProcessError:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", wheel_url]
        )

    info("SAPIEN Nightly Release is installed.")
