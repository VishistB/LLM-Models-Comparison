import React, { useState } from "react";
import "./App.css";
import {
  Container,
  TextField,
  Button,
  Select,
  MenuItem,
  Typography,
  Box,
  CircularProgress,
} from "@mui/material";
import { createTheme, ThemeProvider } from "@mui/material/styles";
import logo from "./logo.svg";

const darkTheme = createTheme({
  palette: {
    mode: "dark",
    primary: {
      main: "#00f5d4",
    },
    secondary: {
      main: "#9b5de5",
    },
    background: {
      default: "#0d0d0d",
      paper: "#1e1e1e",
    },
    text: {
      primary: "#ffffff",
      secondary: "#c1c1c1",
    },
  },
  typography: {
    fontFamily: '"Roboto", "Helvetica", "Arial", sans-serif',
  },
});

function App() {
  const [model, setModel] = useState("gemini");
  const [prompt, setPrompt] = useState("");
  const [response, setResponse] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    if (!prompt) return;

    setLoading(true);
    setResponse("");
    const apiUrls = {
      gemini: "http://localhost:8000/gemini/",
      mistral: "http://localhost:8000/mistral/",
      llama: "http://localhost:8000/llama/",
    };

    try {
      const res = await fetch(apiUrls[model], {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ prompt }),
      });

      const data = await res.json();
      setResponse(data.generated_response || "No response received.");
    } catch (error) {
      console.error("Error:", error);
      setResponse("An error occurred while fetching the response.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <ThemeProvider theme={darkTheme}>
      <Box
        sx={{
          backgroundColor: "background.default",
          color: "text.primary",
          minHeight: "100vh",
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          justifyContent: "center",
        }}
      >
        <Container maxWidth="sm" sx={{ textAlign: "center" }}>
          <img src={logo} alt="logo" style={{ width: "150px", marginBottom: "20px" }} />
          <Typography variant="h4" gutterBottom>
            AI Model Selector
          </Typography>

          <Select
            value={model}
            onChange={(e) => setModel(e.target.value)}
            fullWidth
            variant="outlined"
            sx={{ mb: 2, backgroundColor: "background.paper", color: "primary.main" }}
          >
            <MenuItem value="gemini">Gemini</MenuItem>
            <MenuItem value="mistral">Mistral</MenuItem>
            <MenuItem value="llama">LLaMA</MenuItem>
          </Select>


          <TextField
            fullWidth
            variant="outlined"
            label="Enter your prompt"
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            multiline
            rows={3}
            sx={{
              mb: 2,
              backgroundColor: "background.paper",
              color: "primary.main",
            }}
          />

          <Button
            variant="contained"
            color="primary"
            onClick={handleSubmit}
            disabled={loading}
            fullWidth
            sx={{
              mb: 2,
              fontWeight: "bold",
            }}
          >
            {loading ? <CircularProgress size={24} color="secondary" /> : "Generate"}
          </Button>

          {response && (
            <Box
              sx={{
                p: 2,
                backgroundColor: "background.paper",
                borderRadius: 2,
                boxShadow: 2,
                mt: 2,
              }}
            >
              <Typography variant="h6" sx={{ mb: 1, color: "secondary.main" }}>
                Response:
              </Typography>
              <Typography variant="body1" sx={{ whiteSpace: "pre-wrap" }}>
                {response}
              </Typography>
            </Box>
          )}
        </Container>
      </Box>
    </ThemeProvider>
  );
}

export default App;
