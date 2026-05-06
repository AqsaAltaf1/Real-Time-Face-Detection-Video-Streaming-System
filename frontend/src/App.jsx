import { useEffect, useRef, useState } from "react";
import "./App.css";

const API_BASE = import.meta.env.VITE_API_BASE ?? "http://localhost:8000";
const INGEST_WS_URL = API_BASE.replace(/^http/, "ws") + "/ws/ingest";
const STREAM_WS_URL = API_BASE.replace(/^http/, "ws") + "/ws/stream";

function App() {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const ingestSocketRef = useRef(null);
  const streamSocketRef = useRef(null);
  const frameIdRef = useRef(0);
  const captureIntervalRef = useRef(null);
  const mediaStreamRef = useRef(null);

  const [isRunning, setIsRunning] = useState(false);
  const [connectionStatus, setConnectionStatus] = useState("disconnected");
  const [streamFrame, setStreamFrame] = useState(null);
  const [latestRoi, setLatestRoi] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    return () => {
      stopStreaming();
    };
  }, []);

  const fetchLatestRoi = async () => {
    try {
      const response = await fetch(`${API_BASE}/roi/latest`);
      if (!response.ok) {
        return;
      }
      const data = await response.json();
      setLatestRoi(data);
    } catch {
      // Keep UI resilient; stream can still function without this poll.
    }
  };

  const startStreaming = async () => {
    setError("");
    try {
      const mediaStream = await navigator.mediaDevices.getUserMedia({
        video: { width: 640, height: 480 },
        audio: false,
      });
      mediaStreamRef.current = mediaStream;
      if (videoRef.current) {
        videoRef.current.srcObject = mediaStream;
      }

      const ingestSocket = new WebSocket(INGEST_WS_URL);
      const streamSocket = new WebSocket(STREAM_WS_URL);
      ingestSocketRef.current = ingestSocket;
      streamSocketRef.current = streamSocket;

      ingestSocket.onopen = () => {
        setConnectionStatus("ingest-connected");
      };

      ingestSocket.onerror = () => {
        setError("Ingest socket error");
      };

      streamSocket.onopen = () => {
        setConnectionStatus("stream-connected");
      };

      streamSocket.onerror = () => {
        setError("Stream socket error");
      };

      streamSocket.onmessage = (event) => {
        try {
          const payload = JSON.parse(event.data);
          if (payload.frame) {
            setStreamFrame(payload.frame);
          }
          if (payload.roi) {
            setLatestRoi(payload.roi);
          }
        } catch {
          setError("Invalid stream payload");
        }
      };

      captureIntervalRef.current = window.setInterval(() => {
        const video = videoRef.current;
        const canvas = canvasRef.current;
        const ingest = ingestSocketRef.current;

        if (
          !video ||
          !canvas ||
          !ingest ||
          ingest.readyState !== WebSocket.OPEN
        ) {
          return;
        }

        if (video.videoWidth === 0 || video.videoHeight === 0) {
          return;
        }

        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;

        const ctx = canvas.getContext("2d");
        if (!ctx) {
          return;
        }

        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
        frameIdRef.current += 1;
        ingest.send(
          JSON.stringify({
            frame_id: frameIdRef.current,
            frame: canvas.toDataURL("image/jpeg", 0.8),
          }),
        );
      }, 250);

      setIsRunning(true);
      await fetchLatestRoi();
    } catch {
      setError("Could not access camera or backend");
      stopStreaming();
    }
  };

  const stopStreaming = () => {
    setIsRunning(false);
    setConnectionStatus("disconnected");

    if (captureIntervalRef.current) {
      clearInterval(captureIntervalRef.current);
      captureIntervalRef.current = null;
    }

    if (ingestSocketRef.current) {
      ingestSocketRef.current.close();
      ingestSocketRef.current = null;
    }
    if (streamSocketRef.current) {
      streamSocketRef.current.close();
      streamSocketRef.current = null;
    }

    if (mediaStreamRef.current) {
      mediaStreamRef.current.getTracks().forEach((track) => track.stop());
      mediaStreamRef.current = null;
    }
  };

  return (
    <main className="app">
      <header className="app-header">
        <h1>Face Detection Stream Viewer</h1>
        <p>Status: {connectionStatus}</p>
      </header>

      <section className="controls">
        <button onClick={startStreaming} disabled={isRunning}>
          Start
        </button>
        <button onClick={stopStreaming} disabled={!isRunning}>
          Stop
        </button>
        <button onClick={fetchLatestRoi}>Refresh ROI</button>
      </section>

      {error ? <p className="error">{error}</p> : null}

      <section className="viewer-grid">
        <div className="panel">
          <h2>Local Camera Input</h2>
          <video ref={videoRef} autoPlay muted playsInline className="video" />
          <canvas ref={canvasRef} className="hidden-canvas" />
        </div>

        <div className="panel">
          <h2>Processed Stream Output</h2>
          {streamFrame ? (
            <img src={streamFrame} alt="Processed stream" className="video" />
          ) : (
            <div className="placeholder">No processed frame yet</div>
          )}
        </div>

        <div className="panel">
          <h2>Latest ROI Data</h2>
          <pre className="roi-block">
            {latestRoi ? JSON.stringify(latestRoi, null, 2) : "No ROI data yet"}
          </pre>
        </div>
      </section>
    </main>
  );
}

export default App;
