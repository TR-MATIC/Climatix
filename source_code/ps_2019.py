from ps_2019_objects import CLX_Tester


ps = CLX_Tester()
#ps.invite()
ps.load_config()
if ps.config_OK and ps.path_OK:
    ps.load_data()
else:
    ps.print_center("Loading data skipped.")
    ps.print_line()
if ps.data_OK and ps.consistency_OK:
    ps.send_request()
else:
    ps.print_center("Communication skipped.")
    ps.print_line()