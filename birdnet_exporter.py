from http.server import BaseHTTPRequestHandler, HTTPServer
import sqlite3


class BirdCountsServer(BaseHTTPRequestHandler):
    def read_data(self, path_to_db: str):
        con = sqlite3.connect(path_to_db)
        cur = con.cursor()

        total = cur.execute("SELECT count(*) FROM detections;")
        total = total.fetchone()[0]
        detection_count = cur.execute(
            "SELECT Com_Name, count(*) FROM detections GROUP BY Com_Name;"
        )
        detection_count = detection_count.fetchall()

        return total, detection_count

    def do_GET(self):
        total, detection_count = self.read_data("./birds.db")

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        self.wfile.write(f"total_detections {total}\n".encode("utf-8"))
        for detection in detection_count:
            self.wfile.write(
                f'bird_detection{{common_name="{detection[0]}"}} {detection[1]}\n'.encode(
                    "utf-8"
                )
            )


if __name__ == "__main__":
    webServer = HTTPServer(("0.0.0.0", 9091), BirdCountsServer)

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
