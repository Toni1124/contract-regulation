# Empty init file to mark directory as Python package 

def __init__(self):
    self.reports_dir = 'reports/slither'
    os.makedirs(self.reports_dir, exist_ok=True)
    self.timeout = 300  # 5分钟超时
    
    # 确保基本的 solc 版本已安装
    self._ensure_basic_versions()

def _ensure_basic_versions(self):
    """确保常用的 solc 版本已安装"""
    basic_versions = ['0.4.17', '0.5.0', '0.6.0', '0.7.0', '0.8.0', '0.8.17', '0.8.20']
    for version in basic_versions:
        try:
            install_cmd = f"solc-select install {version}"
            subprocess.run(install_cmd, shell=True, capture_output=True)
            logger.info(f"Ensured solc version {version} is available")
        except Exception as e:
            logger.error(f"Failed to install solc version {version}: {str(e)}") 