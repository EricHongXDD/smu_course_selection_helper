from PyInstaller.utils.hooks import collect_data_files, collect_submodules
hiddenimports = (
    collect_submodules('lxml') +
    collect_data_files('lxml'))
datas = collect_data_files('lxml')