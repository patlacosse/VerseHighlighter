import sys
import os, os.path
import json

proj_dir = os.path.dirname(__file__)
idjs_projects_dir = os.path.dirname(proj_dir)
dev_lib_dir = os.path.join(idjs_projects_dir, '.dev')
sys.path.append(dev_lib_dir)

import idjs.dist as dist
import idjs.idjsx as idjsx
import idjs.install as install

class Manager():
    
    def __init__(self, project_dir, package_file):
        self.project_dir = project_dir
        self.project_name = os.path.basename(self.project_dir)
        self.src_dir = os.path.join(self.project_dir, 'src')
        self.dist_dir = os.path.join(self.project_dir, 'dist')
        package_file_path = os.path.join(project_dir, package_file)
        self.package_info = self._load_package_json(package_file_path)
        self.pkg_name = self.package_info["name"]
        if self.pkg_name == 'auto.use-project-name': self.pkg_name = self.project_name
        self.pkg_dir = os.path.join(self.dist_dir, self.pkg_name)
    
    def build_distribution(self):
        dist_builder = dist.DistributionBuilder(self.src_dir, self.dist_dir, self.pkg_name)
        dist_builder.build()
        idjsx_processor = idjsx.IDJSXProcessor(self.pkg_dir)
        idjsx_processor.do_transformations()
        idjsx_processor.change_extensions()
        
    def build_installers(self):
        releases = self.package_info["install"]["indesign_releases"]
        for r in releases:
            indesign_location = self.package_info["install"]["indesign_script_location"][r]
            ib = install.InstallerBuilder(r, self.pkg_dir, indesign_location)
            ib.build()
    
    def run_installers(self, script_dialect=[]):
        pass
    
    def _load_package_json(self, package_file_path):
        with open(package_file_path, 'r', encoding='UTF-8') as jf:
            return json.load(jf)



def main():
    package_file_path = os.path.join(proj_dir, 'package.json')
    manager = Manager(proj_dir, package_file_path)
    manager.build_distribution()
    manager.build_installers()
    manager.run_installers()


if __name__ == '__main__':
    main()



