def init():
    global plate
    global server_ip
    global server_port
    global server_url
    global ping_threshold
    global check_conn_period
    global data_path
    global data_filename
    global gps_hwid
    global gps_period

    # vehicle data
    plate = "ABC1234"

    # system config
    server_ip = "179.27.99.46"   
    server_port = "3030"
    server_url = "http://"+server_ip+":"+server_port+"/"
    ping_threshold = 1.0
    check_conn_period = 20
    gps_hwid = "10C4:EA60"
    data_path = "./data/records.txt"
    gps_period = 1
