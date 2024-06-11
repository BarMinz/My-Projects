import subprocess


def test_site_up():
    assert "Failed" not in str(subprocess.check_output("curl http://localhost:9090 --max-time 3", shell=True))


def test_connection():
    assert (int(str(subprocess.check_output("curl --include http://localhost:9090", shell=True)).split(" ")[1]) in
            range(200, 400))

if __name__=='__main__':
    test_site_up()
    test_connection()