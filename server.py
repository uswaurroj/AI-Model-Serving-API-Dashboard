import http.server
import socketserver
import json

PORT = 8000

class AIModelRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/api/predict':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            # Parse incoming JSON payload
            try:
                request_json = json.loads(post_data.decode('utf-8'))
                x1 = request_json.get("x1", 0.0)
                x2 = request_json.get("x2", 0.0)
                
                # Perform AI Inference calculation
                predicted_score = (2.5 * x1) + (4.0 * x2) + 15.0
                confidence = round(0.95 + (x1 % 0.04), 4)
                
                # Construct JSON response
                response_data = {
                    "status": "success",
                    "model": "Linear-Regression-v1",
                    "inputs": {"x1": x1, "x2": x2},
                    "predictions": {
                        "predicted_score": round(predicted_score, 4),
                        "confidence_score": confidence
                    },
                    "timestamp": "2026-09-08T08:35:00Z"
                }
                
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(response_data).encode('utf-8'))
                
            except Exception as e:
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode('utf-8'))
        else:
            self.send_error(404, "Endpoint Not Found")

    def do_GET(self):
        if self.path == '/api/health':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "API Server Healthy"}).encode('utf-8'))
        else:
            super().do_GET()

print(f"--- AI Model Serving Server Running on http://localhost:{PORT} ---")
with socketserver.TCPServer(("", PORT), AIModelRequestHandler) as httpd:
    httpd.serve_forever()
