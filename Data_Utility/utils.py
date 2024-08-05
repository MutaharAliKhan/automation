# import os
#
#
# def get_dir(filename, root=True):
#     script_dir = os.path.dirname(os.path.abspath(__file__))
#     if root:
#         project_root = os.path.abspath(os.path.join(script_dir, '..'))
#         dir_path = os.path.join(project_root, filename)
#     else:
#         project_root = os.path.abspath(os.path.join(script_dir))
#         dir_path = os.path.join(project_root, filename)
#
#     return dir_path