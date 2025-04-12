import os
import json
import subprocess
import re
import time
import logging
from typing import Dict, Optional

# 设置日志
logging.basicConfig(
    filename='logs/slither_analyzer.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class SlitherAnalyzer:
    def __init__(self):
        self.reports_dir = 'reports/slither'
        os.makedirs(self.reports_dir, exist_ok=True)
        self.timeout = 300  # 5分钟超时
        
    @staticmethod
    def install_solc_version(version: str) -> bool:
        """按需安装特定的 solc 版本"""
        try:
            # 检查版本是否已安装
            check_cmd = f"solc-select versions"
            check_process = subprocess.run(check_cmd, shell=True, capture_output=True, text=True)
            installed_versions = check_process.stdout.strip().split('\n')
            
            if version not in installed_versions:
                logger.info(f"Installing solc version {version}...")
                install_cmd = f"solc-select install {version}"
                install_process = subprocess.run(install_cmd, shell=True, capture_output=True, text=True)
                
                if install_process.returncode != 0:
                    logger.error(f"Failed to install solc version {version}")
                    return False
                    
            return True
        except Exception as e:
            logger.error(f"Error installing solc version {version}: {str(e)}")
            return False

    def get_solc_version(self, contract_file: str) -> Optional[str]:
        """从合约文件中提取Solidity版本"""
        try:
            with open(contract_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 查找pragma语句
            match = re.search(r'pragma\s+solidity\s+([^;]+);', content)
            if match:
                version_spec = match.group(1).strip()
                # 处理版本规范（例如：^0.4.19 -> 0.4.19）
                # 保留完整的版本号，不要限制
                version = re.sub(r'[\^~>=<]', '', version_spec.split()[0])
                logger.info(f"Detected Solidity version: {version}")
                return version
            
            logger.error(f"Could not find Solidity version in {contract_file}")
            return None
            
        except Exception as e:
            logger.error(f"Error getting Solidity version from {contract_file}: {str(e)}")
            return None

    def ensure_solc_version(self, version: str) -> bool:
        """确保指定版本的solc可用"""
        try:
            # 检查版本是否已安装
            check_cmd = "solc-select versions"
            check_process = subprocess.run(check_cmd, shell=True, capture_output=True, text=True)
            
            if check_process.returncode != 0:
                logger.error("Failed to check installed versions")
                return False
            
            installed_versions = check_process.stdout.strip().split('\n')
            
            if version in installed_versions:
                # 如果版本已安装，直接使用
                use_cmd = f"solc-select use {version}"
                use_process = subprocess.run(use_cmd, shell=True, capture_output=True, text=True)
                
                if use_process.returncode != 0:
                    logger.error(f"Failed to switch to version {version}: {use_process.stderr}")
                    return False
                    
                logger.info(f"Using existing Solidity version {version}")
                return True
            
            # 如果版本未安装，尝试从本地artifacts目录安装
            artifacts_dir = os.path.expanduser('~/.solc-select/artifacts/')
            solc_path = os.path.join(artifacts_dir, f'solc-{version}')
            
            if os.path.exists(solc_path):
                logger.info(f"Found local Solidity binary for version {version}")
                use_cmd = f"solc-select use {version}"
                use_process = subprocess.run(use_cmd, shell=True, capture_output=True, text=True)
                
                if use_process.returncode != 0:
                    logger.error(f"Failed to use local version {version}: {use_process.stderr}")
                    return False
                    
                return True
            
            logger.error(f"Solidity version {version} not found locally")
            return False
            
        except Exception as e:
            logger.error(f"Error ensuring Solidity version {version}: {str(e)}")
            return False

    def analyze_contract(self, contract_file: str) -> Dict:
        """使用Slither分析合约"""
        result = {
            'success': False,
            'output_file': None,
            'error': None
        }

        try:
            abs_contract_file = os.path.abspath(contract_file)
            if not os.path.exists(abs_contract_file):
                result['error'] = f"Contract file not found: {abs_contract_file}"
                return result

            # 获取版本
            version = self.get_solc_version(contract_file)
            if not version:
                result['error'] = 'Could not determine Solidity version'
                return result

            # 确保版本可用
            if not self.ensure_solc_version(version):
                result['error'] = f'Required Solidity version {version} is not available. Please install it manually.'
                return result

            # 构造输出文件路径
            output_file = os.path.join(
                self.reports_dir,
                f"{os.path.splitext(os.path.basename(contract_file))[0]}_slither_report.json"
            )

            # 运行Slither分析
            cmd = f"slither {abs_contract_file} --json {output_file}"
            try:
                process = subprocess.Popen(
                    cmd,
                    shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                
                stdout, stderr = process.communicate(timeout=self.timeout)
                
                if process.returncode != 0 and not os.path.exists(output_file):
                    result['error'] = f"Slither analysis failed: {stderr}"
                    return result
                
                if os.path.exists(output_file):
                    result['success'] = True
                    result['output_file'] = output_file
                    return result
                else:
                    result['error'] = "Slither report file not generated"
                    return result

            except subprocess.TimeoutExpired:
                process.kill()
                result['error'] = f"Slither analysis timed out after {self.timeout} seconds"
                return result
            
        except Exception as e:
            logger.error(f"Error in analyze_contract: {str(e)}")
            result['error'] = str(e)
            return result

    def filter_results(self, results: Dict) -> Dict:
        """过滤Slither结果，只保留高危漏洞"""
        if not results or 'results' not in results:
            return {}
        
        filtered_results = {
            'results': {
                'detectors': []
            }
        }
        
        for detector in results['results'].get('detectors', []):
            impact = detector.get('impact', '').lower()
            if impact == 'high':  # 只保留高危漏洞
                filtered_results['results']['detectors'].append(detector)
        
        return filtered_results
